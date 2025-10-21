#!/usr/bin/env python3
"""
Simple Speech-to-Text approach using available libraries.

This script demonstrates how to use STT to get actual spoken text
and then align it with expected text for word-level analysis.
"""

import json
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple
import re

def transcribe_with_whisper_simple(audio_file: str) -> str:
    """
    Simple Whisper transcription.
    """
    try:
        # Try to import whisper
        import whisper
        
        # Load base model (fastest)
        model = whisper.load_model("base")
        
        # Transcribe
        result = model.transcribe(audio_file)
        return result["text"].strip()
        
    except ImportError:
        print("Whisper not installed. Install with: pip install openai-whisper")
        return ""
    except Exception as e:
        print(f"Error transcribing {audio_file}: {e}")
        return ""

def transcribe_with_speech_recognition(audio_file: str) -> str:
    """
    Use speech_recognition library (simpler, but less accurate).
    """
    try:
        import speech_recognition as sr
        
        r = sr.Recognizer()
        
        with sr.AudioFile(audio_file) as source:
            audio = r.record(source)
        
        # Try Google Speech Recognition
        try:
            text = r.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            print("Could not understand audio")
            return ""
        except sr.RequestError as e:
            print(f"Error with speech recognition: {e}")
            return ""
            
    except ImportError:
        print("speech_recognition not installed. Install with: pip install SpeechRecognition")
        return ""

def create_simple_stt_dataset():
    """
    Create a simple STT dataset for testing.
    """
    # Load existing metadata
    with open('mfa_dataset/metadata.json', 'r') as f:
        samples = json.load(f)
    
    # Create STT dataset directory
    stt_dir = Path("simple_stt_dataset")
    stt_dir.mkdir(exist_ok=True)
    
    audio_dir = stt_dir / "audio"
    text_dir = stt_dir / "text"
    audio_dir.mkdir(exist_ok=True)
    text_dir.mkdir(exist_ok=True)
    
    stt_samples = []
    
    # Test with first 3 samples
    for i, sample in enumerate(samples[:3]):
        sample_id = sample['sample_id']
        state = sample['state']
        
        print(f"Processing {sample_id} ({i+1}/3)...")
        
        # Copy audio file
        audio_src = Path(sample['audio_file'])
        audio_dst = audio_dir / f"{sample_id}.wav"
        
        # Convert MP3 to WAV
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
        
        # Try Whisper first, fallback to speech_recognition
        print(f"  Transcribing with Whisper...")
        transcript = transcribe_with_whisper_simple(str(audio_dst))
        
        if not transcript:
            print(f"  Trying speech_recognition...")
            transcript = transcribe_with_speech_recognition(str(audio_dst))
        
        if not transcript:
            print(f"  No transcription for {sample_id}")
            continue
        
        # Clean transcript
        transcript = re.sub(r'\s+', ' ', transcript).strip()
        
        # Create text file
        text_file = text_dir / f"{sample_id}.txt"
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(transcript)
        
        stt_samples.append({
            'sample_id': sample_id,
            'state': state,
            'audio_file': str(audio_dst),
            'text_file': str(text_file),
            'transcript': transcript
        })
        
        print(f"  Transcribed: {transcript[:100]}...")
    
    # Save metadata
    metadata_file = stt_dir / "metadata.json"
    with open(metadata_file, 'w') as f:
        json.dump(stt_samples, f, indent=2)
    
    print(f"\nCreated simple STT dataset with {len(stt_samples)} samples")
    print(f"Audio directory: {audio_dir}")
    print(f"Text directory: {text_dir}")
    print(f"Metadata: {metadata_file}")
    
    return stt_samples

def analyze_transcript_variations(stt_samples: List[Dict]):
    """
    Analyze how transcripts vary from the expected text.
    """
    expected_words = set("""
    Well here's a story for you Sarah Perry was a veterinary nurse who had been working 
    daily at an old zoo in a deserted district of the territory so she was very happy 
    to start a new job at a superb private practice in north square near the Duke Street 
    Tower That area was much nearer for her and more to her liking Even so on her first 
    morning she felt stressed She ate a bowl of porridge checked herself in the mirror 
    and washed her face in a hurry Then she put on a plain yellow dress and a fleece 
    jacket picked up her kit and headed for work When she got there there was a woman 
    with a goose waiting for her The woman gave Sarah an official letter from the vet 
    The letter implied that the animal could be suffering from a rare form of foot and 
    mouth disease which was surprising because normally you would only expect to see it 
    in a dog or a goat Sarah was sentimental so this made her feel sorry for the beautiful 
    bird Before long that itchy goose began to strut around the office like a lunatic 
    which made an unsanitary mess The goose's owner Mary Harrison kept calling Comma 
    Comma which Sarah thought was an odd choice for a name Comma was strong and huge 
    so it would take some force to trap her but Sarah had a different idea First she 
    tried gently stroking the goose's lower back with her palm then singing a tune to 
    her Finally she administered ether Her efforts were not futile In no time the goose 
    began to tire so Sarah was able to hold onto Comma and give her a relaxing bath Once 
    Sarah had managed to bathe the goose she wiped her off with a cloth and laid her on 
    her right side Then Sarah confirmed the vet's diagnosis Almost immediately she 
    remembered an effective treatment that required her to measure out a lot of medicine 
    Sarah warned that this course of treatment might be expensive either five or six 
    times the cost of penicillin I can't imagine paying so much
    """.lower().split())
    
    print("\n=== Transcript Analysis ===")
    
    for sample in stt_samples:
        sample_id = sample['sample_id']
        state = sample['state']
        transcript = sample['transcript']
        
        transcript_words = set(transcript.lower().split())
        
        # Find common words
        common_words = expected_words.intersection(transcript_words)
        
        # Find missing words
        missing_words = expected_words - transcript_words
        
        # Find extra words
        extra_words = transcript_words - expected_words
        
        print(f"\n{sample_id} ({state}):")
        print(f"  Common words: {len(common_words)}")
        print(f"  Missing words: {len(missing_words)}")
        print(f"  Extra words: {len(extra_words)}")
        
        if common_words:
            print(f"  Sample common words: {list(common_words)[:10]}")
        
        if missing_words:
            print(f"  Sample missing words: {list(missing_words)[:10]}")
        
        if extra_words:
            print(f"  Sample extra words: {list(extra_words)[:10]}")

def main():
    """Main function for simple STT approach."""
    print("=== Simple Speech-to-Text Approach ===")
    print("Using STT to get actual spoken text...")
    
    print("\n1. Creating simple STT dataset...")
    stt_samples = create_simple_stt_dataset()
    
    if stt_samples:
        print("\n2. Analyzing transcript variations...")
        analyze_transcript_variations(stt_samples)
        
        print(f"\nAdvantages of STT approach:")
        print(f"  - Gets actual spoken words")
        print(f"  - Handles speech variations")
        print(f"  - No need for exact text matching")
        print(f"  - Can identify which words were spoken")
        
        print(f"\nNext steps:")
        print(f"  1. Install Whisper: pip install openai-whisper")
        print(f"  2. Run on more samples")
        print(f"  3. Extract features for common words")
        print(f"  4. Compare features across speakers")
    else:
        print("No samples processed. Check your audio files.")

if __name__ == "__main__":
    main()
