import httplib2
import sys
import os

from apiclient import discovery
from google.oauth2 import service_account

class sheets:
    def __init__(self, spreadsheet_id, secret_file='config/client_secret.json'):
        scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly", 'https://www.googleapis.com/auth/drive']

        if not os.path.isfile(secret_file):
            print("No API credentials found")
            print("%s/%s" % (os.getcwd(), secret_file))
            sys.exit(1)

        credentials = service_account.Credentials.from_service_account_file(secret_file, scopes=scopes)
        self.service = discovery.build('sheets', 'v4', credentials=credentials)
        self.spreadsheet_id = spreadsheet_id

    def get(self, range):
        result = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheet_id, range=range).execute()

        values = result.get('values', [])

        return values
    
    def write(self, range, data):
        result = self.service.spreadsheets().values().update(spreadsheetId=self.spreadsheet_id, range=range, body=data, valueInputOption='USER_ENTERED').execute()

        return result
    
    def clear_sheet(self, sheet, range):
        request = self.service.spreadsheets().values().clear(spreadsheetId=self.spreadsheet_id,range=range,body={}).execute()

        return request

    def delete_row(self, start, end, sheet):
        request = {}
        request['deleteDimension'] = {}
        request['deleteDimension']['range'] = {}
        request['deleteDimension']['range']['sheetId'] = sheet
        request['deleteDimension']['range']['startIndex'] = start
        request['deleteDimension']['range']['endIndex'] = end
        request['deleteDimension']['range']['dimension'] = "ROWS"
        body = {}
        body['requests'] = []
        body['requests'].append(request)

        request = self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheet_id, body=body).execute()

        return request