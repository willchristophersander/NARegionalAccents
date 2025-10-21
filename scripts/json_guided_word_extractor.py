#!/usr/bin/env python3
"""
JSON-Guided Word Extractor for Regional Accent Analysis
Uses JSON transcriptions to find word timestamps, then extracts from MP3s.
"""

import json
import os
import subprocess
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import warnings

warnings.filterwarnings('ignore')

class JSONGuidedWordExtractor:
    """Extract specific words using JSON transcription timestamps."""
    
    def __init__(self):
        self.target_word = "goose"
        self.context_words = ["goose", "geese", "gander"]
        self.padding = 0.1  # Padding around each word (seconds)
        
    def find_goose_mentions_in_json(self, json_file: Path) -> List[Dict]:
        """Find all mentions of 'goose' in a JSON transcription file."""
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            goose_mentions = []
            
            # Look through segments for the target word
            for segment in data.get('segments', []):
                segment_text = segment.get('text', '').lower()
                
                # Check if this segment contains goose-related words
                if any(word in segment_text for word in self.context_words):
                    # Find specific word timestamps within this segment
                    words = segment.get('words', [])
                    
                    for word_info in words:
                        word_text = word_info.get('word', '').strip().lower()
                        clean_word = re.sub(r'[^\w]', '', word_text)
                        
                        if clean_word == self.target_word.lower():
                            start = word_info.get('start', 0)
                            end = word_info.get('end', 0)
                            confidence = word_info.get('probability', 0)
                            
                            # Get context (surrounding words)
                            context = self._get_word_context(words, word_info)
                            
                            goose_mentions.append({
                                'word': word_info.get('word', ''),
                                'start': float(start),
                                'end': float(end),
                                'duration': float(end - start),
                                'confidence': float(confidence),
                                'context': context,
                                'segment_text': segment.get('text', ''),
                                'segment_start': segment.get('start', 0),
                                'segment_end': segment.get('end', 0)
                            })
            
            return goose_mentions
            
        except Exception as e:
            print(f"Error reading JSON file {json_file}: {e}")
            return []
    
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
    
    def find_corresponding_audio_file(self, json_file: Path) -> Optional[Path]:
        """Find the corresponding audio file for a JSON transcription."""
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            # Try to get original file path from JSON
            original_file = data.get('original_file', '')
            if original_file:
                # Convert transcription path to audio path
                if '_whisper.json' in original_file:
                    audio_path = original_file.replace('_whisper.json', '.mp3')
                    if os.path.exists(audio_path):
                        return Path(audio_path)
            
            # Try alternative paths
            json_name = json_file.stem
            possible_audio_paths = [
                f"audio/{json_name.replace('_whisper_comma_story', '')}.mp3",
                f"all_states_test_audio/sentence_0/{json_name.replace('_comma_story', '_whisper')}.mp3",
                f"all_states_test_audio/sentence_0/{json_name.replace('_comma_story', '')}.mp3"
            ]
            
            for audio_path in possible_audio_paths:
                if os.path.exists(audio_path):
                    return Path(audio_path)
            
            return None
            
        except Exception as e:
            print(f"Error finding audio file for {json_file}: {e}")
            return None
    
    def extract_goose_pronunciations(self, json_file: Path, output_dir: Path) -> Dict:
        """Extract goose pronunciations using JSON timestamps."""
        # Find goose mentions in JSON
        goose_mentions = self.find_goose_mentions_in_json(json_file)
        
        if not goose_mentions:
            return {
                'json_file': str(json_file),
                'output_dir': str(output_dir),
                'goose_mentions': 0,
                'message': f'No "{self.target_word}" found in JSON transcription'
            }
        
        # Find corresponding audio file
        audio_file = self.find_corresponding_audio_file(json_file)
        if not audio_file:
            return {
                'json_file': str(json_file),
                'output_dir': str(output_dir),
                'goose_mentions': len(goose_mentions),
                'error': 'Could not find corresponding audio file'
            }
        
        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Extract each goose pronunciation
        extracted_files = []
        for i, mention in enumerate(goose_mentions):
            # Create filename with context
            context = mention.get('context', '').replace(' ', '_').replace('.', '').replace(',', '')
            context = re.sub(r'[^\w_-]', '', context)[:20]  # Limit length
            
            start_time = max(0, mention['start'] - self.padding)
            end_time = mention['end'] + self.padding
            duration = end_time - start_time
            
            # Create output filename
            output_file = output_dir / f"{i:02d}_{self.target_word}_{start_time:.2f}s-{end_time:.2f}s_{context}.wav"
            
            # Extract audio
            success = self._extract_audio_segment(audio_file, output_file, start_time, duration)
            
            extracted_files.append({
                'mention_id': i,
                'word': mention['word'],
                'start': mention['start'],
                'end': mention['end'],
                'duration': mention['duration'],
                'confidence': mention['confidence'],
                'context': mention['context'],
                'segment_text': mention['segment_text'],
                'audio_file': str(output_file) if success else None,
                'extracted': success
            })
        
        return {
            'json_file': str(json_file),
            'audio_file': str(audio_file),
            'output_dir': str(output_dir),
            'goose_mentions': len(goose_mentions),
            'mentions': goose_mentions,
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
            return result.returncode == 0
            
        except Exception:
            return False
    
    def batch_extract_from_json_files(self, json_dir: Path, output_base_dir: Path) -> Dict:
        """Extract goose pronunciations from all JSON files."""
        results = {
            'total_files': 0,
            'successful': 0,
            'errors': 0,
            'total_goose_mentions': 0,
            'files': []
        }
        
        # Find all comma story JSON files
        json_files = list(json_dir.glob("*_comma_story.json"))
        results['total_files'] = len(json_files)
        
        print(f"Found {len(json_files)} comma story JSON files")
        print(f"Extracting '{self.target_word}' pronunciations...")
        print()
        
        for i, json_file in enumerate(json_files, 1):
            print(f"Processing {i}/{len(json_files)}: {json_file.name}")
            
            # Create output directory for this file
            file_output_dir = output_base_dir / f"{json_file.stem}_goose_pronunciations"
            
            # Extract goose pronunciations
            result = self.extract_goose_pronunciations(json_file, file_output_dir)
            results['files'].append(result)
            
            if 'error' in result:
                print(f"  ❌ Error: {result['error']}")
                results['errors'] += 1
            else:
                mentions = result.get('goose_mentions', 0)
                results['total_goose_mentions'] += mentions
                results['successful'] += 1
                
                if mentions > 0:
                    print(f"  ✅ Found {mentions} pronunciations of '{self.target_word}'")
                    # Show context for each mention
                    for j, mention in enumerate(result.get('mentions', [])):
                        context = mention.get('context', '')
                        confidence = mention.get('confidence', 0)
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
            'total_pronunciations': results['total_goose_mentions'],
            'pronunciation_statistics': {},
            'files': []
        }
        
        # Collect pronunciation statistics
        all_mentions = []
        confidence_scores = []
        durations = []
        
        for file_result in results['files']:
            if 'error' not in file_result:
                mentions = file_result.get('mentions', [])
                all_mentions.extend(mentions)
                
                for mention in mentions:
                    confidence_scores.append(mention.get('confidence', 0))
                    durations.append(mention.get('duration', 0))
                
                # File summary
                file_summary = {
                    'json_file': file_result['json_file'],
                    'audio_file': file_result.get('audio_file', ''),
                    'goose_mentions': file_result.get('goose_mentions', 0),
                    'mentions': mentions
                }
                summary['files'].append(file_summary)
        
        # Calculate statistics
        if confidence_scores:
            summary['pronunciation_statistics'] = {
                'total_pronunciations': len(all_mentions),
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
        print("Usage: python json_guided_word_extractor.py <json_directory> <output_directory>")
        print()
        print("Examples:")
        print("  python json_guided_word_extractor.py all_states_comma_story/ goose_pronunciations/")
        print("  python json_guided_word_extractor.py comma_story_extracts/ goose_analysis/")
        sys.exit(1)
    
    json_dir = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])
    
    extractor = JSONGuidedWordExtractor()
    
    # Extract goose pronunciations
    results = extractor.batch_extract_from_json_files(json_dir, output_dir)
    
    # Create summary
    summary_file = output_dir / "goose_pronunciation_summary.json"
    extractor.create_pronunciation_summary(results, summary_file)
    
    print(f"\nGoose Pronunciation Extraction Complete:")
    print(f"Total files: {results['total_files']}")
    print(f"Successful: {results['successful']}")
    print(f"Errors: {results['errors']}")
    print(f"Total '{extractor.target_word}' pronunciations: {results['total_goose_mentions']}")
    print(f"Summary saved to: {summary_file}")

if __name__ == "__main__":
    main()
