# ZScaler API Client

> **WARNING**: This is a work in progress and may have bugs that could severily impact your Zscaler implementation, use at your own risk

## Installation

1. Clone the repository in to your project
2. Initialize the API Client using the steps below

```python
import os
from zscaler_client.client import create_client
from zscaler_client.models import UrlCategory, UrlClassificationInformation

# Create a new client connection
client = create_client(api_key=os.getenv('ZSCALER_API_KEY',''), base_url=os.getenv('ZSCALER_BASE_URL',''))

# Authenticate to the API
client.auth(username=os.getenv("ZSCALER_API_USER",""), password=os.getenv("ZSCALER_API_USER_PASSWORD","")
        )

# Fetch URL Categories
categories = UrlCategory.search()
for category in categories:
    print(category.id)

# Search URL Categorizations
lookup = UrlClassificationInformation.search(url=['netsurge.sh'])
print(lookup)
```

## API Coverage

- [x] Activation
- [ ] Admin Audit Logs
    - [x] Create Admin Audit Log Report
    - [x] Download Admin Audit Log Report
    - [x] Convert Admin Audit Log to JSON
    - [x] Delete Admin Audit Log Report (Cancel)
- [ ] Admin & Role Management
- [ ] Cloud Sandbox Report
- [ ] Cloud Sandbox Submission
- [ ] Data Loss Prevention
- [ ] Device Groups
- [ ] Firewall Policies
- [ ] Location Management
- [x] Rule Labels
    - [x] List rule labels
    - [x] Update rule labels
    - [x] Delete rule labels
- [ ] Security Policy Settings
    - [x] Add/Remove values to Advanced Security Deny List
    - [x] Update entire Advanced Security Deny List
- [ ] SSL Inspection Settings
- [ ] Traffic Forwarding
    - [x] Add VPN Credentials
    - [x] List GRE Tunnels
    - [x] List GRE Tunnel Available Internal IP Ranges
    - [x] Get GRE Tunnel
    - [ ] Update GRE Tunnel
    - [ ] Delete GRE Tunnel
    - [x] List Static IPs
    - [x] Create Static IP
    - [x] Update Static IP
    - [x] Delete Static IP
    - [x] List Zscaler Cloud VIPs
    - [x] List Zscaler Cloud VIPs by Datacenter
- [ ] User Management
- [ ] URL Categories
    - [x] URL Category list
    - [ ] Create Custom URL Category
    - [x] URL Category lookup
- [ ] URL Filtering Policies
- [ ] User Authentication Settings