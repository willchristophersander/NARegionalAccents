#!/usr/bin/env python3
"""
Batch rich transcription generator - fast and efficient.

This script:
1. Processes multiple audio files quickly
2. Generates rich JSON with timestamps, tokens, segments
3. Saves organized by state
4. Uses the same format as missouri-8_transcription.json
"""

import os
import json
import subprocess
from pathlib import Path
import time
from typing import Dict, List

def transcribe_rich(audio_file: str, output_dir: str) -> Dict:
    """
    Generate rich transcription with all the data you need.
    """
    try:
        # Fast whisper command with rich output
        cmd = [
            'whisper',
            audio_file,
            '--model', 'tiny',  # Fast model
            '--output_format', 'json',
            '--output_dir', output_dir,
            '--verbose', 'False'
        ]
        
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        end_time = time.time()
        
        if result.returncode == 0:
            # Get the generated JSON file
            audio_name = Path(audio_file).stem
            json_file = Path(output_dir) / f"{audio_name}.json"
            
            if json_file.exists():
                with open(json_file, 'r') as f:
                    whisper_data = json.load(f)
                
                # Create rich transcription file (like missouri-8_transcription.json)
                rich_data = {
                    'audio_file': str(audio_file),
                    'text': whisper_data.get('text', '').strip(),
                    'language': whisper_data.get('language', 'en'),
                    'duration': whisper_data.get('duration', 0),
                    'segments': whisper_data.get('segments', []),
                    'tokens': whisper_data.get('tokens', []),
                    'processing_time': end_time - start_time,
                    'model': 'whisper-tiny',
                    'transcription_date': time.strftime('%Y-%m-%d %H:%M:%S')
                }
                
                # Save rich transcription file
                rich_file = Path(output_dir) / f"{audio_name}_transcription.json"
                with open(rich_file, 'w') as f:
                    json.dump(rich_data, f, indent=2)
                
                # Save simple text file
                text_file = Path(output_dir) / f"{audio_name}.txt"
                with open(text_file, 'w') as f:
                    f.write(rich_data['text'])
                
                return {
                    'success': True,
                    'rich_file': str(rich_file),
                    'text_file': str(text_file),
                    'data': rich_data
                }
            else:
                return {'success': False, 'error': 'JSON file not found'}
        else:
            return {'success': False, 'error': f'Whisper failed: {result.stderr}'}
            
    except subprocess.TimeoutExpired:
        return {'success': False, 'error': 'Transcription timeout'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def process_state_batch(state: str, max_files: int = 5) -> Dict:
    """
    Process a batch of files for one state.
    """
    audio_dir = Path("audio") / state
    output_dir = Path("transcriptions") / "WhisperTranscription"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if not audio_dir.exists():
        print(f"⚠️  No audio directory for {state}")
        return {'state': state, 'files_processed': 0, 'successful': 0, 'failed': 0}
    
    # Find audio files
    audio_files = []
    for ext in ['*.mp3', '*.wav', '*.m4a']:
        audio_files.extend(audio_dir.glob(ext))
    
    if max_files:
        audio_files = audio_files[:max_files]
    
    print(f"📁 {state}: Processing {len(audio_files)} files...")
    
    results = {
        'state': state,
        'files_processed': len(audio_files),
        'successful': 0,
        'failed': 0,
        'transcriptions': []
    }
    
    for i, audio_file in enumerate(audio_files):
        print(f"   [{i+1}/{len(audio_files)}] {audio_file.name}...")
        
        result = transcribe_rich(str(audio_file), str(output_dir))
        
        if result['success']:
            results['successful'] += 1
            results['transcriptions'].append({
                'audio_file': str(audio_file),
                'rich_file': result['rich_file'],
                'text_file': result['text_file'],
                'text': result['data']['text'],
                'duration': result['data']['duration'],
                'segments': len(result['data']['segments']),
                'tokens': len(result['data']['tokens'])
            })
            print(f"      ✅ Success: {len(result['data']['text'])} chars, {len(result['data']['segments'])} segments")
        else:
            results['failed'] += 1
            print(f"      ❌ Failed: {result['error']}")
    
    return results

def main():
    """Main function for batch rich transcriptions."""
    print("=== Batch Rich Transcription Generator ===")
    print("Generating rich transcriptions like missouri-8_transcription.json...")
    
    # Check whisper
    try:
        subprocess.run(['whisper', '--help'], capture_output=True, check=True)
        print("✅ Whisper available")
    except:
        print("❌ Install whisper: pip install openai-whisper")
        return
    
    # Get states to process
    audio_dir = Path("audio")
    states = []
    
    if audio_dir.exists():
        for item in audio_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                states.append(item.name)
    
    states = sorted(states)
    print(f"📁 Found {len(states)} states")
    
    # Process first 5 states with 3 files each
    print(f"🚀 Processing first 5 states, 3 files each...")
    
    all_results = []
    total_start_time = time.time()
    
    for i, state in enumerate(states[:5]):
        print(f"\n🌍 [{i+1}/5] Processing {state}...")
        start_time = time.time()
        
        results = process_state_batch(state, max_files=3)
        all_results.append(results)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"   ⏱️  {state} completed in {duration:.1f}s")
        print(f"   📊 {results['successful']}/{results['files_processed']} successful")
    
    total_end_time = time.time()
    total_duration = total_end_time - total_start_time
    
    # Create manifest
    manifest_file = Path("transcriptions") / "WhisperTranscription" / "batch_manifest.json"
    with open(manifest_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    # Summary
    total_files = sum(r['files_processed'] for r in all_results)
    total_successful = sum(r['successful'] for r in all_results)
    total_failed = sum(r['failed'] for r in all_results)
    
    print(f"\n📊 BATCH SUMMARY:")
    print(f"   States processed: {len(all_results)}")
    print(f"   Total files: {total_files}")
    print(f"   Successful: {total_successful}")
    print(f"   Failed: {total_failed}")
    print(f"   Success rate: {(total_successful/total_files*100):.1f}%")
    print(f"   Total time: {total_duration:.1f} seconds")
    print(f"   Average per file: {total_duration/total_files:.1f} seconds")
    
    print(f"\n✅ Rich transcriptions complete!")
    print(f"   Results: transcriptions/WhisperTranscription/")
    print(f"   Manifest: {manifest_file}")
    
    # Show sample results
    print(f"\n📝 SAMPLE RESULTS:")
    for result in all_results[:3]:
        if result['transcriptions']:
            sample = result['transcriptions'][0]
            print(f"\n{result['state']}:")
            print(f"   File: {Path(sample['audio_file']).name}")
            print(f"   Text: {sample['text'][:50]}...")
            print(f"   Duration: {sample['duration']:.1f}s")
            print(f"   Segments: {sample['segments']}")
            print(f"   Tokens: {sample['tokens']}")

if __name__ == "__main__":
    main()
