from django.db import models

# Create your models here.
from django.db import models

# Create your models here.

class Video(models.Model):
    video_title = models.CharField(max_length= 100)
    video_file = models.FileField(upload_to='videos/')
    created_at = models.DateTimeField(auto_now=True)
    transcript = models.TextField(default='pendings')



class VideoChunk(models.Model):
    video = models.ForeignKey('Video', on_delete=models.CASCADE)
    chunk_data = models.BinaryField()

    def __str__(self):
        return f'Chunk for Video ID {self.video.id}'

