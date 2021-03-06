import cv2
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

data=np.load("face_data.npy")

X=data[:,1:].astype(int)
y=data[:,0]

model=KNeighborsClassifier()

model.fit(X,y)
cap=cv2.VideoCapture(0)
detector=cv2.CascadeClassifier("./haarcascade_frontalface_default.xml")
while True:
    ret,frame=cap.read()
    
    if ret:
        faces=detector.detectMultiScale(frame)
        
        for face in faces:
            x,y,w,h=face
            
            cut=frame[y:y+h,x:x+h]
            
            fix=cv2.resize(cut,(100,100))
            gray=cv2.cvtColor(fix,cv2.COLOR_BGR2GRAY)
            
            output=model.predict([gray.flatten()])
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            
            cv2.putText(frame,str(output[0]),(x,y-10),cv2.FONT_HERSHEY_COMPLEX,2,(255,0,0),2)
            print(output)
            #cv2.imshow("my face",gray)
        
        cv2.imshow("My Screen",frame)
    
    key=cv2.waitKey(1)
    
    if key==ord("q"):
        break
cap.release()
cv2.destroyAllWindows()