import cv2 as cv
import numpy as np

class Masking:
    def __init__(self) -> None:
        pass
    def find_mask_result(self,img : np.ndarray, lower : np.ndarray, upper : np.ndarray) -> np.ndarray:
        '''
        params:
            img: np.ndarray
            lower: np.ndarray lower bound of HSV
            upper: np.ndarray upper bound of HSV
        return:
            np.ndarray result of masking
        '''
        mask = cv.inRange(img, lower, upper)
        return cv.bitwise_and(img, img, mask=mask)

    def find_double_mask_result(self,img : np.ndarray, lower1 : np.ndarray, upper1 : np.ndarray, lower2 : np.ndarray, upper2 : np.ndarray) -> np.ndarray:
        '''
        params:
            img: np.ndarray
            lower1: np.ndarray lower bound of HSV
            upper1: np.ndarray upper bound of HSV
            lower2: np.ndarray lower bound of HSV
            upper2: np.ndarray upper bound of HSV
        return:
            np.ndarray result of masking
        '''
        mask1 = cv.inRange(img, lower1, upper1)
        mask2 = cv.inRange(img, lower2, upper2)
        mask = mask1 + mask2
        return cv.bitwise_and(img, img, mask=mask)
    
    def remove_mask_result(self,img : np.ndarray, lower : np.ndarray, upper : np.ndarray) -> np.ndarray:
        '''
        params:
            img: np.ndarray
            lower: np.ndarray lower bound of HSV
            upper: np.ndarray upper bound of HSV
        return:
            np.ndarray result of masking
        '''
        res = self.find_mask_result(img, lower, upper)
        img_res = cv.bitwise_xor(img, res)
        return img_res