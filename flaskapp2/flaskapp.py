import os
import ssl
from collections import Counter
from flask import Flask, request, render_template, redirect
from werkzeug.utils import secure_filename
import deploy_audio_model
#import sys
#sys.path.append("/home/ubuntu/flaskapp")
#import gkiri
#import sklearn
#import tensorflow as tf
import audio_converter


app = Flask(__name__, static_url_path='/static')
app.secret_key = 'our_secret_key'

#app = Flask(__name__)

app.config["IMAGE_UPLOADS"] = "/home/ubuntu/flaskapp2/static/uploads/audio"
#app.config["IMAGE_UPLOADS"] = "/home/ubuntu"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["WAV","MP4","MP3","AAC","3GP","FLV","OGG","SMF","M4A"]
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
    return "<h1 style='color: red;'>Animesh Chutiyaa!</h1>"

@app.route("/contribution")
def contribution():
    return "<h1 style='color: red;'>Contribution and Prize Distribution percentage: \
            Venky-45%, Kiran-45%, Prashant-9%, Animesh-1% </h1>"

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
                print("Gkiri1 :",process_file)
                #########################
                audio_converter.audio_convert(process_file,process_file)
                print("Gkiri2 :",process_file)
                #########################
                class1=deploy_audio_model.print_prediction_simple(process_file)
                print("venky class1", type(class1))
                #class1 = [0,1]
                temp_str=str("COVID-19 Prelim Score: =") +str(class1[0])  + str(" class2= ")+str(class1[1])
                #return str(class1)
                return temp_str
                #return redirect(request.url)          
                #return render_template("upload_success.html")
                #return "Saturday Easter"
            else:
                print("invalid file extension")

    #return render_template("prediag_backup.html")
    return render_template("prediag.html")


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

@app.route("/audio", methods=["GET", "POST"])
def upload_image1():
    
    if request.method == "POST":
        if request.files['audio.data']:
            print( "Saturday Easter")
            file = request.files['audio_data']
            filename = secure_filename(file.filename) 
            file.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
            return "sat easter"
            #return render_template("prediag_recorderjs.html", request="POST")
        
    return render_template("prediag_backup.html")


#@app.route('/upload', methods=['POST'])
#def upload_file():
#    print request.files
#    if 'file' not n request.files:
#        return "No file found"

#    file = request.files['file']
#    file.save("static/test.jpg")
#    return "file successfully saved"


if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('server.crt', 'server.key')
    app.debug = False
    app.run(host='0.0.0.0',port=8080,threaded=False,ssl_context=context)
    #app.run()
    
