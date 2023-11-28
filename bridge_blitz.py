import cv2 as cv
import numpy as np
from loguru import logger
from detection import Detection

import time
from pygame import mixer


mixer.init()
mixer.music.load("audio/backsound.mp3")

 
class BridgeBlitz:
   
    def __init__(self):
        self.detector = Detection()
        self.first_player = True
        self.started_time = time.time()
        self.time_detik = 0.0
        self.card_remain = 52
        self.is_play = True 
        self.computer_cards = []
        self.computer_cards_num = []
        self.computer_cards_label = []
        self.player_cards = []
        self.player_cards_num = []
        self.player_cards_label = []

        self.player_main_card = []  
        self.player_main_card_num = []
        self.player_main_card_label = []
        self.computer_main_card = []
        self.computer_main_card_num = []
        self.computer_main_card_label = []

        self.opening_card = []
        self.opening_card_num = [] 
        self.opening_card_label = []
        self.turn = "Computer"

        self.is_awal_game = True
        self.is_awal_gamee = True


        
        self.is_new_game = True
        self.status_array = ["Put Computer Card", 
                             "Put Player Card",
                             "Put Opening Card",
                             "Computer Turn",
                             "Player Turn",
                             "Computer Win",
                             "Player Win",
                             "Computer Champion",
                             "Player Champion",
        ]
        self.status = self.status_array[0]


                             
    

    def get_time(self):
        self.time_detik = 900 - (time.time() - self.started_time)
        return str(int(self.time_detik//60)) + ":" + str(int(self.time_detik%60))
    
    def get_computer_card(self):
        _,num,label,_ = self.detector.loop_and_detect()
        list_card = []
        while len(list_card) < 5:
            card = str(num) + label
            if card not in list_card:
                list_card.append(card)
        return list_card
    
    
    def show(self):
        background = cv.imread('img/game_bg.png')
        self.started_time = time.time()
        while True:
            background = cv.imread('img/game_bg.png')
            img,num,label,center = self.detector.loop_and_detect()
            str_time = self.get_time()
            cv.imshow('Bridge Blitz', background)
            x_offset = 390
            y_offset = 313
            background[y_offset:y_offset+img.shape[0], x_offset:x_offset+img.shape[1]] = img
            cv.imshow('Bridge Blitz', background)
            
            if self.is_new_game:
                if len(self.computer_cards) < 5:
                    self.status = self.status_array[0]
                    card = str(num) + label
                    if label == "Unknown":
                        continue
                    if card not in self.computer_cards:
                        self.computer_cards.append(card)
                        self.computer_cards_num.append(num)
                        self.computer_cards_label.append(label)
                    # add delay
                    time.sleep(0.5)
    
                
                
                elif len(self.player_cards) < 5:
                    self.status = self.status_array[1]
                    card = str(num) + label
                    if label == "Unknown":
                        continue
                    if card not in self.player_cards and card not in self.computer_cards:  
                        self.player_cards.append(card)
                        self.player_cards_num.append(num)
                        self.player_cards_label.append(label)
                    # add delay
                    time.sleep(0.5)
                else:
                    self.is_new_game = False
            
                self.card_remain = 52 - len(self.computer_cards) - len(self.player_cards)
            for i in range(len(self.computer_cards)):
                card = cv.imread('img/card/'+str(self.computer_cards[i])+'.png')
                card = cv.resize(card,(112,154))
                x_offset = 10 + (i*112)
                y_offset = 10
                background[y_offset:y_offset+card.shape[0], x_offset:x_offset+card.shape[1]] = card
            for i in range(len(self.player_cards)):
                card = cv.imread('img/card/'+str(self.player_cards[i])+'.png')
                card = cv.resize(card,(112,154))
                x_offset = 10 + (i*112)
                y_offset = 908
                background[y_offset:y_offset+card.shape[0], x_offset:x_offset+card.shape[1]] = card
            

            cv.putText(background, self.status,(1200,380), cv.FONT_HERSHEY_SIMPLEX , 1.2,  
                    (255,255,255), 2, cv.LINE_AA, False)
            cv.putText(background, str(self.card_remain),(1365,680), cv.FONT_HERSHEY_SIMPLEX , 2,  
                    (255,255,255), 10, cv.LINE_AA, False) 
            cv.putText(background, str_time,(1310,880), cv.FONT_HERSHEY_SIMPLEX , 2,  
                    (255,255,255), 10, cv.LINE_AA, False) 
            if self.is_new_game:
                if len(self.computer_cards) == 5 and len(self.player_cards) == 5:
                    self.status = self.status_array[2]

            if self.first_player and len(self.computer_cards) == 5 and len(self.player_cards) == 5:
                self.status = self.status_array[2]
                card = str(num) + label
                if label == "Unknown":
                        continue
                if card not in self.player_cards and card not in self.computer_cards: 
                    self.opening_card = card
                    self.opening_card_num = num 
                    self.opening_card_label = label
                    self.card_remain -= 1
                    self.first_player = False
                    self.is_awal_game = True
                    self.turn = "Player"
                    self.status = self.status_array[3]
            
            if self.is_awal_game and len(self.opening_card) > 0:
                cv.putText(background, str("Opening Card " +self.opening_card),(1200,340), cv.FONT_HERSHEY_SIMPLEX , 1.2,  
                    (255,255,255), 2, cv.LINE_AA, False)
                
                if self.turn == "Player":
                    self.status = self.status_array[4]
                    if label == "Unknown":
                        continue
                    elif num != self.opening_card_num:
                        card = str(num) + label
                        logger.info(card)
                        for i in range(len(self.player_cards)):
                            if self.player_cards_label[i] == label:
                                if self.player_cards_label[i] == self.opening_card_label:
                                    self.player_main_card.append(self.player_cards[i])
                                    self.player_main_card_num.append(self.player_cards_num[i])
                                    self.player_main_card_label.append(self.player_cards_label[i])
                                    self.player_cards.pop(i)
                                    self.player_cards_num.pop(i)
                                    self.player_cards_label.pop(i)
                                    self.turn = "Computer"
                                    break
                                logger.debug("card is not same with opening card")
                        logger.error("card is not in player cards")
                    else:
                        logger.debug("card is same with opening card")
                elif self.turn == "Computer":
                    self.status = self.status_array[3]
                    for i in range(len(self.computer_cards)):
                        if self.computer_cards_label[i] == self.opening_card_label:
                            self.computer_main_card.append(self.computer_cards[i])
                            self.computer_main_card_num.append(self.computer_cards_num[i])
                            self.computer_main_card_label.append(self.computer_cards_label[i])
                            self.computer_cards.pop(i)
                            self.computer_cards_num.pop(i)
                            self.computer_cards_label.pop(i)
                            self.is_awal_game = False
                            break
            if self.is_awal_gamee and not self.is_awal_game:
                if len(self.player_main_card)> 0 and len(self.computer_main_card) > 0:
                    if self.computer_main_card_num[0] > self.player_main_card_num[0]:
                        self.turn = "Computer"
                        self.status = self.status_array[5]
                    else:
                        self.turn = "Player"
                        self.status = self.status_array[6]
                    self.is_awal_gamee = False     
            

            cv.imshow('Bridge Blitz', background)
            if self.is_play:
                mixer.music.play()
                self.is_play = False
            mixer.music.get_busy()  
            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                break

def main():
    bridge_blitz = BridgeBlitz()
    bridge_blitz.show()

if __name__ == '__main__':
    main()