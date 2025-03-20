from moviepy.editor import VideoFileClip
from twilio.rest import Client
import pygame
import cv2, dlib
import numpy as np
from imutils import face_utils
import time
from keras.models import load_model


IMG_SIZE = (34, 26)


vc2=0
stack2=0

two_count=0    #사용자가 자리를 벗어나거나 잠시 내릴때 자동종료하기위한 변수
jol_count=0    #지속적인 경고에도 일어나지 못할때 문자 보내기위한 변수

ws=0
start=0             #전방
startc=0
end=0

starte=0
startec=0           #졸음
ende=0


startce=0
startcode=0



detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

model = load_model('models/2023_01_28_01_31_46.h5')
model.summary()

def send_warn_message():   
    account_sid = 'ACb938bfca389bae47c22d38191043374c'
    auth_token = '9372f10f3484f2f55c05652b05100366'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to="+821072715939",
        from_="+13204387923",
        body="비상! 비상! 운전자의 상태확인이 필요합니다.")

    print(message.sid)


def jol_warnings():                         #졸음운전 경고
    pygame.display.set_caption('warn')

    clip = VideoFileClip('jol.mp4')
    clip.preview()
    pygame.quit()
    
    
def eye_warnings():                         #전방주시 경고
    pygame.display.set_caption('warn')

    clip = VideoFileClip('eye_on_board.mp4')
    clip.preview()
    pygame.quit()
   
def warnings():                             #복합 졸음운전 경고
    pygame.display.set_caption('warn')

    clip = VideoFileClip('continuity_jol.mp4')
    clip.preview()
    pygame.quit()

       
       
def crop_eye(img, eye_points):                  #눈 박스 만들기
  x1, y1 = np.amin(eye_points, axis=0)
  x2, y2 = np.amax(eye_points, axis=0)
  cx, cy = (x1 + x2) / 2, (y1 + y2) / 2

  w = (x2 - x1) * 1.2
  h = w * IMG_SIZE[1] / IMG_SIZE[0]

  margin_x, margin_y = w / 2, h / 2

  min_x, min_y = int(cx - margin_x), int(cy - margin_y)
  max_x, max_y = int(cx + margin_x), (cy + margin_y)

  eye_rect = np.rint([min_x, min_y, max_x, max_y]).astype(np.int64)

  eye_img = gray[eye_rect[1]:eye_rect[3], eye_rect[0]:eye_rect[2]]

  return eye_img, eye_rect

# main




cap = cv2.VideoCapture(0) ##외부 웹캠

pygame.mixer.init()
p=pygame.mixer.Sound('startvoice.wav')
p.play()
time.sleep(11)


while cap.isOpened():
  ret, img_ori = cap.read()
  
  if not ret:
    break
   
 
  img_ori = cv2.resize(img_ori, dsize=(0, 0), fx=0.5, fy=0.5)

  img = img_ori.copy()
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  faces = detector(gray)
  
  
     
  
  
  if faces and startce==0: 
    if startcode<100:
        startcode+=1
        print("READY")
        continue
    elif startcode>=100:
        startce=1
        p=pygame.mixer.Sound('deepstart.wav')
        p.play()
        print("START DRIVE")
        
 
    
    
  xc=((vc2)**(1/3))+((stack2)**(1/2))    
      
  if xc>10:
     warnings()
     jol_count+=1
     stack2=0
     xc=0
     vc2=0      
  
   
    
  
  if not faces and startce==1:
      if startc==0:
         start = time.time()
         print(start)
         startc=1   
         vc2+=1
         
      elif startc==1:
         vc2+=1
         jol_count=0
         end =time.time()
  else:
      jol_count=0
      startc=0
    
      
  if end-start > 4.3:
      eye_warnings()
      jol_count+=1
      startc=0
      start=0
      end=0
      startd=0
      
  if ws>10000:
      ws=0
      
  
  
  
  if jol_count>=3:
     send_warn_message()
     jol_count=0
     
  for face in faces:
   ws+=1 
     
   if ws%5==0:
       
  
   
       
       
    shapes = predictor(gray, face)
    shapes = face_utils.shape_to_np(shapes)

    eye_img_l, eye_rect_l = crop_eye(gray, eye_points=shapes[36:42])
    

    
    eye_img_l = cv2.resize(eye_img_l, dsize=IMG_SIZE)
    eye_input_l = eye_img_l.copy().reshape((1, IMG_SIZE[1], IMG_SIZE[0], 1)).astype(np.float32) / 255.
   

    pred_l = model.predict(eye_input_l)
   

    # visualize
    state_l = 'O %.1f' if pred_l > 0.1 else '- %.1f'
    
        
    state_l = state_l % pred_l
   
    
    cv2.rectangle(img, pt1=tuple(eye_rect_l[0:2]), pt2=tuple(eye_rect_l[2:4]), color=(255,255,255), thickness=2)
   

    cv2.putText(img, state_l, tuple(eye_rect_l[0:2]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
    
    
   
        
    
    if pred_l <= 0.3:
        if startec==0:
           stack2 += 1
           starte = time.time()
           print(starte)
           startec=1   
           ende =time.time()
        elif startec==1:
           jol_count=0
           ende =time.time()
    else:
        jol_count=0
        startec=0
        stack2=0
        vc=0
        
   
           
    if ende-starte > 3:
        jol_warnings()
        jol_count+=1
        startec=0
        starte=0
        ende=0
        vc2=0
        start2=0
        
     
   #for 문 끝
    
    
       
  cv2.imshow('result', img)
 
  if cv2.waitKey(1) == ord('q'):
    break

cv2.destroyAllWindows()
