from flask import Flask, request
from google.oauth2 import service_account

from googleapiclient.discovery import build
import os


from sheet_login import sheet_login

app = Flask(__name__)

sheet = sheet_login()


@app.route('/', methods=['GET'])
def handle_request():
    # Extract parameters from the request
    lead_id = request.args.get('lead_id')
    # Add any other parameters you need

    if not lead_id:
        return 'Missing lead_id parameter', 400

    try:
        sheet = sheet_login()

        # Find the row with the matching lead_id
        cell = sheet.find(lead_id)
        if not cell:
            return f'Lead ID {lead_id} not found', 404

        headers = sheet.row_values(1)
        row = cell.row
        col = headers.index("No Interest") 

        # Update the checkbox column
        sheet.update_cell(row, col, 'TRUE')

        return f'Updated checkbox for lead {lead_id}', 200

    except Exception as e:
        return f'An error occurred: {str(e)}', 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))