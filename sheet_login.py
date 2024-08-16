from oauth2client.service_account import ServiceAccountCredentials
import gspread
import os



def sheet_login():
    # Set up Google Sheets API
    google_sheets_cred_path = os.path.join(os.path.dirname(__file__), 'agentleadmailer-8cc577104ac3.json')
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive', "https://www.googleapis.com/auth/gmail.send"]
    gmailCreds = ServiceAccountCredentials.from_json_keyfile_name(google_sheets_cred_path, scope)
    gc = gspread.authorize(gmailCreds)

    # Open the Google Sheet
    sheet = gc.open('Copy of 2025 Lead Assignment Tracker').sheet1
    return sheet