#!/usr/bin/env python3
"""
Generate real transcriptions from MP3 files using Whisper.

This script:
1. Processes actual MP3 files with Whisper
2. Generates real speech transcriptions
3. Saves rich JSON with timestamps and tokens
4. Fast processing with tiny model
"""

import json
import os
import subprocess
import time
from pathlib import Path
from typing import Optional

def transcribe_mp3(audio_file: Path, output_dir: Path, timeout: Optional[float] = None) -> dict:
    """
    Transcribe MP3 file using Whisper and return rich data.
    """
    try:
        audio_file = audio_file.resolve()
        output_dir = output_dir.resolve()
        # Fast whisper command
        cmd = [
            'whisper',
            str(audio_file),
            '--model', 'tiny',
            '--output_format', 'json',
            '--output_dir', str(output_dir),
            '--verbose', 'False',
            '--device', 'mps',
        ]
        
        start_time = time.time()
        run_kwargs = dict(capture_output=True, text=True)
        if timeout is not None and timeout > 0:
            run_kwargs["timeout"] = timeout
        result = subprocess.run(cmd, **run_kwargs)
        end_time = time.time()
        
        if result.returncode == 0:
            # Get the generated JSON file
            audio_name = audio_file.stem
            json_file = output_dir / f"{audio_name}.json"
            
            if json_file.exists():
                with open(json_file, 'r') as f:
                    whisper_data = json.load(f)
                
                # Create rich transcription
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
                rich_file = output_dir / f"{audio_name}_transcription.json"
                with open(rich_file, 'w') as f:
                    json.dump(rich_data, f, indent=2)
                
                # Save text file
                text_file = output_dir / f"{audio_name}.txt"
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

def process_state_mp3s(
    state: str,
    max_files: Optional[int] = None,
    timeout: Optional[float] = None,
) -> dict:
    """
    Process MP3 files for one state.
    """
    audio_dir = Path("audio") / state
    output_dir = Path("transcriptions") / "WhisperTranscription" / state
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if not audio_dir.exists():
        print(f"⚠️  No audio directory for {state}")
        return {'state': state, 'files_processed': 0, 'successful': 0, 'failed': 0}
    
    # Find MP3 files
    mp3_files = list(audio_dir.glob("*.mp3"))
    audio_total = len(mp3_files)
    print(f"📁 {state}: Found {audio_total} MP3 files.")

    pending_files = []
    skipped_existing = 0
    for candidate in mp3_files:
        transcript_path = output_dir / f"{candidate.stem}.txt"
        if transcript_path.exists():
            skipped_existing += 1
            continue
        pending_files.append(candidate)

    if skipped_existing:
        print(f"   ⏭️  Skipping {skipped_existing} already-transcribed file(s).")

    if not pending_files:
        print("   ℹ️  Nothing new to transcribe.")
        return {'state': state, 'files_processed': 0, 'successful': 0, 'failed': 0}

    if max_files is not None and max_files > 0:
        pending_files = pending_files[:max_files]

    print(f"   🎧 Queued {len(pending_files)} MP3 file(s) for transcription.")
    
    results = {
        'state': state,
        'files_processed': len(pending_files),
        'successful': 0,
        'failed': 0,
        'transcriptions': []
    }
    
    for i, mp3_file in enumerate(pending_files, start=1):
        print(f"   [{i}/{len(pending_files)}] {mp3_file.name}...")
        
        result = transcribe_mp3(mp3_file, output_dir, timeout=timeout)
        
        if result['success']:
            results['successful'] += 1
            results['transcriptions'].append({
                'mp3_file': str(mp3_file),
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
    """Main function for real MP3 transcriptions."""
    print("=== Real MP3 Transcriptions ===")
    print("Processing actual MP3 files with Whisper...")

    timeout_env = os.getenv("WHISPER_TIMEOUT")
    per_file_timeout: Optional[float] = None
    if timeout_env:
        try:
            per_file_timeout = float(timeout_env)
            if per_file_timeout <= 0:
                print("ℹ️  Ignoring non-positive WHISPER_TIMEOUT; running without timeout.")
                per_file_timeout = None
            else:
                print(f"⏱️  Per-file timeout set to {per_file_timeout}s from WHISPER_TIMEOUT.")
        except ValueError:
            print("⚠️  Invalid WHISPER_TIMEOUT value; running without timeout.")
    
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
    state_count = len(states)
    print(f"📁 Found {state_count} states with audio files")
    
    if not states:
        print("⚠️  No states to process. Exiting.")
        return
    
    print("🚀 Processing all states...")
    
    all_results = []
    total_start_time = time.time()
    
    for i, state in enumerate(states, start=1):
        print(f"\n🌍 [{i}/{state_count}] Processing {state}...")
        start_time = time.time()
        
        results = process_state_mp3s(state, max_files=1, timeout=per_file_timeout)
        all_results.append(results)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"   ⏱️  {state} completed in {duration:.1f}s")
        print(f"   📊 {results['successful']}/{results['files_processed']} successful")
    
    total_end_time = time.time()
    total_duration = total_end_time - total_start_time
    
    # Create manifest
    manifest_file = Path("transcriptions") / "WhisperTranscription" / "real_mp3_manifest.json"
    with open(manifest_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    # Summary
    total_files = sum(r['files_processed'] for r in all_results)
    total_successful = sum(r['successful'] for r in all_results)
    total_failed = sum(r['failed'] for r in all_results)
    
    print(f"\n📊 REAL MP3 TRANSCRIPTIONS SUMMARY:")
    print(f"   States processed: {len(all_results)}")
    print(f"   Total files: {total_files}")
    print(f"   Successful: {total_successful}")
    print(f"   Failed: {total_failed}")
    print(f"   Success rate: {(total_successful/total_files*100):.1f}%")
    print(f"   Total time: {total_duration:.1f} seconds")
    print(f"   Average per file: {total_duration/total_files:.1f} seconds")
    
    print(f"\n✅ Real MP3 transcriptions complete!")
    print(f"   Results: transcriptions/WhisperTranscription/")
    print(f"   Manifest: {manifest_file}")
    
    # Show sample results
    print(f"\n📝 SAMPLE RESULTS:")
    for result in all_results[:3]:
        if result['transcriptions']:
            sample = result['transcriptions'][0]
            print(f"\n{result['state']}:")
            print(f"   File: {Path(sample['mp3_file']).name}")
            print(f"   Text: {sample['text'][:100]}...")
            print(f"   Duration: {sample['duration']:.1f}s")
            print(f"   Segments: {sample['segments']}")
            print(f"   Tokens: {sample['tokens']}")

if __name__ == "__main__":
    main()
