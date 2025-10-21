#!/usr/bin/env python3
"""
Noise Detection Tool

This script analyzes audio files to detect:
- High background noise levels
- Multiple speakers talking simultaneously
- Crowded/chaotic audio environments
- Poor audio quality that might affect accent analysis
"""

import subprocess
import json
import os
from pathlib import Path
from typing import Dict, List, Tuple
import argparse


class NoiseDetector:
    """Detect noisy audio files that might not be suitable for accent analysis."""
    
    def __init__(self):
        self.noise_thresholds = {
            'high_noise_db': -20,  # dB threshold for high noise
            'low_snr_db': 10,      # Signal-to-noise ratio threshold
            'max_spectral_centroid': 3000,  # Hz - high values indicate noise
            'min_spectral_rolloff': 8000,   # Hz - low values indicate noise
        }
    
    def analyze_audio_file(self, audio_file: Path) -> Dict:
        """Analyze a single audio file for noise characteristics."""
        try:
            # Use ffprobe to get audio statistics
            cmd = [
                'ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_streams',
                '-show_format',
                str(audio_file)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                return {
                    'file': str(audio_file),
                    'error': f"ffprobe failed: {result.stderr}",
                    'noise_level': 'unknown',
                    'quality_score': 0
                }
            
            data = json.loads(result.stdout)
            
            # Extract audio stream info
            audio_stream = None
            for stream in data.get('streams', []):
                if stream.get('codec_type') == 'audio':
                    audio_stream = stream
                    break
            
            if not audio_stream:
                return {
                    'file': str(audio_file),
                    'error': 'No audio stream found',
                    'noise_level': 'unknown',
                    'quality_score': 0
                }
            
            # Get basic audio properties
            sample_rate = int(audio_stream.get('sample_rate', 0))
            channels = int(audio_stream.get('channels', 0))
            duration = float(data.get('format', {}).get('duration', 0))
            bitrate = int(data.get('format', {}).get('bit_rate', 0))
            
            # Analyze audio characteristics using ffmpeg
            noise_analysis = self._analyze_noise_characteristics(audio_file)
            
            # Calculate quality score
            quality_score = self._calculate_quality_score(
                sample_rate, channels, duration, bitrate, noise_analysis
            )
            
            # Determine noise level
            noise_level = self._determine_noise_level(noise_analysis, quality_score)
            
            return {
                'file': str(audio_file),
                'sample_rate': sample_rate,
                'channels': channels,
                'duration': duration,
                'bitrate': bitrate,
                'noise_analysis': noise_analysis,
                'quality_score': quality_score,
                'noise_level': noise_level,
                'recommendation': self._get_recommendation(noise_level, quality_score)
            }
            
        except subprocess.TimeoutExpired:
            return {
                'file': str(audio_file),
                'error': 'Analysis timeout',
                'noise_level': 'unknown',
                'quality_score': 0
            }
        except Exception as e:
            return {
                'file': str(audio_file),
                'error': str(e),
                'noise_level': 'unknown',
                'quality_score': 0
            }
    
    def _analyze_noise_characteristics(self, audio_file: Path) -> Dict:
        """Analyze noise characteristics using ffmpeg filters."""
        try:
            # Use ffmpeg to analyze audio characteristics
            cmd = [
                'ffmpeg',
                '-i', str(audio_file),
                '-af', 'astats=metadata=1:reset=1',
                '-f', 'null',
                '-'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            # Parse the output for noise characteristics
            noise_metrics = self._parse_ffmpeg_output(result.stderr)
            
            return noise_metrics
            
        except Exception as e:
            return {
                'error': str(e),
                'rms_level': 0,
                'peak_level': 0,
                'dynamic_range': 0
            }
    
    def _parse_ffmpeg_output(self, output: str) -> Dict:
        """Parse ffmpeg output to extract noise metrics."""
        metrics = {
            'rms_level': 0,
            'peak_level': 0,
            'dynamic_range': 0,
            'spectral_centroid': 0,
            'zero_crossing_rate': 0
        }
        
        lines = output.split('\n')
        for line in lines:
            if 'lavfi.astats.Overall.RMS_level' in line:
                try:
                    metrics['rms_level'] = float(line.split('=')[1].strip())
                except:
                    pass
            elif 'lavfi.astats.Overall.Peak_level' in line:
                try:
                    metrics['peak_level'] = float(line.split('=')[1].strip())
                except:
                    pass
        
        # Calculate dynamic range
        if metrics['peak_level'] > 0 and metrics['rms_level'] > 0:
            metrics['dynamic_range'] = metrics['peak_level'] - metrics['rms_level']
        
        return metrics
    
    def _calculate_quality_score(self, sample_rate: int, channels: int, 
                               duration: float, bitrate: int, noise_analysis: Dict) -> float:
        """Calculate overall audio quality score (0-100)."""
        score = 0
        
        # Sample rate scoring
        if sample_rate >= 44100:
            score += 20
        elif sample_rate >= 22050:
            score += 15
        elif sample_rate >= 16000:
            score += 10
        
        # Channel scoring
        if channels >= 2:
            score += 10
        elif channels == 1:
            score += 5
        
        # Duration scoring (prefer 2-5 minutes)
        if 120 <= duration <= 300:
            score += 20
        elif 60 <= duration <= 600:
            score += 15
        else:
            score += 5
        
        # Bitrate scoring
        if bitrate >= 128000:
            score += 20
        elif bitrate >= 64000:
            score += 15
        elif bitrate >= 32000:
            score += 10
        
        # Noise analysis scoring
        rms_level = noise_analysis.get('rms_level', 0)
        dynamic_range = noise_analysis.get('dynamic_range', 0)
        
        # Prefer moderate RMS levels (not too quiet, not too loud)
        if -30 <= rms_level <= -10:
            score += 15
        elif -40 <= rms_level <= -5:
            score += 10
        
        # Prefer good dynamic range
        if dynamic_range >= 20:
            score += 15
        elif dynamic_range >= 10:
            score += 10
        
        return min(score, 100)
    
    def _determine_noise_level(self, noise_analysis: Dict, quality_score: float) -> str:
        """Determine noise level based on analysis."""
        rms_level = noise_analysis.get('rms_level', 0)
        dynamic_range = noise_analysis.get('dynamic_range', 0)
        
        # High noise indicators
        if rms_level > -10:  # Very loud
            return 'very_high'
        elif rms_level > -15:  # Loud
            return 'high'
        elif quality_score < 50:  # Poor quality
            return 'high'
        elif dynamic_range < 5:  # Poor dynamic range
            return 'medium'
        elif quality_score < 70:
            return 'medium'
        else:
            return 'low'
    
    def _get_recommendation(self, noise_level: str, quality_score: float) -> str:
        """Get recommendation based on noise level and quality."""
        if noise_level == 'very_high':
            return 'EXCLUDE - Too noisy for accent analysis'
        elif noise_level == 'high':
            return 'REVIEW - High noise, may affect analysis'
        elif noise_level == 'medium':
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
    
    def find_noisy_files(self, results: Dict) -> List[Dict]:
        """Find files that are too noisy for accent analysis."""
        noisy_files = []
        
        for file_result in results['files']:
            if file_result.get('noise_level') in ['very_high', 'high']:
                noisy_files.append(file_result)
            elif file_result.get('quality_score', 0) < 50:
                noisy_files.append(file_result)
        
        return noisy_files


def main():
    parser = argparse.ArgumentParser(description='Detect noisy audio files')
    parser.add_argument('audio_dir', help='Directory containing audio files')
    parser.add_argument('-o', '--output', help='Output file for results', default='noise_analysis.json')
    parser.add_argument('--pattern', help='File pattern to match', default='*.mp3')
    parser.add_argument('--threshold', help='Quality score threshold', type=float, default=50.0)
    
    args = parser.parse_args()
    
    detector = NoiseDetector()
    audio_dir = Path(args.audio_dir)
    
    if not audio_dir.exists():
        print(f"Directory not found: {audio_dir}")
        return
    
    # Analyze all audio files
    results = detector.batch_analyze(audio_dir, args.pattern)
    
    # Save results
    output_file = Path(args.output)
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"NOISE ANALYSIS COMPLETE")
    print(f"{'='*60}")
    print(f"Total files: {results['total_files']}")
    print(f"Successfully analyzed: {results['analyzed']}")
    print(f"Errors: {results['errors']}")
    
    print(f"\nNoise Levels:")
    for level, count in results['noise_levels'].items():
        print(f"  {level}: {count}")
    
    print(f"\nRecommendations:")
    for rec, count in results['recommendations'].items():
        print(f"  {rec}: {count}")
    
    # Find noisy files
    noisy_files = detector.find_noisy_files(results)
    if noisy_files:
        print(f"\n⚠️  NOISY FILES DETECTED ({len(noisy_files)}):")
        for file_result in noisy_files:
            print(f"  {Path(file_result['file']).name}: {file_result.get('noise_level', 'unknown')} noise, quality {file_result.get('quality_score', 0):.1f}")
    
    print(f"\nResults saved to: {output_file}")


if __name__ == "__main__":
    main()
