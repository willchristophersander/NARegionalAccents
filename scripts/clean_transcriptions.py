#!/usr/bin/env python3
"""
Clean IDEA JSONL data and extract transcriptions for Montreal Forced Alignment.

This script processes the JSONL file and extracts:
1. Clean transcriptions for MFA
2. Audio file paths
3. Sample metadata
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

def clean_transcription(text: str) -> Optional[str]:
    """
    Clean transcription text by removing HTML, extra whitespace, and metadata.
    """
    if not text or text.strip() == "":
        return None
    
    # Remove common HTML artifacts
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'&[^;]+;', '', text)
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove common metadata patterns
    patterns_to_remove = [
        r'International Dialects of English Archive.*?SEARCH THE ARCHIVE',
        r'SEARCH THE ARCHIVE.*?IDEA IS SUPPORTED BY',
        r'IDEA IS SUPPORTED BY.*?SUPPORT IDEA',
        r'SUPPORT IDEA.*?LIKE IDEA ON FACEBOOK',
        r'LIKE IDEA ON FACEBOOK.*?WHAT\'S NEW',
        r'WHAT\'S NEW.*?SHARE ON SOCIAL MEDIA',
        r'error: Content is protected !!',
        r'© \d+.*?Paul Meier Dialect Services, LC',
        r'TRANSCRIBED BY:.*?DATE OF TRANSCRIPTION.*?N/A',
        r'PHONETIC TRANSCRIPTION.*?N/A',
        r'SCHOLARLY COMMENTARY.*?N/A',
        r'COMMENTARY BY.*?N/A',
    ]
    
    for pattern in patterns_to_remove:
        text = re.sub(pattern, '', text, flags=re.DOTALL)
    
    # Clean up remaining artifacts
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    # Check if we have actual transcription content
    if len(text) < 10:  # Too short to be a real transcription
        return None
    
    # Look for transcription indicators
    transcription_indicators = [
        'I was born',
        'I was raised',
        'I grew up',
        'My family',
        'I live',
        'I work',
        'I went to',
        'I studied',
        'I moved',
        'I came from',
        'I was born and raised',
        'I was born in',
        'I was born on',
        'I was born at',
    ]
    
    # Check if this looks like a real transcription
    has_transcription_content = any(indicator in text for indicator in transcription_indicators)
    
    if not has_transcription_content:
        return None
    
    return text

def extract_transcription_from_bio(bio_text: str) -> Optional[str]:
    """
    Extract transcription from biographical information text.
    """
    if not bio_text:
        return None
    
    # Look for the transcription section
    if 'ORTHOGRAPHIC TRANSCRIPTION OF UNSCRIPTED SPEECH:' in bio_text:
        # Extract the transcription part
        transcription_section = bio_text.split('ORTHOGRAPHIC TRANSCRIPTION OF UNSCRIPTED SPEECH:')[1]
        
        # Find the end of the transcription (before TRANSCRIBED BY)
        if 'TRANSCRIBED BY:' in transcription_section:
            transcription = transcription_section.split('TRANSCRIBED BY:')[0].strip()
        else:
            transcription = transcription_section.strip()
        
        return clean_transcription(transcription)
    
    return None

def extract_us_samples(jsonl_path: str) -> List[Dict]:
    """
    Extract US samples with transcriptions from the JSONL file.
    """
    us_samples = []
    
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                data = json.loads(line.strip())
                
                # Only process US states (exclude continents and special collections)
                state = data.get('state', '')
                if not state or state in ['Africa', 'Asia', 'Australia-Oceania', 'Caribbean', 
                                       'Central America', 'Europe', 'Middle East', 'North America', 
                                       'South America', 'General American', 'Received Pronunciation',
                                       'Associate Editors', 'Submission Guidelines', 'Recording Guidelines',
                                       'Become an Associate Editor', 'Corrections & Additions',
                                       'Field Recording Guide', 'Subject Waiver', 'Style Guide for Editors',
                                       'Comma Gets A Cure', 'Copyright & Credit Information', 'FAQ',
                                       'In a Manner of Speaking', 'Links and Resources', 'Other Dialect Services',
                                       'The Rainbow Passage', 'Sponsor IDEA', 'Support IDEA', 'Testimonials & Reviews',
                                       'Wish List', 'Staff', 'Global Map', 'What\'s New', 'Contact']:
                    continue
                
                # Check if we have an audio file
                audio_filename = data.get('audio_filename')
                if not audio_filename or not Path(audio_filename).exists():
                    continue
                
                # Try to get transcription from biographical information in fields
                fields = data.get('fields', {})
                bio_text = fields.get('biographical_information', '')
                transcription = extract_transcription_from_bio(bio_text)
                
                if transcription:
                    sample = {
                        'state': state,
                        'sample_title': data.get('sample_title', ''),
                        'audio_filename': audio_filename,
                        'transcription': transcription,
                        'sample_url': data.get('sample_url', ''),
                        'description_line': data.get('description_line', ''),
                    }
                    us_samples.append(sample)
                    
            except json.JSONDecodeError as e:
                print(f"Error parsing line {line_num}: {e}")
                continue
    
    return us_samples

def create_mfa_dataset(samples: List[Dict], output_dir: str):
    """
    Create dataset structure for Montreal Forced Alignment.
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Create corpus directory
    corpus_dir = output_path / "corpus"
    corpus_dir.mkdir(exist_ok=True)
    
    # Create text directory
    text_dir = output_path / "text"
    text_dir.mkdir(exist_ok=True)
    
    # Create audio directory
    audio_dir = output_path / "audio"
    audio_dir.mkdir(exist_ok=True)
    
    mfa_samples = []
    
    for i, sample in enumerate(samples):
        # Create unique identifier
        sample_id = f"{sample['state'].lower().replace(' ', '_')}_{i+1}"
        
        # Copy audio file
        audio_src = Path(sample['audio_filename'])
        audio_dst = audio_dir / f"{sample_id}.wav"
        
        # Convert to WAV if needed (MFA prefers WAV)
        if audio_src.suffix.lower() == '.mp3':
            # For now, just copy the MP3 - MFA can handle it
            audio_dst = audio_dir / f"{sample_id}.mp3"
        
        # Copy audio file
        import shutil
        shutil.copy2(audio_src, audio_dst)
        
        # Create text file
        text_file = text_dir / f"{sample_id}.txt"
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(sample['transcription'])
        
        mfa_samples.append({
            'sample_id': sample_id,
            'state': sample['state'],
            'audio_file': str(audio_dst),
            'text_file': str(text_file),
            'transcription': sample['transcription'],
            'metadata': {
                'sample_title': sample.get('sample_title', ''),
                'sample_url': sample.get('sample_url', ''),
                'description_line': sample.get('description_line', ''),
            }
        })
    
    # Save metadata
    metadata_file = output_path / "metadata.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(mfa_samples, f, indent=2)
    
    print(f"Created MFA dataset with {len(mfa_samples)} samples")
    print(f"Output directory: {output_path}")
    print(f"Audio files: {audio_dir}")
    print(f"Text files: {text_dir}")
    print(f"Metadata: {metadata_file}")
    
    return mfa_samples

def main():
    """Main function to clean JSONL and prepare MFA dataset."""
    jsonl_path = "data/idea_us_metadata.jsonl"
    output_dir = "mfa_dataset"
    
    print("Extracting US samples with transcriptions...")
    samples = extract_us_samples(jsonl_path)
    print(f"Found {len(samples)} US samples with transcriptions")
    
    if not samples:
        print("No samples found. Check your JSONL file.")
        return
    
    print("\nCreating MFA dataset...")
    mfa_samples = create_mfa_dataset(samples, output_dir)
    
    print(f"\nSample transcriptions:")
    for sample in mfa_samples[:3]:  # Show first 3
        print(f"\n{sample['state']} - {sample['sample_id']}:")
        print(f"  {sample['transcription'][:100]}...")

if __name__ == "__main__":
    main()
