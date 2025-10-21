#!/usr/bin/env python3
"""
Simple Audio Standardizer for Regional Accent Analysis
Standardizes audio files for consistent analysis.
"""

import json
import os
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
import warnings

warnings.filterwarnings('ignore')

class SimpleAudioStandardizer:
    """Simple audio standardization using FFmpeg."""
    
    def __init__(self):
        # Standardization parameters
        self.target_sample_rate = 16000  # 16kHz for speech analysis
        self.target_channels = 1          # Mono
        self.target_bit_depth = 16        # 16-bit
        self.target_lufs = -23.0          # Broadcast standard loudness
        self.max_peak = -1.0             # Maximum peak level (dB)
        
    def standardize_audio_file(self, input_file: Path, output_file: Path) -> Dict:
        """Standardize a single audio file."""
        try:
            # Create output directory if needed
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Build FFmpeg command
            cmd = [
                'ffmpeg', '-i', str(input_file),
                '-ar', str(self.target_sample_rate),      # Sample rate
                '-ac', str(self.target_channels),         # Channels (mono)
                '-sample_fmt', 's16',                     # 16-bit
                '-af', self._build_audio_filters(),       # Audio filters
                '-y',                                     # Overwrite
                str(output_file)
            ]
            
            # Execute
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Verify output
                verification = self._verify_output(output_file)
                return {
                    'input_file': str(input_file),
                    'output_file': str(output_file),
                    'success': True,
                    'verification': verification
                }
            else:
                return {
                    'input_file': str(input_file),
                    'output_file': str(output_file),
                    'success': False,
                    'error': result.stderr
                }
                
        except Exception as e:
            return {
                'input_file': str(input_file),
                'output_file': str(output_file),
                'success': False,
                'error': str(e)
            }
    
    def _build_audio_filters(self) -> str:
        """Build FFmpeg audio filter chain."""
        filters = []
        
        # 1. Loudness normalization (LUFS)
        filters.append(f"loudnorm=I={self.target_lufs}:TP={self.max_peak}:LRA=7")
        
        # 2. Peak limiting
        filters.append(f"alimiter=level_in=1:level_out={10**(self.max_peak/20)}")
        
        # 3. High-pass filter (remove low-frequency noise)
        filters.append("highpass=f=80")
        
        # 4. Low-pass filter (remove high-frequency noise)
        filters.append("lowpass=f=8000")
        
        # 5. Compressor for speech enhancement
        filters.append("acompressor=threshold=0.1:ratio=3:attack=5:release=50")
        
        return ','.join(filters)
    
    def _verify_output(self, output_file: Path) -> Dict:
        """Verify the standardized output."""
        try:
            # Get file info using ffprobe
            cmd = [
                'ffprobe', '-v', 'quiet', '-print_format', 'json',
                '-show_format', '-show_streams', str(output_file)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                info = json.loads(result.stdout)
                stream = info['streams'][0]
                
                return {
                    'sample_rate': int(stream.get('sample_rate', 0)),
                    'channels': int(stream.get('channels', 0)),
                    'duration': float(stream.get('duration', 0)),
                    'bit_rate': int(stream.get('bit_rate', 0)),
                    'format': stream.get('codec_name', 'unknown')
                }
            else:
                return {'error': 'Could not verify output'}
                
        except Exception as e:
            return {'error': str(e)}
    
    def batch_standardize(self, input_dir: Path, output_dir: Path) -> Dict:
        """Standardize multiple audio files."""
        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)
        
        results = {
            'total_files': 0,
            'successful': 0,
            'errors': 0,
            'files': []
        }
        
        # Find audio files
        audio_extensions = ['.mp3', '.wav', '.m4a', '.flac', '.aac']
        audio_files = []
        for ext in audio_extensions:
            audio_files.extend(input_dir.glob(f'*{ext}'))
        
        results['total_files'] = len(audio_files)
        
        print(f"Standardizing {len(audio_files)} audio files...")
        print(f"Target: {self.target_sample_rate}Hz, {self.target_channels}ch, {self.target_bit_depth}bit")
        print(f"Loudness: {self.target_lufs} LUFS, Peak: {self.max_peak} dB")
        print()
        
        for i, audio_file in enumerate(audio_files, 1):
            print(f"Processing {i}/{len(audio_files)}: {audio_file.name}")
            
            # Create output filename
            output_file = output_dir / f"{audio_file.stem}_standardized.wav"
            
            # Standardize
            result = self.standardize_audio_file(audio_file, output_file)
            results['files'].append(result)
            
            if result['success']:
                verification = result.get('verification', {})
                sample_rate = verification.get('sample_rate', 0)
                channels = verification.get('channels', 0)
                duration = verification.get('duration', 0)
                print(f"  ✅ Success: {sample_rate}Hz, {channels}ch, {duration:.1f}s")
                results['successful'] += 1
            else:
                error = result.get('error', 'Unknown error')
                print(f"  ❌ Error: {error}")
                results['errors'] += 1
        
        return results

def main():
    """Main function."""
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python simple_audio_standardizer.py <input_file_or_dir> <output_file_or_dir>")
        print()
        print("Examples:")
        print("  python simple_audio_standardizer.py audio.mp3 standardized.wav")
        print("  python simple_audio_standardizer.py input_dir/ output_dir/")
        sys.exit(1)
    
    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    
    standardizer = SimpleAudioStandardizer()
    
    if input_path.is_file():
        # Single file
        result = standardizer.standardize_audio_file(input_path, output_path)
        print(json.dumps(result, indent=2))
    elif input_path.is_dir():
        # Directory
        results = standardizer.batch_standardize(input_path, output_path)
        
        # Save results
        results_file = output_path / "standardization_results.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\nStandardization Complete:")
        print(f"Total files: {results['total_files']}")
        print(f"Successful: {results['successful']}")
        print(f"Errors: {results['errors']}")
        print(f"Results saved to: {results_file}")
    else:
        print(f"Path not found: {input_path}")
        sys.exit(1)

if __name__ == "__main__":
    main()
