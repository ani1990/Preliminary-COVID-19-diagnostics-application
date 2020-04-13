import os
from collections import Counter
from flask import Flask, request, render_template, redirect
from werkzeug.utils import secure_filename
import deploy_audio_model
#import sys
#sys.path.append("/home/ubuntu/flaskapp")
#import gkiri
#import sklearn
#import tensorflow as tf

app = Flask(__name__, static_url_path='/static')

app.config["IMAGE_UPLOADS"] = "/home/ubuntu/flaskapp2/static/uploads/audio"
#app.config["IMAGE_UPLOADS"] = "/home/ubuntu"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["WAV"]
app.config["MAX_IMAGE_FILESIZE"] = 5 * 1024 * 1024

@app.route('/')
def hello_world(): 
    #import numpy
    return render_template("index.html")


@app.route("/admin/dashboard")
def admin_dashboard():
    return "Admin dashboard"



@app.route("/about")
def about():
    return "<h1 style='color: red;'>I'm a red H1 heading!</h1>"

@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    return render_template("sign_up.html")

@app.route("/upload-audio", methods=["GET", "POST"])
def upload_image():

    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            if image.filename == "":
                print("No file name")
                return redirect(request.url)
            if allowed_audio(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                print("image saved")
                process_file=os.path.join(app.config["IMAGE_UPLOADS"] ,filename)
                #print("Gkiri :",process_file)
                class1=deploy_audio_model.print_prediction_simple(process_file)
                print("venky class1", type(class1))
                #class1 = [0,1]
                temp_str=str("COVID-19 Prelim Score: class1=") +str(class1[0]) + str(" class2= ")+str(class1[1])
                #return str(class1)
                return temp_str
                #return redirect(request.url)          
                #return render_template("upload_success.html")
                #return "Saturday Easter"
            else:
                print("invalid file extension")

    return render_template("upload_image.html")
    #return render_template("upload_audio_with_details")


def allowed_audio(filename):

    # We only want files with a . in the filename
    if not "." in filename:
        return False

    # Split the extension from the filename
    ext = filename.rsplit(".", 1)[1]

    # Check if the extension is in ALLOWED_IMAGE_EXTENSIONS
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

def allowed_image_filesize(filesize):

    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False

@app.route('/countme/<input_str>')
def count_me(input_str):
    input_counter = Counter(input_str)
    response = []
    for letter, count in input_counter.most_common():
        response.append('"{}": {}'.format(letter, count))
    return '<br>'.join(response)

#@app.route('/upload', methods=['POST'])
#def upload_file():
#    print request.files
#    if 'file' not n request.files:
#        return "No file found"

#    file = request.files['file']
#    file.save("static/test.jpg")
#    return "file successfully saved"


if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0',port=5000,threaded=False)
    #app.run()
    
