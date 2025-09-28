#!/usr/bin/env python3
"""
Step 2: Detect speech segments and generate timestamps
Uses energy-based voice activity detection
"""

import os
import sys
import json
import numpy as np
import librosa

def load_audio(audio_path, sample_rate=16000):
    """Load audio file and convert to mono"""
    print("=" * 60)
    print("STEP 2: DETECT SPEECH TIMESTAMPS")
    print("=" * 60)
    
    # Check if input file exists
    if not os.path.exists(audio_path):
        print(f"❌ ERROR: Audio file '{audio_path}' not found!")
        print("Please run '1_extract_audio.py' first.")
        sys.exit(1)
    
    print(f"🎵 Input audio: {audio_path}")
    print(f"📊 Sample rate: {sample_rate} Hz")
    print()
    
    try:
        print("⏳ Loading audio file...")
        # Load audio with librosa (automatically converts to mono)
        audio, sr = librosa.load(audio_path, sr=sample_rate, mono=True)
        
        duration = len(audio) / sr
        print(f"✅ Audio loaded successfully!")
        print(f"⏱️  Duration: {duration:.2f} seconds")
        print(f"🔢 Samples: {len(audio):,}")
        
        return audio, sr
        
    except Exception as e:
        print(f"❌ ERROR loading audio: {e}")
        sys.exit(1)

def detect_speech_segments(audio, sample_rate=16000, 
                          frame_length=512, hop_length=256,
                          threshold=0.025, 
                          min_silence_duration=0.5, 
                          min_speech_duration=0.3):
    """Detect speech segments based on energy threshold"""
    print("\n⏳ Analyzing audio for speech segments...")
    print(f"⚙️  Parameters: threshold={threshold}, min_speech={min_speech_duration}s")
    
    # Calculate short-time energy
    frames = librosa.util.frame(audio, frame_length=frame_length, hop_length=hop_length)
    energy = np.sum(frames ** 2, axis=0) / frame_length
    
    # Normalize energy to 0-1 range
    energy = energy / np.max(energy)
    
    # Apply threshold to detect speech regions
    speech_mask = energy > threshold
    
    # Convert frame indices to time
    times = librosa.frames_to_time(np.arange(len(speech_mask)), 
                                 sr=sample_rate, 
                                 hop_length=hop_length)
    
    # Find speech segments
    segments = []
    in_speech = False
    speech_start = 0
    
    for i, is_speech in enumerate(speech_mask):
        if is_speech and not in_speech:
            # Speech starts
            speech_start = times[i]
            in_speech = True
        elif not is_speech and in_speech:
            # Speech ends
            speech_end = times[i]
            segment_duration = speech_end - speech_start
            
            # Only include segments longer than minimum duration
            if segment_duration >= min_speech_duration:
                segments.append({
                    "start": round(speech_start, 2),
                    "end": round(speech_end, 2),
                    "duration": round(segment_duration, 2)
                })
            in_speech = False
    
    # Handle case where speech continues until end of audio
    if in_speech:
        speech_end = times[-1]
        segment_duration = speech_end - speech_start
        if segment_duration >= min_speech_duration:
            segments.append({
                "start": round(speech_start, 2),
                "end": round(speech_end, 2),
                "duration": round(segment_duration, 2)
            })
    
    print(f"✅ Speech detection completed!")
    print(f"🔊 Detected {len(segments)} speech segments")
    
    return segments

def save_segments_json(segments, output_path="speech_segments.json"):
    """Save segments information to JSON file"""
    print(f"\n⏳ Saving segments to {output_path}...")
    
    try:
        with open(output_path, 'w') as f:
            json.dump(segments, f, indent=2)
        
        print(f"✅ Segments saved successfully!")
        
        # Print summary
        total_duration = sum(segment['duration'] for segment in segments)
        print(f"📊 Total speech duration: {total_duration:.2f}s")
        
        return output_path
        
    except Exception as e:
        print(f"❌ ERROR saving segments: {e}")
        sys.exit(1)

def print_segments_summary(segments):
    """Print a nice summary of detected segments"""
    print("\n" + "=" * 50)
    print("DETECTED SPEECH SEGMENTS SUMMARY")
    print("=" * 50)
    
    for i, segment in enumerate(segments, 1):
        print(f"Segment {i:02d}: {segment['start']:6.2f}s - {segment['end']:6.2f}s "
              f"({segment['duration']:5.2f}s)")
    
    total_duration = sum(segment['duration'] for segment in segments)
    avg_duration = total_duration / len(segments) if segments else 0
    
    print("-" * 50)
    print(f"Total segments: {len(segments)}")
    print(f"Total speech: {total_duration:.2f}s")
    print(f"Average segment: {avg_duration:.2f}s")

def main():
    # Configuration
    AUDIO_FILE = "extracted_audio.wav"
    SEGMENTS_FILE = "speech_segments.json"
    SAMPLE_RATE = 16000
    
    # Detection parameters (adjust these if needed)
    ENERGY_THRESHOLD = 0.025
    MIN_SPEECH_DURATION = 0.3
    MIN_SILENCE_DURATION = 0.5
    
    # Load audio
    audio, sr = load_audio(AUDIO_FILE, SAMPLE_RATE)
    
    # Detect speech segments
    segments = detect_speech_segments(
        audio, 
        sample_rate=sr,
        threshold=ENERGY_THRESHOLD,
        min_speech_duration=MIN_SPEECH_DURATION,
        min_silence_duration=MIN_SILENCE_DURATION
    )
    
    # Save segments to JSON
    segments_file = save_segments_json(segments, SEGMENTS_FILE)
    
    # Print summary
    print_segments_summary(segments)
    
    print("\n" + "=" * 60)
    print("STEP 2 COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print(f"📄 Timestamps saved: {segments_file}")
    print("\n➡️  Next: Run '3_segment_audio.py'")

if __name__ == "__main__":
    main()