#!/usr/bin/env python3
"""
Simple, fast rich transcription - no overcomplications.

This script:
1. Uses tiny model for speed
2. Gets rich data (timestamps, tokens)
3. Simple processing, no timeouts
4. One file at a time
"""

import os
import json
import subprocess
from pathlib import Path
import time

def simple_rich_transcribe(audio_file: str, output_dir: str):
    """Simple rich transcription - fast and effective."""
    print(f"🎵 Processing: {Path(audio_file).name}")
    
    try:
        # Simple, fast command
        cmd = [
            'whisper',
            audio_file,
            '--model', 'tiny',
            '--output_format', 'json',
            '--output_dir', output_dir
        ]
        
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True)
        end_time = time.time()
        
        if result.returncode == 0:
            # Get the generated JSON file
            audio_name = Path(audio_file).stem
            json_file = Path(output_dir) / f"{audio_name}.json"
            
            if json_file.exists():
                with open(json_file, 'r') as f:
                    data = json.load(f)
                
                # Save rich data
                rich_file = Path(output_dir) / f"{audio_name}_rich.json"
                with open(rich_file, 'w') as f:
                    json.dump(data, f, indent=2)
                
                # Save text
                text_file = Path(output_dir) / f"{audio_name}.txt"
                with open(text_file, 'w') as f:
                    f.write(data.get('text', ''))
                
                print(f"   ✅ Done in {end_time - start_time:.1f}s")
                print(f"   📝 Text: {data.get('text', '')[:50]}...")
                print(f"   ⏱️  Duration: {data.get('duration', 0):.1f}s")
                print(f"   📊 Segments: {len(data.get('segments', []))}")
                print(f"   🔤 Tokens: {len(data.get('tokens', []))}")
                
                return True
            else:
                print(f"   ❌ JSON file not found")
                return False
        else:
            print(f"   ❌ Failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    """Simple rich transcription - no complications."""
    print("=== Simple Rich Transcription ===")
    print("Fast, simple, with rich data...")
    
    # Check whisper
    try:
        subprocess.run(['whisper', '--help'], capture_output=True, check=True)
        print("✅ Whisper available")
    except:
        print("❌ Install whisper: pip install openai-whisper")
        return
    
    # Create output
    output_dir = Path("simple_rich_transcriptions")
    output_dir.mkdir(exist_ok=True)
    
    # Find 3 audio files
    audio_files = []
    audio_dir = Path("audio")
    
    if audio_dir.exists():
        for state_dir in audio_dir.iterdir():
            if state_dir.is_dir():
                for audio_file in state_dir.glob("*.mp3"):
                    audio_files.append(audio_file)
                    if len(audio_files) >= 3:
                        break
                if len(audio_files) >= 3:
                    break
    
    if not audio_files:
        print("❌ No audio files found")
        return
    
    print(f"📁 Processing {len(audio_files)} files...")
    
    # Process files
    successful = 0
    for i, audio_file in enumerate(audio_files):
        print(f"\n[{i+1}/{len(audio_files)}] {audio_file.name}")
        if simple_rich_transcribe(str(audio_file), str(output_dir)):
            successful += 1
    
    print(f"\n📊 Done!")
    print(f"   Successful: {successful}/{len(audio_files)}")
    print(f"   Results: {output_dir}/")
    
    print(f"\n💡 Rich data includes:")
    print(f"   - Full text transcription")
    print(f"   - Word timestamps")
    print(f"   - Segment timestamps")
    print(f"   - Token data")
    print(f"   - Language detection")

if __name__ == "__main__":
    main()
