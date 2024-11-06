from flask import Flask
app= Flask(__name__)







import controller.pdf2doc as pdf2doc
import controller.pdf2jpg as pdf2jpg
import controller.pdf2ppt as pdf2ppt
import controller.pdf2xls as pdf2xls
import controller.ppt2pdf as ppt2pdf



if __name__ == '__main__':
    app.run(debug=True)