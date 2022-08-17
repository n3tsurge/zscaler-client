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

# Initialize an AuditLogReport item
report = AuditLogReport(
    startTime=AuditLogReport.generate_timestamp(minutes_ago=30),
    endTime=AuditLogReport.generate_timestamp(),
    actionTypes=['SIGN_IN','ACTIVATE','AUDIT_OPERATION','CREATE','DELETE','DOWNLOAD','FORCED_ACTIVATE','IMPORT','PATCH','REPORT','SIGN_OUT','UPDATE']
)

# Create the report via the ZScaler API
report.create()

# Check the status of the report and continue to check 
# the status if it is still in INIT or EXECUTING phase
r = report.get()
while r.status in ['INIT','EXECUTING']:
    r = report.get()
    time.sleep(1)

# When complete, download the 
if r.status == 'COMPLETE':
    data = AuditLogReportDownload.get()

    entries = AuditLogReport.csv_to_json(data)
    for entry in entries:
        print(json.dumps(json.loads(entry), indent=2))