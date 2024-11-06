from app import app
from flask import Flask, request, send_file, Response,Blueprint
import os
import datetime
from werkzeug.utils import secure_filename
from io import BytesIO
from pdf2docx import Converter







UPLOAD_FOLDER = 'uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def fileSizeInBytes(filePath):
    sizeOfFile = os.path.getsize(filePath)
    return sizeOfFile

@app.route('/pdf2doc', methods=['POST'])
def pdf_to_docx():

 
    file = request.files['pdf']
    filename = secure_filename(file.filename)
    input_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(input_file_path)
    
    
    dt = datetime.datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
    output_filename = f"pdf2docx_{dt}.docx"
    output_file_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)

        # Convert the PDF to DOCX using the pdf2docx library
    try:
            converter = Converter(input_file_path)
            converter.convert(output_file_path, start=0, end=None)
            converter.close()
            print("Conversion successful!")
    except Exception as e:
            print("Conversion failed:", str(e))
            return Response(f"Error during conversion: {str(e)}", status=500)

        # Read the DOCX file content and send it as a response
    with open(output_file_path, 'rb') as docx_file:
            docx_content = docx_file.read()

        # Clean up: Remove the input PDF and output DOCX files
    try:
            os.remove(input_file_path)
            os.remove(output_file_path)
    except Exception as e:
            print(f"Error deleting file: {e}")

    return send_file(
            BytesIO(docx_content),
            as_attachment=True,
            download_name='output.docx',
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
  

if __name__ == '__main__':
    app.run(debug=True)
