#!/usr/bin/env python3
"""
Extract sentence 0 ("Well, here's a story for you") from all comma story JSON files.
Outputs audio segments to all_states_test_audio/sentence_0/
"""

import json
import os
import subprocess
from pathlib import Path

def extract_sentence_0_from_comma_story(comma_story_file, output_dir):
    """Extract sentence 0 from a comma story JSON file."""
    
    with open(comma_story_file, 'r') as f:
        data = json.load(f)
    
    # Get the original audio file path
    original_file = data.get('original_file', '')
    if not original_file:
        print(f"No original_file found in {comma_story_file}")
        return False
    
    # Find the audio file
    audio_file = None
    
    # Extract state and filename from original_file path
    # original_file is like: transcriptions/WhisperTranscription/nevada/nevada-1_whisper.json
    path_parts = original_file.split('/')
    if len(path_parts) >= 3:
        state = path_parts[-2]  # nevada
        filename = path_parts[-1].replace('_whisper.json', '.mp3')  # nevada-1.mp3
        audio_path = f"audio/{state}/{filename}"
        
        if os.path.exists(audio_path):
            audio_file = audio_path
        else:
            # Try alternative paths
            possible_paths = [
                original_file.replace('_whisper.json', '.mp3'),
                original_file.replace('_whisper.json', '_whisper.mp3'),
                f"audio/{filename}",
                f"audio/{state}/{filename}"
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    audio_file = path
                    break
    
    if not audio_file:
        print(f"Could not find audio file for {comma_story_file}")
        return False
    
    # Find sentence 0 in the segments
    sentence_0_text = "Well, here's a story for you"
    sentence_0_segment = None
    
    for segment in data.get('segments', []):
        text = segment.get('text', '').strip()
        if sentence_0_text.lower() in text.lower():
            sentence_0_segment = segment
            break
    
    if not sentence_0_segment:
        print(f"Could not find sentence 0 in {comma_story_file}")
        return False
    
    # Extract timing
    start_time = sentence_0_segment.get('start', 0)
    end_time = sentence_0_segment.get('end', start_time + 5)
    
    # Create output filename
    base_name = os.path.basename(comma_story_file).replace('_whisper_comma_story.json', '_whisper.mp3')
    output_file = os.path.join(output_dir, base_name)
    
    # Extract audio segment using ffmpeg
    cmd = [
        'ffmpeg', '-i', audio_file,
        '-ss', str(start_time),
        '-t', str(end_time - start_time),
        '-c', 'copy',
        '-y',  # Overwrite output file
        output_file
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"Extracted: {base_name} ({start_time:.2f}s - {end_time:.2f}s)")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error extracting {base_name}: {e}")
        return False

def main():
    # Set up paths
    comma_story_dir = "/Users/will/Projects/NARegionalAccents/all_states_comma_story"
    output_dir = "/Users/will/Projects/NARegionalAccents/all_states_test_audio/sentence_0"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all comma story JSON files
    comma_story_files = []
    for file in os.listdir(comma_story_dir):
        if file.endswith('_comma_story.json'):
            comma_story_files.append(os.path.join(comma_story_dir, file))
    
    print(f"Found {len(comma_story_files)} comma story files")
    
    # Extract sentence 0 from each
    success_count = 0
    for comma_story_file in comma_story_files:
        if extract_sentence_0_from_comma_story(comma_story_file, output_dir):
            success_count += 1
    
    print(f"\nExtraction complete: {success_count}/{len(comma_story_files)} successful")

if __name__ == "__main__":
    main()
