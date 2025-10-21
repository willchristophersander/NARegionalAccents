#!/usr/bin/env python3
"""
Batch extract comma stories from all whisper transcriptions.
"""

import subprocess
import sys
from pathlib import Path
import json

def main():
    # Find all whisper files
    whisper_files = list(Path("transcriptions/WhisperTranscription/").rglob("*whisper.json"))
    
    print(f"Found {len(whisper_files)} whisper files to process")
    
    # Create output directory
    output_dir = Path("all_states_comma_story")
    output_dir.mkdir(exist_ok=True)
    
    results = {
        'processed': 0,
        'successful': 0,
        'failed': 0,
        'low_confidence': 0,
        'files': []
    }
    
    for file_path in whisper_files:
        print(f"\nProcessing: {file_path.name}")
        results['processed'] += 1
        
        try:
            # Run the comma story extractor
            cmd = [
                sys.executable, 
                "scripts/comma_story_extractor.py", 
                str(file_path), 
                "-o", 
                str(output_dir)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                if "Successfully extracted comma story" in result.stdout:
                    results['successful'] += 1
                    print(f"✅ Success: {file_path.name}")
                elif "Low confidence" in result.stdout:
                    results['low_confidence'] += 1
                    print(f"⚠️  Low confidence: {file_path.name}")
                else:
                    results['failed'] += 1
                    print(f"❌ Failed: {file_path.name}")
            else:
                results['failed'] += 1
                print(f"❌ Error: {file_path.name}")
                print(f"   Error: {result.stderr}")
            
            results['files'].append({
                'file': str(file_path),
                'success': result.returncode == 0,
                'output': result.stdout,
                'error': result.stderr
            })
            
        except Exception as e:
            results['failed'] += 1
            print(f"❌ Exception: {file_path.name} - {e}")
            results['files'].append({
                'file': str(file_path),
                'success': False,
                'output': '',
                'error': str(e)
            })
    
    # Save results
    with open(output_dir / "extraction_results.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"BATCH EXTRACTION COMPLETE")
    print(f"{'='*50}")
    print(f"Total processed: {results['processed']}")
    print(f"Successful: {results['successful']}")
    print(f"Low confidence: {results['low_confidence']}")
    print(f"Failed: {results['failed']}")
    print(f"Success rate: {results['successful']/results['processed']*100:.1f}%")
    
    return results

if __name__ == "__main__":
    main()
