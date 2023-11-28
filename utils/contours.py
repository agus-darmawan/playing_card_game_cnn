import cv2 as cv
import numpy as np

from keras import models
class Contours:
    def __init__(self) -> None:
        pass
    def find_contours(self,imgg,img,img2, name, min_area=6000):
        imgray2 = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        contours2, hierarchy2 = cv.findContours(imgray2, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        num_black = 0
        label = "Unknown"
        img_mini = None
        center = 0,0
        for cnt in contours2:
            x, y, w, h = cv.boundingRect(cnt)
            if w*h < 1500:
                continue
            if w/h < 0.8:
                if name != "Card":
                    continue
            num_black += 1
            img_a = imgg
            img_mini = imgg[y:y+h,x:x+w]
            
            # try:
            im = cv.resize(img_mini,(128,128))
            cv.imshow('Card', im)
            model = models.load_model('./trained/bentuk.h5')
            img_array = np.array(im)
            img_array = np.expand_dims(img_array, axis=0)
            pred = model.predict(img_array)
            result = pred[0]
            max_index = np.argmax(result)
            if max_index == 0:
                label = 'clubs'
            elif max_index == 1:
                label = 'diamond'
            elif max_index == 2:
                label = 'heart'
            elif max_index == 3:
                label = 'spades'
            else:
                label = 'unknown'

            if name == "Card":
                
                cv.rectangle(img2, (x, y), (x + w, y + h), (0, 0, 0), 2)
                # find center 
                center = (x+w//2,y+20)
        if name != "Card":
            return img2, num_black, label
        return img2, num_black,center