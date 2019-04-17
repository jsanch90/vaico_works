import base64
import os
import cv2
import tensorflow as tf
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
#from model_test import Vaico_helmet_detection

app = Flask(__name__)
CORS(app)

app.config['MONGO_DBNAME'] = 'vaico_works'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/vaico_works'
app.config['SECRET_KEY'] = 'vaico123s'

db = MongoEngine(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

global graph
graph = tf.get_default_graph()

#model = Vaico_helmet_detection()
model = 1 # descomentar la linea de arriba y borrar esta, y descomentar el import 
print('----------Model loaded----------')

@app.route('/predict', methods=['POST'])
def predict_on_image():
    img = str(request.json['image'])
    model.get_image_from_base64(img)
    with graph.as_default():
        model.compute_current_detection()
        res_img = model.draw_boundig_box(model.get_current_detection())
    model.clear_temp_imgs()
    I = cv2.cvtColor(res_img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(I,mode='RGB')
    buff = BytesIO()
    pil_img.save(buff, format="JPEG")
    new_image_string = base64.b64encode(buff.getvalue()).decode("utf-8")
    return jsonify({"predicted": new_image_string})

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

@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()

class RegForm(FlaskForm):
    email = StringField('email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=20)])
    name = StringField(validators=[InputRequired()])
    cel = StringField('Number',validators=[InputRequired()])
    occupation = StringField(validators=[InputRequired()])

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
            return redirect(url_for('index'))
    
    return render_template('register.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
