from moviepy.editor import VideoFileClip

def extract_audio(video_file_path, output_audio_path):
    try:
        # Load the video file
        video_clip = VideoFileClip(video_file_path)

        # Extract audio from the video
        audio_clip = video_clip.audio

        # Write the audio to the output file
        audio_clip.write_audiofile(output_audio_path)

        # Close the video and audio clips
        video_clip.close()
        audio_clip.close()

        return output_audio_path

    except Exception as e:
        print(f"Error: {str(e)}")
        return None
