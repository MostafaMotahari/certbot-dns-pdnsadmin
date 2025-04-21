# certbot-dns-pdnsadmin

![PyPI version](https://badge.fury.io/py/certbot-dns-pdnsadmin.svg) ![PyPI downloads](https://img.shields.io/pypi/dm/certbot-dns-pdnsadmin.svg)

A Python plugin for [Certbot](https://certbot.eff.org/) to perform DNS-01 challenges using the [PowerDNS-Admin](https://github.com/PowerDNS-Admin/PowerDNS-Admin) API.

![certbot-dns-pdnsadmin](https://github.com/MostafaMotahari/certbot-dns-pdnsadmin/images/cover.png)

## Installation

You can install the package from PyPI using pip:


```pip install certbot-dns-pdnsadmin```

Usage

To use this plugin with Certbot, you need to configure it as a DNS plugin for DNS-01 challenges. Here’s an example of how to run Certbot with this plugin:

```certbot certonly --dns-pdnsadmin --dns-pdnsadmin-credentials /path/to/credentials.ini -d example.com```

Make sure to replace ```/path/to/credentials.ini``` with the actual path to your credentials file and example.com with the domain for which you are obtaining a certificate.
Configuration

The plugin requires a credentials file to authenticate with the PowerDNS-Admin API. Here is an example of the required configuration in the credentials.ini file:

```bash
dns_pdnsadmin_api_url = https://your-pdnsadmin-url/api/
dns_pdnsadmin_api_key = your_api_key
```

Requirements

- Certbot
- PowerDNS-Admin
