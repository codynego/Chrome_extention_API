from .models import Video
from rest_framework import serializers

def validate_unique_video_title(value):
    query_set = Video.objects.filter(video_title__iexact=value)
    if query_set.exists():
        raise serializers.ValidationError(f"A video with the title ({value}) already exists")
