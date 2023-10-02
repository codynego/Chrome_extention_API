from celery import Celery
from django.conf import settings
from .models import Video
import requests

app = Celery('tasks', broker=settings.CELERY_BROKER_URL)

base_url = "https://api.assemblyai.com/v2"
headers = {
    "authorization": "0fdf9a400a984bc29b5e63d1cb2e72b1"
}

@app.task
def transcribe_audio(video_id, audio_file_data):
    response = requests.post(base_url + "/upload", headers=headers, data=audio_file_data)
    upload_url = response.json()["upload_url"]

    data = {
        "upload_url": upload_url
    }

    response = requests.post(base_url + "/transcript", json=data, headers=headers)
    transcription_result = response.json()

    if transcription_result['status'] == 'completed':
        transcription_text = transcription_result['text']
        # Save transcription to the specific Video instance
        video_instance = Video.objects.get(pk=video_id)
        video_instance.transcription = transcription_text
        video_instance.save()
    elif transcription_result['status'] == 'error':
        raise RuntimeError(f"Transcription failed: {transcription_result['error']}")
    else:
        raise RuntimeError("Transcription status unknown or still in progress.")
