# importing libraries
from flask import Flask, render_template, request
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from deepface import DeepFace
import json
import os

app = Flask(__name__)
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = "plantdiseaseclassification@gmail.com",
    MAIL_PASSWORD = "PlantDiseaseClassification" 
)
mail = Mail(app)

@app.route('/', methods = ["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/result" ,methods = ["POST"])
def result():
	if request.method == 'POST':
		f = request.files.get('file')
		f.save(os.path.join("static/upload", secure_filename(f.filename)))
		filepath = os.path.join("static/upload", secure_filename(f.filename))
		features = DeepFace.analyze(filepath)
		result = json.dumps(features, indent=4)
		return render_template("index.html", result=result)
	return render_template("index.html")

@app.route("/contact", methods = ["POST"])
def contact():
    if (request.method == 'POST'):
        name = request.form.get('Name')
        email = request.form.get('Email')
        message = request.form.get('Message')
        msg = Message("new message from {}".format(str(name)), sender = "plantdiseaseclassification@gmail.com", recipients = ['dmakwana503@gmail.com'])
        msg.body = message 
        mail.send(msg)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host = "127.0.0.1", port = 5000, debug = True)