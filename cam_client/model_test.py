#install pip install https://github.com/OlafenwaMoses/ImageAI/releases/download/2.0.2/imageai-2.0.2-py3-none-any.whl
import base64
import numpy as np
import os
import cv2
import io
from imageai.Prediction.Custom import CustomImagePrediction
from imageai.Detection import ObjectDetection
from PIL import Image
from skimage import transform
from imageio import imread


class Vaico_helmet_detection:

    def __init__(self,yolo_weigths='../../models_h5/yolo.h5', model_weigths='../../models_h5/model_ex-009_acc-0.921875.h5', model_json='../../models_h5/model_class.json'):
        self.detector = ObjectDetection()
        self.detector.setModelTypeAsYOLOv3()
        self.detector.setModelPath(yolo_weigths)
        self.detector.loadModel()
        
        self.classifier = CustomImagePrediction()
        self.classifier.setModelTypeAsResNet()
        self.classifier.setModelPath(model_weigths)
        self.classifier.setJsonPath(model_json)
        self.classifier.loadModel(num_objects=2)

        self.current_detection = []

    def get_current_detection(self):
        return self.current_detection
    
    def set_current_detection(self,current_detection):
        self.current_detection = current_detection

    def find_persons(self, img_base64, margin=0.01):
        detections = self.detector.detectObjectsFromImage(input_image='static/img/temp_img.jpg', minimum_percentage_probability=30)
        os.remove('.png')
        img = cv2.imread('static/img/temp_img.jpg')
        persons_in_image =[]
        count = 0

        for each_object in detections:
            name = each_object["name"]
            if( name == "person"):
                x1,y1,x2,y2 = each_object["box_points"]
                height, width, channels = img.shape
                """
                print(height, width)#debug
                print(x1,x2,y1,y2)#debug
                """

                x1_new = 0
                x2_new = 0
                y1_new = 0
                y2_new = 0

                if (y1-(y1*margin)) < 0:
                    y1_new = y1
                else:
                    y1_new = int((y1-(y1*margin)))

                if (x1-(x1*margin)) < 0:
                    x1_new = x1
                else:
                    x1_new = int((x1-(x1*margin)))

                if (y2+(y2*margin)) > height:
                    y2_new = y2
                else:
                    y2_new = int((y2+(y2*margin)))
                
                if (x2+(x2*margin)) > width:
                    x2_new = x2
                else:
                    x2_new = int((x2+(x2*margin)))

                person = img[y1_new:y2_new , x1_new:x2_new]
                person_path = 'static/img/test{0}.jpg'.format(count)
                count +=1
                cv2.imwrite(person_path, person)
                person_points = (person,(y1_new, y2_new, x1_new, x2_new),person_path)
                persons_in_image.append(person_points)

        return persons_in_image
    
    def load_image_for_model(self, image_path):
        np_image = Image.open(image_path)
        np_image = np.array(np_image).astype('float32')/255
        np_image = transform.resize(np_image, (350, 350, 3))
        np_image = np.expand_dims(np_image, axis=0)
        return np_image
    
    def predict_on_image(self,image):
        res = self.classifier.predictImage(image)
        print(res,'-------------------------debug---------------------------------\n borrar est en /app/model_test.py metodo predict_on_image()')
        return res
    
    # def prediction_map(self,res,threshold=0.8):
    #     if res[0][0] > threshold:
    #         return 'Tiene casco'
    #     else:
    #         return 'No tiene Casco'

    def get_image_from_base64(self,base64_str):
        #b64_string = base64_str.decode()
        img_temp = imread(io.BytesIO(base64.b64decode(base64_str)))
        cv2_img = cv2.cvtColor(img_temp, cv2.COLOR_RGB2BGR)
        cv2.imwrite("static/img/temp_img.jpg", cv2_img)
    
    def compute_current_detection(self,img_path='static/img/temp_img.jpg'):
        res = self.find_persons(img_path)
        current_detection = []
        for image,coord,path in res:
            label = self.predict_on_image(path)[0][0]
            current_detection.append((label,coord,path))

        self.set_current_detection(current_detection)

    def draw_boundig_box(self, data, original_img_path='static/img/temp_img.jpg'):
        img = cv2.imread(original_img_path)

        for label,coords,_ in data:
            y1,y2,x1,x2 = coords
            if label == 'Tiene casco':
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0),thickness = 3)
                cv2.putText(img,'Tiene casco' , (x1, y1-7), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255),thickness = 3, lineType=cv2.LINE_AA)
            else:
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255),thickness = 3)
                cv2.putText(img,'No tiene casco' , (x1, y1-7), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255),thickness = 3, lineType=cv2.LINE_AA)

        return img#return cv2.imwrite('./out.jpg' , img)#return img #return cv2.imwrite('./out.jpg' , img)

    def clear_temp_imgs(self):
        for _,_,path in self.current_detection:
            os.remove(path)
        os.remove('static/img/temp_img.jpg')
    
    
#model = Vaico_helmet_detection()
#model.get_image_from_base64("/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAIBAQEBAQIBAQECAgICAgQDAgICAgUEBAMEBgUGBgYFBgYGBwkIBgcJBwYGCAsICQoKCgoKBggLDAsKDAkKCgr/2wBDAQICAgICAgUDAwUKBwYHCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgr/wAARCAAqAB4DASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwCglgrECORmYHOTyR7+9XYv2K/2lv2p7jR7D9lf4nafp2uxazFFd6FfqAv2NNrzXU0vLJHg7MbSCcL95gKk8jZ8xJDDk44/Gvqb/gm7dat8O9Z1D4k22pXEcGpXSaMkMTMqvIsclwXbDAkAAYXOPn55Aw8NSdetZHpzqRowufOXxj+FGufBj4na98JvEvkpqOhX7W872+TG4Kq6OmcfKyMrD/ePAxXNxW5t0BlZG4wDjrXpv7W2q2niz9obxL4phiWOS9uUa5IJYtKsYjJyT3CZ/H3rzSaCOaNYzNgL61FePs6vKhQnGceZkC311dXAK2zKo6sW9+tfXP7G/jfw54Y/Zv8AEGp6y0JOh63LcupcFkaaCKGBck/KGk3cnsjV8ewX86IVWTaNvUZz+Yr59/4Kb3fje7/ZnlsvDHiHU7fTJvENn/wkem2N7IkN9CvmeV56qcSBJjGwyOCQeoFbYKuqNS5liIupA+x/jfe2l/8AE/VNXsriKWO48hme3fdEJBAgdVI4YB93PqK41/KkbcEz7AV5t+z/AOJLnVf2ePAupK5V28KWCyKyfxCBFPP1Q9OvU+ld/YahcXEeZMK2Mk+tZYiftKzkXS92nYyUDmBkkdgQrbSMn+VeV/taRa5qH7PXifR9C0O8vLu+sDCPKthKsa7gSSAchuPl9yOlerXPFtkf3K57xyzLbWMKsQklygkQHhuR1HeuSM2mbOKscV+yrZeKdD+AvhXwn4rtDb3lho6pNE7hjEHd5Y1ODgEJJGMHkcjtXq+nrfQLsCZ+XksRisvw9aWsXh5Fito1BR2IVAMtvHP15PNbdkB9hhGBjZ0onNtkJJH/2Q==")
#model.compute_current_detection()
#model.draw_boundig_box(model.get_current_detection())




