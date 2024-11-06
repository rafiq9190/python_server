from app import app
from flask import Flask, request, send_file
import os
import datetime
from werkzeug.utils import secure_filename
import pdfplumber
import pandas as pd
from io import BytesIO

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/pdf2xls', methods=['POST'])
def pdf_to_xls():
    print('Received request:', request.files)
    file = request.files['pdf']

    if not file:
        return {"message": "No file uploaded."}, 400

    filename = secure_filename(file.filename)
    input_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(input_file_path)

    # Create a DataFrame to hold all extracted tables
    all_tables = []

    # Extract tables from the PDF
    with pdfplumber.open(input_file_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                df = pd.DataFrame(table[1:], columns=table[0])  # First row as header
                all_tables.append(df)

    # Combine all tables into a single DataFrame if any tables were found
    if all_tables:
        combined_df = pd.concat(all_tables, ignore_index=True)
        
        # Create an Excel file in memory
        output = BytesIO()
        combined_df.to_excel(output, index=False, engine='openpyxl')
        output.seek(0)  # Move to the beginning of the BytesIO buffer

        # Clean up: Remove the uploaded PDF file
        try:
            os.remove(input_file_path)
        except Exception as e:
            print(f"Error deleting file: {e}")

        return send_file(
            output,
            as_attachment=True,
            download_name='output.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    else:
        return {"message": "No tables found in the PDF."}, 404
