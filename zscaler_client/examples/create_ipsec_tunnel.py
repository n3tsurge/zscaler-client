import time
import json
import os
from ..client import create_client
from ..models import *

API_KEY = os.getenv('ZSCALER_API_KEY','')
API_USERNAME = os.getenv('ZSCALER_API_USERNAME', '')
API_PASSWORD = os.getenv('ZSCALER_API_PASSWORD', '')
API_BASE_URL = os.getenv('ZSCALER_API_BASE_URL', '')

configuration = {
    'static_ips': [
        {
            'ip': '198.199.81.37'
        }
    ],
    'location': {
        'name': 'Netsurge Lab',
        'ipAddresses': [
            '198.199.81.37'
        ],
        'vpnCredentials': [
            {
                'type': 'UFQDN',
                'fqdn': 'netsurge01@netsurge.sh',
                'preSharedKey': 'abc1234',
                'comments': 'netsurge01'
            }
        ],
        'authRequired': False,
        'sslScanEnabled': False,
        'zappSSLScanEnabled': False,
        'xffForwardEnabled': False,
        'surrogateIp': False,
        'ofwEnabled': True,
        'ipsControl': True,
        'aupEnabled': False,
        'cautionEnabled': False,
        'aupBlockInternetUntilAccepted': False,
        'aupForceSslInspection': False,
        'kerberosAuth': False,
        'profile': 'CORPORATE',
        'description': 'This is a test location created by the API'
    }
}

# Authentication to the API
client = create_client(config={'api_key': API_KEY}, base_url=API_BASE_URL)
client.auth(username=API_USERNAME,password=API_PASSWORD)

# Create a new Static IP
static_ips = []
for ip in configuration['static_ips']:
    ip = StaticIp(**ip)
    static_ips.append(ip)

# Create a new VPN Credential
creds = []
for vpncred in configuration['location']['vpnCredentials']:
    cred = VPNCredential(**vpncred)
    cred.create()
    creds.append(cred)

# Create a new location
location = Location(**location)
location.vpnCredentials = creds

# Assign the Static IP to Location
# Assign the 