import cv2
import os
import sys
import time


def take_pictures(dir_name,name,cam=0):
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        raise Exception("Could not open video device")
    ret, frame = video_capture.read()
    full_path = dir_name+'/'+name+'.jpg'
    cv2.imwrite(full_path,frame)
    print("image '{0}' saved".format(full_path))

if __name__ == "__main__":
    counter=0
    if len(sys.argv) <= 4:
        print("Usage: python image_taker.py <directory path to save the images> <device> <out_name> <delay>\nIf the directory doesn't exist, it will be created",
            "\ndevice parameter is a number, 0 is the default webcam, if you have other cam connected and you want to use that camera this parameter must be 1",
            "\nout_name paramater is the name that you want to use to save your pictures",
            "\ndelay parameter is the number of seconds to wait until take the next picture")
        print("Example" )
        print("python image_taker.py '/home/user/images' 0 'block_19_5' 15")
        sys.exit(0)
    dir_name = sys.argv[1]
    device = int(sys.argv[2])
    out_name = sys.argv[3]
    delay = int(sys.argv[4])
    if  not os.path.exists(dir_name):
        os.mkdir(dir_name)

    while True:
        img_name=out_name+str(counter)
        take_pictures(dir_name,img_name,cam=device)
        time.sleep(delay)
        counter = counter + 1