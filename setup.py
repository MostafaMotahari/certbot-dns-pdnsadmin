from setuptools import setup

setup(
    name='certbot-dns-pdnsadmin',
    version='0.1.0',
    description='PowerDNS Admin DNS Authenticator plugin for Certbot',
    url='https://github.com/MostafaMotahari/certbot-dns-pdnsadmin',
    author='Mostafa Motahari',
    author_email='mostafamotahari2004@gmail.com',
    license='Apache License 2.0',
    python_requires='>=3.9',
    packages=['certbot_dns_pdnsadmin'],
    install_requires=[
        'acme>=0.31.0',
        'certbot>=0.31.0',
        'requests>=2.20.0',
        'zope.interface',
    ],
    entry_points={
        'certbot.plugins': [
            'dns-pdnsadmin = certbot_dns_pdnsadmin:Authenticator',
        ],
    },
)
