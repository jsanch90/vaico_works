from imageai.Detection import ObjectDetection
import os
import cv2
import sys

detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath('../../models_h5/yolo.h5')
detector.loadModel()

def find_persons(imgs_dir, out_dir, margin=0.02):

    if not os.path.exists(imgs_dir):
        print('Input directory does not exists')
        sys.exit(0)

    if not os.path.exists(out_dir):
        print(out_dir,'created')
        os.mkdir(out_dir)
    
    imgs = os.listdir(imgs_dir)

    count = 0
    for _img in imgs:
        image = imgs_dir+'/'+_img
        print(image)
        detections = detector.detectObjectsFromImage(input_image=image, minimum_percentage_probability=30)
        os.remove('.png')
        img = cv2.imread(image)
        for each_object in detections:
            name = each_object["name"]
            if( name == "person"):
                x1,y1,x2,y2 = each_object["box_points"]
                height, width, _ = img.shape
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
                person_path = out_dir+'/'+out_dir.split('/')[-1]+str(count)+'.jpg'
                count +=1
                cv2.imwrite(person_path, person)
                print('Image:',person_path,'saved')


if __name__ == "__main__":
    if len(sys.argv) <= 2:
        print("Usage: python yolo_directory.py <input directory with images> <output directory>\nIf output_directory doesn't exist, it will be created")
        print("Example" )
        print("python yolo_directory.py '/home/user/images' '/home/user/persons'")
        sys.exit(0)

    _input = sys.argv[1]
    out = sys.argv[2]

    find_persons(_input,out)