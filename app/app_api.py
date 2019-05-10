import datetime
from flask import Flask, request, render_template, redirect, url_for
from flask_mongoengine import MongoEngine, Document
from mongoengine.queryset.visitor import Q
#from wtforms import StringField
#from wtforms.validators import Email
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_cors import CORS
from db_config import db_config
from email_service import Email_services

app = Flask(__name__)
CORS(app)

app.config['MONGODB_SETTINGS'] = {
    'db': 'vaico_works',
    'host': db_config['host']
}

db = MongoEngine(app)

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
    permissions = db.BooleanField()

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
    date_img = db.StringField()
    date_report = db.StringField()
    description = db.StringField()

class Customer(db.Document):
    meta = {'collection': 'customers'}
    name = db.StringField()
    cel = db.StringField()
    email = db.StringField()

@app.route('/')
def index():
    return redirect(url_for('show_index'))

@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()

@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if request.method == 'POST':
        existing_user = User.objects(email=request.form['email']).first()
        if existing_user is None:
            hashpass = generate_password_hash(request.form['password'], method='sha256')
            hey = User(request.form['email'],hashpass,request.form['first_name'],request.form['cel'],request.form['occupation'], False).save()
            # login_user(hey)
            # return redirect(url_for('show_index',email=request.form['email']))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
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
def show_index():
    users = User.objects()
    if(current_user.is_authenticated):
        permissions = current_user.permissions
        session = True
    else:
        permissions = False
        session = False
    return render_template('index.html', permissions = permissions, session = session)


@app.route('/original_gallery', methods=['GET', 'POST'])
@login_required
def original_gallery():
    imgs = Image_Register.objects()
    permissions = current_user.permissions
    if request.method == 'POST':
        date1 = request.form['date1']
        date2 = request.form['date2']
        if(date1 == ""):
            date1 = "1000-01-01"
        elif (date2 == ""):
            date2 = "4000-12-31"
        elif  (date1 == "" and date2 == ""):
            date1 = "1000-01-01"
            date2 = "4000-12-31"
        date1 += " 00:00:00.0000"
        date2 += " 23:59:59.0000"
        imgs = Image_Register.objects(Q(date__gte=date1) & Q(date__lte=date2))
    return render_template('original_gallery.html', data = imgs, permissions = permissions)

@app.route('/processed_gallery', methods=['GET', 'POST'])
@login_required
def processed_gallery():
    imgs = Image_Register.objects() #.order_by('-date')
    permissions = current_user.permissions
    if request.method == 'POST':
        date1 = request.form['date1']
        date2 = request.form['date2']
        if(date1 == ""):
            date1 = "1000-01-01"
        elif (date2 == ""):
            date2 = "4000-12-31"
        elif  (date1 == "" and date2 == ""):
            date1 = "1000-01-01"
            date2 = "4000-12-31"
        date1 += " 00:00:00.0000"
        date2 += " 23:59:59.0000"
        imgs = Image_Register.objects(Q(date__gte=date1) & Q(date__lte=date2))
    return render_template('processed_gallery.html', data = imgs, permissions = permissions)

@app.route('/image/<date>', methods=['GET', 'POST'])
@login_required
def view_image(date):
    permissions = current_user.permissions
    img = Image_Register.objects(date=date)
    info = img._query
    year = info['date'].split(" ")[0].split("-")[0]
    month = info['date'].split(" ")[0].split("-")[1]
    day = info['date'].split(" ")[0].split("-")[2]
    time = info['date'].split(" ")[1].split(".")[0]
    return render_template('view_image.html', data=img, year=year, month=month, day=day, time=time, permissions = permissions)

@app.route('/gallery', methods=['GET', 'POST'])
@login_required
def gallery():
    permissions = current_user.permissions
    data = {}
    imgs = Image_Register.objects()
    for img in imgs:
        if img.place in data.keys():
            data[img.place].append(img)
        else:
            data[img.place] = [img]
    return render_template('gallery.html', imgs = data, permissions = permissions)

@app.route('/sector_gallery/<place>', methods=['GET', 'POST'])
@login_required
def sector_gallery(place):
    imgs = Image_Register.objects(place = place)
    permissions = current_user.permissions
    return render_template('sector_gallery.html', data = imgs, permissions = permissions)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if(current_user.is_authenticated):
        permissions = current_user.permissions
        session = True
    else:
        permissions = False
        session = False
    if request.method == 'POST':
        name = request.form['name']
        cel = request.form['cel']
        email = request.form['email']
        save_customer(name, cel, email)
        message = "Nombre: " + name + "\n" + "Celular: " + cel + "\n" + "Dirección de correo: " + email + "\n" + "Mensaje: " + request.form['message']
        recipient = email.split(",")
        vaico_contact = "vaicoworkscontacto@gmail.com".split(",")
        email_service = Email_services(sender_email="vaicoworkscontacto@gmail.com", password="vaico_works")
        # Email to Vaico Works
        email_service.send_email(vaico_contact, message = message, subject = "Nuevo contacto", attachment = None)
        # Email to customer
        email_service.send_email(recipient, message = "Hola,\n\n Gracias por contactarnos! Nuestro personal revisará tu mensaje y lo responderá lo más pronto posible. \n\n Un saludo cordial, \n\n Vaico Works.", subject = "Vaico Works", attachment = None)
    return render_template('contact.html', permissions = permissions, session = session)

@app.route('/about', methods=['GET'])
def about():
    if(current_user.is_authenticated):
        permissions = current_user.permissions
        session = True
    else:
        permissions = False
        session = False
    return render_template('about.html', permissions = permissions, session = session)

@app.route('/report/<date>', methods=['GET', 'POST'])
@login_required
def generate_report(date):
    permissions = current_user.permissions
    img = Image_Register.objects(date=date)
    name = ""
    user = current_user
    name = user['name']
    email = user['email']
    cel = user['cel']
    occupation = user['occupation']
    if request.method == 'POST':
        for i in Image_Register.objects:
            if(i.date == date):
                original_img = i.original
                processed_img = i.prediction
                date_img = i.date

        title = request.form['title']
        description = request.form['description']
        recipients = request.form['recipients']
        recipientsAux = recipients.split(",")
        email_service = Email_services()
        email_service.get_image_from_base64(processed_img, out_name = "reporte_de_obra")
        email_service.send_email(recipientsAux, message = description, subject = title, attachment = "static/img/reporte_de_obra.jpg")
        save_report(title, name, email, cel, occupation, original_img, processed_img, date_img, str(datetime.datetime.now()), description)
    return render_template('report.html', data=img, name=name, email=email, cel=cel, occupation=occupation, permissions = permissions)

def save_report(title, name, email, cel, occupation, original_img, processed_img, date_img, date_report, description):
    Report(title, name, email, cel, occupation, original_img, processed_img, date_img, date_report, description).save()


def save_customer(name, cel, email):
    Customer(name, cel, email).save()

@app.route('/reports', methods=['GET', 'POST'])
@login_required
def view_reports():
    permissions = current_user.permissions
    reports = Report.objects()
    return render_template("reports.html", data = reports, permissions = permissions)

@app.route('/delete_user', methods=['GET', 'POST'])
@login_required
def delete_user():
    users = User.objects(permissions = False)
    permissions = current_user.permissions
    return render_template("delete_user.html", data = users, permissions = permissions)

@app.route('/delete_user/<email>', methods=['GET', 'POST'])
@login_required
def delete_specific_user(email):
    User.objects(email = email).delete()
    return redirect(url_for('delete_user'))

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80 ,debug=True)
