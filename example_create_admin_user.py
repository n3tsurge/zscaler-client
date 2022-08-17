# Get admin roles
import os
import time
import json
from dotenv import load_dotenv
from zscaler_client.client import create_client
from zscaler_client.models import *

load_dotenv()

API_KEY = os.getenv('ZSCALER_API_KEY','')
API_USERNAME = os.getenv('ZSCALER_API_USERNAME', '')
API_PASSWORD = os.getenv('ZSCALER_API_PASSWORD', '')
API_BASE_URL = os.getenv('ZSCALER_API_BASE_URL', '')

# Authentication to the API
client = create_client(api_key=API_KEY, base_url=API_BASE_URL)
client.auth(username=API_USERNAME,password=API_PASSWORD)

admin_roles = AdminRoleLite.search()

# Create an admin
new_user_role = next((role for role in admin_roles if role.name == 'SOC Analyst'), None)
if new_user_role:

    user = AdminUser(
        loginName='secops@netsurge.sh',
        userName='Security Operations',
        email='secops@netsurge.sh',
        role=new_user_role.as_dict(),
        comments='Created via Automation',
        adminScope={'Type':'ORGANIZATION'},
        disabled=True,
        password="A_SUPER_STRONG_PASSWORD_HERE",
        isPasswordLoginAllowed=True)

    user.create()