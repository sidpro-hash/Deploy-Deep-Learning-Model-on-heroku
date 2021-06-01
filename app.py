from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
from siddetection import detect
 
app = Flask(__name__)
 
UPLOAD_FOLDER = 'static/uploads/'
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 
@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # replace this function
        detect(file.filename,False)
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        return render_template('index.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg')
        return redirect(request.url)
 
@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/Try_it')
def Try_it():
    filename='traffic.jpg'
    detect(filename,True)
    flash('Image successfully uploaded and displayed below')
    return render_template('index.html', filename=filename)

@app.route('/tRy_it')
def tRy_it():
    filename='desk7.jpg'
    detect(filename,True)
    flash('Image successfully uploaded and displayed below')
    return render_template('index.html', filename=filename)

@app.route('/trY_it')
def trY_it():
    filename='cycle.jpg'
    detect(filename,True)
    flash('Image successfully uploaded and displayed below')
    return render_template('index.html', filename=filename)
 
if __name__ == "__main__":
    app.run(debug=True)
