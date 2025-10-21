#!/usr/bin/env python3
"""
Word Extraction Analyzer for Regional Accent Analysis
Extracts specific words (like "goose") from multiple contexts and speakers.
"""

import json
import os
import subprocess
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import warnings

warnings.filterwarnings('ignore')

class WordExtractionAnalyzer:
    """Extract specific words from multiple speakers and contexts."""
    
    def __init__(self):
        self.whisper_available = self._check_whisper()
        self.target_word = "goose"  # Word to extract
        self.context_words = ["goose", "geese", "gander"]  # Related words to look for
        self.min_word_duration = 0.1
        self.padding = 0.05
        
    def _check_whisper(self) -> bool:
        """Check if Whisper is available."""
        try:
            import whisper
            return True
        except ImportError:
            print("Whisper not available. Install with: pip install openai-whisper")
            return False
    
    def find_goose_story_files(self, base_dir: Path) -> List[Path]:
        """Find all audio files that contain the goose story."""
        goose_files = []
        
        # Look for comma story files (which contain the goose story)
        comma_story_dir = base_dir / "all_states_comma_story"
        if comma_story_dir.exists():
            for json_file in comma_story_dir.glob("*_comma_story.json"):
                if self._contains_goose_story(json_file):
                    # Find corresponding audio file
                    audio_file = self._find_audio_file(json_file)
                    if audio_file and audio_file.exists():
                        goose_files.append(audio_file)
        
        return goose_files
    
    def _contains_goose_story(self, json_file: Path) -> bool:
        """Check if a comma story file contains the goose story."""
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            # Check if the story text contains goose-related words
            story_text = data.get('story_text', '').lower()
            return any(word in story_text for word in self.context_words)
        except Exception:
            return False
    
    def _find_audio_file(self, json_file: Path) -> Optional[Path]:
        """Find the corresponding audio file for a JSON file."""
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            original_file = data.get('original_file', '')
            if not original_file:
                return None
            
            # Try different possible audio file paths
            possible_paths = [
                original_file,
                original_file.replace('_whisper.json', '.mp3'),
                original_file.replace('_whisper.json', '_whisper.mp3'),
                f"audio/{original_file.split('/')[-1].replace('_whisper.json', '.mp3')}"
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    return Path(path)
            
            return None
        except Exception:
            return None
    
    def extract_goose_pronunciations(self, audio_file: Path, output_dir: Path) -> Dict:
        """Extract all pronunciations of 'goose' from an audio file."""
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
            
            # Find all instances of the target word
            goose_instances = self._find_word_instances(result, self.target_word)
            
            if not goose_instances:
                return {
                    'input_file': str(audio_file),
                    'output_dir': str(output_dir),
                    'goose_instances': 0,
                    'instances': [],
                    'transcription': result.get('text', ''),
                    'message': f'No instances of "{self.target_word}" found'
                }
            
            # Extract audio for each instance
            extracted_files = self._extract_word_instances(audio_file, goose_instances, output_dir)
            
            return {
                'input_file': str(audio_file),
                'output_dir': str(output_dir),
                'goose_instances': len(goose_instances),
                'instances': goose_instances,
                'extracted_files': extracted_files,
                'transcription': result.get('text', ''),
                'language': result.get('language', 'unknown')
            }
            
        except Exception as e:
            return {'error': f'Goose extraction failed: {e}'}
    
    def _find_word_instances(self, whisper_result: Dict, target_word: str) -> List[Dict]:
        """Find all instances of a specific word in the transcription."""
        instances = []
        
        for segment in whisper_result.get('segments', []):
            for word_info in segment.get('words', []):
                word = word_info.get('word', '').strip().lower()
                # Remove punctuation for comparison
                clean_word = re.sub(r'[^\w]', '', word)
                
                if clean_word == target_word.lower():
                    start = word_info.get('start', 0)
                    end = word_info.get('end', 0)
                    probability = word_info.get('probability', 0)
                    
                    # Get context (surrounding words)
                    context = self._get_word_context(segment.get('words', []), word_info)
                    
                    instances.append({
                        'word': word_info.get('word', ''),
                        'clean_word': clean_word,
                        'start': float(start),
                        'end': float(end),
                        'duration': float(end - start),
                        'confidence': float(probability),
                        'context': context,
                        'segment_id': len(instances)
                    })
        
        return instances
    
    def _get_word_context(self, words: List[Dict], target_word: Dict) -> str:
        """Get surrounding context for a word."""
        try:
            target_index = words.index(target_word)
            start_idx = max(0, target_index - 2)
            end_idx = min(len(words), target_index + 3)
            
            context_words = []
            for i in range(start_idx, end_idx):
                if i < len(words):
                    word_text = words[i].get('word', '').strip()
                    if word_text:
                        context_words.append(word_text)
            
            return ' '.join(context_words)
        except (ValueError, IndexError):
            return target_word.get('word', '')
    
    def _extract_word_instances(self, audio_file: Path, instances: List[Dict], output_dir: Path) -> List[Dict]:
        """Extract audio files for each word instance."""
        output_dir.mkdir(parents=True, exist_ok=True)
        extracted_files = []
        
        for i, instance in enumerate(instances):
            # Create filename with context
            context = instance.get('context', '').replace(' ', '_').replace('.', '').replace(',', '')
            context = re.sub(r'[^\w_-]', '', context)[:20]  # Limit length
            
            start_time = max(0, instance['start'] - self.padding)
            end_time = instance['end'] + self.padding
            duration = end_time - start_time
            
            # Create output filename
            output_file = output_dir / f"{i:02d}_{self.target_word}_{start_time:.2f}s-{end_time:.2f}s_{context}.wav"
            
            # Extract audio
            success = self._extract_audio_segment(audio_file, output_file, start_time, duration)
            
            extracted_files.append({
                'instance_id': i,
                'word': instance['word'],
                'start': instance['start'],
                'end': instance['end'],
                'duration': instance['duration'],
                'confidence': instance['confidence'],
                'context': instance['context'],
                'audio_file': str(output_file) if success else None,
                'extracted': success
            })
        
        return extracted_files
    
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
    
    def batch_extract_goose_pronunciations(self, base_dir: Path, output_dir: Path) -> Dict:
        """Extract goose pronunciations from all relevant files."""
        if not self.whisper_available:
            return {'error': 'Whisper not available'}
        
        # Find all files with goose story
        goose_files = self.find_goose_story_files(base_dir)
        
        if not goose_files:
            return {'error': 'No goose story files found'}
        
        results = {
            'total_files': len(goose_files),
            'successful': 0,
            'errors': 0,
            'total_goose_instances': 0,
            'files': []
        }
        
        print(f"Found {len(goose_files)} files with goose story")
        print(f"Extracting '{self.target_word}' pronunciations...")
        print()
        
        for i, audio_file in enumerate(goose_files, 1):
            print(f"Processing {i}/{len(goose_files)}: {audio_file.name}")
            
            # Create output directory for this file
            file_output_dir = output_dir / f"{audio_file.stem}_goose_pronunciations"
            
            # Extract goose pronunciations
            result = self.extract_goose_pronunciations(audio_file, file_output_dir)
            results['files'].append(result)
            
            if 'error' in result:
                print(f"  ❌ Error: {result['error']}")
                results['errors'] += 1
            else:
                instances = result.get('goose_instances', 0)
                results['total_goose_instances'] += instances
                results['successful'] += 1
                
                if instances > 0:
                    print(f"  ✅ Found {instances} pronunciations of '{self.target_word}'")
                    # Show context for each instance
                    for j, instance in enumerate(result.get('instances', [])):
                        context = instance.get('context', '')
                        confidence = instance.get('confidence', 0)
                        print(f"    {j+1}. \"{context}\" (confidence: {confidence:.2f})")
                else:
                    print(f"  ⚠️  No '{self.target_word}' found in this file")
        
        return results
    
    def create_pronunciation_summary(self, results: Dict, output_file: Path) -> None:
        """Create a summary of all goose pronunciations."""
        summary = {
            'target_word': self.target_word,
            'total_files_processed': results['total_files'],
            'successful_files': results['successful'],
            'error_files': results['errors'],
            'total_pronunciations': results['total_goose_instances'],
            'pronunciation_statistics': {},
            'files': []
        }
        
        # Collect pronunciation statistics
        all_instances = []
        confidence_scores = []
        durations = []
        
        for file_result in results['files']:
            if 'error' not in file_result:
                instances = file_result.get('instances', [])
                all_instances.extend(instances)
                
                for instance in instances:
                    confidence_scores.append(instance.get('confidence', 0))
                    durations.append(instance.get('duration', 0))
                
                # File summary
                file_summary = {
                    'file': file_result['input_file'],
                    'goose_instances': file_result.get('goose_instances', 0),
                    'transcription': file_result.get('transcription', ''),
                    'instances': instances
                }
                summary['files'].append(file_summary)
        
        # Calculate statistics
        if confidence_scores:
            summary['pronunciation_statistics'] = {
                'total_pronunciations': len(all_instances),
                'average_confidence': sum(confidence_scores) / len(confidence_scores),
                'average_duration': sum(durations) / len(durations),
                'min_confidence': min(confidence_scores),
                'max_confidence': max(confidence_scores),
                'min_duration': min(durations),
                'max_duration': max(durations)
            }
        
        # Save summary
        with open(output_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"Pronunciation summary saved to: {output_file}")

def main():
    """Main function."""
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python word_extraction_analyzer.py <base_directory> <output_directory>")
        print()
        print("Examples:")
        print("  python word_extraction_analyzer.py /path/to/project goose_pronunciations/")
        print("  python word_extraction_analyzer.py . goose_analysis/")
        sys.exit(1)
    
    base_dir = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])
    
    analyzer = WordExtractionAnalyzer()
    
    # Extract goose pronunciations
    results = analyzer.batch_extract_goose_pronunciations(base_dir, output_dir)
    
    if 'error' in results:
        print(f"Error: {results['error']}")
        sys.exit(1)
    
    # Create summary
    summary_file = output_dir / "goose_pronunciation_summary.json"
    analyzer.create_pronunciation_summary(results, summary_file)
    
    print(f"\nGoose Pronunciation Extraction Complete:")
    print(f"Total files: {results['total_files']}")
    print(f"Successful: {results['successful']}")
    print(f"Errors: {results['errors']}")
    print(f"Total '{analyzer.target_word}' pronunciations: {results['total_goose_instances']}")
    print(f"Summary saved to: {summary_file}")

if __name__ == "__main__":
    main()
