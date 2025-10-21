#!/usr/bin/env python3
"""
Prepare scripted speech dataset for MFA alignment.

Since all speakers read the same "Comma Gets a Cure" passage,
we can create a more reliable alignment dataset.
"""

import json
import subprocess
from pathlib import Path

# The standard "Comma Gets a Cure" passage
COMMA_GETS_A_CURE = """Well, here's a story for you: Sarah Perry was a veterinary nurse who had been working daily at an old zoo in a deserted district of the territory, so she was very happy to start a new job at a superb private practice in north square near the Duke Street Tower. That area was much nearer for her and more to her liking. Even so, on her first morning, she felt stressed. She ate a bowl of porridge, checked herself in the mirror and washed her face in a hurry. Then she put on a plain yellow dress and a fleece jacket, picked up her kit and headed for work. When she got there, there was a woman with a goose waiting for her. The woman gave Sarah an official letter from the vet. The letter implied that the animal could be suffering from a rare form of foot and mouth disease, which was surprising, because normally you would only expect to see it in a dog or a goat. Sarah was sentimental, so this made her feel sorry for the beautiful bird. Before long, that itchy goose began to strut around the office like a lunatic, which made an unsanitary mess. The goose's owner, Mary Harrison, kept calling, "Comma, Comma," which Sarah thought was an odd choice for a name. Comma was strong and huge, so it would take some force to trap her, but Sarah had a different idea. First she tried gently stroking the goose's lower back with her palm, then singing a tune to her. Finally, she administered ether. Her efforts were not futile. In no time, the goose began to tire, so Sarah was able to hold onto Comma and give her a relaxing bath. Once Sarah had managed to bathe the goose, she wiped her off with a cloth and laid her on her right side. Then Sarah confirmed the vet's diagnosis. Almost immediately, she remembered an effective treatment that required her to measure out a lot of medicine. Sarah warned that this course of treatment might be expensive—either five or six times the cost of penicillin. I can't imagine paying so much."""

def create_scripted_dataset():
    """Create a dataset with just the scripted speech for reliable alignment."""
    
    # Load existing metadata
    with open('mfa_dataset/metadata.json', 'r') as f:
        samples = json.load(f)
    
    # Create new dataset directory
    scripted_dir = Path("scripted_dataset")
    scripted_dir.mkdir(exist_ok=True)
    
    audio_dir = scripted_dir / "audio"
    text_dir = scripted_dir / "text"
    audio_dir.mkdir(exist_ok=True)
    text_dir.mkdir(exist_ok=True)
    
    scripted_samples = []
    
    for sample in samples:
        sample_id = sample['sample_id']
        state = sample['state']
        
        # Copy audio file
        audio_src = Path(sample['audio_file'])
        audio_dst = audio_dir / f"{sample_id}.wav"
        
        # Convert MP3 to WAV for MFA
        if audio_src.suffix.lower() == '.mp3':
            try:
                subprocess.run([
                    'ffmpeg', '-i', str(audio_src), '-ar', '16000', '-ac', '1', 
                    str(audio_dst), '-y'
                ], check=True, capture_output=True)
            except subprocess.CalledProcessError as e:
                print(f"Error converting {sample_id}: {e}")
                continue
        else:
            import shutil
            shutil.copy2(audio_src, audio_dst)
        
        # Create text file with just the scripted speech
        text_file = text_dir / f"{sample_id}.txt"
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(COMMA_GETS_A_CURE)
        
        scripted_samples.append({
            'sample_id': sample_id,
            'state': state,
            'audio_file': str(audio_dst),
            'text_file': str(text_file),
            'scripted_text': COMMA_GETS_A_CURE
        })
    
    # Save metadata
    metadata_file = scripted_dir / "metadata.json"
    with open(metadata_file, 'w') as f:
        json.dump(scripted_samples, f, indent=2)
    
    print(f"Created scripted dataset with {len(scripted_samples)} samples")
    print(f"Audio directory: {audio_dir}")
    print(f"Text directory: {text_dir}")
    print(f"Metadata: {metadata_file}")
    
    return scripted_samples

def create_unscripted_dataset():
    """Create a separate dataset with unscripted speech."""
    
    # Load existing metadata
    with open('mfa_dataset/metadata.json', 'r') as f:
        samples = json.load(f)
    
    # Create new dataset directory
    unscripted_dir = Path("unscripted_dataset")
    unscripted_dir.mkdir(exist_ok=True)
    
    audio_dir = unscripted_dir / "audio"
    text_dir = unscripted_dir / "text"
    audio_dir.mkdir(exist_ok=True)
    text_dir.mkdir(exist_ok=True)
    
    unscripted_samples = []
    
    for sample in samples:
        sample_id = sample['sample_id']
        state = sample['state']
        
        # Copy audio file
        audio_src = Path(sample['audio_file'])
        audio_dst = audio_dir / f"{sample_id}.wav"
        
        # Convert MP3 to WAV for MFA
        if audio_src.suffix.lower() == '.mp3':
            try:
                subprocess.run([
                    'ffmpeg', '-i', str(audio_src), '-ar', '16000', '-ac', '1', 
                    str(audio_dst), '-y'
                ], check=True, capture_output=True)
            except subprocess.CalledProcessError as e:
                print(f"Error converting {sample_id}: {e}")
                continue
        else:
            import shutil
            shutil.copy2(audio_src, audio_dst)
        
        # Create text file with unscripted speech
        text_file = text_dir / f"{sample_id}.txt"
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(sample['transcription'])
        
        unscripted_samples.append({
            'sample_id': sample_id,
            'state': state,
            'audio_file': str(audio_dst),
            'text_file': str(text_file),
            'unscripted_text': sample['transcription']
        })
    
    # Save metadata
    metadata_file = unscripted_dir / "metadata.json"
    with open(metadata_file, 'w') as f:
        json.dump(unscripted_samples, f, indent=2)
    
    print(f"Created unscripted dataset with {len(unscripted_samples)} samples")
    print(f"Audio directory: {audio_dir}")
    print(f"Text directory: {text_dir}")
    print(f"Metadata: {metadata_file}")
    
    return unscripted_samples

def main():
    """Create separate datasets for scripted and unscripted speech."""
    print("Creating separate datasets for MFA alignment...")
    
    print("\n1. Creating scripted speech dataset (Comma Gets a Cure)...")
    scripted_samples = create_scripted_dataset()
    
    print("\n2. Creating unscripted speech dataset...")
    unscripted_samples = create_unscripted_dataset()
    
    print(f"\nSummary:")
    print(f"  Scripted samples: {len(scripted_samples)}")
    print(f"  Unscripted samples: {len(unscripted_samples)}")
    print(f"\nNext steps:")
    print(f"  1. Install MFA: conda install -c conda-forge montreal-forced-alignment")
    print(f"  2. Run MFA on scripted dataset first (more reliable)")
    print(f"  3. Run MFA on unscripted dataset")
    print(f"  4. Extract word-level features from alignments")

if __name__ == "__main__":
    main()
