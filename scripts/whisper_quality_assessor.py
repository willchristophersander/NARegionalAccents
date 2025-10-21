#!/usr/bin/env python3
"""
AI-powered audio quality assessment using Whisper's built-in quality metrics.
This leverages Whisper's confidence scores and speech detection capabilities.
"""

import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Optional
import numpy as np
import scipy.io.wavfile as wavfile
import warnings

warnings.filterwarnings('ignore')

class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle numpy types."""
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.bool_):
            return bool(obj)
        return super(NumpyEncoder, self).default(obj)

class WhisperQualityAssessor:
    """AI-powered audio quality assessment using Whisper."""
    
    def __init__(self):
        self.whisper_available = self._check_whisper()
        
    def _check_whisper(self) -> bool:
        """Check if Whisper is available."""
        try:
            import whisper
            return True
        except ImportError:
            print("Whisper not available. Install with: pip install openai-whisper")
            return False
    
    def assess_audio_quality(self, audio_file: Path) -> Dict:
        """Assess audio quality using Whisper's AI capabilities."""
        if not self.whisper_available:
            return {'error': 'Whisper not available'}
        
        # Convert to WAV if needed
        wav_file = self._ensure_wav_format(audio_file)
        if not wav_file:
            return {'error': 'Could not convert to WAV format'}
        
        try:
            import whisper
            model = whisper.load_model("base")
            result = model.transcribe(str(wav_file))
            
            # Extract quality metrics from Whisper's analysis
            quality_metrics = self._extract_quality_metrics(result)
            
            # Analyze the audio for noise patterns
            noise_analysis = self._analyze_noise_patterns(wav_file, result)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(quality_metrics, noise_analysis)
            
            results = {
                'file': str(audio_file),
                'whisper_analysis': {
                    'text': result.get('text', ''),
                    'language': result.get('language', 'unknown'),
                    'segments': len(result.get('segments', [])),
                },
                'quality_metrics': quality_metrics,
                'noise_analysis': noise_analysis,
                'recommendations': recommendations
            }
            
            # Cleanup
            if wav_file != audio_file:
                os.unlink(wav_file)
                
            return results
            
        except Exception as e:
            return {'error': f'Whisper analysis failed: {e}'}
    
    def _ensure_wav_format(self, audio_file: Path) -> Optional[Path]:
        """Convert audio to WAV format if needed."""
        if audio_file.suffix.lower() == '.wav':
            return audio_file
            
        try:
            wav_file = audio_file.with_suffix('.wav')
            cmd = [
                'ffmpeg', '-i', str(audio_file),
                '-ar', '16000',  # 16kHz sample rate
                '-ac', '1',      # Mono
                '-y',            # Overwrite
                str(wav_file)
            ]
            subprocess.run(cmd, capture_output=True, check=True)
            return wav_file
        except subprocess.CalledProcessError:
            return None
    
    def _extract_quality_metrics(self, whisper_result: Dict) -> Dict:
        """Extract quality metrics from Whisper's result."""
        segments = whisper_result.get('segments', [])
        
        if not segments:
            return {
                'overall_confidence': 0.0,
                'speech_detection_confidence': 0.0,
                'no_speech_probability': 1.0,
                'segment_count': 0,
                'avg_segment_length': 0.0
            }
        
        # Extract confidence scores
        confidences = []
        no_speech_probs = []
        segment_lengths = []
        
        for segment in segments:
            if 'no_speech_prob' in segment:
                no_speech_probs.append(segment['no_speech_prob'])
            if 'avg_logprob' in segment:
                confidences.append(segment['avg_logprob'])
            if 'end' in segment and 'start' in segment:
                segment_lengths.append(segment['end'] - segment['start'])
        
        # Calculate metrics
        overall_confidence = np.mean(confidences) if confidences else 0.0
        speech_detection_confidence = 1.0 - np.mean(no_speech_probs) if no_speech_probs else 0.0
        avg_no_speech_prob = np.mean(no_speech_probs) if no_speech_probs else 1.0
        avg_segment_length = np.mean(segment_lengths) if segment_lengths else 0.0
        
        return {
            'overall_confidence': float(overall_confidence),
            'speech_detection_confidence': float(speech_detection_confidence),
            'no_speech_probability': float(avg_no_speech_prob),
            'segment_count': len(segments),
            'avg_segment_length': float(avg_segment_length)
        }
    
    def _analyze_noise_patterns(self, audio_file: Path, whisper_result: Dict) -> Dict:
        """Analyze noise patterns using audio data and Whisper results."""
        try:
            # Load audio data
            sample_rate, audio_data = wavfile.read(audio_file)
            if len(audio_data.shape) > 1:
                audio_data = audio_data.mean(axis=1)
            
            # Calculate basic audio metrics
            rms = np.sqrt(np.mean(audio_data**2))
            peak = np.max(np.abs(audio_data))
            dynamic_range = 20 * np.log10(peak / (rms + 1e-10))
            
            # Analyze silence patterns
            silence_threshold = 0.01 * peak
            silence_mask = np.abs(audio_data) < silence_threshold
            silence_ratio = np.mean(silence_mask)
            
            # Analyze Whisper's speech detection
            segments = whisper_result.get('segments', [])
            speech_detected = len(segments) > 0
            
            # Calculate noise indicators
            noise_indicators = {
                'low_amplitude': rms < 0.01,
                'high_silence_ratio': silence_ratio > 0.5,
                'poor_speech_detection': len(segments) == 0,
                'low_confidence': np.mean([seg.get('avg_logprob', -1) for seg in segments]) < -0.5 if segments else True
            }
            
            # Overall noise assessment
            noise_score = 0
            if noise_indicators['low_amplitude']:
                noise_score += 0.3
            if noise_indicators['high_silence_ratio']:
                noise_score += 0.3
            if noise_indicators['poor_speech_detection']:
                noise_score += 0.4
            if noise_indicators['low_confidence']:
                noise_score += 0.2
            
            return {
                'noise_score': noise_score,
                'noise_level': self._classify_noise_level(noise_score),
                'audio_metrics': {
                    'rms': float(rms),
                    'peak': float(peak),
                    'dynamic_range': float(dynamic_range),
                    'silence_ratio': float(silence_ratio)
                },
                'indicators': noise_indicators
            }
            
        except Exception as e:
            return {
                'noise_score': 1.0,
                'noise_level': 'unknown',
                'error': str(e)
            }
    
    def _classify_noise_level(self, noise_score: float) -> str:
        """Classify noise level based on score."""
        if noise_score < 0.2:
            return "low"
        elif noise_score < 0.4:
            return "medium"
        elif noise_score < 0.6:
            return "high"
        else:
            return "very_high"
    
    def _generate_recommendations(self, quality_metrics: Dict, noise_analysis: Dict) -> Dict:
        """Generate recommendations based on AI analysis."""
        recommendations = {
            'overall_quality': 'unknown',
            'suitable_for_analysis': True,
            'confidence_level': 'unknown',
            'issues': [],
            'suggestions': []
        }
        
        # Analyze Whisper's confidence
        speech_confidence = quality_metrics.get('speech_detection_confidence', 0)
        no_speech_prob = quality_metrics.get('no_speech_probability', 1)
        
        if speech_confidence < 0.5:
            recommendations['issues'].append(f'Low speech detection confidence: {speech_confidence:.2f}')
            recommendations['suggestions'].append('Audio may be too quiet or unclear')
        
        if no_speech_prob > 0.5:
            recommendations['issues'].append(f'High no-speech probability: {no_speech_prob:.2f}')
            recommendations['suggestions'].append('Audio may contain mostly noise or silence')
        
        # Analyze noise
        noise_level = noise_analysis.get('noise_level', 'unknown')
        noise_score = noise_analysis.get('noise_score', 0)
        
        if noise_level in ['high', 'very_high']:
            recommendations['suitable_for_analysis'] = False
            recommendations['issues'].append(f'High noise level: {noise_level} (score: {noise_score:.2f})')
            recommendations['suggestions'].append('Consider noise reduction or exclude from analysis')
        
        # Overall assessment
        if not recommendations['issues']:
            recommendations['overall_quality'] = 'excellent'
            recommendations['confidence_level'] = 'high'
        elif len(recommendations['issues']) == 1:
            recommendations['overall_quality'] = 'good'
            recommendations['confidence_level'] = 'medium'
        elif len(recommendations['issues']) == 2:
            recommendations['overall_quality'] = 'acceptable'
            recommendations['confidence_level'] = 'low'
        else:
            recommendations['overall_quality'] = 'poor'
            recommendations['confidence_level'] = 'very_low'
            recommendations['suitable_for_analysis'] = False
        
        return recommendations

def batch_assess_audio_files(input_dir: Path, output_file: Path):
    """Batch assess multiple audio files."""
    assessor = WhisperQualityAssessor()
    
    if not assessor.whisper_available:
        print("Whisper not available. Install with: pip install openai-whisper")
        return
    
    results = {
        'total_files': 0,
        'successful': 0,
        'errors': 0,
        'files': []
    }
    
    audio_files = list(input_dir.glob('*.mp3')) + list(input_dir.glob('*.wav'))
    results['total_files'] = len(audio_files)
    
    print(f"Assessing {len(audio_files)} audio files with AI...")
    
    for i, audio_file in enumerate(audio_files, 1):
        print(f"Analyzing {i}/{len(audio_files)}: {audio_file.name}")
        
        try:
            result = assessor.assess_audio_quality(audio_file)
            results['files'].append(result)
            results['successful'] += 1
            
            # Print summary
            if 'error' in result:
                print(f"  ❌ Error: {result['error']}")
            else:
                quality = result.get('recommendations', {}).get('overall_quality', 'unknown')
                noise_level = result.get('noise_analysis', {}).get('noise_level', 'unknown')
                print(f"  ✅ Quality: {quality}, Noise: {noise_level}")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
            results['errors'] += 1
    
    # Save results
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, cls=NumpyEncoder)
    
    print(f"\nAI Assessment Complete:")
    print(f"Total files: {results['total_files']}")
    print(f"Successful: {results['successful']}")
    print(f"Errors: {results['errors']}")
    print(f"Results saved to: {output_file}")

def main():
    """Main function."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python whisper_quality_assessor.py <audio_file_or_directory> [output_file]")
        sys.exit(1)
    
    input_path = Path(sys.argv[1])
    output_file = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("whisper_quality_analysis.json")
    
    if input_path.is_file():
        # Single file
        assessor = WhisperQualityAssessor()
        result = assessor.assess_audio_quality(input_path)
        print(json.dumps(result, indent=2))
    elif input_path.is_dir():
        # Directory
        batch_assess_audio_files(input_path, output_file)
    else:
        print(f"Path not found: {input_path}")
        sys.exit(1)

if __name__ == "__main__":
    main()
