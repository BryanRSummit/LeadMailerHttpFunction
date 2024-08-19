from flask import Flask, request
from google.oauth2 import service_account
import functions_framework
from googleapiclient.discovery import build
import os
from flask import request, jsonify

from sheet_login import sheet_login

sheet = sheet_login()

from functools import wraps

def cors_enabled(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if request.method == 'OPTIONS':
            headers = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Max-Age': '3600'
            }
            return ('', 204, headers)

        headers = {
            'Access-Control-Allow-Origin': '*'
        }
        
        result = f(*args, **kwargs)
        if isinstance(result, tuple):
            response, status_code = result
            return response, status_code, headers
        else:
            return result, 200, headers
    return wrapper


@functions_framework.http
@cors_enabled
def leadMailer(request):
    if request.method == 'POST':
        lead_id = request.args.get("lead_id")

        if not lead_id:
            return jsonify({"error": "Missing lead_id"}), 400

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
                return jsonify({"error": f'Lead ID {lead_id} not found'}), 404

            # Update the 12th column (index 11 in zero-based indexing)
            update_column = 13  # This is the 12th column
            sheet.update_cell(row_index + 1, update_column, 'TRUE')  # +1 because sheet rows are 1-indexed

            return jsonify({"message": f"Lead updated, emails will no longer be sent!\t, {lead_id}"}), 200

        except Exception as e:
            return f'An error occurred: {str(e)}', 500
        
    elif request.method == 'GET':
        # Handle GET request if needed
        lead_id = request.args.get("lead_id")
        returnStr = f"GET request received, to update lead use POST {lead_id}"
        return jsonify({"message": returnStr}), 200
    else:
        return jsonify({"error": "Unsupported method"}), 405