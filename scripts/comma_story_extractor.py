#!/usr/bin/env python3
"""
Comma Story Extractor

This script identifies and extracts the "Comma Gets a Cure" story from transcription files.
It uses fuzzy matching to handle transcription variations and reading errors.
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from difflib import SequenceMatcher
import argparse


class CommaStoryExtractor:
    """Extract the comma story from transcription files with fuzzy matching."""
    
    def __init__(self):
        # Reference text for "Comma Gets a Cure" story
        self.reference_text = """Well, here's a story for you: Sarah Perry was a veterinary nurse who had been working daily at an old zoo in a deserted district of the territory, so she was very happy to start a new job at a superb private practice in north square near the Duke Street Tower. That area was much nearer for her and more to her liking. Even so, on her first morning, she felt stressed. She ate a bowl of porridge, checked herself in the mirror and washed her face in a hurry. Then she put on a plain yellow dress and a fleece jacket, picked up her kit and headed for work. When she got there, there was a woman with a goose waiting for her. The woman gave Sarah an official letter from the vet. The letter implied that the animal could be suffering from a rare form of foot and mouth disease, which was surprising, because normally you would only expect to see it in a dog or a goat. Sarah was sentimental, so this made her feel sorry for the beautiful bird. Before long, that itchy goose began to strut around the office like a lunatic, which made an unsanitary mess. The goose's owner, Mary Harrison, kept calling, "Comma, Comma," which Sarah thought was an odd choice for a name. Comma was strong and huge, so it would take some force to trap her, but Sarah had a different idea. First she tried gently stroking the goose's lower back with her palm, then singing a tune to her. Finally, she administered ether. Her efforts were not futile. In no time, the goose began to tire, so Sarah was able to hold onto Comma and give her a relaxing bath. Once Sarah had managed to bathe the goose, she wiped her off with a cloth and laid her on her right side. Then Sarah confirmed the vet's diagnosis. Almost immediately, she remembered an effective treatment that required her to measure out a lot of medicine. Sarah warned that this course of treatment might be expensive—either five or six times the cost of penicillin. I can't imagine paying so much."""
        
        # Key phrases that should appear in the story (for fuzzy matching)
        self.key_phrases = [
            "here's a story for you",
            "Sarah Perry",
            "veterinary nurse",
            "old zoo",
            "deserted district",
            "superb private practice",
            "Duke Street Tower",
            "bowl of porridge",
            "plain yellow dress",
            "fleece jacket",
            "woman with a goose",
            "official letter from the vet",
            "foot and mouth disease",
            "dog or a goat",
            "sentimental",
            "itchy goose",
            "strut around",
            "lunatic",
            "unsanitary mess",
            "Mary Harrison",
            "Comma",
            "strong and huge",
            "force to trap",
            "stroking the goose",
            "singing a tune",
            "administered ether",
            "efforts were not futile",
            "relaxing bath",
            "wiped her off",
            "right side",
            "vet's diagnosis",
            "effective treatment",
            "measure out",
            "expensive",
            "five or six times",
            "penicillin",
            "can't imagine paying so much"
        ]
        
        # Alternative spellings/transcriptions we might encounter
        self.alternatives = {
            "comma": ["kama", "kamma", "comma"],
            "sarah perry": ["therapy", "sarah", "perry"],
            "veterinary": ["veterinarian", "vet"],
            "deserted": ["dessert", "desert"],
            "superb": ["cerber", "super"],
            "porridge": ["porage", "porrige"],
            "fleece": ["fleece", "fleece"],
            "unsanitary": ["unsenitary", "unsanitary"],
            "ether": ["either", "ether"],
            "futile": ["brutal", "futile"],
            "penicillin": ["peninsula", "penicillin"]
        }
    
    def normalize_text(self, text: str) -> str:
        """Normalize text for comparison by removing punctuation and converting to lowercase."""
        # Remove punctuation and extra whitespace
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def find_key_phrase_matches(self, text: str, threshold: float = 0.6) -> List[Tuple[str, float, int, int]]:
        """Find matches for key phrases in the text with fuzzy matching."""
        normalized_text = self.normalize_text(text)
        matches = []
        
        for phrase in self.key_phrases:
            normalized_phrase = self.normalize_text(phrase)
            
            # Try exact match first
            if normalized_phrase in normalized_text:
                start = normalized_text.find(normalized_phrase)
                matches.append((phrase, 1.0, start, start + len(normalized_phrase)))
                continue
            
            # Try fuzzy matching
            words = normalized_phrase.split()
            if len(words) >= 3:  # Only fuzzy match phrases with 3+ words
                for i in range(len(normalized_text) - len(normalized_phrase) + 1):
                    window = normalized_text[i:i + len(normalized_phrase) + 50]  # Slightly larger window
                    similarity = SequenceMatcher(None, normalized_phrase, window).ratio()
                    
                    if similarity >= threshold:
                        matches.append((phrase, similarity, i, i + len(normalized_phrase)))
        
        return matches
    
    def find_story_boundaries(self, segments: List[Dict], text: str) -> Tuple[Optional[int], Optional[int]]:
        """Find the start and end boundaries of the comma story in the segments."""
        # Look for the story start
        start_segment = None
        end_segment = None
        
        for i, segment in enumerate(segments):
            segment_text = segment.get('text', '').lower()
            
            # Look for story start indicators
            if start_segment is None:
                if any(phrase in segment_text for phrase in [
                    "here's a story for you",
                    "sarah perry",
                    "veterinary nurse",
                    "old zoo"
                ]):
                    start_segment = i
                    continue
            
            # Look for story end indicators
            if start_segment is not None and end_segment is None:
                if any(phrase in segment_text for phrase in [
                    "can't imagine paying so much",
                    "i can't imagine paying",
                    "paying so much",
                    "millionaire lawyer"
                ]):
                    end_segment = i
                    break
        
        return start_segment, end_segment
    
    def calculate_story_confidence(self, text: str) -> float:
        """Calculate confidence that the text contains the comma story."""
        matches = self.find_key_phrase_matches(text)
        
        if not matches:
            return 0.0
        
        # Calculate weighted confidence based on number of matches and their quality
        total_confidence = 0.0
        total_weight = 0.0
        
        for phrase, similarity, start, end in matches:
            # Weight important phrases more heavily
            weight = 1.0
            if phrase in ["sarah perry", "comma", "veterinary nurse", "duke street tower"]:
                weight = 2.0
            elif phrase in ["here's a story for you", "can't imagine paying so much"]:
                weight = 3.0
            
            total_confidence += similarity * weight
            total_weight += weight
        
        return total_confidence / total_weight if total_weight > 0 else 0.0
    
    def extract_comma_story(self, transcription_file: Path) -> Optional[Dict]:
        """Extract the comma story from a transcription file."""
        try:
            with open(transcription_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error reading {transcription_file}: {e}")
            return None
        
        # Get the full text
        full_text = data.get('text', '')
        segments = data.get('segments', [])
        
        # Calculate confidence that this contains the comma story
        confidence = self.calculate_story_confidence(full_text)
        
        if confidence < 0.3:  # Low confidence threshold
            print(f"Low confidence ({confidence:.2f}) for {transcription_file.name}")
            return None
        
        # Find story boundaries
        start_segment, end_segment = self.find_story_boundaries(segments, full_text)
        
        if start_segment is None:
            print(f"Could not find story start in {transcription_file.name}")
            return None
        
        if end_segment is None:
            print(f"Could not find story end in {transcription_file.name}")
            # Use all segments from start to end
            end_segment = len(segments) - 1
        
        # Extract story segments
        story_segments = segments[start_segment:end_segment + 1]
        
        # Reconstruct story text
        story_text = ' '.join(segment.get('text', '') for segment in story_segments)
        
        # Create result
        result = {
            'original_file': str(transcription_file),
            'confidence': confidence,
            'start_segment': start_segment,
            'end_segment': end_segment,
            'story_text': story_text.strip(),
            'segments': story_segments,
            'metadata': {
                'total_segments': len(segments),
                'story_segments': len(story_segments),
                'start_time': story_segments[0].get('start', 0) if story_segments else 0,
                'end_time': story_segments[-1].get('end', 0) if story_segments else 0
            }
        }
        
        return result
    
    def process_transcription_file(self, input_file: Path, output_dir: Path) -> bool:
        """Process a single transcription file and save the comma story."""
        result = self.extract_comma_story(input_file)
        
        if result is None:
            return False
        
        # Create output filename
        output_file = output_dir / f"{input_file.stem}_comma_story.json"
        
        # Save the result
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"Extracted comma story from {input_file.name} -> {output_file.name} (confidence: {result['confidence']:.2f})")
            return True
            
        except Exception as e:
            print(f"Error saving {output_file}: {e}")
            return False
    
    def batch_process(self, input_dir: Path, output_dir: Path, pattern: str = "*.json") -> Dict[str, int]:
        """Process all transcription files in a directory."""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        results = {
            'processed': 0,
            'successful': 0,
            'failed': 0,
            'low_confidence': 0
        }
        
        for file_path in input_dir.glob(pattern):
            if file_path.is_file():
                results['processed'] += 1
                
                # Check if this looks like a transcription file
                if any(keyword in file_path.name.lower() for keyword in ['transcription', 'whisper', 'rich']):
                    success = self.process_transcription_file(file_path, output_dir)
                    if success:
                        results['successful'] += 1
                    else:
                        results['failed'] += 1
                else:
                    print(f"Skipping {file_path.name} (doesn't appear to be a transcription file)")
        
        return results


def main():
    parser = argparse.ArgumentParser(description='Extract comma story from transcription files')
    parser.add_argument('input', help='Input file or directory')
    parser.add_argument('-o', '--output', help='Output directory', default='comma_story_extracts')
    parser.add_argument('--pattern', help='File pattern to match', default='*.json')
    parser.add_argument('--single', action='store_true', help='Process single file instead of directory')
    
    args = parser.parse_args()
    
    extractor = CommaStoryExtractor()
    input_path = Path(args.input)
    output_path = Path(args.output)
    
    if args.single or input_path.is_file():
        # Process single file
        if input_path.is_file():
            success = extractor.process_transcription_file(input_path, output_path)
            if success:
                print("Successfully extracted comma story")
            else:
                print("Failed to extract comma story")
        else:
            print(f"File not found: {input_path}")
    else:
        # Process directory
        if input_path.is_dir():
            results = extractor.batch_process(input_path, output_path, args.pattern)
            print(f"\nProcessing complete:")
            print(f"  Processed: {results['processed']}")
            print(f"  Successful: {results['successful']}")
            print(f"  Failed: {results['failed']}")
        else:
            print(f"Directory not found: {input_path}")


if __name__ == "__main__":
    main()
