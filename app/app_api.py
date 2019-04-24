import base64
import os
import cv2
import datetime
from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_wtf import FlaskForm
from flask_mongoengine import MongoEngine, Document
from wtforms import StringField, PasswordField
from wtforms.validators import Email, Length, InputRequired
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_cors import CORS
from flask_pymongo import PyMongo
from io import BytesIO
from PIL import Image
from db_config import db_config
from mongoengine import connect

app = Flask(__name__)
CORS(app)


app.config['MONGODB_SETTINGS'] = {
    'db': 'vaico_works',
    'host': db_config['host']
}


# app.config['MONGO_DBNAME'] = 'vaico_works'
# app.config['MONGO_URI'] = 'mongodb://vaico_works:vaico_works1@ds145916.mlab.com:45916/vaico_works'


db = MongoEngine(app)
#mongo = PyMongo(app)

app.config['SECRET_KEY'] = 'vaico123s'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

################################################################################################
                                           #Models
################################################################################################
class User(UserMixin, db.Document):                                                                                            
    meta = {'collection': 'users'}                                                                                             
    email = db.StringField(max_length=30)
    password = db.StringField()
    name = db.StringField()
    cel = db.StringField()
    occupation = db.StringField()

# class Image_Register(db.Document):                                                                                            
#     meta = {'collection': 'image_registers'}                                                                                             
#     original = db.StringField()
#     processed = db.StringField()
#     date = db.StringField()

class Image_Register(db.Document):
    meta = {'collection': 'image_registers'}
    place = db.StringField()
    date = db.StringField()
    original = db.StringField()
    prediction = db.StringField()

class Report(db.Document):                                                                                            
    meta = {'collection': 'reports'}  
    title = db.StringField()
    name = db.StringField()
    email = db.StringField()
    cel = db.StringField()
    occupation = db.StringField()                                                                                           
    original_img = db.StringField()
    processed_img = db.StringField()
    year_img = db.StringField()
    month_img = db.StringField()
    day_img = db.StringField()
    time_img = db.StringField()
    date_report = db.StringField()
    description = db.StringField()

@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()

@app.route('/register', methods=['GET', 'POST'])
def register():
    #print(request.form['first_name'])
    if request.method == 'POST':
        print('init validaton')
        print(request.form['email'])
        existing_user = User.objects(email=request.form['email']).first()
        print('validation ended')
        if existing_user is None:
            hashpass = generate_password_hash(request.form['password'], method='sha256')
            hey = User(request.form['email'],hashpass,request.form['first_name'],request.form['cel'],request.form['occupation']).save()
            login_user(hey)
            print(request.form['first_name'])
            return redirect(url_for('show_index',email=request.form['email']))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    print(app.config)
    print(current_user.is_authenticated,'---------------------------------------------------')
    if current_user.is_authenticated == True:
        return redirect(url_for('show_index'))
    if request.method == 'POST':
        check_user = User.objects(email=request.form['email']).first()
        if check_user:
            if check_password_hash(check_user['password'], request.form['password']):
                login_user(check_user)
                return redirect(url_for('show_index',email=request.form['email']))
    return render_template('login.html')


@app.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/index', methods=['GET', 'POST'])
@login_required
def show_index():
    print(current_user.name)
    users = User.objects()
    print("soy el numero de usuarios:", len(users))
    imgs = Image_Register.objects()
    for i in imgs:
        print(i.date)
    print("soy el len: ", len(imgs))
    return render_template('index.html')


@app.route('/original_gallery', methods=['GET', 'POST'])
@login_required
def original_gallery():
    imgs = Image_Register.objects
    #imgs = mongo.db.image_registers.find()
    return render_template('original_gallery.html',data=imgs)

@app.route('/processed_gallery', methods=['GET', 'POST'])
@login_required
def processed_gallery():
    imgs = Image_Register.objects
    return render_template('processed_gallery.html',data=imgs)

@app.route('/image/<date>', methods=['GET', 'POST'])
@login_required
def view_image(date):
    img = Image_Register.objects(date=date)
    print(len(img))
    info = img._query
    year = info['date'].split(" ")[0].split("-")[0]
    month = info['date'].split(" ")[0].split("-")[1]
    day = info['date'].split(" ")[0].split("-")[2]
    time = info['date'].split(" ")[1].split(".")[0]

    return render_template('view_image.html', data=img, year=year, month=month, day=day, time=time)

@app.route('/gallery', methods=['GET', 'POST'])
@login_required
def gallery():
    return render_template('gallery.html')

@app.route('/contact', methods=['GET'])
@login_required
def contact():
    return render_template('contact.html')

@app.route('/about', methods=['GET'])
@login_required
def about():
    return render_template('about.html')

@app.route('/report/<date>', methods=['GET', 'POST'])
@login_required
def generate_report(date):
    img = Image_Register.objects(date=date)
    info = img._query
    year = info['date'].split(" ")[0].split("-")[0]
    month = info['date'].split(" ")[0].split("-")[1]
    day = info['date'].split(" ")[0].split("-")[2]
    time = info['date'].split(" ")[1].split(".")[0]
    if request.method == 'POST':
        for i in Image_Register.objects:
            if(i.date == date):
                original_img = i.original
                processed_img = i.prediction
                complete_date = i.date

        year_img = complete_date.split(" ")[0].split("-")[0]
        month_img = complete_date.split(" ")[0].split("-")[1]
        day_img = complete_date.split(" ")[0].split("-")[2]
        time_img = complete_date.split(" ")[1].split(".")[0]
        user = current_user
        name = user['name']
        email = user['email']
        cel = user['cel']
        occupation = user['occupation']
        title = request.form['title']
        description = request.form['description']
        save_report(title, name, email, cel, occupation, original_img, processed_img, year_img, month_img, day_img, time_img, str(datetime.datetime.now()), description)
    print(year, month, day, time)
    return render_template('report.html', data=img, year=year, month=month, day=day, time=time)

def save_report(title, name, email, cel, occupation, original_img, processed_img, year_img, month_img, day_img, time_img, date_report, description):
    Report(title, name, email, cel, occupation, original_img, processed_img, year_img, month_img, day_img, time_img, date_report, description).save()

@app.route('/reports', methods=['GET', 'POST'])
@login_required
def view_reports():
    
    reports = Report.objects()
    return render_template("reports.html", data = reports)


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
