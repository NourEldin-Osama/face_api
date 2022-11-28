from django.urls import path

from apps.face_api_app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('detect_face_user_move', views.detect_face_user_move, name='detect_face_user_move'),
]
