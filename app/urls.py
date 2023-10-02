from django.urls import path
from . import views

urlpatterns =[
    path('create-recording/', views.VideoCreateAPIView.as_view(), name='upload-video'),
    path('get-recording/<int:video_id>/', views.VideoGetAPIView.as_view(), name='get-video'),
    path('update-recording/<int:video_id>/', views.VideoUpdateAPIView.as_view(), name='update-video'),
]
