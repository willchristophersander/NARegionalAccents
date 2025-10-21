#!/usr/bin/env python3
"""
Isolate Goose Word Extractor
Extracts only the word "goose" from each segment using Whisper word-level timestamps.
"""

import json
import os
import subprocess
import re
from pathlib import Path
from typing import Dict, List, Optional
import warnings

warnings.filterwarnings('ignore')

class IsolateGooseWordExtractor:
    """Extract only the word 'goose' from each segment."""
    
    def __init__(self):
        self.target_word = "goose"
        self.padding = 0.05  # Small padding around the word (seconds)
        
    def isolate_goose_word(self, segment_file: Path, output_file: Path) -> Dict:
        """Extract only the word 'goose' from a segment file."""
        try:
            import whisper
            model = whisper.load_model("base")
            
            # Transcribe with word-level timestamps
            result = model.transcribe(
                str(segment_file),
                word_timestamps=True,
                verbose=False
            )
            
            # Find the word "goose" in the transcription
            goose_word = None
            for segment in result.get('segments', []):
                for word_info in segment.get('words', []):
                    word_text = word_info.get('word', '').strip().lower()
                    clean_word = re.sub(r'[^\w]', '', word_text)
                    
                    if clean_word == self.target_word.lower():
                        goose_word = {
                            'word': word_info.get('word', ''),
                            'start': word_info.get('start', 0),
                            'end': word_info.get('end', 0),
                            'confidence': word_info.get('probability', 0)
                        }
                        break
                if goose_word:
                    break
            
            if not goose_word:
                return {
                    'input_file': str(segment_file),
                    'output_file': str(output_file),
                    'success': False,
                    'message': f'Word "{self.target_word}" not found in segment'
                }
            
            # Extract just the word with small padding
            start_time = max(0, goose_word['start'] - self.padding)
            end_time = goose_word['end'] + self.padding
            duration = end_time - start_time
            
            # Extract the word
            success = self._extract_audio_segment(segment_file, output_file, start_time, duration)
            
            return {
                'input_file': str(segment_file),
                'output_file': str(output_file),
                'success': success,
                'word_info': goose_word,
                'extraction_timing': {
                    'start': start_time,
                    'end': end_time,
                    'duration': duration
                }
            }
            
        except Exception as e:
            return {
                'input_file': str(segment_file),
                'output_file': str(output_file),
                'success': False,
                'error': str(e)
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
            return False
            
        except Exception:
            return False
    
    def batch_isolate_goose_words(self, input_dir: Path, output_dir: Path) -> Dict:
        """Extract just the word 'goose' from all segment files."""
        results = {
            'total_files': 0,
            'successful': 0,
            'errors': 0,
            'files': []
        }
        
        # Find all WAV files in the input directory
        wav_files = list(input_dir.rglob("*.wav"))
        results['total_files'] = len(wav_files)
        
        print(f"Found {len(wav_files)} segment files")
        print(f"Isolating word '{self.target_word}' from each segment...")
        print()
        
        for i, segment_file in enumerate(wav_files, 1):
            print(f"Processing {i}/{len(wav_files)}: {segment_file.name}")
            
            # Create output filename
            relative_path = segment_file.relative_to(input_dir)
            output_file = output_dir / relative_path.with_name(f"goose_{segment_file.name}")
            
            # Create output directory
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Isolate the goose word
            result = self.isolate_goose_word(segment_file, output_file)
            results['files'].append(result)
            
            if result['success']:
                word_info = result.get('word_info', {})
                confidence = word_info.get('confidence', 0)
                duration = result.get('extraction_timing', {}).get('duration', 0)
                file_size = output_file.stat().st_size if output_file.exists() else 0
                print(f"  ✅ Extracted: {output_file.name} ({file_size} bytes, {duration:.2f}s, confidence: {confidence:.2f})")
                results['successful'] += 1
            else:
                error_msg = result.get('error', result.get('message', 'Unknown error'))
                print(f"  ❌ Failed: {error_msg}")
                results['errors'] += 1
        
        return results

def main():
    """Main function."""
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python isolate_goose_word.py <input_directory> <output_directory>")
        print()
        print("Examples:")
        print("  python isolate_goose_word.py fixed_goose_segments/ isolated_goose_words/")
        sys.exit(1)
    
    input_dir = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])
    
    extractor = IsolateGooseWordExtractor()
    
    # Isolate goose words
    results = extractor.batch_isolate_goose_words(input_dir, output_dir)
    
    print(f"\nGoose Word Isolation Complete:")
    print(f"Total files: {results['total_files']}")
    print(f"Successful: {results['successful']}")
    print(f"Errors: {results['errors']}")

if __name__ == "__main__":
    main()
