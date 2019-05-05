#install requeriments.txt
import cv2
import base64
#import os
import time
import sys
import datetime
from io import BytesIO
from PIL import Image
from pymongo import MongoClient
from db_config import db_config
from model_test import Vaico_helmet_detection

class Cam_Client():
    
    def __init__(self,place):
        self.client = MongoClient(db_config['host'])
        self.db = self.client.vaico_works
        self.model = Vaico_helmet_detection()
        saved_places = self.db.places.find_one({'place':place})
        if saved_places == None:
            self.db.places.insert_one({'place':place})
        self.place = place
        

    def take_picture(self,path):
        ##
        #UNCOMENT THIS 
        ## 
        
        #video_capture = cv2.VideoCapture(1)
        #if not video_capture.isOpened():
        #    raise Exception("Could not open video device")
        #ret, frame = video_capture.read()

        ##
        #UNCOMENT THIS 
        ## 

        frame = cv2.imread(path)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #video_capture.release()
        pil_img = Image.fromarray(frame,mode='RGB')
        buff = BytesIO()
        pil_img.save(buff, format="JPEG")
        new_image_string = base64.b64encode(buff.getvalue()).decode("utf-8")
        return new_image_string

    def predict(self,img):
        self.model.get_image_from_base64(img)
        self.model.compute_current_detection()
        res_img = self.model.draw_boundig_box(self.model.get_current_detection())
        self.model.clear_temp_imgs()
        I = cv2.cvtColor(res_img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(I,mode='RGB')
        buff = BytesIO()
        pil_img.save(buff, format="JPEG")
        new_image_string = base64.b64encode(buff.getvalue()).decode("utf-8")
        return new_image_string

    # def start_capture(self,interval=10):
    #     while True:
    #         time.sleep(interval)
    #         img = self.take_picture()
    #         print('initializing prediction')
    #         pred = self.predict(img)
    #         print('sending to db')
    #         self.db.image_registers.insert_one({'original':img,'prediction':pred,'place':self.place,'date':str(datetime.datetime.now())})

##
#UNCOMENT THIS 
## 

# if __name__ == "__main__":

#     if len(sys.argv) <= 1:
#         print("Usage: python cam_client.py <place where camera is>" )
#         print("Example" )
#         print("python cam_client.py 'science building'")
#         sys.exit(0)
#     cc = Cam_Client(sys.argv[1])
#     cc.start_capture()

##
#UNCOMENT THIS
##

if __name__ == "__main__":

    cc = Cam_Client(sys.argv[1])
    #cc.take_picture(sys.argv[2])
    img = cc.take_picture(sys.argv[2])
    print('initializing prediction')
    pred = cc.predict(img)
    print('sending to db')
    cc.db.image_registers.insert_one({'original':img,'prediction':pred,'place':cc.place,'date':str(datetime.datetime.now())})


#global graph
# graph = tf.get_default_graph()

# model = Vaico_helmet_detection()

# client = MongoClient(db_config['host'])
# db = client.vaico_works

# def take_picture():
#     video_capture = cv2.VideoCapture(0)
#     if not video_capture.isOpened():
#         raise Exception("Could not open video device")
#         # Read picture. ret === True on success
#     ret, frame = video_capture.read()
#     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     #cv2.imwrite('./test_cam.jpg', frame)
#     # Close device
#     video_capture.release()
#     pil_img = Image.fromarray(frame,mode='RGB')
#     buff = BytesIO()
#     pil_img.save(buff, format="JPEG")
#     new_image_string = base64.b64encode(buff.getvalue()).decode("utf-8")
#     return new_image_string

# def predict(img):
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
#     return new_image_string

# def image_to_base64(img):
#     pass

# def start_capture(place,interval=30):
#     while True:
#         img = take_picture()
#         print('initializing prediction')
#         pred = predict(img)
#         print('sending to db')
#         db.image_registers.insert_one({'original':img,'prediction':pred,'place':place,'date':datetime.datetime.now()})
#         time.sleep(interval)

# start_capture('Mi casa :v')