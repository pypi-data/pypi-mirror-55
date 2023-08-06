import httplib2
import sys
import os

from apiclient import discovery
from google.oauth2 import service_account

class sheets:
    def __init__(self, spreadsheet_id, secret_file='client_secret.json'):
        scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly", 'https://www.googleapis.com/auth/drive']

        if not os.path.isfile(secret_file):
            print("No API credentials found")
            sys.exit()

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