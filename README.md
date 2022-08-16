# ZScaler API Client

> **WARNING**: This is a work in progress and may have bugs that could severily impact your Zscaler implementation, use at your own risk

## Installation

1. Clone the repository in to your project
2. Initialize the API Client using the steps below

```python
from zscaler_client.client import create_client
from zscaler_client.models import UrlCategory

# Create a new client connection
client = create_client(config={'api_key': 'YOUR_API_KEY_HERE'}, base_url="YOUR_BASE_URL_HERE")

# Authenticate to the API
client.auth(username="API_USER", password="API_USER_PASSWORD")

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
- [ ] Admin & Role Management
- [ ] Cloud Sandbox Report
- [ ] Cloud Sandbox Submission
- [ ] Data Loss Prevention
- [ ] Device Groups
- [ ] Firewall Policies
- [ ] Location Management
- [x] Rule Labels
    - [x] Get rule labels
    - [x] Update rule labels
    - [x] Delete rule labels
- [ ] Security Policy Settings
    - [x] Add/Remove values to Advanced Security Deny List
    - [ ] Update entire Advanced Security Deny List (overwrite)
- [ ] SSL Inspection Settings
- [ ] Traffic Forwarding
    - [x] Add VPN Credentials
- [ ] User Management
- [ ] URL Categories
    - [x] URL Category list
    - [ ] Create Custom URL Category
    - [x] URL Category lookup
- [ ] URL Filtering Policies
- [ ] User Authentication Settings