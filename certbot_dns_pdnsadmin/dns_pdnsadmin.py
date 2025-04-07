import json
import logging

import requests
import zope.interface
from certbot import errors
from certbot import interfaces
from certbot.plugins import dns_common

logger = logging.getLogger(__name__)

@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for PowerDNS Admin"""

    description = "Obtain certificates using a DNS TXT record with PowerDNS Admin API"

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.credentials = None

    @classmethod
    def add_parser_arguments(cls, add):
        super(Authenticator, cls).add_parser_arguments(add, default_propagation_seconds=30)
        add("credentials", help="PowerDNS Admin credentials INI file.")

    def more_info(self):
        return ("This plugin configures a DNS TXT record to respond to a DNS-01 challenge using "
                "the PowerDNS Admin API.")

    def _setup_credentials(self):
        self.credentials = self._configure_credentials(
            "credentials",
            "PowerDNS Admin credentials INI file",
            {
                "api-key": "API key for PowerDNS Admin",
                "api-url": "URL for PowerDNS Admin API (e.g., http://localhost:80/api/v1)",
                "server-id": "Server ID (typically 'localhost')"
            }
        )

    def _perform(self, domain, validation_name, validation):
        self._get_powerdnsadmin_client().add_txt_record(
            domain, validation_name, validation
        )

    def _cleanup(self, domain, validation_name, validation):
        self._get_powerdnsadmin_client().del_txt_record(
            domain, validation_name, validation
        )

    def _get_powerdnsadmin_client(self):
        return _PowerDNSAdminClient(
            self.credentials.conf("api-key"),
            self.credentials.conf("api-url"),
            self.credentials.conf("server-id")
        )


class _PowerDNSAdminClient:
    """Encapsulates all communication with the PowerDNS Admin API."""

    def __init__(self, api_key, api_url, server_id):
        self.api_key = api_key
        self.api_url = api_url.rstrip('/')
        self.server_id = server_id
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': self.api_key,
            'Content-Type': 'application/json'
        })

    def add_txt_record(self, domain, record_name, validation):
        """Add a TXT record for DNS-01 challenge."""

        zone_id = self._find_zone_id(domain)
        if not zone_id:
            raise errors.PluginError(f"Could not find zone for domain {domain}")

        payload = {
            "rrsets": [{
                "name": f"{record_name}.",
                "type": "TXT",
                "ttl": 60,
                "changetype": "REPLACE",
                "records": [{
                    "content": f'"{validation}"',
                    "disabled": False
                }]
            }]
        }

        response = self.session.patch(
            f"{self.api_url}/servers/{self.server_id}/zones/{zone_id}",
            data=json.dumps(payload)
        )

        if response.status_code != 204:
            raise errors.PluginError(
                f"Error adding TXT record: {response.status_code} - {response.text}"
            )

        logger.info("Successfully added TXT record for %s", record_name)

    def del_txt_record(self, domain, record_name, validation):
        """Remove the TXT record after DNS-01 challenge."""

        zone_id = self._find_zone_id(domain)
        if not zone_id:
            logger.warning("Could not find zone for domain %s during cleanup", domain)
            return

        payload = {
            "rrsets": [{
                "name": f"{record_name}.",
                "type": "TXT",
                "changetype": "DELETE"
            }]
        }

        response = self.session.patch(
            f"{self.api_url}/servers/{self.server_id}/zones/{zone_id}",
            data=json.dumps(payload)
        )

        if response.status_code != 204:
            logger.warning(
                "Error deleting TXT record: %s - %s", response.status_code, response.text
            )
        else:
            logger.info("Successfully deleted TXT record for %s", record_name)

    def _find_zone_id(self, domain):
        """Find the zone ID for a given domain."""
        
        # Try progressively more specific domains
        parts = domain.split('.')
        for i in range(0, len(parts) - 1):
            test_zone = '.'.join(parts[i:]) + '.'
            response = self.session.get(
                f"{self.api_url}/servers/{self.server_id}/zones",
                params={'zone': test_zone}
            )

            if response.status_code == 200 and response.json():
                return response.json()[0]['id']

        return None
