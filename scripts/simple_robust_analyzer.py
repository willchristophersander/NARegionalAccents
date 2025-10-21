#!/usr/bin/env python3
"""
Simple Robust Audio Analyzer

A simplified version that handles JSON serialization properly and focuses on
the key metrics that actually work for noise detection.
"""

import subprocess
import json
import numpy as np
from pathlib import Path
from typing import Dict, List
import argparse
from scipy import signal
from scipy.fft import fft, fftfreq
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')


class SimpleRobustAnalyzer:
    """Simple robust audio analyzer with proper JSON serialization."""
    
    def __init__(self):
        # Calibrated thresholds based on your feedback
        # Montana-2 and North-Dakota-1 are good quality, so being less aggressive
        self.thresholds = {
            'very_high_noise_rms': -5,      # Very loud
            'high_noise_rms': -10,          # Loud (less aggressive)
            'medium_noise_rms': -20,       # Moderate (less aggressive)
            
            'very_high_dynamic_range': 5,   # Very compressed
            'high_dynamic_range': 10,      # Compressed (less aggressive)
            'medium_dynamic_range': 20,    # Moderate (less aggressive)
            
            'multiple_speakers_ratio': 0.4,
            'background_noise_ratio': 0.1,
        }
    
    def analyze_audio_file(self, audio_file: Path) -> Dict:
        """Analyze a single audio file for quality and noise."""
        try:
            # Load audio data
            audio_data, sample_rate = self._load_audio_data(audio_file)
            
            if audio_data is None:
                return {
                    'file': str(audio_file),
                    'error': 'Could not load audio data',
                    'noise_level': 'unknown',
                    'quality_score': 0,
                    'recommendation': 'ERROR - Cannot load audio'
                }
            
            # Basic info
            duration = len(audio_data) / sample_rate
            file_size = audio_file.stat().st_size
            
            # Audio analysis
            rms_energy = np.sqrt(np.mean(audio_data**2))
            rms_db = float(20 * np.log10(rms_energy) if rms_energy > 0 else -100)
            
            peak_level = np.max(np.abs(audio_data))
            peak_db = float(20 * np.log10(peak_level) if peak_level > 0 else -100)
            
            dynamic_range = float(peak_db - rms_db)
            
            # Zero crossing rate
            zero_crossings = np.sum(np.diff(np.sign(audio_data)) != 0)
            zero_crossing_rate = float(zero_crossings / len(audio_data) if len(audio_data) > 0 else 0)
            
            # Silence analysis
            silence_analysis = self._analyze_silence(audio_data, sample_rate)
            
            # Calculate quality score
            quality_score = self._calculate_quality_score(
                rms_db, dynamic_range, zero_crossing_rate, 
                silence_analysis, file_size, duration
            )
            
            # Determine noise level
            noise_level = self._determine_noise_level(
                rms_db, dynamic_range, zero_crossing_rate,
                silence_analysis, quality_score
            )
            
            # Get recommendation
            recommendation = self._get_recommendation(noise_level, quality_score)
            
            return {
                'file': str(audio_file),
                'basic_info': {
                    'sample_rate': int(sample_rate),
                    'duration': float(duration),
                    'file_size': int(file_size),
                    'samples': int(len(audio_data))
                },
                'audio_analysis': {
                    'rms_db': rms_db,
                    'peak_db': peak_db,
                    'dynamic_range': dynamic_range,
                    'zero_crossing_rate': zero_crossing_rate
                },
                'silence_analysis': silence_analysis,
                'quality_score': float(quality_score),
                'noise_level': noise_level,
                'recommendation': recommendation
            }
            
        except Exception as e:
            return {
                'file': str(audio_file),
                'error': str(e),
                'noise_level': 'unknown',
                'quality_score': 0,
                'recommendation': 'ERROR - Cannot analyze'
            }
    
    def _load_audio_data(self, audio_file: Path) -> tuple:
        """Load audio data using ffmpeg."""
        try:
            cmd = [
                'ffmpeg',
                '-i', str(audio_file),
                '-f', 'f32le',
                '-ac', '1',
                '-ar', '22050',
                '-'
            ]
            
            result = subprocess.run(cmd, capture_output=True, timeout=30)
            
            if result.returncode != 0:
                return None, None
            
            audio_data = np.frombuffer(result.stdout, dtype=np.float32)
            return audio_data, 22050
            
        except Exception as e:
            return None, None
    
    def _analyze_silence(self, audio_data: np.ndarray, sample_rate: int) -> Dict:
        """Analyze silence patterns."""
        try:
            # Convert to dB
            audio_db = 20 * np.log10(np.abs(audio_data) + 1e-10)
            
            # Silence threshold
            silence_threshold = -40
            min_silence_samples = int(0.1 * sample_rate)
            
            # Find silence periods
            silence_mask = audio_db < silence_threshold
            
            # Count silence periods
            silence_periods = []
            in_silence = False
            silence_start = 0
            
            for i, is_silent in enumerate(silence_mask):
                if is_silent and not in_silence:
                    silence_start = i
                    in_silence = True
                elif not is_silent and in_silence:
                    silence_duration = i - silence_start
                    if silence_duration >= min_silence_samples:
                        silence_periods.append((silence_start, i))
                    in_silence = False
            
            # Close final silence
            if in_silence:
                silence_duration = len(audio_data) - silence_start
                if silence_duration >= min_silence_samples:
                    silence_periods.append((silence_start, len(audio_data)))
            
            # Calculate ratios
            total_silence_samples = sum(end - start for start, end in silence_periods)
            silence_ratio = float(total_silence_samples / len(audio_data) if len(audio_data) > 0 else 0)
            
            # Short silence periods
            short_silence_periods = sum(1 for start, end in silence_periods 
                                      if (end - start) < int(0.5 * sample_rate))
            
            multiple_speakers_ratio = float(short_silence_periods / max(len(silence_periods), 1))
            multiple_speakers_detected = multiple_speakers_ratio > self.thresholds['multiple_speakers_ratio']
            background_noise_detected = silence_ratio < self.thresholds['background_noise_ratio']
            
            return {
                'silence_periods': int(len(silence_periods)),
                'silence_ratio': silence_ratio,
                'short_silence_periods': int(short_silence_periods),
                'multiple_speakers_ratio': multiple_speakers_ratio,
                'multiple_speakers_detected': bool(multiple_speakers_detected),
                'background_noise_detected': bool(background_noise_detected)
            }
            
        except Exception as e:
            return {
                'silence_periods': 0,
                'silence_ratio': 0.0,
                'short_silence_periods': 0,
                'multiple_speakers_ratio': 0.0,
                'multiple_speakers_detected': False,
                'background_noise_detected': False,
                'error': str(e)
            }
    
    def _calculate_quality_score(self, rms_db: float, dynamic_range: float, 
                               zero_crossing_rate: float, silence_analysis: Dict,
                               file_size: int, duration: float) -> float:
        """Calculate quality score."""
        score = 0
        
        # RMS energy scoring
        if -25 <= rms_db <= -10:
            score += 25
        elif -35 <= rms_db <= -5:
            score += 20
        elif -45 <= rms_db <= 0:
            score += 15
        else:
            score += 5
        
        # Dynamic range scoring
        if dynamic_range >= 30:
            score += 25
        elif dynamic_range >= 20:
            score += 20
        elif dynamic_range >= 10:
            score += 15
        else:
            score += 5
        
        # Zero crossing rate scoring
        if zero_crossing_rate < 0.05:
            score += 20
        elif zero_crossing_rate < 0.1:
            score += 15
        elif zero_crossing_rate < 0.2:
            score += 10
        else:
            score += 5
        
        # File size scoring
        if file_size >= 50000:
            score += 10
        elif file_size >= 20000:
            score += 8
        elif file_size >= 10000:
            score += 5
        
        # Duration scoring
        if 2 <= duration <= 5:
            score += 15
        elif 1 <= duration <= 10:
            score += 10
        else:
            score += 5
        
        # Penalties
        if silence_analysis.get('multiple_speakers_detected', False):
            score -= 15
        if silence_analysis.get('background_noise_detected', False):
            score -= 10
        
        return max(0, min(100, score))
    
    def _determine_noise_level(self, rms_db: float, dynamic_range: float,
                             zero_crossing_rate: float, silence_analysis: Dict,
                             quality_score: float) -> str:
        """Determine noise level."""
        # Count indicators
        very_high_indicators = 0
        high_indicators = 0
        
        # Very high noise
        if rms_db > self.thresholds['very_high_noise_rms']:
            very_high_indicators += 1
        if dynamic_range < self.thresholds['very_high_dynamic_range']:
            very_high_indicators += 1
        if zero_crossing_rate > 0.3:
            very_high_indicators += 1
        if (silence_analysis.get('multiple_speakers_detected', False) and 
            silence_analysis.get('background_noise_detected', False)):
            very_high_indicators += 1
        if quality_score < 30:
            very_high_indicators += 1
        
        if very_high_indicators >= 2:
            return 'very_high'
        
        # High noise
        if rms_db > self.thresholds['high_noise_rms']:
            high_indicators += 1
        if dynamic_range < self.thresholds['high_dynamic_range']:
            high_indicators += 1
        if zero_crossing_rate > 0.2:
            high_indicators += 1
        # Only flag as high noise if there's significant background noise
        # Multiple speakers alone is normal for accent analysis
        if (silence_analysis.get('background_noise_detected', False) and
            silence_analysis.get('background_noise_ratio', 0) > 0.2):
            high_indicators += 1
        if quality_score < 50:
            high_indicators += 1
        
        if high_indicators >= 2:
            return 'high'
        
        # Medium noise
        if (rms_db > self.thresholds['medium_noise_rms'] or 
            dynamic_range < self.thresholds['medium_dynamic_range'] or
            quality_score < 70):
            return 'medium'
        
        return 'low'
    
    def _get_recommendation(self, noise_level: str, quality_score: float) -> str:
        """Get recommendation."""
        if noise_level == 'very_high' or quality_score < 30:
            return 'EXCLUDE - Too noisy for accent analysis'
        elif noise_level == 'high' or quality_score < 50:
            return 'REVIEW - High noise, may affect analysis'
        elif noise_level == 'medium' or quality_score < 70:
            return 'ACCEPTABLE - Moderate noise, usable with caution'
        else:
            return 'GOOD - Low noise, suitable for analysis'
    
    def batch_analyze(self, audio_dir: Path, pattern: str = "*.mp3") -> Dict:
        """Analyze all audio files."""
        audio_files = list(audio_dir.rglob(pattern))
        
        results = {
            'total_files': len(audio_files),
            'analyzed': 0,
            'errors': 0,
            'noise_levels': {'very_high': 0, 'high': 0, 'medium': 0, 'low': 0, 'unknown': 0},
            'recommendations': {'exclude': 0, 'review': 0, 'acceptable': 0, 'good': 0},
            'multiple_speakers': 0,
            'files': []
        }
        
        print(f"Analyzing {len(audio_files)} audio files...")
        
        for i, audio_file in enumerate(audio_files):
            print(f"Analyzing {i+1}/{len(audio_files)}: {audio_file.name}")
            
            analysis = self.analyze_audio_file(audio_file)
            results['files'].append(analysis)
            
            if 'error' in analysis:
                results['errors'] += 1
                results['noise_levels']['unknown'] += 1
            else:
                results['analyzed'] += 1
                noise_level = analysis.get('noise_level', 'unknown')
                results['noise_levels'][noise_level] += 1
                
                if analysis.get('silence_analysis', {}).get('multiple_speakers_detected', False):
                    results['multiple_speakers'] += 1
                
                recommendation = analysis.get('recommendation', '')
                if 'EXCLUDE' in recommendation:
                    results['recommendations']['exclude'] += 1
                elif 'REVIEW' in recommendation:
                    results['recommendations']['review'] += 1
                elif 'ACCEPTABLE' in recommendation:
                    results['recommendations']['acceptable'] += 1
                elif 'GOOD' in recommendation:
                    results['recommendations']['good'] += 1
        
        return results


def main():
    parser = argparse.ArgumentParser(description='Simple robust audio analysis')
    parser.add_argument('audio_dir', help='Directory containing audio files')
    parser.add_argument('-o', '--output', help='Output file for results', default='simple_robust_analysis.json')
    parser.add_argument('--pattern', help='File pattern to match', default='*.mp3')
    
    args = parser.parse_args()
    
    analyzer = SimpleRobustAnalyzer()
    audio_dir = Path(args.audio_dir)
    
    if not audio_dir.exists():
        print(f"Directory not found: {audio_dir}")
        return
    
    # Analyze all audio files
    results = analyzer.batch_analyze(audio_dir, args.pattern)
    
    # Save results
    output_file = Path(args.output)
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"SIMPLE ROBUST AUDIO ANALYSIS COMPLETE")
    print(f"{'='*60}")
    print(f"Total files: {results['total_files']}")
    print(f"Successfully analyzed: {results['analyzed']}")
    print(f"Errors: {results['errors']}")
    print(f"Multiple speakers detected: {results['multiple_speakers']}")
    
    print(f"\nNoise Levels:")
    for level, count in results['noise_levels'].items():
        print(f"  {level}: {count}")
    
    print(f"\nRecommendations:")
    for rec, count in results['recommendations'].items():
        print(f"  {rec}: {count}")
    
    # Show individual file results
    print(f"\nIndividual File Analysis:")
    for file_result in results['files']:
        if 'error' not in file_result:
            filename = Path(file_result['file']).name
            noise_level = file_result.get('noise_level', 'unknown')
            quality_score = file_result.get('quality_score', 0)
            multi_speaker = file_result.get('silence_analysis', {}).get('multiple_speakers_detected', False)
            
            status = "✅" if noise_level in ['low', 'medium'] else "⚠️" if noise_level == 'high' else "❌"
            print(f"  {status} {filename}: {noise_level} noise, quality {quality_score:.1f}" + 
                  (" (multiple speakers)" if multi_speaker else ""))
    
    print(f"\nResults saved to: {output_file}")


if __name__ == "__main__":
    main()
