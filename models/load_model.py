from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
from keras.models import load_model

import numpy
import os


model = load_model('vaico_mobilenet.h5')

from PIL import Image
import numpy as np
from skimage import transform

def load(filename):
   np_image = Image.open(filename)
   print(type(np_image),'--------------------------------------------------------------------------')
   np_image = np.array(np_image).astype('float32')/255
   np_image = transform.resize(np_image, (350, 350, 3))
   np_image = np.expand_dims(np_image, axis=0)
   return np_image

def prediction(res):
   if res[0][0] > 0.8:
      return 'Tiene casco'
   else:
      return 'No tiene Casco'

image = load('test7733.jpg')
print(type(image))
res = model.predict(image)
print(prediction(res))
print(res)
