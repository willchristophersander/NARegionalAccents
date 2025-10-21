#!/usr/bin/env python3
"""
Audio Standardization System for Regional Accent Analysis
Standardizes audio files for consistent analysis across different recordings.
"""

import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import numpy as np
import scipy.io.wavfile as wavfile
import warnings

warnings.filterwarnings('ignore')

class AudioStandardizer:
    """Comprehensive audio standardization for accent analysis."""
    
    def __init__(self):
        # Standardization parameters
        self.target_sample_rate = 16000  # 16kHz for speech analysis
        self.target_channels = 1         # Mono
        self.target_bit_depth = 16       # 16-bit
        self.target_format = 'wav'      # WAV format
        
        # Normalization parameters
        self.target_lufs = -23.0        # Broadcast standard
        self.max_peak = -1.0            # Maximum peak level (dB)
        self.normalization_method = 'lufs'  # or 'peak' or 'rms'
        
        # Noise reduction parameters
        self.noise_reduction = True
        self.noise_reduction_strength = 0.5  # 0.0 to 1.0
        
        # Speech enhancement parameters
        self.enhance_speech = True
        self.enhancement_strength = 0.3  # 0.0 to 1.0
        
    def standardize_audio_file(self, input_file: Path, output_file: Path) -> Dict:
        """Standardize a single audio file."""
        try:
            # Step 1: Basic format conversion
            temp_file = self._convert_format(input_file)
            if not temp_file:
                return {'error': 'Format conversion failed'}
            
            # Step 2: Audio analysis
            analysis = self._analyze_audio(temp_file)
            
            # Step 3: Apply standardization
            standardized_file = self._apply_standardization(temp_file, output_file, analysis)
            
            # Step 4: Quality check
            quality_check = self._quality_check(standardized_file)
            
            # Cleanup
            if temp_file != input_file:
                os.unlink(temp_file)
            
            return {
                'input_file': str(input_file),
                'output_file': str(output_file),
                'analysis': analysis,
                'quality_check': quality_check,
                'standardization_applied': True
            }
            
        except Exception as e:
            return {'error': f'Standardization failed: {e}'}
    
    def _convert_format(self, input_file: Path) -> Optional[Path]:
        """Convert audio to standard format."""
        try:
            # Create temporary file
            temp_file = input_file.with_suffix('.temp.wav')
            
            cmd = [
                'ffmpeg', '-i', str(input_file),
                '-ar', str(self.target_sample_rate),
                '-ac', str(self.target_channels),
                '-sample_fmt', 's16',  # 16-bit
                '-y',  # Overwrite
                str(temp_file)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                return temp_file
            else:
                print(f"FFmpeg error: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"Format conversion error: {e}")
            return None
    
    def _analyze_audio(self, audio_file: Path) -> Dict:
        """Analyze audio characteristics."""
        try:
            sample_rate, audio_data = wavfile.read(audio_file)
            
            # Convert to float for analysis
            if audio_data.dtype == np.int16:
                audio_data = audio_data.astype(np.float32) / 32768.0
            elif audio_data.dtype == np.int32:
                audio_data = audio_data.astype(np.float32) / 2147483648.0
            
            # Calculate metrics
            rms = np.sqrt(np.mean(audio_data**2))
            peak = np.max(np.abs(audio_data))
            dynamic_range = 20 * np.log10(peak / (rms + 1e-10))
            
            # Calculate LUFS (Loudness Units relative to Full Scale)
            lufs = self._calculate_lufs(audio_data, sample_rate)
            
            # Calculate spectral characteristics
            spectral_centroid = self._calculate_spectral_centroid(audio_data, sample_rate)
            zero_crossing_rate = self._calculate_zcr(audio_data)
            
            return {
                'sample_rate': int(sample_rate),
                'channels': 1 if len(audio_data.shape) == 1 else audio_data.shape[1],
                'duration': len(audio_data) / sample_rate,
                'rms': float(rms),
                'peak': float(peak),
                'dynamic_range': float(dynamic_range),
                'lufs': float(lufs),
                'spectral_centroid': float(spectral_centroid),
                'zero_crossing_rate': float(zero_crossing_rate)
            }
            
        except Exception as e:
            return {'error': f'Audio analysis failed: {e}'}
    
    def _calculate_lufs(self, audio_data: np.ndarray, sample_rate: int) -> float:
        """Calculate LUFS (simplified implementation)."""
        # Simplified LUFS calculation
        # In practice, you'd use a proper LUFS library like pyloudnorm
        try:
            import pyloudnorm as pyln
            meter = pyln.Meter(sample_rate)
            lufs = meter.integrated_loudness(audio_data)
            return float(lufs)
        except ImportError:
            # Fallback to RMS-based approximation
            rms = np.sqrt(np.mean(audio_data**2))
            lufs = 20 * np.log10(rms + 1e-10)
            return float(lufs)
        except Exception:
            return -23.0  # Default value
    
    def _calculate_spectral_centroid(self, audio_data: np.ndarray, sample_rate: int) -> float:
        """Calculate spectral centroid."""
        try:
            fft = np.fft.fft(audio_data)
            freqs = np.fft.fftfreq(len(fft), 1/sample_rate)
            magnitude = np.abs(fft)
            
            # Only use positive frequencies
            positive_freqs = freqs[:len(freqs)//2]
            positive_magnitude = magnitude[:len(magnitude)//2]
            
            if np.sum(positive_magnitude) > 0:
                centroid = np.sum(positive_freqs * positive_magnitude) / np.sum(positive_magnitude)
                return float(centroid)
            else:
                return 0.0
        except Exception:
            return 0.0
    
    def _calculate_zcr(self, audio_data: np.ndarray) -> float:
        """Calculate zero crossing rate."""
        zero_crossings = np.sum(np.diff(np.sign(audio_data)) != 0)
        return zero_crossings / len(audio_data)
    
    def _apply_standardization(self, input_file: Path, output_file: Path, analysis: Dict) -> Path:
        """Apply audio standardization."""
        try:
            # Build FFmpeg command for standardization
            cmd = ['ffmpeg', '-i', str(input_file)]
            
            # Audio filters
            filters = []
            
            # 1. Normalize loudness
            if self.normalization_method == 'lufs':
                target_lufs = self.target_lufs
                current_lufs = analysis.get('lufs', -23.0)
                gain_db = target_lufs - current_lufs
                if abs(gain_db) > 0.1:  # Only apply if significant difference
                    filters.append(f"volume={gain_db}dB")
            
            # 2. Peak limiting
            max_peak_db = self.max_peak
            filters.append(f"alimiter=level_in=1:level_out={10**(max_peak_db/20)}")
            
            # 3. Noise reduction (if enabled)
            if self.noise_reduction and self.noise_reduction_strength > 0:
                # Use FFmpeg's afftdn filter for noise reduction
                strength = self.noise_reduction_strength
                filters.append(f"afftdn=nr={strength}:nf={strength*0.8}")
            
            # 4. Speech enhancement (if enabled)
            if self.enhance_speech and self.enhancement_strength > 0:
                # Use FFmpeg's acompressor for speech enhancement
                strength = self.enhancement_strength
                filters.append(f"acompressor=threshold=0.1:ratio=3:attack=5:release=50")
            
            # Apply filters
            if filters:
                cmd.extend(['-af', ','.join(filters)])
            
            # Output settings
            cmd.extend([
                '-ar', str(self.target_sample_rate),
                '-ac', str(self.target_channels),
                '-sample_fmt', 's16',
                '-y',  # Overwrite
                str(output_file)
            ])
            
            # Execute
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                return output_file
            else:
                print(f"Standardization error: {result.stderr}")
                return input_file
                
        except Exception as e:
            print(f"Standardization error: {e}")
            return input_file
    
    def _quality_check(self, audio_file: Path) -> Dict:
        """Check quality of standardized audio."""
        try:
            sample_rate, audio_data = wavfile.read(audio_file)
            
            # Convert to float
            if audio_data.dtype == np.int16:
                audio_data = audio_data.astype(np.float32) / 32768.0
            
            # Quality metrics
            rms = np.sqrt(np.mean(audio_data**2))
            peak = np.max(np.abs(audio_data))
            dynamic_range = 20 * np.log10(peak / (rms + 1e-10))
            
            # Check if standardization was successful
            sample_rate_ok = sample_rate == self.target_sample_rate
            channels_ok = len(audio_data.shape) == 1  # Mono
            level_ok = -30 < 20 * np.log10(rms + 1e-10) < -6  # Reasonable level
            peak_ok = peak < 0.95  # Not clipping
            
            quality_score = sum([sample_rate_ok, channels_ok, level_ok, peak_ok]) / 4
            
            return {
                'sample_rate_correct': sample_rate_ok,
                'channels_correct': channels_ok,
                'level_appropriate': level_ok,
                'no_clipping': peak_ok,
                'quality_score': float(quality_score),
                'rms': float(rms),
                'peak': float(peak),
                'dynamic_range': float(dynamic_range)
            }
            
        except Exception as e:
            return {'error': f'Quality check failed: {e}'}
    
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
        
        for i, audio_file in enumerate(audio_files, 1):
            print(f"Processing {i}/{len(audio_files)}: {audio_file.name}")
            
            # Create output filename
            output_file = output_dir / f"{audio_file.stem}_standardized.wav"
            
            # Standardize
            result = self.standardize_audio_file(audio_file, output_file)
            results['files'].append(result)
            
            if 'error' in result:
                print(f"  ❌ Error: {result['error']}")
                results['errors'] += 1
            else:
                quality_score = result.get('quality_check', {}).get('quality_score', 0)
                print(f"  ✅ Quality score: {quality_score:.2f}")
                results['successful'] += 1
        
        return results

def main():
    """Main function."""
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python audio_standardizer.py <input_file_or_dir> <output_file_or_dir>")
        sys.exit(1)
    
    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    
    standardizer = AudioStandardizer()
    
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
