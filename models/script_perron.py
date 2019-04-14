from imageai.Detection import ObjectDetection
import os
import cv2

execution_path = os.getcwd()


detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath( os.path.join(execution_path , "yolo.h5"))
detector.loadModel()
detections = detector.detectObjectsFromImage(input_image="/home/josh/MEGA/Keras/test_vaico/test_helmets/helmets/IMG_20190402_174115482_HDR.jpg", output_image_path=os.path.join(execution_path , "output.jpeg"), minimum_percentage_probability=30)

n_img = 0
margin = 0.01
print(detections)
img = cv2.imread("/home/josh/MEGA/Keras/test_vaico/test_helmets/helmets/IMG_20190402_174115482_HDR.jpg")
for eachObject in detections:
     print(eachObject)
     name = eachObject["name"]
     x1,y1,x2,y2 = eachObject["box_points"]
     if( name == "person"):
          height, width, channels = img.shape
          print(height, width)
          print(x1,x2,y1,y2)

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

          img_o = img[y1_new:y2_new , x1_new:x2_new]
          #cv2.imshow("original" , img_o)
          cv2.imwrite(os.path.join(execution_path,".", "person{0}.jpg".format(n_img)) , img_o)
          n_img += 1
          #print(eachObject["name"] , " : ", eachObject["percentage_probability"], " : ", eachObject["box_points"] )

