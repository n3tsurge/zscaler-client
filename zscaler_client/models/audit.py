import datetime
import json
from io import BytesIO, TextIOWrapper
from csv import reader
from .base import BaseModel

class AuditLogReportDownload(BaseModel):

    endpoint = '/auditlogEntryReport/download'
    actions = ['get']

class AuditLogReport(BaseModel):

    endpoint = '/auditlogEntryReport'
    updatable_fields = [
        'startTime','endTime','actionTypes','category','subcategories',
        'actionResult','actionInterface','clientIP','adminName'
    ]
    actions = ['get','create','delete']

    @classmethod
    def generate_timestamp(cls, days_ago=0):
        ''' 
        A helper function to generate a timestamp in a format
        that the API expects
        '''
        return int((datetime.datetime.now() - datetime.timedelta(days_ago)).timestamp())*1000

    @classmethod
    def csv_to_json(cls, data):
        '''
        A helper function that converts CSV data in to JSON
        '''

        entries = []
        with BytesIO(data.encode()) as csv_file:
            with TextIOWrapper(csv_file, encoding='utf8') as fo:
                result = reader(fo, delimiter=",", quotechar='"')
                rows = [row for row in result][5:]
                headers = rows.pop(0)
                for row in rows:
                    data = {}
                    for header in headers:
                        index = headers.index(header)
                        clean_header_title = header.lower().replace(' ','_')
                        data[clean_header_title] = row[index] if row[index] != "" else None

                    entries.append(json.dumps(data))
        return entries