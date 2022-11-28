import base64
from random import randint

import cv2
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + r'haarcascade_frontalface_default.xml')
pro_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + r'haarcascade_profileface.xml')


def home(request):
    context = {"title": "Home"}
    return render(request, 'home.html', context)


@api_view(['POST'])
def detect_face_user_move(request):
    if request.method == 'POST':
        try:
            frame_ = request.POST.get('image')
            frame_ = str(frame_)
            data = frame_.replace('data:image/jpeg;base64,', '')
            data = data.replace(' ', '+')
            imgdata = base64.b64decode(data)
            filename = r'media/' + F'image_{randint(1, 1000000000000)}.jpg'
            with open(filename, 'wb') as f:
                f.write(imgdata)
            img = cv2.imread(filename)
            faces = face_cascade.detectMultiScale(img, 1.3, 5)
            pros = pro_cascade.detectMultiScale(img, 1.3, 5)
            if len(pros) == 0:
                pros = pro_cascade.detectMultiScale(cv2.flip(img, 1, 1), 1.3, 5)
                for n in pros:
                    n[0] = 640 - n[0] - n[3]
            if (len(faces) == 0) & (len(pros) > 0):
                for (x, y, w, h) in pros:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    response = "Red"
                    cv2.waitKey(100)
            elif len(faces) > 0:
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    response = "Blue"
                    cv2.waitKey(100)
            else:
                response = "No Face"
        except Exception as e:
            print('Error', e)
    try:
        r = response
    except NameError:
        response = "ERROR"
    return Response({'Json': response}, status=200)
