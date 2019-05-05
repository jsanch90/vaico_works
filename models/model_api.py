import base64
#import os
import cv2
import tensorflow as tf
from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
from flask_pymongo import PyMongo
from io import BytesIO
from PIL import Image
from model_test import Vaico_helmet_detection

app = Flask(__name__)
CORS(app)

app.config['MONGO_DBNAME'] = 'vaico_works'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/vaico_works'
app.config['SECRET_KEY'] = 'vaico123s'

mongo = PyMongo(app)

global graph
graph = tf.get_default_graph()

model = Vaico_helmet_detection()
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


#@app.route('/login', methods=['POST'])


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
