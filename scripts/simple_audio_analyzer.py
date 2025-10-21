#!/usr/bin/env python3
"""
Simple Audio Quality Analyzer

This script uses basic audio analysis to detect:
- High background noise levels
- Multiple speakers talking simultaneously
- Crowded/chaotic audio environments
- Poor audio quality that might affect accent analysis

Uses only standard libraries and ffmpeg/ffprobe.
"""

import subprocess
import json
import re
from pathlib import Path
from typing import Dict, List
import argparse


class SimpleAudioAnalyzer:
    """Simple audio quality analyzer using ffmpeg/ffprobe."""
    
    def __init__(self):
        self.quality_thresholds = {
            'min_bitrate': 32000,      # Minimum bitrate
            'max_duration': 600,       # Maximum duration (seconds)
            'min_duration': 30,        # Minimum duration (seconds)
        }
    
    def analyze_audio_file(self, audio_file: Path) -> Dict:
        """Analyze a single audio file for quality and noise."""
        try:
            # Get basic audio information
            basic_info = self._get_audio_info(audio_file)
            
            if 'error' in basic_info:
                return basic_info
            
            # Analyze audio characteristics
            audio_analysis = self._analyze_audio_characteristics(audio_file)
            
            # Calculate quality score
            quality_score = self._calculate_quality_score(basic_info, audio_analysis)
            
            # Determine noise level
            noise_level = self._determine_noise_level(audio_analysis, quality_score)
            
            # Get recommendation
            recommendation = self._get_recommendation(noise_level, quality_score)
            
            return {
                'file': str(audio_file),
                'basic_info': basic_info,
                'audio_analysis': audio_analysis,
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
    
    def _analyze_audio_characteristics(self, audio_file: Path) -> Dict:
        """Analyze audio characteristics using ffmpeg filters."""
        try:
            # Use ffmpeg to analyze audio with astats filter
            cmd = [
                'ffmpeg',
                '-i', str(audio_file),
                '-af', 'astats=metadata=1:reset=1',
                '-f', 'null',
                '-'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            # Parse the output for audio characteristics
            characteristics = self._parse_ffmpeg_astats(result.stderr)
            
            # Additional analysis for noise detection
            noise_analysis = self._analyze_noise_patterns(audio_file)
            
            return {
                **characteristics,
                **noise_analysis
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _parse_ffmpeg_astats(self, output: str) -> Dict:
        """Parse ffmpeg astats output."""
        metrics = {}
        
        # Parse RMS and Peak levels
        rms_match = re.search(r'lavfi\.astats\.Overall\.RMS_level=([-\d.]+)', output)
        peak_match = re.search(r'lavfi\.astats\.Overall\.Peak_level=([-\d.]+)', output)
        
        if rms_match:
            metrics['rms_level'] = float(rms_match.group(1))
        if peak_match:
            metrics['peak_level'] = float(peak_match.group(1))
        
        # Calculate dynamic range
        if 'rms_level' in metrics and 'peak_level' in metrics:
            metrics['dynamic_range'] = metrics['peak_level'] - metrics['rms_level']
        
        # Parse DC offset
        dc_match = re.search(r'lavfi\.astats\.Overall\.DC_offset=([-\d.]+)', output)
        if dc_match:
            metrics['dc_offset'] = float(dc_match.group(1))
        
        return metrics
    
    def _analyze_noise_patterns(self, audio_file: Path) -> Dict:
        """Analyze for noise patterns that might indicate multiple speakers or background noise."""
        try:
            # Use ffmpeg to detect silence and analyze patterns
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
            
            # Get basic info for duration
            basic_info = self._get_audio_info(audio_file)
            duration = basic_info.get('duration', 1)
            
            # Calculate silence ratio
            silence_ratio = total_silence_time / duration if duration > 0 else 0
            
            # Analyze for multiple speakers (many short silence periods)
            short_silence_periods = sum(1 for start, end in zip(silence_matches, silence_end_matches)
                                      if float(end) - float(start) < 0.5)
            
            return {
                'silence_periods': silence_periods,
                'silence_ratio': silence_ratio,
                'short_silence_periods': short_silence_periods,
                'multiple_speakers_indicator': short_silence_periods > silence_periods * 0.3,
                'background_noise_indicator': silence_ratio < 0.1  # Very little silence
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _calculate_quality_score(self, basic_info: Dict, audio_analysis: Dict) -> float:
        """Calculate overall quality score (0-100)."""
        score = 0
        
        # Bitrate scoring
        bitrate = basic_info.get('bitrate', 0)
        if bitrate >= 128000:
            score += 25
        elif bitrate >= 64000:
            score += 20
        elif bitrate >= 32000:
            score += 15
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
        
        # Duration scoring (prefer 2-5 minutes)
        duration = basic_info.get('duration', 0)
        if 120 <= duration <= 300:
            score += 20
        elif 60 <= duration <= 600:
            score += 15
        else:
            score += 5
        
        # Audio quality scoring
        rms_level = audio_analysis.get('rms_level', 0)
        dynamic_range = audio_analysis.get('dynamic_range', 0)
        
        # Prefer moderate RMS levels
        if -30 <= rms_level <= -10:
            score += 15
        elif -40 <= rms_level <= -5:
            score += 10
        
        # Prefer good dynamic range
        if dynamic_range >= 20:
            score += 15
        elif dynamic_range >= 10:
            score += 10
        
        # Penalize for noise indicators
        if audio_analysis.get('multiple_speakers_indicator', False):
            score -= 20
        if audio_analysis.get('background_noise_indicator', False):
            score -= 15
        
        return max(0, min(100, score))
    
    def _determine_noise_level(self, audio_analysis: Dict, quality_score: float) -> str:
        """Determine noise level based on analysis."""
        rms_level = audio_analysis.get('rms_level', 0)
        dynamic_range = audio_analysis.get('dynamic_range', 0)
        multiple_speakers = audio_analysis.get('multiple_speakers_indicator', False)
        background_noise = audio_analysis.get('background_noise_indicator', False)
        
        # Very high noise indicators
        if (rms_level > -5 or dynamic_range < 5 or 
            multiple_speakers or background_noise or quality_score < 30):
            return 'very_high'
        # High noise indicators
        elif (rms_level > -10 or dynamic_range < 10 or 
              quality_score < 50):
            return 'high'
        # Medium noise indicators
        elif (rms_level > -15 or dynamic_range < 15 or 
              quality_score < 70):
            return 'medium'
        else:
            return 'low'
    
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
                if analysis.get('audio_analysis', {}).get('multiple_speakers_indicator', False):
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
    parser = argparse.ArgumentParser(description='Analyze audio quality using ffmpeg')
    parser.add_argument('audio_dir', help='Directory containing audio files')
    parser.add_argument('-o', '--output', help='Output file for results', default='audio_quality_analysis.json')
    parser.add_argument('--pattern', help='File pattern to match', default='*.mp3')
    
    args = parser.parse_args()
    
    analyzer = SimpleAudioAnalyzer()
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
            file_result.get('audio_analysis', {}).get('multiple_speakers_indicator', False)):
            problematic_files.append(file_result)
    
    if problematic_files:
        print(f"\n⚠️  PROBLEMATIC FILES DETECTED ({len(problematic_files)}):")
        for file_result in problematic_files:
            filename = Path(file_result['file']).name
            noise_level = file_result.get('noise_level', 'unknown')
            quality_score = file_result.get('quality_score', 0)
            multi_speaker = file_result.get('audio_analysis', {}).get('multiple_speakers_indicator', False)
            
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
