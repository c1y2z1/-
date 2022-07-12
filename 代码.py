import mediapipe as mp
import cv2
import numpy as np
import subprocess
import os
import virtkey
import time

def get_str_guester(up_fingers,list_lms):
    if len(up_fingers)==1 and up_fingers[0]==8:
        str_guester = "1"
	v.press_keysym(65431)
	v.release_keysym(65431)

       

    elif len(up_fingers)==2 and up_fingers[0]==8 and up_fingers[1]==12:
        str_guester = "2"
        v.press_keysym(65433)
        v.release_keysym(65433)

    elif len(up_fingers)==4 and up_fingers[0]==8 and up_fingers[1]==12 and up_fingers[2]==16 and up_fingers[3]==20:
        str_guester = "4"
	os.system('pactl set-sink-volume 1 +10%')
	time.sleep(1)

    elif len(up_fingers)==5:
        str_guester = "5"
        os.system('pactl set-sink-volume 1 -10%')
	time.sleep(1)
        
    elif len(up_fingers)==2 and up_fingers[0]==4 and up_fingers[1]==20:
        str_guester = "6"
        v.press_unicode(ord('z'))
        v.release_unicode(ord('z'))


    elif len(up_fingers)==3 and up_fingers[0]==4 and up_fingers[1]==8 and up_fingers[2]==12:
        str_guester = "ROCK"
        v.press_keysym(65507)
        v.release_keysym(65433)
        time.sleep(0.5)            
     else:
        str_guester = " "
        
    return str_guester
        

if __name__ == "__main__":
   
   
    cap = cv2.VideoCapture("http://admin:admin@192.168.1.5:8081/")
    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils
  
    while True:
     
        success, img = cap.read()
        if not success:
            continue
        image_height, image_width, _ = np.shape(img)
        
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        results = hands.process(imgRGB)
        
        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            
            mpDraw.draw_landmarks(img,hand,mpHands.HAND_CONNECTIONS)
            
            list_lms = []    
            for i in range(21):
                pos_x = hand.landmark[i].x*image_width
                pos_y = hand.landmark[i].y*image_height
                list_lms.append([int(pos_x),int(pos_y)])
            
            list_lms = np.array(list_lms,dtype=np.int32)
            hull_index = [0,1,2,3,6,10,14,19,18,17,10]
            hull = cv2.convexHull(list_lms[hull_index,:])
            cv2.polylines(img,[hull], True, (0, 255, 0), 2)
                
            n_fig = -1
            ll = [4,8,12,16,20] 
            up_fingers = []
            
            for i in ll:
                pt = (int(list_lms[i][0]),int(list_lms[i][1]))
                dist= cv2.pointPolygonTest(hull,pt,True)
                if dist <0:
                    up_fingers.append(i)
            
            # print(up_fingers)
            # print(list_lms)
            # print(np.shape(list_lms))
            str_guester = get_str_guester(up_fingers,list_lms)
            
            
            cv2.putText(img,' %s'%(str_guester),(90,90),cv2.FONT_HERSHEY_SIMPLEX,3,(255,255,0),4,cv2.LINE_AA)
            
                
             
            for i in ll:
                pos_x = hand.landmark[i].x*image_width
                pos_y = hand.landmark[i].y*image_height
                cv2.circle(img, (int(pos_x),int(pos_y)), 3, (0,255,255),-1)
                    
       
        #cv2.imshow("hands",img)

        key =  cv2.waitKey(1) & 0xFF   

        if key ==  ord('q'):
            break
cap.release() 
