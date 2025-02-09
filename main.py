import cv2
import numpy as np
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from transformers import pipeline
from scenedetect import detect, ContentDetector
from pydub import AudioSegment
from pydub.silence import split_on_silence
import pafy  # For YouTube streaming
import os

# Initialize sentiment analysis pipeline
sentiment_analyzer = pipeline("sentiment-analysis")
# Initialize scene detector
scene_detector = ContentDetector()

# Function to analyze video and extract engaging moments
def auto_highlights(video_path, output_path, max_duration=60):
    # Load video
    video = VideoFileClip(video_path)
    duration = video.duration
    # Analyze scenes
    scene_list = detect(video_path, scene_detector)
    engaging_scenes = []
    # Analyze sentiment and motion in each scene
    for i, (start_time, end_time) in enumerate(scene_list):
        scene = video.subclip(start_time, end_time)
        audio = scene.audio.to_soundarray()
        motion_score = calculate_motion_score(scene)
        sentiment_score = analyze_sentiment(scene)
        # Prioritize scenes with high motion and positive sentiment
        engaging_scenes.append({
            "start": start_time,
            "end": end_time,
            "motion_score": motion_score,
            "sentiment_score": sentiment_score
        })
    # Sort scenes by engagement score
    engaging_scenes.sort(key=lambda x: x["motion_score"] + x["sentiment_score"], reverse=True)
    # Compile the final highlight reel
    final_clip = []
    total_duration = 0
    for scene in engaging_scenes:
        if total_duration + (scene["end"] - scene["start"]) <= max_duration:
            final_clip.append(video.subclip(scene["start"], scene["end"]))
            total_duration += scene["end"] - scene["start"]
        else:
            break
    # Concatenate clips
    highlight_reel = CompositeVideoClip(final_clip)
    highlight_reel.write_videofile(output_path, codec="libx264")

# Function to calculate motion score
def calculate_motion_score(clip):
    frames = [frame for frame in clip.iter_frames()]
    motion_score = 0
    for i in range(1, len(frames)):
        diff = cv2.absdiff(frames[i - 1], frames[i])
        motion_score += np.mean(diff)
    return motion_score / len(frames)

# Function to analyze sentiment
def analyze_sentiment(clip):
    audio = clip.audio.to_soundarray()
    sentiment = sentiment_analyzer(audio.tolist())
    return 1 if sentiment[0]["label"] == "POSITIVE" else 0

# Function to generate auto captions
def generate_captions(video_path, output_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile("temp_audio.wav")
    # Split audio into chunks
    sound = AudioSegment.from_wav("temp_audio.wav")
    chunks = split_on_silence(sound, min_silence_len=500, silence_thresh=-40)
    # Generate captions for each chunk
    captions = []
    for i, chunk in enumerate(chunks):
        chunk.export(f"chunk{i}.wav", format="wav")
        # Use a speech-to-text API (e.g., Google Speech-to-Text) to generate captions
        # captions.append(transcribe_audio(f"chunk{i}.wav"))
    # Add captions to video
    caption_clips = [TextClip(text, fontsize=24, color="white").set_position("bottom").set_duration(len(chunk) / 1000) for chunk, text in zip(chunks, captions)]
    final_clip = CompositeVideoClip([video] + caption_clips)
    final_clip.write_videofile(output_path, codec="libx264")

# Function to adapt aspect ratio
def adapt_aspect_ratio(video_path, output_path, aspect_ratio="16:9"):
    video = VideoFileClip(video_path)
    if aspect_ratio == "9:16":
        video = video.resize(height=1080)
        video = video.crop(x1=video.w / 2 - 540, width=1080, height=1920)
    elif aspect_ratio == "1:1":
        video = video.resize(height=1080)
        video = video.crop(x1=video.w / 2 - 540, width=1080, height=1080)
    video.write_videofile(output_path, codec="libx264")

# Function to add text and logo overlay
def add_overlay(video_path, output_path, text="", logo_path=None):
    video = VideoFileClip(video_path)
    if logo_path:
        logo = VideoFileClip(logo_path).set_position(("right", "top")).set_duration(video.duration)
    if text:
        text_clip = TextClip(text, fontsize=24, color="white").set_position("bottom").set_duration(video.duration)
    final_clip = CompositeVideoClip([video, logo, text_clip])
    final_clip.write_videofile(output_path, codec="libx264")

# Function to stream YouTube video
def stream_youtube_video(url, output_path="input_video.mp4"):
    try:
        video = pafy.new(url)
        print(f"Streaming video: {video.title}")
        best_stream = video.getbest(preftype="mp4")  # Get the best quality MP4 stream
        print(f"Stream URL: {best_stream.url}")
        # Download only the first 5 minutes of the video
        os.system(f"ffmpeg -i {best_stream.url} -t 300 -c copy {output_path}")
        print(f"Video saved successfully: {output_path}")
        return output_path
    except Exception as e:
        print(f"Error streaming video: {e}")
        return None

# Example usage
if __name__ == "__main__":
    # Input: YouTube video URL
    youtube_url = input("Enter the YouTube video URL: ")
    
    # Step 1: Stream the YouTube video
    video_path = stream_youtube_video(youtube_url)
    if not video_path:
        print("Failed to stream the video. Exiting...")
        exit()

    # Step 2: Generate highlights
    auto_highlights(video_path, "highlights.mp4")

    # Step 3: Generate captions
    generate_captions(video_path, "captions.mp4")

    # Step 4: Adapt aspect ratio for social media
    adapt_aspect_ratio(video_path, "vertical_video.mp4", aspect_ratio="9:16")

    # Step 5: Add overlay (text and logo)
    add_overlay(video_path, "branded_video.mp4", text="Subscribe!", logo_path="logo.png")

    print("Processing complete! Check the output files.")
