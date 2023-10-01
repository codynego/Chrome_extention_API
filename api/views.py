from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Video
from .serializers import VideoSerializer

class VideoCreateAPIView(APIView):
    def get(self, request, *args, **kwargs):
        video_instance = Video.objects.create()  # Create a new Video object
        response_data = {
            'id': video_instance.id,
            'message': 'Video created successfully.'
        }
        return Response(response_data, status=status.HTTP_201_CREATED)




