#!/usr/bin/env python3
"""
Step 1: Extract audio from video file using pydub
"""

import os
import sys
from pydub import AudioSegment

def extract_audio_from_video(video_path, audio_output_path, sample_rate=16000):
    """Extract audio from video file and convert to standard format"""
    print("=" * 60)
    print("STEP 1: EXTRACT AUDIO FROM VIDEO")
    print("=" * 60)
    
    # Check if input file exists
    if not os.path.exists(video_path):
        print(f"❌ ERROR: Video file '{video_path}' not found!")
        print("Please make sure the video file is in the current directory.")
        sys.exit(1)
    
    print(f"📹 Input video: {video_path}")
    print(f"🎵 Output audio: {audio_output_path}")
    print(f"📊 Sample rate: {sample_rate} Hz (mono)")
    print()
    
    try:
        print("⏳ Loading video and extracting audio...")
        # Load video file
        video = AudioSegment.from_file(video_path)
        
        print(f"📊 Original audio: {video.channels} channels, {video.frame_rate} Hz")
        print(f"⏱️ Original duration: {len(video)/1000:.2f} seconds")
        
        # Convert to mono and set sample rate
        print("⏳ Converting to mono and resampling...")
        audio = video.set_channels(1).set_frame_rate(sample_rate)
        
        # Export as WAV
        print("⏳ Saving audio file...")
        audio.export(audio_output_path, format="wav")
        
        # Verify the output file
        if os.path.exists(audio_output_path):
            file_size = os.path.getsize(audio_output_path) / (1024 * 1024)  # MB
            print(f"✅ Audio extracted successfully!")
            print(f"📁 File size: {file_size:.2f} MB")
            print(f"⏱️ Duration: {len(audio)/1000:.2f} seconds")
            print(f"🔊 Channels: {audio.channels}")
            print(f"📊 Sample rate: {audio.frame_rate} Hz")
        else:
            print("❌ ERROR: Output audio file was not created!")
            sys.exit(1)
            
        return audio_output_path
            
    except Exception as e:
        print(f"❌ ERROR during audio extraction: {e}")
        print("\n💡 TROUBLESHOOTING TIPS:")
        print("1. Make sure ffmpeg is installed on your system")
        print("2. Download ffmpeg from: https://ffmpeg.org/download.html")
        print("3. Or install via chocolatey: 'choco install ffmpeg'")
        print("4. Or add ffmpeg to your PATH environment variable")
        sys.exit(1)

def main():
    # Configuration
    VIDEO_FILE = "gachikuta.mp4"
    AUDIO_OUTPUT = "extracted_audio.wav"
    SAMPLE_RATE = 16000
    
    # Extract audio
    audio_path = extract_audio_from_video(VIDEO_FILE, AUDIO_OUTPUT, SAMPLE_RATE)
    
    print("\n" + "=" * 60)
    print("STEP 1 COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print(f"🎵 Audio ready for next step: {audio_path}")
    print("\n➡️  Next: Run '2_detect_speech_timestamps.py'")

if __name__ == "__main__":
    main()