import os
from zscaler_client.zscaler_client.client import create_client
from zscaler_client.zscaler_client.models import *

API_KEY = os.getenv('ZSCALER_API_KEY','')
API_USERNAME = os.getenv('ZSCALER_API_USERNAME', '')
API_PASSWORD = os.getenv('ZSCALER_API_PASSWORD', '')
API_BASE_URL = os.getenv('ZSCALER_API_BASE_URL', '')

# Initialize an AuditLogReport item
report = AuditLogReport(
    startTime=AuditLogReport.generate_timestamp(days_ago=7),
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
    r = AuditLogReportDownload.get()

    # Write the file to disk
    with open('report.csv','w+') as f:
        f.write(r)