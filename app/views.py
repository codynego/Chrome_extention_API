from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Video
from .serializers import VideoSerializer
from .models import Video
from .tasks import transcribe_audio
from .extract_audio import extract_audio

class VideoCreateAPIView(APIView):
    def get(self, request, *args, **kwargs):
        video_instance = Video.objects.create()
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



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Video, VideoChunk
from .tasks import transcribe_audio
from .extract_audio import extract_audio
import io
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.base import ContentFile


import tempfile
import io
import os
import ffmpeg
from django.http import JsonResponse
from django.core.files.base import ContentFile
from .models import Video


class VideoUploadAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Get the binary video data from the request body
        video_binary_data = request.body

        # Get the file extension (assuming it's mp4, you can modify this logic if different formats are expected)
        file_extension = '.mp4'

        # Convert binary data to a video file
        video_path = self.save_video_to_disk(video_binary_data, file_extension)

        if video_path:
            # Save the video path to the database (assuming you have a Video model with a field 'video_file')
            video_instance = Video(video_file=video_path)
            video_instance.save()

            # Respond with success message and video path
            return JsonResponse({'message': 'Video uploaded and saved successfully', 'video_path': video_path}, status=200)
        else:
            # Respond with an error if video conversion fails
            return JsonResponse({'error': 'Failed to process video'}, status=500)

    def save_video_to_disk(self, video_binary_data, file_extension):
        try:
            # Create a temporary file to save the video data
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=file_extension)
            temp_file.write(video_binary_data)
            temp_file.close()

            # Specify output file path for the converted video
            output_file_path = f"media/videos/{temp_file.name.split('/')[-1].split('.')[0]}_converted{file_extension}"

            # Use ffmpeg to convert the video to the desired format
            ffmpeg.input(temp_file.name).output(output_file_path).run()

            # Delete the temporary file
            os.remove(temp_file.name)

            # Return the path where the converted video is saved
            return output_file_path
        except Exception as e:
            # Handle any exceptions that might occur during video processing
            print(f"Error: {e}")
            return None
