from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Video
from .serializers import VideoSerializer

class VideoCreateAPIView(APIView):
    def get(self, request, *args, **kwargs):
        video_instance = Video
        response_data = {
            'id': video_instance.id,
            'message': 'Video created successfully.'
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


class VideoGetAPIView(APIView):
    def get(self, request, *args, **kwargs):
        video_id = kwargs.get('video_id')
        video_instance = Video.objects.get(id=video_id)
        serializer = VideoSerializer(video_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)




