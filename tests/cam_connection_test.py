import cv2
import pytest

@pytest.fixture()
def test_cam_connect():
    video_capture = cv2.VideoCapture(0)
    #print(video_capture.isOpened())
    if not video_capture.isOpened():
        return True
    return False
    

@pytest.fixture()
def test_cam_not_connect():
    video_capture = cv2.VideoCapture(2)
    #print(video_capture.isOpened())
    return video_capture.isOpened()

def test_answer(test_cam_connect,test_cam_not_connect):
    res = test_cam_connect
    res2 = test_cam_not_connect
    assert res == True
    assert res2 == False