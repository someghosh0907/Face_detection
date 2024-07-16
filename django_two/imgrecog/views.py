from django.shortcuts import render
from django.http import JsonResponse,HttpResponse,response
from .models import Image
import cv2
from .forms import ImageForm
import numpy as np
import face_recognition
import time
import sys

#os.environ.pop("QT_QPA_PLATFORM_PLUGIN_PATH")

# Create your views here.    
def post_img(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return HttpResponse('successfully uploaded',form)
    else:
        form = ImageForm()
    return HttpResponse(request, {"form": form})  

def img_detection(request,pk):
#Implementation using OpenCV
    #Getting img from DB
    db_img=Image.objects.get(pk=pk) 
    input_img=db_img.image 
    #serializer = ImageSerializer(input_img, many=True)
    img_path=str(input_img)
    #load the cascade classifier for face detection   
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    #load the image 
    img = cv2.imread('./media/'+img_path)  
    #img = cv2.imread(input_img)
    #convert the image to grayscale  
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #detect faces in the image  
    faces = face_cascade.detectMultiScale( gray,scaleFactor=1.09, minNeighbors=6 ,minSize=(27,27))  
    #list of rectangles
    rect_list = []  
    #draw a rectangle around the detected faces  
    for (x, y, w, h) in faces:
        rect=cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 3)
        rect_list.append(rect)
    #display the image 
    #cv2.imshow('img01', img)  
    #cv2.waitKey()  
    #cv2.destroyAllWindows() 
    #Getting the Response 
    people=len(rect_list)
    print(people)
    if(people==0):
        msg='No Face Found'
        return JsonResponse(data={"people":msg})
    # datas={"No. of people:" : people}
    return JsonResponse(data={"people":people})

def video_detection(request):
    cap = cv2.VideoCapture('/home/vyrazu-70/Desktop/django_video.mp4')
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap.set(3,640) # set Width
    cap.set(4,480) # set Height
    delay = 1
    window_name = 'frame'
    #if not cap.isOpened():
    #    sys.exit()
    while True:
        ret, frame = cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray,scaleFactor=1.09,minNeighbors=7,minSize=(100, 100))
            for (x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2) 
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]
                #if(rect==0):
                #    print('No Face Is Visible')
            cv2.imshow(window_name, frame)
            if cv2.waitKey(delay) & 0xFF == ord('q'):
                break
        else:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    cv2.destroyWindow(window_name)
    return JsonResponse({"res":"working"})

def hello(request):
    is_auth="no"
    if(request.user.is_authenticated):
        is_auth="yes"
    return JsonResponse({"message":is_auth})
