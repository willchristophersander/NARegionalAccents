#!/usr/bin/env python3
"""
Comma Story Aligner

This script creates aligned segments of the comma story across different transcriptions,
enabling direct comparison of how different speakers pronounce the same sentences.
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from difflib import SequenceMatcher
import argparse


class CommaStoryAligner:
    """Align comma story segments across different transcriptions for comparison."""
    
    def __init__(self):
        # Reference sentences from the comma story for alignment
        self.reference_sentences = [
            "Well, here's a story for you",
            "Sarah Perry was a veterinary nurse who had been working daily at an old zoo in a deserted district of the territory",
            "so she was very happy to start a new job at a superb private practice in north square near the Duke Street Tower",
            "That area was much nearer for her and more to her liking",
            "Even so, on her first morning, she felt stressed",
            "She ate a bowl of porridge, checked herself in the mirror and washed her face in a hurry",
            "Then she put on a plain yellow dress and a fleece jacket, picked up her kit and headed for work",
            "When she got there, there was a woman with a goose waiting for her",
            "The woman gave Sarah an official letter from the vet",
            "The letter implied that the animal could be suffering from a rare form of foot and mouth disease, which was surprising, because normally you would only expect to see it in a dog or a goat",
            "Sarah was sentimental, so this made her feel sorry for the beautiful bird",
            "Before long, that itchy goose began to strut around the office like a lunatic, which made an unsanitary mess",
            "The goose's owner, Mary Harrison, kept calling, \"Comma, Comma,\" which Sarah thought was an odd choice for a name",
            "Comma was strong and huge, so it would take some force to trap her, but Sarah had a different idea",
            "First she tried gently stroking the goose's lower back with her palm, then singing a tune to her",
            "Finally, she administered ether",
            "Her efforts were not futile",
            "In no time, the goose began to tire, so Sarah was able to hold onto Comma and give her a relaxing bath",
            "Once Sarah had managed to bathe the goose, she wiped her off with a cloth and laid her on her right side",
            "Then Sarah confirmed the vet's diagnosis",
            "Almost immediately, she remembered an effective treatment that required her to measure out a lot of medicine",
            "Sarah warned that this course of treatment might be expensive—either five or six times the cost of penicillin",
            "I can't imagine paying so much"
        ]
        
        # Alternative patterns for each sentence to handle transcription variations
        self.sentence_patterns = {
            0: ["here's a story for you", "story for you"],
            1: ["sarah perry", "veterinary nurse", "old zoo", "deserted district"],
            2: ["superb private practice", "north square", "duke street tower"],
            3: ["much nearer for her", "more to her liking"],
            4: ["first morning", "felt stressed"],
            5: ["bowl of porridge", "checked herself", "washed her face"],
            6: ["plain yellow dress", "fleece jacket", "picked up her kit"],
            7: ["woman with a goose", "waiting for her"],
            8: ["official letter from the vet"],
            9: ["foot and mouth disease", "dog or a goat"],
            10: ["sentimental", "feel sorry for the beautiful bird"],
            11: ["itchy goose", "strut around", "lunatic", "unsanitary mess"],
            12: ["mary harrison", "comma comma", "odd choice for a name"],
            13: ["strong and huge", "force to trap her", "different idea"],
            14: ["stroking the goose", "lower back", "singing a tune"],
            15: ["administered ether"],
            16: ["efforts were not futile"],
            17: ["goose began to tire", "hold onto comma", "relaxing bath"],
            18: ["bathe the goose", "wiped her off", "right side"],
            19: ["confirmed the vet's diagnosis"],
            20: ["effective treatment", "measure out", "lot of medicine"],
            21: ["expensive", "five or six times", "cost of penicillin"],
            22: ["can't imagine paying so much"]
        }
    
    def normalize_text(self, text: str) -> str:
        """Normalize text for comparison."""
        # Remove punctuation and extra whitespace
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def find_sentence_in_segments(self, segments: List[Dict], sentence_idx: int) -> Optional[Dict]:
        """Find which segment contains the target sentence."""
        target_patterns = self.sentence_patterns.get(sentence_idx, [])
        
        for segment in segments:
            segment_text = self.normalize_text(segment.get('text', ''))
            
            # Check if any target patterns are in this segment
            for pattern in target_patterns:
                if pattern in segment_text:
                    return segment
        
        return None
    
    def extract_sentence_segments(self, comma_story_data: Dict) -> List[Dict]:
        """Extract individual sentence segments from comma story data."""
        segments = comma_story_data.get('segments', [])
        sentence_segments = []
        
        for i, reference_sentence in enumerate(self.reference_sentences):
            # Find the segment containing this sentence
            segment = self.find_sentence_in_segments(segments, i)
            
            if segment:
                sentence_segments.append({
                    'sentence_idx': i,
                    'reference_text': reference_sentence,
                    'segment': segment,
                    'start_time': segment.get('start', 0),
                    'end_time': segment.get('end', 0),
                    'text': segment.get('text', '').strip(),
                    'duration': segment.get('end', 0) - segment.get('start', 0)
                })
            else:
                # Create placeholder for missing sentence
                sentence_segments.append({
                    'sentence_idx': i,
                    'reference_text': reference_sentence,
                    'segment': None,
                    'start_time': None,
                    'end_time': None,
                    'text': None,
                    'duration': None,
                    'missing': True
                })
        
        return sentence_segments
    
    def create_aligned_dataset(self, comma_story_files: List[Path]) -> Dict:
        """Create an aligned dataset of comma story segments across multiple transcriptions."""
        aligned_data = {
            'metadata': {
                'total_speakers': len(comma_story_files),
                'total_sentences': len(self.reference_sentences),
                'reference_sentences': self.reference_sentences
            },
            'speakers': {},
            'sentence_alignments': {}
        }
        
        # Process each speaker's comma story
        for file_path in comma_story_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    comma_story_data = json.load(f)
                
                # Extract speaker info from filename
                speaker_id = file_path.stem.replace('_comma_story', '')
                
                # Extract sentence segments
                sentence_segments = self.extract_sentence_segments(comma_story_data)
                
                aligned_data['speakers'][speaker_id] = {
                    'file': str(file_path),
                    'confidence': comma_story_data.get('confidence', 0),
                    'sentences': sentence_segments,
                    'total_duration': comma_story_data.get('metadata', {}).get('end_time', 0) - 
                                    comma_story_data.get('metadata', {}).get('start_time', 0)
                }
                
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                continue
        
        # Create sentence-level alignments
        for sentence_idx in range(len(self.reference_sentences)):
            sentence_alignments = []
            
            for speaker_id, speaker_data in aligned_data['speakers'].items():
                sentence_data = speaker_data['sentences'][sentence_idx]
                
                if not sentence_data.get('missing', False):
                    sentence_alignments.append({
                        'speaker_id': speaker_id,
                        'start_time': sentence_data['start_time'],
                        'end_time': sentence_data['end_time'],
                        'text': sentence_data['text'],
                        'duration': sentence_data['duration'],
                        'confidence': speaker_data['confidence']
                    })
            
            aligned_data['sentence_alignments'][f'sentence_{sentence_idx}'] = {
                'reference_text': self.reference_sentences[sentence_idx],
                'speakers': sentence_alignments,
                'total_speakers': len(sentence_alignments)
            }
        
        return aligned_data
    
    def generate_audio_segments_script(self, aligned_data: Dict, audio_base_dir: Path, output_dir: Path) -> str:
        """Generate a script to extract audio segments for each sentence."""
        script_lines = [
            "#!/bin/bash",
            "# Generated script to extract comma story audio segments",
            f"# Output directory: {output_dir}",
            "",
            "set -e",
            "",
            f"mkdir -p {output_dir}",
            ""
        ]
        
        for sentence_key, sentence_data in aligned_data['sentence_alignments'].items():
            sentence_idx = sentence_key.replace('sentence_', '')
            sentence_dir = output_dir / f"sentence_{sentence_idx}"
            
            script_lines.append(f"# {sentence_data['reference_text']}")
            script_lines.append(f"mkdir -p {sentence_dir}")
            script_lines.append("")
            
            for speaker in sentence_data['speakers']:
                speaker_id = speaker['speaker_id']
                start_time = speaker['start_time']
                end_time = speaker['end_time']
                duration = speaker['duration']
                
                # Find the original audio file
                audio_file = self.find_audio_file(audio_base_dir, speaker_id)
                
                if audio_file:
                    output_file = sentence_dir / f"{speaker_id}.mp3"
                    
                    script_lines.append(f"# Extract {speaker_id} - {start_time:.2f}s to {end_time:.2f}s")
                    script_lines.append(f"ffmpeg -i \"{audio_file}\" -ss {start_time:.2f} -t {duration:.2f} -c copy \"{output_file}\"")
                    script_lines.append("")
        
        return "\n".join(script_lines)
    
    def find_audio_file(self, audio_base_dir: Path, speaker_id: str) -> Optional[Path]:
        """Find the original audio file for a speaker."""
        # Try different patterns to find the audio file
        patterns = [
            f"{speaker_id}.mp3",
            f"{speaker_id.replace('_whisper', '')}.mp3",
            f"{speaker_id.replace('_transcription', '')}.mp3"
        ]
        
        for pattern in patterns:
            audio_file = audio_base_dir / pattern
            if audio_file.exists():
                return audio_file
        
        # Try searching in subdirectories
        for audio_file in audio_base_dir.rglob(f"*{speaker_id.split('_')[0]}*.mp3"):
            return audio_file
        
        return None
    
    def save_aligned_dataset(self, aligned_data: Dict, output_file: Path):
        """Save the aligned dataset to a JSON file."""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(aligned_data, f, indent=2, ensure_ascii=False)
    
    def create_comparison_summary(self, aligned_data: Dict) -> Dict:
        """Create a summary of the aligned dataset for analysis."""
        summary = {
            'total_speakers': len(aligned_data['speakers']),
            'total_sentences': len(self.reference_sentences),
            'sentence_coverage': {},
            'speaker_coverage': {},
            'missing_segments': []
        }
        
        # Calculate sentence coverage
        for sentence_key, sentence_data in aligned_data['sentence_alignments'].items():
            sentence_idx = sentence_key.replace('sentence_', '')
            coverage = len(sentence_data['speakers']) / len(aligned_data['speakers'])
            summary['sentence_coverage'][sentence_idx] = {
                'coverage': coverage,
                'speakers_count': len(sentence_data['speakers']),
                'reference': sentence_data['reference_text']
            }
        
        # Calculate speaker coverage
        for speaker_id, speaker_data in aligned_data['speakers'].items():
            missing_count = sum(1 for s in speaker_data['sentences'] if s.get('missing', False))
            coverage = (len(speaker_data['sentences']) - missing_count) / len(self.reference_sentences)
            summary['speaker_coverage'][speaker_id] = {
                'coverage': coverage,
                'missing_sentences': missing_count,
                'confidence': speaker_data['confidence']
            }
        
        return summary


def main():
    parser = argparse.ArgumentParser(description='Align comma story segments across transcriptions')
    parser.add_argument('input_dir', help='Directory containing comma story JSON files')
    parser.add_argument('-o', '--output', help='Output directory', default='aligned_comma_story')
    parser.add_argument('--audio-dir', help='Base directory for original audio files', default='audio')
    parser.add_argument('--pattern', help='File pattern to match', default='*_comma_story.json')
    parser.add_argument('--generate-script', action='store_true', help='Generate audio extraction script')
    
    args = parser.parse_args()
    
    aligner = CommaStoryAligner()
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output)
    audio_dir = Path(args.audio_dir)
    
    # Find all comma story files
    comma_story_files = list(input_dir.glob(args.pattern))
    
    if not comma_story_files:
        print(f"No comma story files found in {input_dir} with pattern {args.pattern}")
        return
    
    print(f"Found {len(comma_story_files)} comma story files")
    
    # Create aligned dataset
    print("Creating aligned dataset...")
    aligned_data = aligner.create_aligned_dataset(comma_story_files)
    
    # Save aligned dataset
    output_dir.mkdir(parents=True, exist_ok=True)
    dataset_file = output_dir / "aligned_comma_story.json"
    aligner.save_aligned_dataset(aligned_data, dataset_file)
    print(f"Saved aligned dataset to {dataset_file}")
    
    # Create summary
    summary = aligner.create_comparison_summary(aligned_data)
    summary_file = output_dir / "alignment_summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"Saved alignment summary to {summary_file}")
    
    # Generate audio extraction script if requested
    if args.generate_script:
        script_content = aligner.generate_audio_segments_script(aligned_data, audio_dir, output_dir / "audio_segments")
        script_file = output_dir / "extract_audio_segments.sh"
        with open(script_file, 'w') as f:
            f.write(script_content)
        script_file.chmod(0o755)  # Make executable
        print(f"Generated audio extraction script: {script_file}")
    
    # Print summary
    print(f"\nAlignment Summary:")
    print(f"  Total speakers: {summary['total_speakers']}")
    print(f"  Total sentences: {summary['total_sentences']}")
    
    # Show sentence coverage
    print(f"\nSentence Coverage:")
    for sentence_idx, coverage_data in summary['sentence_coverage'].items():
        print(f"  Sentence {sentence_idx}: {coverage_data['coverage']:.1%} ({coverage_data['speakers_count']}/{summary['total_speakers']} speakers)")
    
    # Show speaker coverage
    print(f"\nSpeaker Coverage:")
    for speaker_id, coverage_data in summary['speaker_coverage'].items():
        print(f"  {speaker_id}: {coverage_data['coverage']:.1%} ({coverage_data['missing_sentences']} missing)")


if __name__ == "__main__":
    main()
