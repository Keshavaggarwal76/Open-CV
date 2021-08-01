import cv2
import  numpy as np
from os import listdir
from  os.path import isfile, join

face_classifier = cv2.CascadeClassifier("C:/Python 3.7/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml")
def face_extractor(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray,1.3,5)
    if faces is():
        return None
    for(x,y,w,h) in faces:
        cropped_face = img[y:y+h, x:x+w]
    return cropped_face
cap = cv2.VideoCapture(0)
count = 0
while True:
    ret, frame = cap.read()
    if face_extractor(frame) is not None:
        count+=1
        face = cv2.resize(face_extractor(frame),(200,200))
        face = cv2.cvtColor(face,cv2.COLOR_BGR2GRAY)
        file_name_path = "C:/Users/Admin/Documents/Keshav/Python Practice/Open CV/Faces/user"+str(count)+".jpg"
        cv2.imwrite(file_name_path,face)

        cv2.putText(face,str(count),(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
        cv2.imshow("Face Cropper",face)
    else:
        print("Face not Found")
        pass
    if cv2.waitKey(1)==13 or count==100:
        break
cap.release()
cv2.destroyAllWindows()
print("Collecting Samples Completed!!")

data_path = "C:/Users/Admin/Documents/Keshav/Python Practice/Open CV/Faces/"
only_files = [f for f in listdir(data_path) if isfile(join(data_path,f))]
Traning_data, labels = [], []
for i, files in enumerate(only_files):
    image_path = data_path + only_files[i]
    images = cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)
    Traning_data.append(np.asarray(images,dtype=np.uint8))
    labels.append(i)
labels = np.asarray(labels,dtype=np.int32)
model = cv2.face.LBPHFaceRecognizer_create()
model.train(np.asarray(Traning_data),np.asarray(labels))
print("Model Traning Completed!!")

face_classifier = cv2.CascadeClassifier("C:/Python 3.7/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml")
def face_detector(img,size = 0.5):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray,1.3,5)
    if faces is():
        return img, []
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),2)
        roi = img[y:y+h, x:x+w]
        roi = cv2.resize(roi, (200,200))
    return img, roi
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    image, face = face_detector(frame)
    try:
        face = cv2.cvtColor(face,cv2.COLOR_BGR2GRAY)
        result = model.predict(face)
        if result[1]<500:
            confidense = int(100*(1 - (result[1])/300))
            display_string = str(confidense)+ "% Confidense it is user"
        cv2.putText(image,display_string,(100,200),cv2.FONT_HERSHEY_COMPLEX,1,(250,120,255),2)
        if confidense>75:
            cv2.putText(image, "Unlocked", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255,0),2)
            cv2.imshow("Face Cropper",image)
        else:
            cv2.putText(image, "Locked", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow("Face Cropper", image)
    except:
        cv2.putText(image, "Face not Found", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0, 0), 2)
        cv2.imshow("Face Cropper", image)
        pass
    if cv2.waitKey(1) == 13:
        break
cap.release()
cv2.destroyAllWindows()