#!/usr/bin/env python3
"""
Professional Audio Quality Analyzer using pydub

This script uses pydub (a professional audio library) to detect:
- High background noise levels
- Multiple speakers talking simultaneously
- Crowded/chaotic audio environments
- Poor audio quality that might affect accent analysis

Based on your feedback:
- Nevada-1: Good quality (should be low/medium noise)
- Oklahoma-9: Unacceptably noisy (should be high/very_high noise)
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List
import argparse
from pydub import AudioSegment
from pydub.utils import which
import warnings

# Suppress pydub warnings
warnings.filterwarnings('ignore')


class ProfessionalAudioAnalyzer:
    """Professional audio quality analyzer using pydub."""
    
    def __init__(self):
        # Calibrated thresholds based on your feedback
        self.thresholds = {
            # RMS energy thresholds (dB)
            'very_high_noise_rms': -10,     # Very loud/overloaded
            'high_noise_rms': -20,          # Loud
            'medium_noise_rms': -30,       # Moderate
            
            # Dynamic range thresholds (dB)
            'very_high_noise_dynamic_range': 10,   # Very compressed
            'high_noise_dynamic_range': 20,        # Compressed
            'medium_noise_dynamic_range': 30,      # Moderate
            
            # Spectral analysis thresholds
            'high_frequency_noise_threshold': 0.3,  # High freq content ratio
            'spectral_centroid_threshold': 2000,   # Hz
            
            # Silence analysis
            'multiple_speakers_silence_ratio': 0.3,  # Short silence ratio
            'background_noise_silence_ratio': 0.05,  # Very little silence
        }
    
    def analyze_audio_file(self, audio_file: Path) -> Dict:
        """Analyze a single audio file for quality and noise."""
        try:
            # Load audio file with pydub
            audio = AudioSegment.from_file(str(audio_file))
            
            # Basic audio properties
            basic_info = self._get_basic_info(audio, audio_file)
            
            # Analyze audio characteristics
            audio_analysis = self._analyze_audio_characteristics(audio)
            
            # Detect multiple speakers
            speaker_analysis = self._detect_multiple_speakers(audio)
            
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
    
    def _get_basic_info(self, audio: AudioSegment, audio_file: Path) -> Dict:
        """Get basic audio information."""
        return {
            'sample_rate': audio.frame_rate,
            'channels': audio.channels,
            'duration': len(audio) / 1000.0,  # Convert to seconds
            'bitrate': audio.frame_rate * audio.sample_width * 8 * audio.channels,
            'file_size': audio_file.stat().st_size,
            'format': audio_file.suffix.lower()
        }
    
    def _analyze_audio_characteristics(self, audio: AudioSegment) -> Dict:
        """Analyze audio characteristics using pydub."""
        # Convert to numpy array for analysis
        samples = np.array(audio.get_array_of_samples())
        if audio.channels == 2:
            samples = samples.reshape((-1, 2))
            samples = samples.mean(axis=1)  # Convert to mono
        
        # Normalize samples
        if len(samples) > 0:
            samples = samples.astype(np.float32)
            if samples.max() != 0:
                samples = samples / samples.max()
        
        # RMS energy (loudness)
        rms_energy = np.sqrt(np.mean(samples**2))
        rms_db = 20 * np.log10(rms_energy) if rms_energy > 0 else -100
        
        # Peak level
        peak_level = np.max(np.abs(samples))
        peak_db = 20 * np.log10(peak_level) if peak_level > 0 else -100
        
        # Dynamic range
        dynamic_range = peak_db - rms_db
        
        # Spectral analysis
        spectral_analysis = self._analyze_spectrum(samples, audio.frame_rate)
        
        # Zero crossing rate (indicates noise/chaos)
        zero_crossings = np.sum(np.diff(np.sign(samples)) != 0)
        zero_crossing_rate = zero_crossings / len(samples) if len(samples) > 0 else 0
        
        return {
            'rms_energy': rms_energy,
            'rms_db': rms_db,
            'peak_level': peak_level,
            'peak_db': peak_db,
            'dynamic_range': dynamic_range,
            'zero_crossing_rate': zero_crossing_rate,
            **spectral_analysis
        }
    
    def _analyze_spectrum(self, samples: np.ndarray, sample_rate: int) -> Dict:
        """Analyze frequency spectrum."""
        try:
            # Simple spectral analysis using FFT
            fft = np.fft.fft(samples)
            freqs = np.fft.fftfreq(len(samples), 1/sample_rate)
            
            # Get positive frequencies only
            positive_freqs = freqs[:len(freqs)//2]
            positive_fft = np.abs(fft[:len(fft)//2])
            
            # Spectral centroid (center of mass of spectrum)
            if np.sum(positive_fft) > 0:
                spectral_centroid = np.sum(positive_freqs * positive_fft) / np.sum(positive_fft)
            else:
                spectral_centroid = 0
            
            # High frequency content ratio
            nyquist = sample_rate / 2
            high_freq_mask = positive_freqs > (nyquist * 0.5)  # Above half Nyquist
            high_freq_ratio = np.sum(positive_fft[high_freq_mask]) / np.sum(positive_fft) if np.sum(positive_fft) > 0 else 0
            
            # Spectral rolloff (frequency below which 85% of energy lies)
            cumulative_energy = np.cumsum(positive_fft)
            total_energy = cumulative_energy[-1]
            rolloff_threshold = 0.85 * total_energy
            spectral_rolloff_idx = np.where(cumulative_energy >= rolloff_threshold)[0]
            spectral_rolloff = positive_freqs[spectral_rolloff_idx[0]] if len(spectral_rolloff_idx) > 0 else 0
            
            return {
                'spectral_centroid': spectral_centroid,
                'high_frequency_ratio': high_freq_ratio,
                'spectral_rolloff': spectral_rolloff,
                'spectral_bandwidth': np.sum(positive_fft) / len(positive_fft) if len(positive_fft) > 0 else 0
            }
            
        except Exception as e:
            return {
                'spectral_centroid': 0,
                'high_frequency_ratio': 0,
                'spectral_rolloff': 0,
                'spectral_bandwidth': 0,
                'error': str(e)
            }
    
    def _detect_multiple_speakers(self, audio: AudioSegment) -> Dict:
        """Detect multiple speakers using silence analysis."""
        try:
            # Detect silence periods
            silence_threshold = -40  # dB
            min_silence_len = 100   # ms
            
            # Find silence periods
            silence_periods = []
            current_silence_start = None
            
            # Analyze in chunks
            chunk_size = 100  # ms
            for i in range(0, len(audio), chunk_size):
                chunk = audio[i:i + chunk_size]
                chunk_db = chunk.dBFS
                
                if chunk_db < silence_threshold:
                    if current_silence_start is None:
                        current_silence_start = i
                else:
                    if current_silence_start is not None:
                        silence_duration = i - current_silence_start
                        if silence_duration >= min_silence_len:
                            silence_periods.append((current_silence_start, i))
                        current_silence_start = None
            
            # Close final silence period
            if current_silence_start is not None:
                silence_duration = len(audio) - current_silence_start
                if silence_duration >= min_silence_len:
                    silence_periods.append((current_silence_start, len(audio)))
            
            # Analyze silence patterns
            total_silence_time = sum(end - start for start, end in silence_periods)
            silence_ratio = total_silence_time / len(audio) if len(audio) > 0 else 0
            
            # Count short silence periods (indicates multiple speakers)
            short_silence_periods = sum(1 for start, end in silence_periods 
                                      if (end - start) < 500)  # Less than 500ms
            
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
        
        # RMS energy scoring (prefer moderate levels)
        if -30 <= rms_db <= -10:
            score += 25
        elif -40 <= rms_db <= -5:
            score += 20
        elif -50 <= rms_db <= 0:
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
        
        # Spectral quality scoring
        if 1000 <= spectral_centroid <= 3000:  # Good for speech
            score += 20
        elif 500 <= spectral_centroid <= 4000:
            score += 15
        else:
            score += 10
        
        # File quality factors
        bitrate = basic_info.get('bitrate', 0)
        if bitrate >= 128000:
            score += 10
        elif bitrate >= 64000:
            score += 8
        elif bitrate >= 32000:
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
        """Determine noise level using professional criteria."""
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
    parser = argparse.ArgumentParser(description='Professional audio quality analysis using pydub')
    parser.add_argument('audio_dir', help='Directory containing audio files')
    parser.add_argument('-o', '--output', help='Output file for results', default='professional_audio_analysis.json')
    parser.add_argument('--pattern', help='File pattern to match', default='*.mp3')
    
    args = parser.parse_args()
    
    analyzer = ProfessionalAudioAnalyzer()
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
    print(f"PROFESSIONAL AUDIO QUALITY ANALYSIS COMPLETE")
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
