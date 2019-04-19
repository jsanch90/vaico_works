"""
Generar requeriments.txt y readme.txt
"""
#install $ pip install https://github.com/OlafenwaMoses/ImageAI/releases/download/2.0.2/imageai-2.0.2-py3-none-any.whl
import cv2
import base64
import os
import time
import datetime
import tensorflow as tf
from io import BytesIO
from PIL import Image
from pymongo import MongoClient
from db_config import db_config
from model_test import Vaico_helmet_detection

global graph
graph = tf.get_default_graph()

model = Vaico_helmet_detection()

client = MongoClient(host=db_config['host'], port=db_config['port'])
db = client.vaico_works

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
    pil_img = Image.fromarray(frame,mode='RGB')
    buff = BytesIO()
    pil_img.save(buff, format="JPEG")
    new_image_string = base64.b64encode(buff.getvalue()).decode("utf-8")
    return new_image_string

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

def image_to_base64(img):
    pass

def start_capture(place,interval=30):
    while True:
        img = take_picture()
        print('initializing prediction')
        pred = predict(img)
        print('sending to db')
        db.image_registers.insert_one({'original':img,'prediction':pred,'place':place,'date':datetime.datetime.now()})
        time.sleep(interval)

start_capture('Mi casa :v')