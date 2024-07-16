from django.urls import path
from .views import hello,post_img,img_detection,video_detection

urlpatterns = [
    path('',hello),
    path('post-img/',post_img,name='post-img'),
    path('img-res/<int:pk>/',img_detection,name='img-detection'),
    path('video/',video_detection,name='video_detect')
]

