import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Video
from .tasks import transcribe_audio
from .your_extract_audio_module import extract_audio_from_video  # Import your extract_audio_from_video function

class VideoConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.video_chunks = []

    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        video_chunk_data = data.get('data')
        is_last_chunk = data.get('is_last_chunk', False)

        # Save the video chunk data to temporary storage
        self.save_video_chunk(video_chunk_data)

        if is_last_chunk:
            # Compile and save the complete video file
            compiled_video_data = self.compile_video_chunks()

            # Specify the path for the extracted audio file
            audio_file_path = "audio/file.wav"  # Adjust the destination path as needed

            # Extract audio from the compiled video
            extracted_audio_path = extract_audio_from_video(compiled_video_data, audio_file_path)

            if extracted_audio_path:
                # Transcribe the extracted audio asynchronously
                transcribe_audio.apply_async(args=[extracted_audio_path, self.scope['user']])

                # Save the compiled video data as a Video instance
                video_instance = Video(video_file=compiled_video_data)
                video_instance.save()

                # Send a response back to the frontend indicating successful processing
                await self.send(text_data=json.dumps({'message': 'Video processed successfully'}))
            else:
                await self.send(text_data=json.dumps({'message': 'Failed to process video'}))
        else:
            # Send a response back to the frontend indicating successful processing of the chunk
            await self.send(text_data=json.dumps({'message': 'Chunk processed successfully'}))

    def save_video_chunk(self, video_chunk_data):
        # Save video chunk data to temporary storage (list in memory)
        self.video_chunks.append(video_chunk_data)

    def compile_video_chunks(self):
        # Concatenate video chunks into a complete video file
        compiled_video_data = b''.join(self.video_chunks)
        # Clear the video chunks list for future use
        self.video_chunks = []
        return compiled_video_data
