#!/usr/bin/env python3
"""
Step 3: Split audio into segments based on detected timestamps
Export individual speech segments as WAV files
"""

import os
import sys
import json
import numpy as np
import librosa
import soundfile as sf

def load_audio_and_segments(audio_path, segments_path):
    """Load audio file and segments JSON"""
    print("=" * 60)
    print("STEP 3: SEGMENT AUDIO INTO CLIPS")
    print("=" * 60)
    
    # Check if input files exist
    if not os.path.exists(audio_path):
        print(f"❌ ERROR: Audio file '{audio_path}' not found!")
        print("Please run '1_extract_audio.py' first.")
        sys.exit(1)
        
    if not os.path.exists(segments_path):
        print(f"❌ ERROR: Segments file '{segments_path}' not found!")
        print("Please run '2_detect_speech_timestamps.py' first.")
        sys.exit(1)
    
    print(f"🎵 Input audio: {audio_path}")
    print(f"📄 Input segments: {segments_path}")
    print()
    
    try:
        print("⏳ Loading audio file...")
        audio, sr = librosa.load(audio_path, sr=None, mono=True)
        
        print("⏳ Loading segments file...")
        with open(segments_path, 'r') as f:
            segments = json.load(f)
        
        print(f"✅ Files loaded successfully!")
        print(f"🔊 Audio: {len(audio)/sr:.2f}s, {sr} Hz")
        print(f"📊 Segments: {len(segments)} detected")
        
        return audio, sr, segments
        
    except Exception as e:
        print(f"❌ ERROR loading files: {e}")
        sys.exit(1)

def create_output_directory(output_dir="segments"):
    """Create output directory for segments"""
    print(f"\n⏳ Creating output directory '{output_dir}'...")
    
    try:
        os.makedirs(output_dir, exist_ok=True)
        
        # Check if directory already has files
        existing_files = [f for f in os.listdir(output_dir) if f.endswith('.wav')]
        if existing_files:
            print(f"⚠️  Warning: {len(existing_files)} existing WAV files in '{output_dir}'")
            response = input("❓ Delete existing files? (y/n): ").lower().strip()
            if response == 'y':
                for file in existing_files:
                    os.remove(os.path.join(output_dir, file))
                print("✅ Existing files deleted.")
        
        print(f"✅ Output directory ready: {output_dir}")
        return output_dir
        
    except Exception as e:
        print(f"❌ ERROR creating directory: {e}")
        sys.exit(1)

def export_segments(audio, sample_rate, segments, output_dir="segments"):
    """Export detected speech segments as individual audio files"""
    print(f"\n⏳ Exporting {len(segments)} segments...")
    print("-" * 40)
    
    exported_files = []
    success_count = 0
    
    for i, segment in enumerate(segments, 1):
        try:
            # Calculate sample indices
            start_sample = int(segment["start"] * sample_rate)
            end_sample = int(segment["end"] * sample_rate)
            
            # Ensure we don't exceed audio bounds
            start_sample = max(0, min(start_sample, len(audio)))
            end_sample = max(0, min(end_sample, len(audio)))
            
            # Extract segment
            segment_audio = audio[start_sample:end_sample]
            
            # Generate filename
            filename = f"segment_{i:02d}.wav"
            filepath = os.path.join(output_dir, filename)
            
            # Save segment as WAV file
            sf.write(filepath, segment_audio, sample_rate)
            exported_files.append(filepath)
            success_count += 1
            
            print(f"✅ {filename}: {segment['start']:6.2f}s - {segment['end']:6.2f}s "
                  f"({segment['duration']:5.2f}s)")
            
        except Exception as e:
            print(f"❌ ERROR exporting segment {i}: {e}")
            continue
    
    return exported_files, success_count

def main():
    # Configuration
    AUDIO_FILE = "extracted_audio.wav"
    SEGMENTS_FILE = "speech_segments.json"
    OUTPUT_DIR = "segments"
    
    # Load audio and segments
    audio, sr, segments = load_audio_and_segments(AUDIO_FILE, SEGMENTS_FILE)
    
    # Create output directory
    output_dir = create_output_directory(OUTPUT_DIR)
    
    # Export segments
    exported_files, success_count = export_segments(audio, sr, segments, output_dir)
    
    # Final summary
    print("\n" + "=" * 60)
    print("STEP 3 COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print(f"📁 Output directory: {output_dir}/")
    print(f"✅ Successfully exported: {success_count}/{len(segments)} segments")
    
    if success_count > 0:
        total_duration = sum(segment['duration'] for segment in segments[:success_count])
        print(f"⏱️  Total exported duration: {total_duration:.2f}s")
        print(f"📊 Average segment length: {total_duration/success_count:.2f}s")
        
        print(f"\n📋 Exported files:")
        for i, filepath in enumerate(exported_files[:5], 1):  # Show first 5
            print(f"  {os.path.basename(filepath)}")
        if len(exported_files) > 5:
            print(f"  ... and {len(exported_files) - 5} more")
    
    print(f"\n🎉 ALL STEPS COMPLETED!")
    print("=" * 60)

if __name__ == "__main__":
    main()