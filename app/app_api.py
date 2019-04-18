import base64
import os
import cv2
import tensorflow as tf
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
from model_test import Vaico_helmet_detection

app = Flask(__name__)
CORS(app)

app.config['MONGODB_SETTINGS'] = {
    'db': 'vaico_works',
    'host': 'mongodb://localhost:27017/vaico_works'
}

db = MongoEngine(app)
app.config['SECRET_KEY'] = 'vaico123s'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

global graph
graph = tf.get_default_graph()

model = Vaico_helmet_detection()
#model = 1 # descomentar la linea de arriba y borrar esta, y descomentar el import 
print('----------Model loaded----------')

# @app.route('/predict', methods=['POST'])
# def predict_on_image():
#     img = str(request.json['image'])
#     model.get_image_from_base64(img)
#     with graph.as_default():
#         model.compute_current_detection()
#         res_img = model.draw_boundig_box(model.get_current_detection())
#     model.clear_temp_imgs()
#     I = cv2.cvtColor(res_img, cv2.COLOR_BGR2RGB)
#     pil_img = Image.fromarray(I,mode='RGB')
#     buff = BytesIO()
#     pil_img.save(buff, format="JPEG")
#     new_image_string = base64.b64encode(buff.getvalue()).decode("utf-8")
#     return jsonify({"predicted": new_image_string})

def predict(img):
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
    return new_image_string

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

class Image_Register(db.Document):                                                                                            
    meta = {'collection': 'image_registers'}                                                                                             
    original = db.StringField()
    processed = db.StringField()
    date = db.StringField()

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
    #email = request.args['email']
    res_img = take_picture()
    pil_img = Image.fromarray(res_img,mode='RGB')
    buff = BytesIO()
    pil_img.save(buff, format="JPEG")
    new_image_string = base64.b64encode(buff.getvalue()).decode("utf-8")
    res_pred = predict(new_image_string)
    save_register(new_image_string,res_pred,str(datetime.datetime.now()))
    return render_template('index.html',image=new_image_string, pred=res_pred)


def take_picture():
    video_capture = cv2.VideoCapture(0) 
    if not video_capture.isOpened():                                                                                                                                          
        raise Exception("Could not open video device")                                                                                                                        
        # Read picture. ret === True on success                                                                                                                               
    ret, frame = video_capture.read()                                                                                                                                         
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)                                                                                                                            
    #cv2.imwrite('./test_cam.jpg', frame)
    # Close device                                                                                                                                                            
    video_capture.release()
    return frame

def save_register(original_img, proc_img, date):
    Image_Register(original_img,proc_img,date).save()


@app.route('/show_gallery', methods=['GET', 'POST'])
@login_required
def show_gallery():
    imgs = Image_Register.objects
    return render_template('portfolio-4-col.html',data=imgs)

@app.route('/gallery', methods=['GET', 'POST'])
@login_required
def gallery():
    return render_template('portfolio-2-col.html')








if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
