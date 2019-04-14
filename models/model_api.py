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

#from model_test import Vaico_helmet_detection

app = Flask(__name__)
CORS(app)

#model = Vaico_helmet_detection()
#print('----------Model loaded----------')

@app.route('/predict', methods=['POST'])
def predict_on_image():
    #img = str(request.json['image'])
    #model.get_image_from_base64(img)
    #img_2 = Image.open('out3225.jpg')
    #model.compute_current_detection()
    #res_img = model.draw_boundig_box(model.get_current_detection())
    #model.clear_temp_imgs()
    #print(type(res_img))
    #base64_str = base64.b64encode(res_img).decode("utf-8")
    #print(base64_str)
    #pil_img = Image.fromarray(res_img)
    #buff = BytesIO()
    #pil_img.save(buff, format="JPEG")
    #new_image_string = base64.b64encode(buff.getvalue()).decode("utf-8")

    #cv2.imwrite('./out.jpg' , res_img)
    return jsonify({"predicted": np.array(img_2)})

if __name__ == '__main__':
    app.run(debug=True)