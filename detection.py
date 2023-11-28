import cv2 as cv
import numpy as np
from utils.masking import Masking
from utils.contours import Contours

class Detection:
    def __init__(self):
        self.camera_index = 1
        self.masking = Masking()
        self.contours = Contours()
        self.card_mask_kernel = np.ones((5,5),np.uint8)
    
    def loop_and_detect(self):
        cap = cv.VideoCapture(self.camera_index)
        ret, frame = cap.read()
        while ret:
            ret, frame = cap.read()
            frame = frame[400:848, 500:837]
            img_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            card_mask = self.masking.remove_mask_result(img_hsv, np.array([40, 50, 50]), np.array([80, 255, 255]))
            card_mask_erode = cv.erode(card_mask, self.card_mask_kernel, iterations=1)
            card_countours,_,center = self.contours.find_contours(frame,card_mask_erode,frame,"Card")

            clas_red = "Unknown"
            clas_black = "Unknown"
            red_obj = self.masking.find_double_mask_result(card_mask,np.array([0,50,50]),np.array([10,255,255]),np.array([165,50,50]),np.array([180,255,255]))
            self.red_obj_erote_kernel = np.ones((5, 5), np.uint8) 
            red_obj = cv.erode(red_obj, self.red_obj_erote_kernel, iterations=1)
            red_obj = cv.dilate(red_obj, self.red_obj_erote_kernel, iterations=2)
            card_countours,num_red,clas_red = self.contours.find_contours(frame,red_obj, card_countours,"Red")
            
            after_red_img = cv.bitwise_xor(card_mask, red_obj)
            lower_black = np.array([0, 0, 0])
            upper_black = np.array([255, 255, 170])
            black_mask = self.masking.find_mask_result(after_red_img, lower_black, upper_black)
            self.black_mask_erote_kernel = np.ones((10, 10), np.uint8)
            black_mask = cv.erode(black_mask, self.black_mask_erote_kernel, iterations=1)
            card_countours,num_black,clas_black = self.contours.find_contours(frame,black_mask, card_countours,"Black")
           
            color = None
            label = "Unknown"
            is_special = False
            if num_black > num_red:
                num = num_black
                color = "Black"
                is_special = False
            else:
                num = num_red
                color = "Red"
                is_special = False
            if num_black > num_red:
                label = clas_black
            else:
                label = clas_red
            if num_black > 1 and num_red > 1:
                is_special = True
            if is_special:
                name = "Card Special"
            else:
                name = str(num) + " "+label
            if num == 1:
                name = "Card Ace " + label
                num = 11
            cv.putText(frame, name, (center[0]-60, center[1]), cv.FONT_HERSHEY_SIMPLEX, 1, (40, 163, 212), 3)
            cv.putText(frame, name, (center[0]-62, center[1]), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)
            cv.imshow("frame", frame)
            return frame, num,label,center