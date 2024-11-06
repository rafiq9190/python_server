from app import app

from flask import Flask, request,send_file,Response
import os
import datetime
import subprocess
from werkzeug.utils import secure_filename
from io import BytesIO




UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def fileSizeInBytes(filePath):
    sizeOfFile = os.path.getsize(filePath)
    return sizeOfFile

@app.route('/pdf2ppt', methods=['POST'])
def pdftoppt():
        print('check request',request.files) 
        file = request.files['pdf']
        filename = secure_filename(file.filename)
        infil=os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(infil)
        fsize=fileSizeInBytes(infil)
        if fsize<62914560:
            dt = datetime.datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
            fname = 'pdf2ppt_.pptx'
            outfil=os.path.join(app.config['UPLOAD_FOLDER'], fname)
            print("Output file path:", outfil)
         
            list_files=subprocess.run(["pdf2pptx",infil,"-o"+ outfil])
            if list_files.returncode == 0:
                    print("Conversion successful!")
            else:
                print("Conversion failed. Check the error.")
                print(list_files.stderr)
            print(list_files.stderr)
            with open(outfil, 'rb') as pptx_file:
                pptx_content = pptx_file.read()
            try:
             os.remove(infil)
             
            except Exception as e:
             print(f"Error deleting file: {e}")
            return send_file(
                BytesIO(pptx_content),
                as_attachment=True,
                download_name='output.pptx',
                mimetype='application/octet-stream'
            )
        else:
            return  Response( "limit exceded less then 60MB",status=400)
