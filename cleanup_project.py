#!/usr/bin/env python3
"""
Cleanup script for project organization.
"""

import os
import shutil
from pathlib import Path

def cleanup_project():
    """Clean up the project directory."""
    print("🧹 Cleaning up project...")
    
    # Files to remove
    files_to_remove = [
        "reliable_transcription.py",
        "rich_whisper_transcriptions.py", 
        "ultra_fast_transcription.py",
        "fast_m1_transcription.py",
        "one_per_state_transcription.py",
        "organize_whisper_transcriptions.py",
        "transcribe_ten_states.py",
        "simple_demo.py",
        "keyword_alignment.py",
        "robust_alignment.py",
        "stt_alignment.py",
        "word_level_extractor.py",
        "word_level_feature_extractor.py"
    ]
    
    # Remove files
    for file in files_to_remove:
        if Path(file).exists():
            os.remove(file)
            print(f"   ❌ Removed {file}")
    
    # Create organized directories
    os.makedirs("transcriptions", exist_ok=True)
    os.makedirs("datasets", exist_ok=True)
    os.makedirs("scripts", exist_ok=True)
    
    print("✅ Cleanup complete!")
    print("📁 Organized structure:")
    print("   - transcriptions/ (all transcription data)")
    print("   - datasets/ (all dataset directories)")
    print("   - scripts/ (core Python scripts)")

if __name__ == "__main__":
    cleanup_project()
