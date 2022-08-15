# ZScaler API Client

## Installation

1. Clone the repository in to your project
2. Initialize the API Client using the steps below

```python
from zscaler_client.client import APIClient

api = APIClient(config={'api_key': 'YOUR_API_KEY_HERE'}, base_url="YOUR_BASE_URL_HERE")
api.auth(username="API_USER", password="API_USER_PASSWORD")
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
- [ ] Rule Labels
- [ ] Security Policy Settings
    - [x] Add/Remove values to Advanced Security Deny List
    - [ ] Update entire Advanced Security Deny List (overwrite)
- [ ] SSL Inspection Settings
- [ ] Traffic Forwarding
    - [x] Add VPN Credentials
- [ ] User Management
- [ ] URL Categories
- [ ] URL Filtering Policies
- [ ] User Authentication Settings