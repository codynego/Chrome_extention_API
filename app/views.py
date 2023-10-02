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
import os
from django.core.files.base import ContentFile
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Video, VideoChunk
from moviepy.editor import VideoFileClip, concatenate_videoclips

class VideoUpdateAPIView(APIView):
    def post(self, request, video_id, format=None):
        try:
            video_instance = Video.objects.get(id=video_id)
        except Video.DoesNotExist:
            return Response({'error': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)

        video_chunk_data = request.body
        is_last = request.query_params.get('is_last', False)

        # Save the video chunk data to the database
        VideoChunk.objects.create(video=video_instance, chunk_data=video_chunk_data)

        if is_last:
            # Retrieve all chunks associated with this video
            video_chunks = VideoChunk.objects.filter(video=video_instance)

            # Concatenate video chunks into a complete video file
            final_clip = self.compile_video_chunks(video_chunks)

            # Save the concatenated video data to the video model
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as final_tempfile:
                final_clip.write_videofile(final_tempfile.name, codec='libx264')
                final_tempfile_path = final_tempfile.name

            video_instance.video_file.save('compiled_video.mp4', ContentFile(open(final_tempfile_path, 'rb').read()))

            # Clean up temporary files
            os.remove(final_tempfile_path)

            return Response({'message': 'Video processed successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Chunk processed successfully'}, status=status.HTTP_200_OK)

    def compile_video_chunks(self, video_chunks):
        temp_files = []

        # Create VideoFileClip objects for each chunk and save them as temporary files
        clips = []
        for chunk in video_chunks:
            chunk_data = chunk.chunk_data
            video_file = io.BytesIO(chunk_data)

            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
            temp_file.write(video_file.read())
            temp_file.close()

            # Append temporary file to the list for cleanup later
            temp_files.append(temp_file.name)

            # Create VideoFileClip object from the temporary file
            clip = VideoFileClip(temp_file.name)
            clips.append(clip)

        # Concatenate video clips
        final_clip = concatenate_videoclips(clips)

        # Save the concatenated video data to BytesIO
        compiled_video_data = io.BytesIO()
        final_clip.write_videofile(compiled_video_data, codec='libx264')

        # Clean up temporary files
        for temp_file in temp_files:
            os.remove(temp_file)

        # Get the compiled video binary data
        compiled_video_data.seek(0)
        compiled_video_binary = compiled_video_data.read()

        # Close the BytesIO object to free up resources
        compiled_video_data.close()

        return compiled_video_binary

    