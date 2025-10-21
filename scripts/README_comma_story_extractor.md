# Comma Story Extractor

This script identifies and extracts the "Comma Gets a Cure" story from transcription files using fuzzy matching to handle transcription variations and reading errors.

## Features

- **Fuzzy Matching**: Handles transcription variations like "Kama" vs "Comma", "Therapy" vs "Sarah Perry"
- **Confidence Scoring**: Calculates confidence that a transcription contains the comma story
- **Segment Extraction**: Extracts only the story portions, preserving timing information
- **Batch Processing**: Process multiple files or entire directories
- **Robust Error Handling**: Gracefully handles files that don't contain the story

## Usage

### Single File
```bash
python scripts/comma_story_extractor.py path/to/transcription.json -o output_directory
```

### Batch Processing
```bash
python scripts/comma_story_extractor.py path/to/transcription_directory/ -o output_directory --pattern "*.json"
```

## Output Format

The script creates JSON files with the following structure:

```json
{
  "original_file": "path/to/original.json",
  "confidence": 1.0,
  "start_segment": 2,
  "end_segment": 36,
  "story_text": "Well, here's a story for you...",
  "segments": [...],
  "metadata": {
    "total_segments": 50,
    "story_segments": 35,
    "start_time": 13.08,
    "end_time": 120.45
  }
}
```

## Key Features

### Fuzzy Matching
The script uses multiple strategies to identify the comma story:

1. **Key Phrase Matching**: Identifies important phrases like "Sarah Perry", "veterinary nurse", "Duke Street Tower"
2. **Alternative Spellings**: Handles common transcription errors like "Kama" vs "Comma"
3. **Confidence Scoring**: Weights important phrases more heavily for better accuracy

### Story Boundaries
- **Start**: Looks for phrases like "here's a story for you", "Sarah Perry", "veterinary nurse"
- **End**: Identifies ending phrases like "can't imagine paying so much", "millionaire lawyer"

### Confidence Thresholds
- High confidence (≥0.7): Very likely to contain the story
- Medium confidence (0.3-0.7): May contain the story with variations
- Low confidence (<0.3): Unlikely to contain the story

## Examples

### Process a single transcription
```bash
python scripts/comma_story_extractor.py transcriptions/WhisperTranscription/nevada/nevada-1_whisper.json -o comma_story_extracts
```

### Process all whisper transcriptions
```bash
python scripts/comma_story_extractor.py transcriptions/WhisperTranscription/ -o comma_story_extracts --pattern "*whisper.json"
```

### Process a specific state
```bash
python scripts/comma_story_extractor.py transcriptions/WhisperTranscription/texas/ -o comma_story_extracts
```

## Error Handling

The script handles various error conditions:

- **Low Confidence**: Files with confidence < 0.3 are skipped
- **Missing Story Start**: Files where the story beginning cannot be identified
- **Missing Story End**: Files where the story ending cannot be identified (uses all remaining segments)
- **File Errors**: JSON parsing errors, missing files, etc.

## Performance

- Processes files individually for memory efficiency
- Uses fuzzy string matching for robust transcription handling
- Preserves original segment timing information
- Creates clean, structured output files

## Dependencies

- Python 3.6+
- Standard library only (json, pathlib, re, difflib, argparse)
