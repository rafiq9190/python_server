from app import app
from flask import Flask, jsonify, request,send_file
import os
from io import BytesIO
from PIL import Image
import datetime
from werkzeug.utils import secure_filename




UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/jpg2pdf', methods=['POST'])

def jpg2jpdf():
    file = request.files['img']
    print(file)
    filename = secure_filename(file.filename)
    infil = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(infil)
    image_1 = Image.open(infil)
    im_1 = image_1.convert('RGB')
    dt = datetime.datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
    pdfname = 'jpg2pdf.pdf'
    outfil = os.path.join(app.config['UPLOAD_FOLDER'], pdfname)

# Save the image as a BytesIO stream
    
    pdf_content_stream = BytesIO()
    im_1.save(pdf_content_stream, format='PDF')

    try:
        os.remove(infil)
        os.remove(outfil)
    except Exception as e:
        print(f"Error deleting file: {e}")

# Move the stream position to the beginning before sending it
    pdf_content_stream.seek(0)

    return send_file(pdf_content_stream, as_attachment=True, download_name='output.pdf', mimetype='application/pdf')
