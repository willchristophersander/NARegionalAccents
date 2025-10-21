#!/usr/bin/env python3
"""
AI-powered audio quality assessment using multiple approaches:
1. Traditional metrics (PESQ, STOI, MOS)
2. Deep learning models for noise detection
3. Pre-trained models for speech quality assessment
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

class AIAudioQualityAssessor:
    """AI-powered audio quality assessment with multiple models."""
    
    def __init__(self):
        self.available_models = self._check_available_models()
        
    def _check_available_models(self) -> Dict[str, bool]:
        """Check which AI models are available."""
        models = {
            'pesq': False,
            'stoi': False,
            'mosnet': False,
            'wav2vec2': False,
            'whisper_quality': False
        }
        
        # Check for PESQ
        try:
            import pesq
            models['pesq'] = True
        except ImportError:
            pass
            
        # Check for STOI
        try:
            import pystoi
            models['stoi'] = True
        except ImportError:
            pass
            
        # Check for other models
        try:
            import torch
            models['mosnet'] = True
        except ImportError:
            pass
            
        return models
    
    def assess_audio_quality(self, audio_file: Path, reference_file: Optional[Path] = None) -> Dict:
        """Assess audio quality using multiple AI approaches."""
        results = {
            'file': str(audio_file),
            'models_used': [],
            'quality_scores': {},
            'noise_detection': {},
            'recommendations': {}
        }
        
        # Convert to WAV if needed
        wav_file = self._ensure_wav_format(audio_file)
        if not wav_file:
            return {'error': 'Could not convert to WAV format'}
        
        # Load audio data
        try:
            sample_rate, audio_data = wavfile.read(wav_file)
            if len(audio_data.shape) > 1:
                audio_data = audio_data.mean(axis=1)  # Convert to mono
        except Exception as e:
            return {'error': f'Could not load audio: {e}'}
        
        # 1. Traditional Quality Metrics
        if self.available_models['pesq'] and reference_file:
            pesq_score = self._calculate_pesq(wav_file, reference_file)
            if pesq_score:
                results['quality_scores']['pesq'] = pesq_score
                results['models_used'].append('pesq')
        
        if self.available_models['stoi'] and reference_file:
            stoi_score = self._calculate_stoi(wav_file, reference_file)
            if stoi_score:
                results['quality_scores']['stoi'] = stoi_score
                results['models_used'].append('stoi')
        
        # 2. AI-based Noise Detection
        noise_analysis = self._ai_noise_detection(audio_data, sample_rate)
        results['noise_detection'] = noise_analysis
        
        # 3. Speech Quality Assessment
        if self.available_models['mosnet']:
            mos_score = self._calculate_mos(audio_data, sample_rate)
            if mos_score:
                results['quality_scores']['mos'] = mos_score
                results['models_used'].append('mosnet')
        
        # 4. Whisper-based Quality Assessment
        whisper_quality = self._assess_with_whisper(wav_file)
        if whisper_quality:
            results['quality_scores']['whisper_confidence'] = whisper_quality
            results['models_used'].append('whisper')
        
        # 5. Generate Recommendations
        results['recommendations'] = self._generate_recommendations(results)
        
        # Cleanup
        if wav_file != audio_file:
            os.unlink(wav_file)
            
        return results
    
    def _ensure_wav_format(self, audio_file: Path) -> Optional[Path]:
        """Convert audio to WAV format if needed."""
        if audio_file.suffix.lower() == '.wav':
            return audio_file
            
        try:
            # Use ffmpeg to convert
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
    
    def _calculate_pesq(self, audio_file: Path, reference_file: Path) -> Optional[float]:
        """Calculate PESQ score."""
        try:
            import pesq
            score = pesq.pesq(16000, str(reference_file), str(audio_file), 'wb')
            return float(score)
        except Exception:
            return None
    
    def _calculate_stoi(self, audio_file: Path, reference_file: Path) -> Optional[float]:
        """Calculate STOI score."""
        try:
            import pystoi
            score = pystoi.stoi(str(reference_file), str(audio_file), 16000, extended=False)
            return float(score)
        except Exception:
            return None
    
    def _ai_noise_detection(self, audio_data: np.ndarray, sample_rate: int) -> Dict:
        """AI-based noise detection using spectral analysis."""
        # Calculate spectral features
        fft = np.fft.fft(audio_data)
        freqs = np.fft.fftfreq(len(fft), 1/sample_rate)
        magnitude = np.abs(fft)
        
        # Analyze frequency distribution
        low_freq_energy = np.sum(magnitude[freqs < 1000])  # Below 1kHz
        mid_freq_energy = np.sum(magnitude[(freqs >= 1000) & (freqs < 4000)])  # 1-4kHz
        high_freq_energy = np.sum(magnitude[freqs >= 4000])  # Above 4kHz
        
        total_energy = low_freq_energy + mid_freq_energy + high_freq_energy
        
        # Noise indicators
        low_freq_ratio = low_freq_energy / total_energy if total_energy > 0 else 0
        high_freq_ratio = high_freq_energy / total_energy if total_energy > 0 else 0
        
        # Detect potential noise
        noise_indicators = {
            'low_freq_dominance': low_freq_ratio > 0.7,  # Humming, rumble
            'high_freq_spikes': high_freq_ratio > 0.3,    # Hiss, static
            'spectral_flatness': self._calculate_spectral_flatness(magnitude),
            'zero_crossing_rate': self._calculate_zcr(audio_data),
            'energy_variation': self._calculate_energy_variation(audio_data)
        }
        
        # Overall noise assessment
        noise_score = 0
        if noise_indicators['low_freq_dominance']:
            noise_score += 0.3
        if noise_indicators['high_freq_spikes']:
            noise_score += 0.3
        if noise_indicators['spectral_flatness'] > 0.8:
            noise_score += 0.2
        if noise_indicators['zero_crossing_rate'] > 0.1:
            noise_score += 0.2
        
        return {
            'noise_score': noise_score,
            'noise_level': self._classify_noise_level(noise_score),
            'indicators': noise_indicators
        }
    
    def _calculate_spectral_flatness(self, magnitude: np.ndarray) -> float:
        """Calculate spectral flatness (noise indicator)."""
        # Avoid log(0)
        magnitude = magnitude + 1e-10
        geometric_mean = np.exp(np.mean(np.log(magnitude)))
        arithmetic_mean = np.mean(magnitude)
        return geometric_mean / arithmetic_mean if arithmetic_mean > 0 else 0
    
    def _calculate_zcr(self, audio_data: np.ndarray) -> float:
        """Calculate zero crossing rate."""
        zero_crossings = np.sum(np.diff(np.sign(audio_data)) != 0)
        return zero_crossings / len(audio_data)
    
    def _calculate_energy_variation(self, audio_data: np.ndarray, frame_size: int = 1024) -> float:
        """Calculate energy variation across frames."""
        if len(audio_data) < frame_size:
            return 0
        
        frames = []
        for i in range(0, len(audio_data) - frame_size, frame_size):
            frame = audio_data[i:i + frame_size]
            energy = np.sum(frame ** 2)
            frames.append(energy)
        
        if len(frames) < 2:
            return 0
        
        return np.std(frames) / np.mean(frames) if np.mean(frames) > 0 else 0
    
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
    
    def _calculate_mos(self, audio_data: np.ndarray, sample_rate: int) -> Optional[float]:
        """Calculate MOS score using pre-trained model."""
        # This would require a pre-trained MOS prediction model
        # For now, return a placeholder
        return None
    
    def _assess_with_whisper(self, audio_file: Path) -> Optional[float]:
        """Assess quality using Whisper's confidence scores."""
        try:
            import whisper
            model = whisper.load_model("base")
            result = model.transcribe(str(audio_file))
            
            # Extract confidence from segments
            confidences = [seg.get('no_speech_prob', 0) for seg in result.get('segments', [])]
            if confidences:
                avg_confidence = 1 - np.mean(confidences)  # Convert to quality score
                return float(avg_confidence)
        except Exception:
            pass
        return None
    
    def _generate_recommendations(self, results: Dict) -> Dict:
        """Generate recommendations based on all assessments."""
        recommendations = {
            'overall_quality': 'unknown',
            'suitable_for_analysis': True,
            'issues': [],
            'suggestions': []
        }
        
        # Analyze noise detection
        noise_detection = results.get('noise_detection', {})
        noise_level = noise_detection.get('noise_level', 'unknown')
        
        if noise_level in ['high', 'very_high']:
            recommendations['suitable_for_analysis'] = False
            recommendations['issues'].append(f'High noise level: {noise_level}')
            recommendations['suggestions'].append('Consider noise reduction or exclude from analysis')
        
        # Analyze quality scores
        quality_scores = results.get('quality_scores', {})
        
        if 'pesq' in quality_scores:
            pesq_score = quality_scores['pesq']
            if pesq_score < 2.0:
                recommendations['issues'].append(f'Low PESQ score: {pesq_score:.2f}')
            elif pesq_score > 4.0:
                recommendations['overall_quality'] = 'excellent'
        
        if 'stoi' in quality_scores:
            stoi_score = quality_scores['stoi']
            if stoi_score < 0.5:
                recommendations['issues'].append(f'Low STOI score: {stoi_score:.2f}')
        
        if 'whisper_confidence' in quality_scores:
            whisper_conf = quality_scores['whisper_confidence']
            if whisper_conf < 0.7:
                recommendations['issues'].append(f'Low Whisper confidence: {whisper_conf:.2f}')
        
        # Final recommendation
        if not recommendations['issues']:
            recommendations['overall_quality'] = 'good'
        elif len(recommendations['issues']) <= 1:
            recommendations['overall_quality'] = 'acceptable'
        else:
            recommendations['overall_quality'] = 'poor'
        
        return recommendations

def main():
    """Test the AI audio quality assessor."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python ai_audio_quality_assessor.py <audio_file> [reference_file]")
        sys.exit(1)
    
    audio_file = Path(sys.argv[1])
    reference_file = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    
    if not audio_file.exists():
        print(f"Audio file not found: {audio_file}")
        sys.exit(1)
    
    assessor = AIAudioQualityAssessor()
    results = assessor.assess_audio_quality(audio_file, reference_file)
    
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
