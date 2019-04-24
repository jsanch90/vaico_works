from flask import Flask, render_template, url_for, request, session, redirect, send_from_directory,jsonify,json
from uuid import uuid4
import bcrypt
import os
import base64
import requests
from flask import current_app
import pymongo

app = Flask(__name__)
global name

mongo = pymongo.MongoClient("mongodb+srv://vaico:7iBcC3Pqk3RuNnYK@vaicorockets-05ijn.mongodb.net/test?retryWrites=true")
print(mongo.mflix)
db = mongo.login
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    if 'username' in session:
        return render_template("upload.html")
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':    
        login_user = db.users.find_one({'name' : request.form['username']})

        if login_user:
            print("____________________________")
            print(login_user['password'])
            if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
                session['username'] = request.form['username']
                return redirect(url_for('index'))
                # return 'You are logged in as ' + session['username']

        return 'Invalid username/password combination'
    return render_template('login.html')
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        existing_user = db.users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            db.users.insert_one({'name' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('register.html')

@app.route("/upload", methods=["POST"])
def upload():
    global name
    target = os.path.join(APP_ROOT, 'C:/Users/ESTEBAN/Documents/EAFIT/Proyecto2/vaico_works\web_app/static/img/')
    # target = os.path.join(APP_ROOT, 'static/')
    print(target)
    if not os.path.isdir(target):
            os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        name = filename
        destination = "/".join([target, filename])
        print ("Accept incoming file:", filename)
        print ("Save it to:", destination)
        upload.save(destination)

    # return send_from_directory("images", filename, as_attachment=True)
    return render_template("complete.html", image_name=filename)

@app.route('/upload/<filename>')
def send_image(filename):
    print(send_from_directory("static/img/", filename,as_attachment=True))
    return send_from_directory("static/img/", filename)

@app.route("/send", methods=["GET"])
def send_images():
    global name
    with open("./static/img/"+name, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return jsonify({'result' : str(encoded_string)})

@app.route("/recieve", methods=["GET"])
def recieve():
    r = requests.get(url = 'http://localhost:5000/send')
    json_data = json.loads(r.text)
    # imgdata = base64.b64decode(json_data['result'])
    return "<html><body><img src=\"data:image/jpeg;base64,"+json_data['result']+"\" /></body></html>"

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)