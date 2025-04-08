from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="certbot-dns-pdnsadmin",
    version="0.1.1",
    author="Mostafa Motahari",
    author_email="mostafamotahari2004@gmail.com",
    description="PowerDNS Admin DNS Authenticator plugin for Certbot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MostafaMotahari/certbot-dns-pdnsadmin",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "acme>=0.31.0",
        "certbot>=0.31.0",
        "requests>=2.20.0",
        "zope.interface",
    ],
    entry_points={
        "certbot.plugins": [
            "dns-pdnsadmin = certbot_dns_pdnsadmin:Authenticator",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Plugins",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Security",
        "Topic :: System :: Installation/Setup",
        "Topic :: System :: Networking",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
)
