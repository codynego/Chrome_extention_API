from django.urls import path
from . import views

urlpatterns =[
    path('create-recording/', views.VideoCreateAPIView.as_view(), name='upload-video'),
]
