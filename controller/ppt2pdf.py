from pptx import Presentation
from app import app
from flask import Flask, request, send_file,Response
from PyPDF2 import PdfWriter, PdfFileReader
import os
import datetime
from werkzeug.utils import secure_filename
from io import BytesIO
import subprocess

def fileSizeInBytes(filePath):
    sizeOfFile = os.path.getsize(filePath)
    return sizeOfFile


UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/ppt2pdf', methods=['POST'])
def ppt2pdf():
     
        file = request.files['ppt']
        filename = secure_filename(file.filename)
        dt = datetime.datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
        ap=filename.split('.')
        infile=os.path.join(app.config['UPLOAD_FOLDER'],filename)
        file.save(infile)
        outname = 'Ppt2pdf.pdf'
        outfile=os.path.join(app.config['UPLOAD_FOLDER'],outname)
        subprocess.run(['unoconv', '-f', 'pdf',  '-o', outfile,  infile])
        # htp=os.path.join("https://pdf-tools.mycdnpro.com/uploads/"+outname)
        with open(outfile, 'rb') as pdf_file:
                pdf_content = pdf_file.read()
        os.remove(infile)
        os.remove(outfile)
        return send_file(
                BytesIO(pdf_content),
                as_attachment=True,
                download_name='output.pdf',
                mimetype='application/octet-stream'
            )