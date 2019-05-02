#install pip install https://github.com/OlafenwaMoses/ImageAI/releases/download/2.0.2/imageai-2.0.2-py3-none-any.whl
from imageai.Detection import ObjectDetection
from imageai.Prediction.Custom import CustomImagePrediction
import numpy as np
from PIL import Image
from skimage import transform
import os
import cv2
import random
from io import BytesIO    



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

    def find_persons(self, img_path, margin=0.02):
        detections = self.detector.detectObjectsFromImage(input_image=img_path, minimum_percentage_probability=30)
        os.remove('.png')
        img = cv2.imread(img_path)
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
                person_path = 'test{0}.jpg'.format(count)
                count +=1
                cv2.imwrite(person_path, person)
                person_points = (person,(y1_new, y2_new, x1_new, x2_new),person_path)
                persons_in_image.append(person_points)
        #print(persons_in_image)
        return persons_in_image
    
    def load_image_for_model(self, image_path):
        np_image = Image.open(image_path)
        #cv2.imwrite('test{0}.jpg'.format(random.randint(1,10000)), image)
        #image2 = Image.fromarray(image, mode='RGB')

        #b = BytesIO()
        #image2.save(b,format="jpeg")

        #image3 = Image.open(b)

        #print(type(image3),'--------------------------------------------------------------------------------')
        np_image = np.array(np_image).astype('float32')/255
        np_image = transform.resize(np_image, (350, 350, 3))
        np_image = np.expand_dims(np_image, axis=0)
        return np_image
    
    def predict_on_image(self,image):
        res = self.classifier.predictImage(image)
        #print(res,'Debug--------------------------------------------------------------------')
        return res
    
    # def prediction_map(self,res,threshold=0.8):
    #     if res[0][0] > threshold:
    #         return 'Tiene casco'
    #     else:
    #         return 'No tiene Casco'
    
    def compute_current_detection(self,img_path):
        res = self.find_persons(img_path)
        current_detection = []
        for image,coord,path in res:
            label = self.predict_on_image(path)[0][0]
            current_detection.append((label,coord,path))

        self.set_current_detection(current_detection)

    def draw_boundig_box(self, data, original_img_path):
        img = cv2.imread(original_img_path)

        for label,coords,path in data:
            y1,y2,x1,x2 = coords
            if label == 'Tiene casco':
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0),thickness = 3)
                cv2.putText(img,'Tiene casco' , (x1, y1-7), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255),thickness = 3, lineType=cv2.LINE_AA)
            else:
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255),thickness = 3)
                cv2.putText(img,'No tiene casco' , (x1, y1-7), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255),thickness = 3, lineType=cv2.LINE_AA)

        return cv2.imwrite('./out{0}.jpg'.format(random.randint(1,10000)) , img)#return img #return cv2.imwrite('./out.jpg' , img)

    def clear_temp_imgs(self):
        for _,_,path in self.current_detection:
            os.remove(path)

    
    
model = Vaico_helmet_detection()
#model.compute_current_detection("/home/josh/MEGA/Keras/test_vaico/test_helmets/no_helmets/IMG_20190405_110505348.jpg")
#model.draw_boundig_box(model.get_current_detection(),"/home/josh/MEGA/Keras/test_vaico/test_helmets/no_helmets/IMG_20190405_110505348.jpg")
model.compute_current_detection("/home/josh/MEGA/U_S_VII/P2/datasets/datos_29_abril_2019/no_casco/29-5/29-598.jpg")
model.draw_boundig_box(model.get_current_detection(),"/home/josh/MEGA/U_S_VII/P2/datasets/datos_29_abril_2019/no_casco/29-5/29-598.jpg")
model.clear_temp_imgs()


