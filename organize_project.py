#!/usr/bin/env python3
"""
Organize and clean up the project directory.

This script:
1. Analyzes current directory structure
2. Identifies duplicates and outdated files
3. Creates organized folder structure
4. Suggests what to keep/remove
"""

import os
import shutil
from pathlib import Path
from collections import defaultdict
import json

def analyze_directory():
    """Analyze the current directory structure."""
    print("=== PROJECT DIRECTORY ANALYSIS ===")
    
    # Get all files and directories
    current_dir = Path(".")
    all_items = list(current_dir.iterdir())
    
    # Categorize items
    categories = {
        'python_scripts': [],
        'data_directories': [],
        'transcription_directories': [],
        'other_files': [],
        'system_files': []
    }
    
    for item in all_items:
        if item.name.startswith('.'):
            categories['system_files'].append(item)
        elif item.is_file() and item.suffix == '.py':
            categories['python_scripts'].append(item)
        elif item.is_dir():
            if any(keyword in item.name.lower() for keyword in ['transcription', 'dataset', 'stt', 'whisper']):
                categories['transcription_directories'].append(item)
            elif any(keyword in item.name.lower() for keyword in ['data', 'audio', 'features', 'plots']):
                categories['data_directories'].append(item)
            else:
                categories['other_files'].append(item)
        else:
            categories['other_files'].append(item)
    
    # Print analysis
    for category, items in categories.items():
        if items:
            print(f"\n📁 {category.replace('_', ' ').title()}:")
            for item in items:
                if item.is_file():
                    size = item.stat().st_size
                    print(f"   📄 {item.name} ({size:,} bytes)")
                else:
                    file_count = len(list(item.rglob('*')))
                    print(f"   📁 {item.name}/ ({file_count} items)")
    
    return categories

def identify_duplicates():
    """Identify duplicate and similar files."""
    print("\n=== DUPLICATE ANALYSIS ===")
    
    # Look for similar Python scripts
    python_scripts = list(Path(".").glob("*.py"))
    
    # Group by functionality
    script_groups = defaultdict(list)
    
    for script in python_scripts:
        name = script.stem.lower()
        
        if 'transcription' in name or 'whisper' in name:
            script_groups['transcription'].append(script)
        elif 'alignment' in name or 'mfa' in name:
            script_groups['alignment'].append(script)
        elif 'stt' in name or 'speech' in name:
            script_groups['stt'].append(script)
        elif 'word' in name or 'feature' in name:
            script_groups['features'].append(script)
        elif 'clean' in name or 'prepare' in name:
            script_groups['preparation'].append(script)
        else:
            script_groups['other'].append(script)
    
    # Show groups
    for group, scripts in script_groups.items():
        if scripts:
            print(f"\n🔍 {group.title()} Scripts:")
            for script in scripts:
                size = script.stat().st_size
                print(f"   - {script.name} ({size:,} bytes)")
    
    return script_groups

def suggest_organization():
    """Suggest how to organize the project."""
    print("\n=== ORGANIZATION SUGGESTIONS ===")
    
    suggestions = {
        'keep_core': [
            'accent_feature_extractor.py',
            'feature_visualizer.py',
            'idea_us_scraper_v2.py',
            'clean_transcriptions.py'
        ],
        'keep_best_transcription': [
            'simple_rich_fast.py'  # Most recent and simple
        ],
        'remove_duplicates': [
            'reliable_transcription.py',
            'rich_whisper_transcriptions.py',
            'ultra_fast_transcription.py',
            'fast_m1_transcription.py',
            'one_per_state_transcription.py',
            'organize_whisper_transcriptions.py',
            'transcribe_ten_states.py',
            'simple_demo.py'
        ],
        'remove_old_alignment': [
            'keyword_alignment.py',
            'robust_alignment.py',
            'stt_alignment.py',
            'word_level_extractor.py',
            'word_level_feature_extractor.py'
        ],
        'organize_directories': {
            'transcriptions/': [
                'WhisperTranscription/',
                'reliable_transcriptions/',
                'simple_stt_dataset/',
                'ten_states_transcriptions/',
                'ultra_fast_transcriptions/',
                'simple_rich_transcriptions/'
            ],
            'datasets/': [
                'mfa_dataset/',
                'keyword_dataset/',
                'minimal_dataset/',
                'phrase_dataset/',
                'unscripted_dataset/',
                'word_features/'
            ]
        }
    }
    
    print("📋 RECOMMENDED ACTIONS:")
    
    print("\n✅ KEEP (Core files):")
    for file in suggestions['keep_core']:
        if Path(file).exists():
            print(f"   - {file}")
    
    print("\n✅ KEEP (Best transcription script):")
    for file in suggestions['keep_best_transcription']:
        if Path(file).exists():
            print(f"   - {file}")
    
    print("\n❌ REMOVE (Duplicate transcription scripts):")
    for file in suggestions['remove_duplicates']:
        if Path(file).exists():
            print(f"   - {file}")
    
    print("\n❌ REMOVE (Old alignment scripts):")
    for file in suggestions['remove_old_alignment']:
        if Path(file).exists():
            print(f"   - {file}")
    
    print("\n📁 ORGANIZE (Group directories):")
    for new_dir, old_dirs in suggestions['organize_directories'].items():
        print(f"   {new_dir}:")
        for old_dir in old_dirs:
            if Path(old_dir).exists():
                print(f"     - {old_dir}")
    
    return suggestions

def create_cleanup_script(suggestions):
    """Create a cleanup script."""
    cleanup_script = """#!/usr/bin/env python3
\"\"\"
Cleanup script for project organization.
\"\"\"

import os
import shutil
from pathlib import Path

def cleanup_project():
    \"\"\"Clean up the project directory.\"\"\"
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
"""
    
    with open("cleanup_project.py", "w") as f:
        f.write(cleanup_script)
    
    print(f"\n📝 Created cleanup script: cleanup_project.py")

def main():
    """Main organization function."""
    print("=== PROJECT ORGANIZATION ===")
    print("Analyzing current directory structure...")
    
    # Analyze directory
    categories = analyze_directory()
    
    # Identify duplicates
    script_groups = identify_duplicates()
    
    # Suggest organization
    suggestions = suggest_organization()
    
    # Create cleanup script
    create_cleanup_script(suggestions)
    
    print(f"\n🎯 NEXT STEPS:")
    print(f"   1. Review the suggestions above")
    print(f"   2. Run: python cleanup_project.py")
    print(f"   3. Manually organize remaining directories")
    print(f"   4. Keep only the essential files")

if __name__ == "__main__":
    main()
