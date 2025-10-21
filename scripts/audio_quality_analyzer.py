#!/usr/bin/env python3
"""
Audio Quality Analyzer using librosa

This script uses librosa (a professional audio analysis library) to detect:
- High background noise levels
- Multiple speakers talking simultaneously
- Crowded/chaotic audio environments
- Poor audio quality that might affect accent analysis
"""

import librosa
import numpy as np
import json
from pathlib import Path
from typing import Dict, List, Tuple
import argparse
import warnings

# Suppress librosa warnings
warnings.filterwarnings('ignore')


class AudioQualityAnalyzer:
    """Analyze audio quality using librosa for noise detection."""
    
    def __init__(self):
        # Quality thresholds
        self.thresholds = {
            'snr_min': 10,           # Minimum signal-to-noise ratio (dB)
            'spectral_centroid_max': 3000,  # Hz - high values indicate noise
            'zero_crossing_rate_max': 0.1,  # High values indicate noise
            'spectral_rolloff_min': 4000,   # Hz - low values indicate noise
            'mfcc_variance_min': 0.5,       # Low variance indicates noise
            'tempo_max': 200,               # BPM - very high indicates noise
        }
    
    def analyze_audio_file(self, audio_file: Path) -> Dict:
        """Analyze a single audio file for quality and noise."""
        try:
            # Load audio file
            y, sr = librosa.load(str(audio_file), sr=None)
            
            # Basic audio properties
            duration = len(y) / sr
            
            # Extract audio features
            features = self._extract_audio_features(y, sr)
            
            # Calculate quality metrics
            quality_metrics = self._calculate_quality_metrics(y, sr, features)
            
            # Determine noise level
            noise_level = self._determine_noise_level(quality_metrics)
            
            # Calculate overall quality score
            quality_score = self._calculate_quality_score(quality_metrics)
            
            # Get recommendation
            recommendation = self._get_recommendation(noise_level, quality_score)
            
            return {
                'file': str(audio_file),
                'sample_rate': sr,
                'duration': duration,
                'features': features,
                'quality_metrics': quality_metrics,
                'noise_level': noise_level,
                'quality_score': quality_score,
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
    
    def _extract_audio_features(self, y: np.ndarray, sr: int) -> Dict:
        """Extract audio features using librosa."""
        features = {}
        
        # Spectral features
        features['spectral_centroid'] = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
        features['spectral_rolloff'] = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr))
        features['spectral_bandwidth'] = np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr))
        
        # Zero crossing rate (indicates noise/chaos)
        features['zero_crossing_rate'] = np.mean(librosa.feature.zero_crossing_rate(y))
        
        # MFCC features (for speech quality)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        features['mfcc_mean'] = np.mean(mfccs, axis=1)
        features['mfcc_variance'] = np.var(mfccs, axis=1)
        
        # RMS energy
        features['rms_energy'] = np.mean(librosa.feature.rms(y=y))
        
        # Tempo (high tempo might indicate noise)
        try:
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            features['tempo'] = tempo
        except:
            features['tempo'] = 0
        
        # Spectral contrast
        features['spectral_contrast'] = np.mean(librosa.feature.spectral_contrast(y=y, sr=sr))
        
        return features
    
    def _calculate_quality_metrics(self, y: np.ndarray, sr: int, features: Dict) -> Dict:
        """Calculate quality metrics from audio features."""
        metrics = {}
        
        # Signal-to-noise ratio estimation
        # Use spectral centroid as a proxy for noise level
        spectral_centroid = features['spectral_centroid']
        metrics['estimated_snr'] = max(0, 20 - (spectral_centroid / 100))
        
        # Speech clarity indicators
        mfcc_variance = np.mean(features['mfcc_variance'])
        metrics['speech_clarity'] = min(100, mfcc_variance * 20)
        
        # Noise indicators
        zero_crossing_rate = features['zero_crossing_rate']
        metrics['noise_level'] = min(100, zero_crossing_rate * 1000)
        
        # Spectral quality
        spectral_rolloff = features['spectral_rolloff']
        metrics['spectral_quality'] = min(100, (spectral_rolloff / 8000) * 100)
        
        # Dynamic range (using RMS energy)
        rms_energy = features['rms_energy']
        metrics['dynamic_range'] = min(100, rms_energy * 1000)
        
        # Overall quality (combination of factors)
        quality_factors = [
            metrics['speech_clarity'],
            metrics['spectral_quality'],
            metrics['dynamic_range']
        ]
        metrics['overall_quality'] = np.mean(quality_factors)
        
        return metrics
    
    def _determine_noise_level(self, metrics: Dict) -> str:
        """Determine noise level based on quality metrics."""
        snr = metrics.get('estimated_snr', 0)
        noise_level = metrics.get('noise_level', 0)
        speech_clarity = metrics.get('speech_clarity', 0)
        
        # Very high noise indicators
        if snr < 5 or noise_level > 50 or speech_clarity < 20:
            return 'very_high'
        # High noise indicators
        elif snr < 10 or noise_level > 30 or speech_clarity < 40:
            return 'high'
        # Medium noise indicators
        elif snr < 15 or noise_level > 20 or speech_clarity < 60:
            return 'medium'
        else:
            return 'low'
    
    def _calculate_quality_score(self, metrics: Dict) -> float:
        """Calculate overall quality score (0-100)."""
        # Weight different quality factors
        weights = {
            'speech_clarity': 0.3,
            'spectral_quality': 0.2,
            'dynamic_range': 0.2,
            'overall_quality': 0.3
        }
        
        score = 0
        for factor, weight in weights.items():
            score += metrics.get(factor, 0) * weight
        
        return min(100, max(0, score))
    
    def _get_recommendation(self, noise_level: str, quality_score: float) -> str:
        """Get recommendation based on noise level and quality."""
        if noise_level == 'very_high' or quality_score < 30:
            return 'EXCLUDE - Too noisy for accent analysis'
        elif noise_level == 'high' or quality_score < 50:
            return 'REVIEW - High noise, may affect analysis'
        elif noise_level == 'medium' or quality_score < 70:
            return 'ACCEPTABLE - Moderate noise, usable with caution'
        else:
            return 'GOOD - Low noise, suitable for analysis'
    
    def detect_multiple_speakers(self, audio_file: Path) -> Dict:
        """Detect if there are multiple speakers or background noise."""
        try:
            y, sr = librosa.load(str(audio_file), sr=None)
            
            # Analyze for multiple speakers using voice activity detection
            # and spectral analysis
            
            # Voice activity detection
            intervals = librosa.effects.split(y, top_db=20)
            
            # If too many short intervals, might be multiple speakers
            short_intervals = sum(1 for start, end in intervals if (end - start) / sr < 0.5)
            total_intervals = len(intervals)
            
            # Spectral analysis for background noise
            spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
            zero_crossing_rate = np.mean(librosa.feature.zero_crossing_rate(y))
            
            # Multiple speaker indicators
            multiple_speakers = (
                short_intervals / max(total_intervals, 1) > 0.3 or  # Many short segments
                zero_crossing_rate > 0.1 or  # High zero crossing rate
                spectral_centroid > 3000  # High spectral centroid
            )
            
            return {
                'multiple_speakers_detected': multiple_speakers,
                'short_intervals_ratio': short_intervals / max(total_intervals, 1),
                'zero_crossing_rate': zero_crossing_rate,
                'spectral_centroid': spectral_centroid,
                'confidence': min(100, (short_intervals / max(total_intervals, 1)) * 100)
            }
            
        except Exception as e:
            return {
                'multiple_speakers_detected': False,
                'error': str(e),
                'confidence': 0
            }
    
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
            
            # Basic quality analysis
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
                multi_speaker_analysis = self.detect_multiple_speakers(audio_file)
                if multi_speaker_analysis.get('multiple_speakers_detected', False):
                    results['multiple_speakers'] += 1
                    analysis['multiple_speakers'] = multi_speaker_analysis
                
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
    parser = argparse.ArgumentParser(description='Analyze audio quality using librosa')
    parser.add_argument('audio_dir', help='Directory containing audio files')
    parser.add_argument('-o', '--output', help='Output file for results', default='audio_quality_analysis.json')
    parser.add_argument('--pattern', help='File pattern to match', default='*.mp3')
    
    args = parser.parse_args()
    
    analyzer = AudioQualityAnalyzer()
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
    print(f"AUDIO QUALITY ANALYSIS COMPLETE")
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
    
    # Find problematic files
    problematic_files = []
    for file_result in results['files']:
        if (file_result.get('noise_level') in ['very_high', 'high'] or 
            file_result.get('quality_score', 0) < 50 or
            file_result.get('multiple_speakers', {}).get('multiple_speakers_detected', False)):
            problematic_files.append(file_result)
    
    if problematic_files:
        print(f"\n⚠️  PROBLEMATIC FILES DETECTED ({len(problematic_files)}):")
        for file_result in problematic_files:
            filename = Path(file_result['file']).name
            noise_level = file_result.get('noise_level', 'unknown')
            quality_score = file_result.get('quality_score', 0)
            multi_speaker = file_result.get('multiple_speakers', {}).get('multiple_speakers_detected', False)
            
            issues = []
            if noise_level in ['very_high', 'high']:
                issues.append(f"{noise_level} noise")
            if quality_score < 50:
                issues.append(f"low quality ({quality_score:.1f})")
            if multi_speaker:
                issues.append("multiple speakers")
            
            print(f"  {filename}: {', '.join(issues)}")
    
    print(f"\nResults saved to: {output_file}")


if __name__ == "__main__":
    main()
