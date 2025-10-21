#!/usr/bin/env python3
"""
Robust Audio Quality Analyzer using scipy and numpy

This script uses scipy and numpy for professional audio analysis:
- High background noise levels
- Multiple speakers talking simultaneously
- Crowded/chaotic audio environments
- Poor audio quality that might affect accent analysis

Based on your feedback:
- Nevada-1: Good quality (should be low/medium noise)
- Oklahoma-9: Unacceptably noisy (should be high/very_high noise)
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


class RobustAudioAnalyzer:
    """Robust audio quality analyzer using scipy and numpy."""
    
    def __init__(self):
        # Calibrated thresholds based on your feedback
        self.thresholds = {
            # RMS energy thresholds (dB)
            'very_high_noise_rms': -5,      # Very loud/overloaded
            'high_noise_rms': -15,          # Loud
            'medium_noise_rms': -25,       # Moderate
            
            # Dynamic range thresholds (dB)
            'very_high_noise_dynamic_range': 5,    # Very compressed
            'high_noise_dynamic_range': 15,       # Compressed
            'medium_noise_dynamic_range': 25,      # Moderate
            
            # Spectral analysis thresholds
            'high_frequency_noise_threshold': 0.4,  # High freq content ratio
            'spectral_centroid_speech_min': 500,    # Hz - good for speech
            'spectral_centroid_speech_max': 3000,   # Hz - good for speech
            
            # Silence analysis
            'multiple_speakers_silence_ratio': 0.4,  # Short silence ratio
            'background_noise_silence_ratio': 0.1,   # Very little silence
        }
    
    def analyze_audio_file(self, audio_file: Path) -> Dict:
        """Analyze a single audio file for quality and noise."""
        try:
            # Load audio data using ffmpeg
            audio_data, sample_rate = self._load_audio_data(audio_file)
            
            if audio_data is None:
                return {
                    'file': str(audio_file),
                    'error': 'Could not load audio data',
                    'noise_level': 'unknown',
                    'quality_score': 0,
                    'recommendation': 'ERROR - Cannot load audio'
                }
            
            # Basic audio properties
            basic_info = self._get_basic_info(audio_data, sample_rate, audio_file)
            
            # Analyze audio characteristics
            audio_analysis = self._analyze_audio_characteristics(audio_data, sample_rate)
            
            # Detect multiple speakers
            speaker_analysis = self._detect_multiple_speakers(audio_data, sample_rate)
            
            # Calculate quality score
            quality_score = self._calculate_quality_score(basic_info, audio_analysis, speaker_analysis)
            
            # Determine noise level
            noise_level = self._determine_noise_level(audio_analysis, speaker_analysis, quality_score)
            
            # Get recommendation
            recommendation = self._get_recommendation(noise_level, quality_score)
            
            return {
                'file': str(audio_file),
                'basic_info': basic_info,
                'audio_analysis': audio_analysis,
                'speaker_analysis': speaker_analysis,
                'quality_score': quality_score,
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
            # Use ffmpeg to convert to raw audio data
            cmd = [
                'ffmpeg',
                '-i', str(audio_file),
                '-f', 'f32le',  # 32-bit float little-endian
                '-ac', '1',     # Mono
                '-ar', '22050', # 22kHz sample rate
                '-'
            ]
            
            result = subprocess.run(cmd, capture_output=True, timeout=30)
            
            if result.returncode != 0:
                return None, None
            
            # Convert bytes to numpy array
            audio_data = np.frombuffer(result.stdout, dtype=np.float32)
            
            return audio_data, 22050
            
        except Exception as e:
            return None, None
    
    def _get_basic_info(self, audio_data: np.ndarray, sample_rate: int, audio_file: Path) -> Dict:
        """Get basic audio information."""
        duration = len(audio_data) / sample_rate
        file_size = audio_file.stat().st_size
        
        return {
            'sample_rate': sample_rate,
            'duration': duration,
            'file_size': file_size,
            'samples': len(audio_data)
        }
    
    def _analyze_audio_characteristics(self, audio_data: np.ndarray, sample_rate: int) -> Dict:
        """Analyze audio characteristics using scipy and numpy."""
        # RMS energy (loudness)
        rms_energy = np.sqrt(np.mean(audio_data**2))
        rms_db = 20 * np.log10(rms_energy) if rms_energy > 0 else -100
        
        # Peak level
        peak_level = np.max(np.abs(audio_data))
        peak_db = 20 * np.log10(peak_level) if peak_level > 0 else -100
        
        # Dynamic range
        dynamic_range = peak_db - rms_db
        
        # Zero crossing rate (indicates noise/chaos)
        zero_crossings = np.sum(np.diff(np.sign(audio_data)) != 0)
        zero_crossing_rate = zero_crossings / len(audio_data) if len(audio_data) > 0 else 0
        
        # Spectral analysis
        spectral_analysis = self._analyze_spectrum(audio_data, sample_rate)
        
        return {
            'rms_energy': rms_energy,
            'rms_db': rms_db,
            'peak_level': peak_level,
            'peak_db': peak_db,
            'dynamic_range': dynamic_range,
            'zero_crossing_rate': zero_crossing_rate,
            **spectral_analysis
        }
    
    def _analyze_spectrum(self, audio_data: np.ndarray, sample_rate: int) -> Dict:
        """Analyze frequency spectrum using FFT."""
        try:
            # Apply window function to reduce spectral leakage
            windowed_data = audio_data * signal.windows.hann(len(audio_data))
            
            # Compute FFT
            fft_data = fft(windowed_data)
            freqs = fftfreq(len(audio_data), 1/sample_rate)
            
            # Get positive frequencies only
            positive_mask = freqs >= 0
            positive_freqs = freqs[positive_mask]
            positive_fft = np.abs(fft_data[positive_mask])
            
            # Spectral centroid (center of mass of spectrum)
            if np.sum(positive_fft) > 0:
                spectral_centroid = np.sum(positive_freqs * positive_fft) / np.sum(positive_fft)
            else:
                spectral_centroid = 0
            
            # High frequency content ratio
            nyquist = sample_rate / 2
            high_freq_mask = positive_freqs > (nyquist * 0.3)  # Above 30% of Nyquist
            high_freq_ratio = np.sum(positive_fft[high_freq_mask]) / np.sum(positive_fft) if np.sum(positive_fft) > 0 else 0
            
            # Spectral rolloff (frequency below which 85% of energy lies)
            cumulative_energy = np.cumsum(positive_fft)
            total_energy = cumulative_energy[-1]
            rolloff_threshold = 0.85 * total_energy
            rolloff_idx = np.where(cumulative_energy >= rolloff_threshold)[0]
            spectral_rolloff = positive_freqs[rolloff_idx[0]] if len(rolloff_idx) > 0 else 0
            
            # Spectral bandwidth
            if spectral_centroid > 0 and np.sum(positive_fft) > 0:
                spectral_bandwidth = np.sqrt(np.sum(((positive_freqs - spectral_centroid)**2) * positive_fft) / np.sum(positive_fft))
            else:
                spectral_bandwidth = 0
            
            return {
                'spectral_centroid': spectral_centroid,
                'high_frequency_ratio': high_freq_ratio,
                'spectral_rolloff': spectral_rolloff,
                'spectral_bandwidth': spectral_bandwidth
            }
            
        except Exception as e:
            return {
                'spectral_centroid': 0,
                'high_frequency_ratio': 0,
                'spectral_rolloff': 0,
                'spectral_bandwidth': 0,
                'error': str(e)
            }
    
    def _detect_multiple_speakers(self, audio_data: np.ndarray, sample_rate: int) -> Dict:
        """Detect multiple speakers using silence analysis."""
        try:
            # Convert to dB for silence detection
            audio_db = 20 * np.log10(np.abs(audio_data) + 1e-10)
            
            # Silence threshold
            silence_threshold = -40  # dB
            min_silence_samples = int(0.1 * sample_rate)  # 100ms minimum
            
            # Find silence periods
            silence_mask = audio_db < silence_threshold
            
            # Find continuous silence periods
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
            
            # Close final silence period
            if in_silence:
                silence_duration = len(audio_data) - silence_start
                if silence_duration >= min_silence_samples:
                    silence_periods.append((silence_start, len(audio_data)))
            
            # Analyze silence patterns
            total_silence_samples = sum(end - start for start, end in silence_periods)
            silence_ratio = total_silence_samples / len(audio_data) if len(audio_data) > 0 else 0
            
            # Count short silence periods (indicates multiple speakers)
            short_silence_periods = sum(1 for start, end in silence_periods 
                                      if (end - start) < int(0.5 * sample_rate))  # Less than 500ms
            
            # Multiple speakers indicators
            multiple_speakers_ratio = short_silence_periods / max(len(silence_periods), 1)
            multiple_speakers_detected = multiple_speakers_ratio > self.thresholds['multiple_speakers_silence_ratio']
            
            # Background noise indicator (very little silence)
            background_noise_detected = silence_ratio < self.thresholds['background_noise_silence_ratio']
            
            return {
                'silence_periods': len(silence_periods),
                'silence_ratio': silence_ratio,
                'short_silence_periods': short_silence_periods,
                'multiple_speakers_ratio': multiple_speakers_ratio,
                'multiple_speakers_detected': multiple_speakers_detected,
                'background_noise_detected': background_noise_detected
            }
            
        except Exception as e:
            return {
                'silence_periods': 0,
                'silence_ratio': 0,
                'short_silence_periods': 0,
                'multiple_speakers_ratio': 0,
                'multiple_speakers_detected': False,
                'background_noise_detected': False,
                'error': str(e)
            }
    
    def _calculate_quality_score(self, basic_info: Dict, audio_analysis: Dict, speaker_analysis: Dict) -> float:
        """Calculate overall quality score (0-100)."""
        score = 0
        
        # Audio quality factors
        rms_db = audio_analysis.get('rms_db', -100)
        dynamic_range = audio_analysis.get('dynamic_range', 0)
        zero_crossing_rate = audio_analysis.get('zero_crossing_rate', 0)
        spectral_centroid = audio_analysis.get('spectral_centroid', 0)
        
        # RMS energy scoring (prefer moderate levels for speech)
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
        
        # Zero crossing rate scoring (lower is better for speech)
        if zero_crossing_rate < 0.05:
            score += 20
        elif zero_crossing_rate < 0.1:
            score += 15
        elif zero_crossing_rate < 0.2:
            score += 10
        else:
            score += 5
        
        # Spectral quality scoring (prefer speech-like frequencies)
        if (self.thresholds['spectral_centroid_speech_min'] <= spectral_centroid <= 
            self.thresholds['spectral_centroid_speech_max']):
            score += 20
        elif 200 <= spectral_centroid <= 5000:
            score += 15
        else:
            score += 10
        
        # File quality factors
        file_size = basic_info.get('file_size', 0)
        if file_size >= 50000:
            score += 10
        elif file_size >= 20000:
            score += 8
        elif file_size >= 10000:
            score += 5
        
        # Penalties for problems
        if speaker_analysis.get('multiple_speakers_detected', False):
            score -= 15
        if speaker_analysis.get('background_noise_detected', False):
            score -= 10
        if audio_analysis.get('high_frequency_ratio', 0) > self.thresholds['high_frequency_noise_threshold']:
            score -= 10
        
        return max(0, min(100, score))
    
    def _determine_noise_level(self, audio_analysis: Dict, speaker_analysis: Dict, quality_score: float) -> str:
        """Determine noise level using robust criteria."""
        rms_db = audio_analysis.get('rms_db', -100)
        dynamic_range = audio_analysis.get('dynamic_range', 0)
        zero_crossing_rate = audio_analysis.get('zero_crossing_rate', 0)
        multiple_speakers = speaker_analysis.get('multiple_speakers_detected', False)
        background_noise = speaker_analysis.get('background_noise_detected', False)
        
        # Count noise indicators
        very_high_indicators = 0
        high_indicators = 0
        
        # Very high noise indicators
        if rms_db > self.thresholds['very_high_noise_rms']:
            very_high_indicators += 1
        if dynamic_range < self.thresholds['very_high_noise_dynamic_range']:
            very_high_indicators += 1
        if zero_crossing_rate > 0.3:  # Very chaotic
            very_high_indicators += 1
        if multiple_speakers and background_noise:
            very_high_indicators += 1
        if quality_score < 30:
            very_high_indicators += 1
        
        if very_high_indicators >= 2:
            return 'very_high'
        
        # High noise indicators
        if rms_db > self.thresholds['high_noise_rms']:
            high_indicators += 1
        if dynamic_range < self.thresholds['high_noise_dynamic_range']:
            high_indicators += 1
        if zero_crossing_rate > 0.2:
            high_indicators += 1
        if multiple_speakers:
            high_indicators += 1
        if quality_score < 50:
            high_indicators += 1
        
        if high_indicators >= 2:
            return 'high'
        
        # Medium noise indicators
        if (rms_db > self.thresholds['medium_noise_rms'] or 
            dynamic_range < self.thresholds['medium_noise_dynamic_range'] or
            quality_score < 70):
            return 'medium'
        
        # Low noise: Good quality
        return 'low'
    
    def _get_recommendation(self, noise_level: str, quality_score: float) -> str:
        """Get recommendation based on noise level."""
        if noise_level == 'very_high' or quality_score < 30:
            return 'EXCLUDE - Too noisy for accent analysis'
        elif noise_level == 'high' or quality_score < 50:
            return 'REVIEW - High noise, may affect analysis'
        elif noise_level == 'medium' or quality_score < 70:
            return 'ACCEPTABLE - Moderate noise, usable with caution'
        else:
            return 'GOOD - Low noise, suitable for analysis'
    
    def batch_analyze(self, audio_dir: Path, pattern: str = "*.mp3") -> Dict:
        """Analyze all audio files in a directory."""
        audio_files = list(audio_dir.rglob(pattern))
        
        results = {
            'total_files': len(audio_files),
            'analyzed': 0,
            'errors': 0,
            'noise_levels': {
                'very_high': 0,
                'high': 0,
                'medium': 0,
                'low': 0,
                'unknown': 0
            },
            'recommendations': {
                'exclude': 0,
                'review': 0,
                'acceptable': 0,
                'good': 0
            },
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
                
                # Check for multiple speakers
                if analysis.get('speaker_analysis', {}).get('multiple_speakers_detected', False):
                    results['multiple_speakers'] += 1
                
                # Count recommendations
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
    parser = argparse.ArgumentParser(description='Robust audio quality analysis using scipy')
    parser.add_argument('audio_dir', help='Directory containing audio files')
    parser.add_argument('-o', '--output', help='Output file for results', default='robust_audio_analysis.json')
    parser.add_argument('--pattern', help='File pattern to match', default='*.mp3')
    
    args = parser.parse_args()
    
    analyzer = RobustAudioAnalyzer()
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
    print(f"ROBUST AUDIO QUALITY ANALYSIS COMPLETE")
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
            multi_speaker = file_result.get('speaker_analysis', {}).get('multiple_speakers_detected', False)
            
            status = "✅" if noise_level in ['low', 'medium'] else "⚠️" if noise_level == 'high' else "❌"
            print(f"  {status} {filename}: {noise_level} noise, quality {quality_score:.1f}" + 
                  (" (multiple speakers)" if multi_speaker else ""))
    
    print(f"\nResults saved to: {output_file}")


if __name__ == "__main__":
    main()
