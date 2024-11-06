from app import app
from urllib.parse import urlparse
from flask import Flask, request, jsonify, send_file,Response
import os
import datetime
from urllib.request import urlretrieve
import subprocess
from werkzeug.utils import secure_filename
from io import BytesIO
import fitz
import zipfile
import shutil

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER






def zip_directory(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, mode='w') as zipf:
        len_dir_path = len(folder_path)
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, file_path[len_dir_path:])

def fileSizeInBytes(filePath):
    sizeOfFile = os.path.getsize(filePath)
    return sizeOfFile




@app.route('/pdf2jpg', methods=['POST'])
def pdf2jpg():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        sen = request.get_json()
        url = sen['pdf']
        a = urlparse(url)
        filename=os.path.basename(a.path)
        dt = datetime.datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
        exe='pdf2ppt'+dt
        infile=os.path.join(app.config['UPLOAD_FOLDER'], filename)
        outf=os.path.join(app.config['UPLOAD_FOLDER'],exe)
        download_url(url, app.config['UPLOAD_FOLDER'])
        os.mkdir(outf)
        doc = fitz.open(infile)
        for i,page in enumerate(doc):
            pix = page.get_pixmap()
            f_name=str(i) +'.jpg'
            fname=exe+f_name
            outfil=os.path.join(outf, fname)
            pix.save(outfil)
        zipname = 'pdf2jpg_'+dt+'.jpg'
        zipout=os.path.join(app.config['UPLOAD_FOLDER'],zipname)
        htp=os.path.join("ps://xddd/uploads/"+zipname)
        zip_directory(outf, zipout)
        shutil.rmtree(outf)
        outurl={"output_url":htp}
        os.remove(infile)
        return send_file(
            zipout,
            as_attachment=True,
            download_name=zipname,
            mimetype='application/jpg'
        )

    else:

        file = request.files['pdf']
        filename = secure_filename(file.filename)
        exe=filename.split(".")[0]
        infile=os.path.join(app.config['UPLOAD_FOLDER'],filename)
        outf=os.path.join(app.config['UPLOAD_FOLDER'],exe)
        os.mkdir(outf)
        file.save(infile)
        fsize=fileSizeInBytes(infile)
        if fsize<62914560:
            doc = fitz.open(infile)
            for i,page in enumerate(doc):
                pix = page.get_pixmap()
                f_name=str(i) +'.jpg'
                fname=exe+f_name
                outfil=os.path.join(outf, fname)
                pix.save(outfil)
            dt = datetime.datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
            zipname = 'pdf2jpg_'+dt+'.zip'
            zipout=os.path.join(app.config['UPLOAD_FOLDER'],zipname)
            htp=os.path.join("https://pddd/uploads/"+zipname)
            zip_directory(outf, zipout)
            shutil.rmtree(outf)
            outurl={"output_url":htp}
            os.remove(infile)
            return send_file(
            zipout,
            as_attachment=True,
            download_name=zipname,
            mimetype='application/zip'
        )
        else:
            return  Response( "limit exceded less then 60MB",status=400)
