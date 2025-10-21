#!/usr/bin/env python3
"""
Simple Noise Detector

A much simpler approach that focuses on the metrics that actually work:
- File size and bitrate (reliable indicators)
- Silence patterns (detect multiple speakers)
- Basic audio properties

Based on your feedback:
- Nevada-1: Good quality
- Oklahoma-9: Unacceptably noisy
"""

import subprocess
import json
import re
from pathlib import Path
from typing import Dict, List
import argparse


class SimpleNoiseDetector:
    """Simple noise detector using reliable metrics."""
    
    def __init__(self):
        # Simple thresholds based on your feedback
        self.thresholds = {
            'min_bitrate': 30000,        # Minimum acceptable bitrate
            'min_file_size': 15000,      # Minimum file size (bytes)
            'max_duration': 10,          # Maximum duration for short clips
            'min_duration': 1,           # Minimum duration
            'multiple_speakers_ratio': 0.3,  # Short silence ratio threshold
        }
    
    def analyze_audio_file(self, audio_file: Path) -> Dict:
        """Analyze a single audio file for noise."""
        try:
            # Get basic audio information
            basic_info = self._get_audio_info(audio_file)
            
            if 'error' in basic_info:
                return basic_info
            
            # Analyze silence patterns for multiple speakers
            silence_analysis = self._analyze_silence_patterns(audio_file)
            
            # Calculate simple quality score
            quality_score = self._calculate_simple_quality_score(basic_info, silence_analysis)
            
            # Determine noise level
            noise_level = self._determine_simple_noise_level(basic_info, silence_analysis, quality_score)
            
            # Get recommendation
            recommendation = self._get_simple_recommendation(noise_level, quality_score)
            
            return {
                'file': str(audio_file),
                'basic_info': basic_info,
                'silence_analysis': silence_analysis,
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
    
    def _get_audio_info(self, audio_file: Path) -> Dict:
        """Get basic audio information using ffprobe."""
        try:
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
                return {'error': f"ffprobe failed: {result.stderr}"}
            
            data = json.loads(result.stdout)
            
            # Extract audio stream
            audio_stream = None
            for stream in data.get('streams', []):
                if stream.get('codec_type') == 'audio':
                    audio_stream = stream
                    break
            
            if not audio_stream:
                return {'error': 'No audio stream found'}
            
            return {
                'sample_rate': int(audio_stream.get('sample_rate', 0)),
                'channels': int(audio_stream.get('channels', 0)),
                'codec': audio_stream.get('codec_name', 'unknown'),
                'bitrate': int(data.get('format', {}).get('bit_rate', 0)),
                'duration': float(data.get('format', {}).get('duration', 0)),
                'size': int(data.get('format', {}).get('size', 0))
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _analyze_silence_patterns(self, audio_file: Path) -> Dict:
        """Analyze silence patterns to detect multiple speakers."""
        try:
            # Use ffmpeg to detect silence
            cmd = [
                'ffmpeg',
                '-i', str(audio_file),
                '-af', 'silencedetect=noise=-30dB:duration=0.1',
                '-f', 'null',
                '-'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            # Count silence periods
            silence_matches = re.findall(r'silence_start: ([\d.]+)', result.stderr)
            silence_end_matches = re.findall(r'silence_end: ([\d.]+)', result.stderr)
            
            # Analyze silence patterns
            silence_periods = len(silence_matches)
            total_silence_time = sum(float(end) - float(start) 
                                   for start, end in zip(silence_matches, silence_end_matches))
            
            # Get duration
            basic_info = self._get_audio_info(audio_file)
            duration = basic_info.get('duration', 1)
            
            # Calculate ratios
            silence_ratio = total_silence_time / duration if duration > 0 else 0
            
            # Count short silence periods (indicates multiple speakers)
            short_silence_periods = sum(1 for start, end in zip(silence_matches, silence_end_matches)
                                      if float(end) - float(start) < 0.5)
            
            # Multiple speakers indicator
            multiple_speakers = (short_silence_periods / max(silence_periods, 1)) > self.thresholds['multiple_speakers_ratio']
            
            return {
                'silence_periods': silence_periods,
                'silence_ratio': silence_ratio,
                'short_silence_periods': short_silence_periods,
                'multiple_speakers_detected': multiple_speakers,
                'short_silence_ratio': short_silence_periods / max(silence_periods, 1)
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _calculate_simple_quality_score(self, basic_info: Dict, silence_analysis: Dict) -> float:
        """Calculate quality score using simple, reliable metrics."""
        score = 0
        
        # Bitrate scoring (most reliable indicator)
        bitrate = basic_info.get('bitrate', 0)
        if bitrate >= 128000:
            score += 40
        elif bitrate >= 64000:
            score += 35
        elif bitrate >= 32000:
            score += 25
        else:
            score += 10
        
        # File size scoring (indicates content quality)
        file_size = basic_info.get('size', 0)
        if file_size >= 50000:
            score += 20
        elif file_size >= 20000:
            score += 15
        elif file_size >= 10000:
            score += 10
        else:
            score += 5
        
        # Sample rate scoring
        sample_rate = basic_info.get('sample_rate', 0)
        if sample_rate >= 44100:
            score += 20
        elif sample_rate >= 22050:
            score += 15
        elif sample_rate >= 16000:
            score += 10
        
        # Duration scoring (prefer reasonable lengths)
        duration = basic_info.get('duration', 0)
        if 2 <= duration <= 5:
            score += 20
        elif 1 <= duration <= 10:
            score += 15
        else:
            score += 10
        
        # Penalty for multiple speakers
        if silence_analysis.get('multiple_speakers_detected', False):
            score -= 15
        
        # Penalty for too much silence (might indicate poor recording)
        silence_ratio = silence_analysis.get('silence_ratio', 0)
        if silence_ratio > 0.7:  # More than 70% silence
            score -= 10
        
        return max(0, min(100, score))
    
    def _determine_simple_noise_level(self, basic_info: Dict, silence_analysis: Dict, quality_score: float) -> str:
        """Determine noise level using simple, reliable criteria."""
        bitrate = basic_info.get('bitrate', 0)
        file_size = basic_info.get('size', 0)
        multiple_speakers = silence_analysis.get('multiple_speakers_detected', False)
        silence_ratio = silence_analysis.get('silence_ratio', 0)
        
        # Very high noise: Multiple clear indicators
        very_high_indicators = 0
        if bitrate < self.thresholds['min_bitrate']:
            very_high_indicators += 1
        if file_size < self.thresholds['min_file_size']:
            very_high_indicators += 1
        if multiple_speakers:
            very_high_indicators += 1
        if silence_ratio > 0.8:  # Too much silence
            very_high_indicators += 1
        if quality_score < 30:
            very_high_indicators += 1
        
        if very_high_indicators >= 2:
            return 'very_high'
        
        # High noise: Some clear problems
        high_indicators = 0
        if bitrate < 50000:
            high_indicators += 1
        if file_size < 25000:
            high_indicators += 1
        if multiple_speakers:
            high_indicators += 1
        if quality_score < 50:
            high_indicators += 1
        
        if high_indicators >= 2:
            return 'high'
        
        # Medium noise: Some issues
        if (bitrate < 80000 or file_size < 40000 or 
            quality_score < 70 or silence_ratio > 0.6):
            return 'medium'
        
        # Low noise: Good quality
        return 'low'
    
    def _get_simple_recommendation(self, noise_level: str, quality_score: float) -> str:
        """Get recommendation based on noise level."""
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
                if analysis.get('silence_analysis', {}).get('multiple_speakers_detected', False):
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
    parser = argparse.ArgumentParser(description='Simple noise detection using reliable metrics')
    parser.add_argument('audio_dir', help='Directory containing audio files')
    parser.add_argument('-o', '--output', help='Output file for results', default='simple_noise_analysis.json')
    parser.add_argument('--pattern', help='File pattern to match', default='*.mp3')
    
    args = parser.parse_args()
    
    detector = SimpleNoiseDetector()
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
    print(f"SIMPLE NOISE DETECTION COMPLETE")
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
