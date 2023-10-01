from django.db import models

# Create your models here.

class Video(models.Model):
    video_title = models.CharField(max_length= 100)
    video_file = models.FileField(upload_to='videos/')
    created_at = models.DateTimeField(auto_now=True)
    transcript = models.TextField(default='pending')
