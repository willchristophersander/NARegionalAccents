#!/usr/bin/env python3
"""
Fixed Goose Extractor for Regional Accent Analysis
Extracts segments containing 'goose' directly from the correct audio files.
"""

import json
import os
import subprocess
import re
from pathlib import Path
from typing import Dict, List, Optional
import warnings

warnings.filterwarnings('ignore')

class FixedGooseExtractor:
    """Extract goose segments directly from the correct audio files."""
    
    def __init__(self):
        self.target_word = "goose"
        self.padding = 0.2  # Padding around each segment (seconds)
        
    def find_goose_segments_in_json(self, json_file: Path) -> List[Dict]:
        """Find segments containing 'goose' in a JSON file."""
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            goose_segments = []
            
            # Look through segments for the target word
            for segment in data.get('segments', []):
                segment_text = segment.get('text', '').lower()
                
                if self.target_word in segment_text:
                    goose_segments.append({
                        'segment_id': segment.get('id', 0),
                        'start': segment.get('start', 0),
                        'end': segment.get('end', 0),
                        'text': segment.get('text', ''),
                        'confidence': segment.get('avg_logprob', 0)
                    })
            
            return goose_segments
            
        except Exception as e:
            print(f"Error reading JSON file {json_file}: {e}")
            return []
    
    def find_corresponding_audio_file(self, json_file: Path) -> Optional[Path]:
        """Find the corresponding audio file for a JSON file."""
        try:
            # Extract state and filename from JSON filename
            # e.g., nevada-1_whisper_comma_story.json -> nevada/nevada-1.mp3
            json_name = json_file.stem
            if '_whisper_comma_story' in json_name:
                # Remove the suffix to get the base name
                base_name = json_name.replace('_whisper_comma_story', '')
                # Extract state and number (e.g., nevada-1)
                if '-' in base_name:
                    state, number = base_name.split('-', 1)
                    audio_path = f"audio/{state}/{state}-{number}.mp3"
                    if os.path.exists(audio_path):
                        return Path(audio_path)
            
            # Try alternative paths
            possible_paths = [
                f"audio/{json_name.replace('_whisper_comma_story', '')}.mp3",
                f"all_states_test_audio/sentence_0/{json_name.replace('_comma_story', '_whisper')}.mp3",
                f"all_states_test_audio/sentence_0/{json_name.replace('_comma_story', '')}.mp3"
            ]
            
            for audio_path in possible_paths:
                if os.path.exists(audio_path):
                    return Path(audio_path)
            
            return None
            
        except Exception as e:
            print(f"Error finding audio file for {json_file}: {e}")
            return None
    
    def extract_goose_segments(self, json_file: Path, output_dir: Path) -> Dict:
        """Extract goose segments from a JSON file."""
        # Find goose segments in JSON
        goose_segments = self.find_goose_segments_in_json(json_file)
        
        if not goose_segments:
            return {
                'json_file': str(json_file),
                'output_dir': str(output_dir),
                'goose_segments': 0,
                'message': f'No "{self.target_word}" found in JSON transcription'
            }
        
        # Find corresponding audio file
        audio_file = self.find_corresponding_audio_file(json_file)
        if not audio_file:
            return {
                'json_file': str(json_file),
                'output_dir': str(output_dir),
                'goose_segments': len(goose_segments),
                'error': 'Could not find corresponding audio file'
            }
        
        print(f"  Using audio file: {audio_file}")
        
        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Extract each goose segment
        extracted_files = []
        
        for i, segment in enumerate(goose_segments):
            print(f"  Processing segment {i+1}: \"{segment['text'][:50]}...\"")
            
            # Create filename
            context = segment['text'].replace(' ', '_').replace('.', '').replace(',', '')
            context = re.sub(r'[^\w_-]', '', context)[:30]  # Limit length
            
            start_time = max(0, segment['start'] - self.padding)
            end_time = segment['end'] + self.padding
            duration = end_time - start_time
            
            output_file = output_dir / f"{i:02d}_goose_segment_{start_time:.2f}s-{end_time:.2f}s_{context}.wav"
            
            # Extract audio segment
            success = self._extract_audio_segment(audio_file, output_file, start_time, duration)
            
            extracted_files.append({
                'segment_id': i,
                'start': segment['start'],
                'end': segment['end'],
                'duration': duration,
                'confidence': segment['confidence'],
                'text': segment['text'],
                'audio_file': str(output_file) if success else None,
                'extracted': success
            })
            
            if success:
                # Check file size to verify it's not empty
                file_size = output_file.stat().st_size if output_file.exists() else 0
                print(f"    ✅ Extracted: {output_file.name} ({file_size} bytes)")
            else:
                print(f"    ❌ Failed to extract segment")
        
        return {
            'json_file': str(json_file),
            'audio_file': str(audio_file),
            'output_dir': str(output_dir),
            'goose_segments': len(goose_segments),
            'segments': goose_segments,
            'extracted_files': extracted_files
        }
    
    def _extract_audio_segment(self, input_file: Path, output_file: Path, start_time: float, duration: float) -> bool:
        """Extract audio segment using ffmpeg."""
        try:
            cmd = [
                'ffmpeg',
                '-i', str(input_file),
                '-ss', str(start_time),
                '-t', str(duration),
                '-ar', '16000',  # 16kHz
                '-ac', '1',       # Mono
                '-y',             # Overwrite
                str(output_file)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                # Verify the file was created and has content
                if output_file.exists() and output_file.stat().st_size > 1000:  # At least 1KB
                    return True
            else:
                print(f"    FFmpeg error: {result.stderr}")
            return False
            
        except Exception as e:
            print(f"    Exception: {e}")
            return False
    
    def batch_extract_from_json_files(self, json_dir: Path, output_base_dir: Path) -> Dict:
        """Extract goose segments from all JSON files."""
        results = {
            'total_files': 0,
            'successful': 0,
            'errors': 0,
            'total_goose_segments': 0,
            'files': []
        }
        
        # Find all comma story JSON files
        json_files = list(json_dir.glob("*_comma_story.json"))
        results['total_files'] = len(json_files)
        
        print(f"Found {len(json_files)} comma story JSON files")
        print(f"Extracting '{self.target_word}' segments...")
        print()
        
        for i, json_file in enumerate(json_files, 1):
            print(f"Processing {i}/{len(json_files)}: {json_file.name}")
            
            # Create output directory for this file
            file_output_dir = output_base_dir / f"{json_file.stem}_goose_segments"
            
            # Extract goose segments
            result = self.extract_goose_segments(json_file, file_output_dir)
            results['files'].append(result)
            
            if 'error' in result:
                print(f"  ❌ Error: {result['error']}")
                results['errors'] += 1
            else:
                segments = result.get('goose_segments', 0)
                results['total_goose_segments'] += segments
                results['successful'] += 1
                
                if segments > 0:
                    print(f"  ✅ Found {segments} segments containing '{self.target_word}'")
                    # Show text for each segment
                    for j, segment in enumerate(result.get('segments', [])):
                        text = segment.get('text', '')
                        print(f"    {j+1}. \"{text[:60]}{'...' if len(text) > 60 else ''}\"")
                else:
                    print(f"  ⚠️  No '{self.target_word}' found in this file")
        
        return results

def main():
    """Main function."""
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python fixed_goose_extractor.py <json_directory> <output_directory>")
        print()
        print("Examples:")
        print("  python fixed_goose_extractor.py all_states_comma_story/ fixed_goose_segments/")
        sys.exit(1)
    
    json_dir = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])
    
    extractor = FixedGooseExtractor()
    
    # Extract goose segments
    results = extractor.batch_extract_from_json_files(json_dir, output_dir)
    
    print(f"\nGoose Segment Extraction Complete:")
    print(f"Total files: {results['total_files']}")
    print(f"Successful: {results['successful']}")
    print(f"Errors: {results['errors']}")
    print(f"Total '{extractor.target_word}' segments: {results['total_goose_segments']}")

if __name__ == "__main__":
    main()
