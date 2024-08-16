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

        # Get all values from the sheet
        all_values = sheet.get_all_values()

        # Find the row with the matching lead_id
        row_index = None
        for i, row in enumerate(all_values):
            for cell in row:
                if lead_id in cell:
                    row_index = i
                    break
            if row_index is not None:
                break

        if row_index is None:
            return f'Lead ID {lead_id} not found', 404

        # Update the 12th column (index 11 in zero-based indexing)
        update_column = 12  # This is the 12th column
        sheet.update_cell(row_index + 1, update_column, 'TRUE')  # +1 because sheet rows are 1-indexed

        return f'Updated checkbox for lead {lead_id}', 200

    except Exception as e:
        return f'An error occurred: {str(e)}', 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))