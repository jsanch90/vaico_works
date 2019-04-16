from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
import base64
import time
import os
import cv2
from io import BytesIO
from PIL import Image
import numpy as np
import keras
from model_test import Vaico_helmet_detection
import tensorflow as tf

app = Flask(__name__)
CORS(app)

global graph
graph = tf.get_default_graph()
model = Vaico_helmet_detection()

print('----------Model loaded----------')

@app.route('/predict', methods=['POST'])
def predict_on_image():
    #
    img = str(request.json['image'])
    model.get_image_from_base64(img)
    with graph.as_default():
        model.compute_current_detection()
        res_img = model.draw_boundig_box(model.get_current_detection())
    model.clear_temp_imgs()

    I = cv2.cvtColor(res_img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(I,mode='RGB')
    pil_img.show()
    buff = BytesIO()
    pil_img.save(buff, format="JPEG")
    new_image_string = base64.b64encode(buff.getvalue()).decode("utf-8")
    #cv2.imwrite('./out.jpg' , res_img)
    return jsonify({"predicted": new_image_string})

if __name__ == '__main__':
    app.run(debug=True)
