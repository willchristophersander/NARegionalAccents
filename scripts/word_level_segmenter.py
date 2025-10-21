#!/usr/bin/env python3
"""
Word-Level Audio Segmenter using Whisper
Extracts individual words from audio files with precise timestamps.
"""

import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import warnings

warnings.filterwarnings('ignore')

class WordLevelSegmenter:
    """Extract individual words from audio using Whisper."""
    
    def __init__(self):
        self.whisper_available = self._check_whisper()
        self.min_word_duration = 0.1  # Minimum word duration (seconds)
        self.padding = 0.05  # Padding around each word (seconds)
        
    def _check_whisper(self) -> bool:
        """Check if Whisper is available."""
        try:
            import whisper
            return True
        except ImportError:
            print("Whisper not available. Install with: pip install openai-whisper")
            return False
    
    def segment_audio_to_words(self, audio_file: Path, output_dir: Path) -> Dict:
        """Segment audio file into individual words."""
        if not self.whisper_available:
            return {'error': 'Whisper not available'}
        
        try:
            import whisper
            model = whisper.load_model("base")
            
            # Transcribe with word-level timestamps
            result = model.transcribe(
                str(audio_file),
                word_timestamps=True,
                verbose=False
            )
            
            # Extract words with timestamps
            words = self._extract_words_with_timestamps(result)
            
            # Create word audio files
            word_files = self._create_word_audio_files(audio_file, words, output_dir)
            
            return {
                'input_file': str(audio_file),
                'output_dir': str(output_dir),
                'total_words': len(words),
                'words': words,
                'word_files': word_files,
                'transcription': result.get('text', ''),
                'language': result.get('language', 'unknown')
            }
            
        except Exception as e:
            return {'error': f'Word segmentation failed: {e}'}
    
    def _extract_words_with_timestamps(self, whisper_result: Dict) -> List[Dict]:
        """Extract words with timestamps from Whisper result."""
        words = []
        
        for segment in whisper_result.get('segments', []):
            for word_info in segment.get('words', []):
                word = word_info.get('word', '').strip()
                start = word_info.get('start', 0)
                end = word_info.get('end', 0)
                probability = word_info.get('probability', 0)
                
                # Filter out very short words or low confidence
                if (len(word) > 0 and 
                    end - start >= self.min_word_duration and 
                    probability > 0.5):
                    
                    words.append({
                        'word': word,
                        'start': float(start),
                        'end': float(end),
                        'duration': float(end - start),
                        'confidence': float(probability),
                        'segment_id': len(words)  # Word index
                    })
        
        return words
    
    def _create_word_audio_files(self, audio_file: Path, words: List[Dict], output_dir: Path) -> List[Dict]:
        """Create individual audio files for each word."""
        output_dir.mkdir(parents=True, exist_ok=True)
        word_files = []
        
        for i, word_data in enumerate(words):
            # Create filename (sanitize word for filesystem)
            word_text = word_data['word'].replace(' ', '_').replace('.', '').replace(',', '').replace('?', '').replace('!', '')
            word_text = ''.join(c for c in word_text if c.isalnum() or c in '_-')
            
            if not word_text:
                word_text = f"word_{i:03d}"
            
            # Add padding to timestamps
            start_time = max(0, word_data['start'] - self.padding)
            end_time = word_data['end'] + self.padding
            duration = end_time - start_time
            
            # Create output filename
            output_file = output_dir / f"{i:03d}_{word_text}_{start_time:.2f}s-{end_time:.2f}s.wav"
            
            # Extract word using ffmpeg
            success = self._extract_audio_segment(
                audio_file, 
                output_file, 
                start_time, 
                duration
            )
            
            if success:
                word_files.append({
                    'word': word_data['word'],
                    'start': word_data['start'],
                    'end': word_data['end'],
                    'duration': word_data['duration'],
                    'confidence': word_data['confidence'],
                    'segment_id': word_data['segment_id'],
                    'audio_file': str(output_file),
                    'extracted': True
                })
            else:
                word_files.append({
                    'word': word_data['word'],
                    'start': word_data['start'],
                    'end': word_data['end'],
                    'duration': word_data['duration'],
                    'confidence': word_data['confidence'],
                    'segment_id': word_data['segment_id'],
                    'audio_file': None,
                    'extracted': False
                })
        
        return word_files
    
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
            return result.returncode == 0
            
        except Exception:
            return False
    
    def batch_segment_audio_files(self, input_dir: Path, output_base_dir: Path) -> Dict:
        """Segment multiple audio files into words."""
        if not self.whisper_available:
            return {'error': 'Whisper not available'}
        
        results = {
            'total_files': 0,
            'successful': 0,
            'errors': 0,
            'files': []
        }
        
        # Find audio files
        audio_extensions = ['.mp3', '.wav', '.m4a', '.flac', '.aac']
        audio_files = []
        for ext in audio_extensions:
            audio_files.extend(input_dir.glob(f'*{ext}'))
        
        results['total_files'] = len(audio_files)
        
        print(f"Segmenting {len(audio_files)} audio files into words...")
        
        for i, audio_file in enumerate(audio_files, 1):
            print(f"Processing {i}/{len(audio_files)}: {audio_file.name}")
            
            # Create output directory for this file
            output_dir = output_base_dir / f"{audio_file.stem}_words"
            
            # Segment into words
            result = self.segment_audio_to_words(audio_file, output_dir)
            results['files'].append(result)
            
            if 'error' in result:
                print(f"  ❌ Error: {result['error']}")
                results['errors'] += 1
            else:
                total_words = result.get('total_words', 0)
                word_files = result.get('word_files', [])
                extracted_count = sum(1 for wf in word_files if wf.get('extracted', False))
                print(f"  ✅ {total_words} words found, {extracted_count} audio files created")
                results['successful'] += 1
        
        return results
    
    def create_word_alignment_summary(self, results: Dict, output_file: Path) -> None:
        """Create a summary of word alignments across all files."""
        summary = {
            'total_files': results['total_files'],
            'successful_files': results['successful'],
            'error_files': results['errors'],
            'word_statistics': {},
            'files': []
        }
        
        total_words = 0
        word_lengths = []
        
        for file_result in results['files']:
            if 'error' not in file_result:
                words = file_result.get('words', [])
                total_words += len(words)
                
                # Collect word statistics
                for word_data in words:
                    word_lengths.append(len(word_data['word']))
                
                # File summary
                file_summary = {
                    'file': file_result['input_file'],
                    'total_words': len(words),
                    'transcription': file_result.get('transcription', ''),
                    'language': file_result.get('language', 'unknown'),
                    'words': words
                }
                summary['files'].append(file_summary)
        
        # Calculate statistics
        if word_lengths:
            summary['word_statistics'] = {
                'total_words': total_words,
                'average_word_length': sum(word_lengths) / len(word_lengths),
                'shortest_word': min(word_lengths),
                'longest_word': max(word_lengths)
            }
        
        # Save summary
        with open(output_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"Word alignment summary saved to: {output_file}")

def main():
    """Main function."""
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python word_level_segmenter.py <input_file_or_dir> <output_dir>")
        print()
        print("Examples:")
        print("  python word_level_segmenter.py audio.mp3 words_output/")
        print("  python word_level_segmenter.py sentence_0/ word_segments/")
        sys.exit(1)
    
    input_path = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])
    
    segmenter = WordLevelSegmenter()
    
    if input_path.is_file():
        # Single file
        result = segmenter.segment_audio_to_words(input_path, output_dir)
        print(json.dumps(result, indent=2))
    elif input_path.is_dir():
        # Directory
        results = segmenter.batch_segment_audio_files(input_path, output_dir)
        
        # Create summary
        summary_file = output_dir / "word_alignment_summary.json"
        segmenter.create_word_alignment_summary(results, summary_file)
        
        print(f"\nWord Segmentation Complete:")
        print(f"Total files: {results['total_files']}")
        print(f"Successful: {results['successful']}")
        print(f"Errors: {results['errors']}")
        print(f"Summary saved to: {summary_file}")
    else:
        print(f"Path not found: {input_path}")
        sys.exit(1)

if __name__ == "__main__":
    main()
