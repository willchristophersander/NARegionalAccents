#!/bin/bash
# Generated script to extract comma story audio segments
# Output directory: all_states_aligned/audio_segments

set -e

mkdir -p all_states_aligned/audio_segments

# Well, here's a story for you
mkdir -p all_states_aligned/audio_segments/sentence_0

# Extract montana-2_whisper - 13.04s to 20.08s
ffmpeg -i "audio/montana/montana-2.mp3" -ss 13.04 -t 7.04 -c copy "all_states_aligned/audio_segments/sentence_0/montana-2_whisper.mp3"

# Extract north-dakota-1_whisper - 12.00s to 21.00s
ffmpeg -i "audio/north-dakota/north-dakota-1.mp3" -ss 12.00 -t 9.00 -c copy "all_states_aligned/audio_segments/sentence_0/north-dakota-1_whisper.mp3"

# Extract north-carolina-10_whisper - 10.00s to 17.00s
ffmpeg -i "audio/north-carolina/north-carolina-10.mp3" -ss 10.00 -t 7.00 -c copy "all_states_aligned/audio_segments/sentence_0/north-carolina-10_whisper.mp3"

# Extract oklahoma-9_whisper - 12.00s to 21.00s
ffmpeg -i "audio/oklahoma/oklahoma-9.mp3" -ss 12.00 -t 9.00 -c copy "all_states_aligned/audio_segments/sentence_0/oklahoma-9_whisper.mp3"

# Extract mississippi-9_whisper - 13.00s to 24.00s
ffmpeg -i "audio/mississippi/mississippi-9.mp3" -ss 13.00 -t 11.00 -c copy "all_states_aligned/audio_segments/sentence_0/mississippi-9_whisper.mp3"

# Extract nebraska-2_whisper - 11.00s to 20.00s
ffmpeg -i "audio/nebraska/nebraska-2.mp3" -ss 11.00 -t 9.00 -c copy "all_states_aligned/audio_segments/sentence_0/nebraska-2_whisper.mp3"

# Extract new-mexico-4_whisper - 12.00s to 23.00s
ffmpeg -i "audio/new-mexico/new-mexico-4.mp3" -ss 12.00 -t 11.00 -c copy "all_states_aligned/audio_segments/sentence_0/new-mexico-4_whisper.mp3"

# Extract michigan-15_whisper - 13.20s to 14.68s
ffmpeg -i "audio/michigan/michigan-15.mp3" -ss 13.20 -t 1.48 -c copy "all_states_aligned/audio_segments/sentence_0/michigan-15_whisper.mp3"

# Extract south-dakota-1_whisper - 13.00s to 21.00s
ffmpeg -i "audio/south-dakota/south-dakota-1.mp3" -ss 13.00 -t 8.00 -c copy "all_states_aligned/audio_segments/sentence_0/south-dakota-1_whisper.mp3"

# Extract rhode-island-1_whisper - 12.68s to 15.96s
ffmpeg -i "audio/rhode-island/rhode-island-1.mp3" -ss 12.68 -t 3.28 -c copy "all_states_aligned/audio_segments/sentence_0/rhode-island-1_whisper.mp3"

# Extract received-pronunciation-4_whisper - 12.30s to 14.80s
ffmpeg -i "audio/received-pronunciation/received-pronunciation-4.mp3" -ss 12.30 -t 2.50 -c copy "all_states_aligned/audio_segments/sentence_0/received-pronunciation-4_whisper.mp3"

# Extract nevada-1_whisper - 13.08s to 16.28s
ffmpeg -i "audio/nevada/nevada-1.mp3" -ss 13.08 -t 3.20 -c copy "all_states_aligned/audio_segments/sentence_0/nevada-1_whisper.mp3"

# Extract new-jersey-8_whisper - 12.12s to 13.96s
ffmpeg -i "audio/new-jersey/new-jersey-8.mp3" -ss 12.12 -t 1.84 -c copy "all_states_aligned/audio_segments/sentence_0/new-jersey-8_whisper.mp3"

# Extract ohio-3_whisper - 10.96s to 17.00s
ffmpeg -i "audio/ohio/ohio-3.mp3" -ss 10.96 -t 6.04 -c copy "all_states_aligned/audio_segments/sentence_0/ohio-3_whisper.mp3"

# Extract oregon-4_whisper - 12.96s to 18.56s
ffmpeg -i "audio/oregon/oregon-4.mp3" -ss 12.96 -t 5.60 -c copy "all_states_aligned/audio_segments/sentence_0/oregon-4_whisper.mp3"

# Extract minnesota-9_whisper - 12.38s to 14.80s
ffmpeg -i "audio/minnesota/minnesota-9.mp3" -ss 12.38 -t 2.42 -c copy "all_states_aligned/audio_segments/sentence_0/minnesota-9_whisper.mp3"

# Sarah Perry was a veterinary nurse who had been working daily at an old zoo in a deserted district of the territory
mkdir -p all_states_aligned/audio_segments/sentence_1

# Extract montana-2_whisper - 13.04s to 20.08s
ffmpeg -i "audio/montana/montana-2.mp3" -ss 13.04 -t 7.04 -c copy "all_states_aligned/audio_segments/sentence_1/montana-2_whisper.mp3"

# Extract north-dakota-1_whisper - 12.00s to 21.00s
ffmpeg -i "audio/north-dakota/north-dakota-1.mp3" -ss 12.00 -t 9.00 -c copy "all_states_aligned/audio_segments/sentence_1/north-dakota-1_whisper.mp3"

# Extract north-carolina-10_whisper - 10.00s to 17.00s
ffmpeg -i "audio/north-carolina/north-carolina-10.mp3" -ss 10.00 -t 7.00 -c copy "all_states_aligned/audio_segments/sentence_1/north-carolina-10_whisper.mp3"

# Extract south-carolina-9_whisper - 17.00s to 28.00s
ffmpeg -i "audio/south-carolina/south-carolina-9.mp3" -ss 17.00 -t 11.00 -c copy "all_states_aligned/audio_segments/sentence_1/south-carolina-9_whisper.mp3"

# Extract oklahoma-9_whisper - 12.00s to 21.00s
ffmpeg -i "audio/oklahoma/oklahoma-9.mp3" -ss 12.00 -t 9.00 -c copy "all_states_aligned/audio_segments/sentence_1/oklahoma-9_whisper.mp3"

# Extract mississippi-9_whisper - 13.00s to 24.00s
ffmpeg -i "audio/mississippi/mississippi-9.mp3" -ss 13.00 -t 11.00 -c copy "all_states_aligned/audio_segments/sentence_1/mississippi-9_whisper.mp3"

# Extract nebraska-2_whisper - 11.00s to 20.00s
ffmpeg -i "audio/nebraska/nebraska-2.mp3" -ss 11.00 -t 9.00 -c copy "all_states_aligned/audio_segments/sentence_1/nebraska-2_whisper.mp3"

# Extract new-mexico-4_whisper - 12.00s to 23.00s
ffmpeg -i "audio/new-mexico/new-mexico-4.mp3" -ss 12.00 -t 11.00 -c copy "all_states_aligned/audio_segments/sentence_1/new-mexico-4_whisper.mp3"

# Extract michigan-15_whisper - 14.68s to 20.16s
ffmpeg -i "audio/michigan/michigan-15.mp3" -ss 14.68 -t 5.48 -c copy "all_states_aligned/audio_segments/sentence_1/michigan-15_whisper.mp3"

# Extract south-dakota-1_whisper - 13.00s to 21.00s
ffmpeg -i "audio/south-dakota/south-dakota-1.mp3" -ss 13.00 -t 8.00 -c copy "all_states_aligned/audio_segments/sentence_1/south-dakota-1_whisper.mp3"

# Extract rhode-island-1_whisper - 15.96s to 21.68s
ffmpeg -i "audio/rhode-island/rhode-island-1.mp3" -ss 15.96 -t 5.72 -c copy "all_states_aligned/audio_segments/sentence_1/rhode-island-1_whisper.mp3"

# Extract received-pronunciation-4_whisper - 14.80s to 20.90s
ffmpeg -i "audio/received-pronunciation/received-pronunciation-4.mp3" -ss 14.80 -t 6.10 -c copy "all_states_aligned/audio_segments/sentence_1/received-pronunciation-4_whisper.mp3"

# Extract nevada-1_whisper - 16.28s to 20.32s
ffmpeg -i "audio/nevada/nevada-1.mp3" -ss 16.28 -t 4.04 -c copy "all_states_aligned/audio_segments/sentence_1/nevada-1_whisper.mp3"

# Extract new-jersey-8_whisper - 13.96s to 18.56s
ffmpeg -i "audio/new-jersey/new-jersey-8.mp3" -ss 13.96 -t 4.60 -c copy "all_states_aligned/audio_segments/sentence_1/new-jersey-8_whisper.mp3"

# Extract ohio-3_whisper - 10.96s to 17.00s
ffmpeg -i "audio/ohio/ohio-3.mp3" -ss 10.96 -t 6.04 -c copy "all_states_aligned/audio_segments/sentence_1/ohio-3_whisper.mp3"

# Extract oregon-4_whisper - 12.96s to 18.56s
ffmpeg -i "audio/oregon/oregon-4.mp3" -ss 12.96 -t 5.60 -c copy "all_states_aligned/audio_segments/sentence_1/oregon-4_whisper.mp3"

# Extract minnesota-9_whisper - 14.80s to 20.32s
ffmpeg -i "audio/minnesota/minnesota-9.mp3" -ss 14.80 -t 5.52 -c copy "all_states_aligned/audio_segments/sentence_1/minnesota-9_whisper.mp3"

# Extract pennsylvania-5_whisper - 15.00s to 20.00s
ffmpeg -i "audio/pennsylvania/pennsylvania-5.mp3" -ss 15.00 -t 5.00 -c copy "all_states_aligned/audio_segments/sentence_1/pennsylvania-5_whisper.mp3"

# so she was very happy to start a new job at a superb private practice in north square near the Duke Street Tower
mkdir -p all_states_aligned/audio_segments/sentence_2

# Extract montana-2_whisper - 27.12s to 33.60s
ffmpeg -i "audio/montana/montana-2.mp3" -ss 27.12 -t 6.48 -c copy "all_states_aligned/audio_segments/sentence_2/montana-2_whisper.mp3"

# Extract north-dakota-1_whisper - 21.00s to 31.00s
ffmpeg -i "audio/north-dakota/north-dakota-1.mp3" -ss 21.00 -t 10.00 -c copy "all_states_aligned/audio_segments/sentence_2/north-dakota-1_whisper.mp3"

# Extract north-carolina-10_whisper - 17.00s to 22.00s
ffmpeg -i "audio/north-carolina/north-carolina-10.mp3" -ss 17.00 -t 5.00 -c copy "all_states_aligned/audio_segments/sentence_2/north-carolina-10_whisper.mp3"

# Extract south-carolina-9_whisper - 28.00s to 39.00s
ffmpeg -i "audio/south-carolina/south-carolina-9.mp3" -ss 28.00 -t 11.00 -c copy "all_states_aligned/audio_segments/sentence_2/south-carolina-9_whisper.mp3"

# Extract oklahoma-9_whisper - 21.00s to 28.00s
ffmpeg -i "audio/oklahoma/oklahoma-9.mp3" -ss 21.00 -t 7.00 -c copy "all_states_aligned/audio_segments/sentence_2/oklahoma-9_whisper.mp3"

# Extract mississippi-9_whisper - 24.00s to 32.00s
ffmpeg -i "audio/mississippi/mississippi-9.mp3" -ss 24.00 -t 8.00 -c copy "all_states_aligned/audio_segments/sentence_2/mississippi-9_whisper.mp3"

# Extract nebraska-2_whisper - 20.00s to 27.00s
ffmpeg -i "audio/nebraska/nebraska-2.mp3" -ss 20.00 -t 7.00 -c copy "all_states_aligned/audio_segments/sentence_2/nebraska-2_whisper.mp3"

# Extract new-mexico-4_whisper - 23.00s to 28.00s
ffmpeg -i "audio/new-mexico/new-mexico-4.mp3" -ss 23.00 -t 5.00 -c copy "all_states_aligned/audio_segments/sentence_2/new-mexico-4_whisper.mp3"

# Extract michigan-15_whisper - 20.16s to 25.52s
ffmpeg -i "audio/michigan/michigan-15.mp3" -ss 20.16 -t 5.36 -c copy "all_states_aligned/audio_segments/sentence_2/michigan-15_whisper.mp3"

# Extract south-dakota-1_whisper - 21.00s to 28.50s
ffmpeg -i "audio/south-dakota/south-dakota-1.mp3" -ss 21.00 -t 7.50 -c copy "all_states_aligned/audio_segments/sentence_2/south-dakota-1_whisper.mp3"

# Extract rhode-island-1_whisper - 24.40s to 29.24s
ffmpeg -i "audio/rhode-island/rhode-island-1.mp3" -ss 24.40 -t 4.84 -c copy "all_states_aligned/audio_segments/sentence_2/rhode-island-1_whisper.mp3"

# Extract received-pronunciation-4_whisper - 20.90s to 28.10s
ffmpeg -i "audio/received-pronunciation/received-pronunciation-4.mp3" -ss 20.90 -t 7.20 -c copy "all_states_aligned/audio_segments/sentence_2/received-pronunciation-4_whisper.mp3"

# Extract nevada-1_whisper - 24.62s to 27.84s
ffmpeg -i "audio/nevada/nevada-1.mp3" -ss 24.62 -t 3.22 -c copy "all_states_aligned/audio_segments/sentence_2/nevada-1_whisper.mp3"

# Extract new-jersey-8_whisper - 23.32s to 26.76s
ffmpeg -i "audio/new-jersey/new-jersey-8.mp3" -ss 23.32 -t 3.44 -c copy "all_states_aligned/audio_segments/sentence_2/new-jersey-8_whisper.mp3"

# Extract ohio-3_whisper - 21.16s to 29.16s
ffmpeg -i "audio/ohio/ohio-3.mp3" -ss 21.16 -t 8.00 -c copy "all_states_aligned/audio_segments/sentence_2/ohio-3_whisper.mp3"

# Extract oregon-4_whisper - 25.12s to 30.32s
ffmpeg -i "audio/oregon/oregon-4.mp3" -ss 25.12 -t 5.20 -c copy "all_states_aligned/audio_segments/sentence_2/oregon-4_whisper.mp3"

# Extract minnesota-9_whisper - 25.32s to 29.68s
ffmpeg -i "audio/minnesota/minnesota-9.mp3" -ss 25.32 -t 4.36 -c copy "all_states_aligned/audio_segments/sentence_2/minnesota-9_whisper.mp3"

# Extract pennsylvania-5_whisper - 25.50s to 29.50s
ffmpeg -i "audio/pennsylvania/pennsylvania-5.mp3" -ss 25.50 -t 4.00 -c copy "all_states_aligned/audio_segments/sentence_2/pennsylvania-5_whisper.mp3"

# That area was much nearer for her and more to her liking
mkdir -p all_states_aligned/audio_segments/sentence_3

# Extract montana-2_whisper - 34.72s to 42.08s
ffmpeg -i "audio/montana/montana-2.mp3" -ss 34.72 -t 7.36 -c copy "all_states_aligned/audio_segments/sentence_3/montana-2_whisper.mp3"

# Extract north-dakota-1_whisper - 31.00s to 38.00s
ffmpeg -i "audio/north-dakota/north-dakota-1.mp3" -ss 31.00 -t 7.00 -c copy "all_states_aligned/audio_segments/sentence_3/north-dakota-1_whisper.mp3"

# Extract north-carolina-10_whisper - 22.00s to 26.00s
ffmpeg -i "audio/north-carolina/north-carolina-10.mp3" -ss 22.00 -t 4.00 -c copy "all_states_aligned/audio_segments/sentence_3/north-carolina-10_whisper.mp3"

# Extract south-carolina-9_whisper - 39.00s to 45.00s
ffmpeg -i "audio/south-carolina/south-carolina-9.mp3" -ss 39.00 -t 6.00 -c copy "all_states_aligned/audio_segments/sentence_3/south-carolina-9_whisper.mp3"

# Extract oklahoma-9_whisper - 28.00s to 31.00s
ffmpeg -i "audio/oklahoma/oklahoma-9.mp3" -ss 28.00 -t 3.00 -c copy "all_states_aligned/audio_segments/sentence_3/oklahoma-9_whisper.mp3"

# Extract mississippi-9_whisper - 32.00s to 39.00s
ffmpeg -i "audio/mississippi/mississippi-9.mp3" -ss 32.00 -t 7.00 -c copy "all_states_aligned/audio_segments/sentence_3/mississippi-9_whisper.mp3"

# Extract nebraska-2_whisper - 27.00s to 32.00s
ffmpeg -i "audio/nebraska/nebraska-2.mp3" -ss 27.00 -t 5.00 -c copy "all_states_aligned/audio_segments/sentence_3/nebraska-2_whisper.mp3"

# Extract new-mexico-4_whisper - 28.00s to 33.00s
ffmpeg -i "audio/new-mexico/new-mexico-4.mp3" -ss 28.00 -t 5.00 -c copy "all_states_aligned/audio_segments/sentence_3/new-mexico-4_whisper.mp3"

# Extract michigan-15_whisper - 25.52s to 28.44s
ffmpeg -i "audio/michigan/michigan-15.mp3" -ss 25.52 -t 2.92 -c copy "all_states_aligned/audio_segments/sentence_3/michigan-15_whisper.mp3"

# Extract south-dakota-1_whisper - 28.50s to 35.50s
ffmpeg -i "audio/south-dakota/south-dakota-1.mp3" -ss 28.50 -t 7.00 -c copy "all_states_aligned/audio_segments/sentence_3/south-dakota-1_whisper.mp3"

# Extract rhode-island-1_whisper - 32.88s to 37.56s
ffmpeg -i "audio/rhode-island/rhode-island-1.mp3" -ss 32.88 -t 4.68 -c copy "all_states_aligned/audio_segments/sentence_3/rhode-island-1_whisper.mp3"

# Extract received-pronunciation-4_whisper - 28.30s to 31.90s
ffmpeg -i "audio/received-pronunciation/received-pronunciation-4.mp3" -ss 28.30 -t 3.60 -c copy "all_states_aligned/audio_segments/sentence_3/received-pronunciation-4_whisper.mp3"

# Extract nevada-1_whisper - 27.84s to 31.38s
ffmpeg -i "audio/nevada/nevada-1.mp3" -ss 27.84 -t 3.54 -c copy "all_states_aligned/audio_segments/sentence_3/nevada-1_whisper.mp3"

# Extract new-jersey-8_whisper - 26.76s to 30.52s
ffmpeg -i "audio/new-jersey/new-jersey-8.mp3" -ss 26.76 -t 3.76 -c copy "all_states_aligned/audio_segments/sentence_3/new-jersey-8_whisper.mp3"

# Extract ohio-3_whisper - 29.16s to 38.88s
ffmpeg -i "audio/ohio/ohio-3.mp3" -ss 29.16 -t 9.72 -c copy "all_states_aligned/audio_segments/sentence_3/ohio-3_whisper.mp3"

# Extract oregon-4_whisper - 31.20s to 38.88s
ffmpeg -i "audio/oregon/oregon-4.mp3" -ss 31.20 -t 7.68 -c copy "all_states_aligned/audio_segments/sentence_3/oregon-4_whisper.mp3"

# Extract minnesota-9_whisper - 29.68s to 34.40s
ffmpeg -i "audio/minnesota/minnesota-9.mp3" -ss 29.68 -t 4.72 -c copy "all_states_aligned/audio_segments/sentence_3/minnesota-9_whisper.mp3"

# Extract pennsylvania-5_whisper - 29.50s to 33.50s
ffmpeg -i "audio/pennsylvania/pennsylvania-5.mp3" -ss 29.50 -t 4.00 -c copy "all_states_aligned/audio_segments/sentence_3/pennsylvania-5_whisper.mp3"

# Even so, on her first morning, she felt stressed
mkdir -p all_states_aligned/audio_segments/sentence_4

# Extract montana-2_whisper - 34.72s to 42.08s
ffmpeg -i "audio/montana/montana-2.mp3" -ss 34.72 -t 7.36 -c copy "all_states_aligned/audio_segments/sentence_4/montana-2_whisper.mp3"

# Extract north-dakota-1_whisper - 31.00s to 38.00s
ffmpeg -i "audio/north-dakota/north-dakota-1.mp3" -ss 31.00 -t 7.00 -c copy "all_states_aligned/audio_segments/sentence_4/north-dakota-1_whisper.mp3"

# Extract north-carolina-10_whisper - 26.00s to 32.00s
ffmpeg -i "audio/north-carolina/north-carolina-10.mp3" -ss 26.00 -t 6.00 -c copy "all_states_aligned/audio_segments/sentence_4/north-carolina-10_whisper.mp3"

# Extract south-carolina-9_whisper - 45.00s to 50.00s
ffmpeg -i "audio/south-carolina/south-carolina-9.mp3" -ss 45.00 -t 5.00 -c copy "all_states_aligned/audio_segments/sentence_4/south-carolina-9_whisper.mp3"

# Extract oklahoma-9_whisper - 31.00s to 34.00s
ffmpeg -i "audio/oklahoma/oklahoma-9.mp3" -ss 31.00 -t 3.00 -c copy "all_states_aligned/audio_segments/sentence_4/oklahoma-9_whisper.mp3"

# Extract mississippi-9_whisper - 32.00s to 39.00s
ffmpeg -i "audio/mississippi/mississippi-9.mp3" -ss 32.00 -t 7.00 -c copy "all_states_aligned/audio_segments/sentence_4/mississippi-9_whisper.mp3"

# Extract nebraska-2_whisper - 32.00s to 36.00s
ffmpeg -i "audio/nebraska/nebraska-2.mp3" -ss 32.00 -t 4.00 -c copy "all_states_aligned/audio_segments/sentence_4/nebraska-2_whisper.mp3"

# Extract new-mexico-4_whisper - 33.00s to 37.00s
ffmpeg -i "audio/new-mexico/new-mexico-4.mp3" -ss 33.00 -t 4.00 -c copy "all_states_aligned/audio_segments/sentence_4/new-mexico-4_whisper.mp3"

# Extract michigan-15_whisper - 28.52s to 31.24s
ffmpeg -i "audio/michigan/michigan-15.mp3" -ss 28.52 -t 2.72 -c copy "all_states_aligned/audio_segments/sentence_4/michigan-15_whisper.mp3"

# Extract south-dakota-1_whisper - 28.50s to 35.50s
ffmpeg -i "audio/south-dakota/south-dakota-1.mp3" -ss 28.50 -t 7.00 -c copy "all_states_aligned/audio_segments/sentence_4/south-dakota-1_whisper.mp3"

# Extract rhode-island-1_whisper - 37.56s to 41.84s
ffmpeg -i "audio/rhode-island/rhode-island-1.mp3" -ss 37.56 -t 4.28 -c copy "all_states_aligned/audio_segments/sentence_4/rhode-island-1_whisper.mp3"

# Extract received-pronunciation-4_whisper - 31.90s to 35.40s
ffmpeg -i "audio/received-pronunciation/received-pronunciation-4.mp3" -ss 31.90 -t 3.50 -c copy "all_states_aligned/audio_segments/sentence_4/received-pronunciation-4_whisper.mp3"

# Extract nevada-1_whisper - 31.38s to 34.72s
ffmpeg -i "audio/nevada/nevada-1.mp3" -ss 31.38 -t 3.34 -c copy "all_states_aligned/audio_segments/sentence_4/nevada-1_whisper.mp3"

# Extract new-jersey-8_whisper - 30.52s to 33.34s
ffmpeg -i "audio/new-jersey/new-jersey-8.mp3" -ss 30.52 -t 2.82 -c copy "all_states_aligned/audio_segments/sentence_4/new-jersey-8_whisper.mp3"

# Extract ohio-3_whisper - 29.16s to 38.88s
ffmpeg -i "audio/ohio/ohio-3.mp3" -ss 29.16 -t 9.72 -c copy "all_states_aligned/audio_segments/sentence_4/ohio-3_whisper.mp3"

# Extract oregon-4_whisper - 31.20s to 38.88s
ffmpeg -i "audio/oregon/oregon-4.mp3" -ss 31.20 -t 7.68 -c copy "all_states_aligned/audio_segments/sentence_4/oregon-4_whisper.mp3"

# Extract minnesota-9_whisper - 34.40s to 37.40s
ffmpeg -i "audio/minnesota/minnesota-9.mp3" -ss 34.40 -t 3.00 -c copy "all_states_aligned/audio_segments/sentence_4/minnesota-9_whisper.mp3"

# Extract pennsylvania-5_whisper - 33.50s to 36.50s
ffmpeg -i "audio/pennsylvania/pennsylvania-5.mp3" -ss 33.50 -t 3.00 -c copy "all_states_aligned/audio_segments/sentence_4/pennsylvania-5_whisper.mp3"

# She ate a bowl of porridge, checked herself in the mirror and washed her face in a hurry
mkdir -p all_states_aligned/audio_segments/sentence_5

# Extract montana-2_whisper - 42.08s to 49.52s
ffmpeg -i "audio/montana/montana-2.mp3" -ss 42.08 -t 7.44 -c copy "all_states_aligned/audio_segments/sentence_5/montana-2_whisper.mp3"

# Extract north-dakota-1_whisper - 38.00s to 43.00s
ffmpeg -i "audio/north-dakota/north-dakota-1.mp3" -ss 38.00 -t 5.00 -c copy "all_states_aligned/audio_segments/sentence_5/north-dakota-1_whisper.mp3"

# Extract north-carolina-10_whisper - 26.00s to 32.00s
ffmpeg -i "audio/north-carolina/north-carolina-10.mp3" -ss 26.00 -t 6.00 -c copy "all_states_aligned/audio_segments/sentence_5/north-carolina-10_whisper.mp3"

# Extract south-carolina-9_whisper - 50.00s to 58.00s
ffmpeg -i "audio/south-carolina/south-carolina-9.mp3" -ss 50.00 -t 8.00 -c copy "all_states_aligned/audio_segments/sentence_5/south-carolina-9_whisper.mp3"

# Extract oklahoma-9_whisper - 34.00s to 39.00s
ffmpeg -i "audio/oklahoma/oklahoma-9.mp3" -ss 34.00 -t 5.00 -c copy "all_states_aligned/audio_segments/sentence_5/oklahoma-9_whisper.mp3"

# Extract mississippi-9_whisper - 39.00s to 46.00s
ffmpeg -i "audio/mississippi/mississippi-9.mp3" -ss 39.00 -t 7.00 -c copy "all_states_aligned/audio_segments/sentence_5/mississippi-9_whisper.mp3"

# Extract nebraska-2_whisper - 36.00s to 41.00s
ffmpeg -i "audio/nebraska/nebraska-2.mp3" -ss 36.00 -t 5.00 -c copy "all_states_aligned/audio_segments/sentence_5/nebraska-2_whisper.mp3"

# Extract new-mexico-4_whisper - 37.00s to 42.00s
ffmpeg -i "audio/new-mexico/new-mexico-4.mp3" -ss 37.00 -t 5.00 -c copy "all_states_aligned/audio_segments/sentence_5/new-mexico-4_whisper.mp3"

# Extract michigan-15_whisper - 31.24s to 35.04s
ffmpeg -i "audio/michigan/michigan-15.mp3" -ss 31.24 -t 3.80 -c copy "all_states_aligned/audio_segments/sentence_5/michigan-15_whisper.mp3"

# Extract south-dakota-1_whisper - 35.50s to 40.50s
ffmpeg -i "audio/south-dakota/south-dakota-1.mp3" -ss 35.50 -t 5.00 -c copy "all_states_aligned/audio_segments/sentence_5/south-dakota-1_whisper.mp3"

# Extract rhode-island-1_whisper - 41.84s to 45.32s
ffmpeg -i "audio/rhode-island/rhode-island-1.mp3" -ss 41.84 -t 3.48 -c copy "all_states_aligned/audio_segments/sentence_5/rhode-island-1_whisper.mp3"

# Extract received-pronunciation-4_whisper - 35.40s to 40.60s
ffmpeg -i "audio/received-pronunciation/received-pronunciation-4.mp3" -ss 35.40 -t 5.20 -c copy "all_states_aligned/audio_segments/sentence_5/received-pronunciation-4_whisper.mp3"

# Extract nevada-1_whisper - 34.72s to 38.44s
ffmpeg -i "audio/nevada/nevada-1.mp3" -ss 34.72 -t 3.72 -c copy "all_states_aligned/audio_segments/sentence_5/nevada-1_whisper.mp3"

# Extract new-jersey-8_whisper - 33.34s to 38.08s
ffmpeg -i "audio/new-jersey/new-jersey-8.mp3" -ss 33.34 -t 4.74 -c copy "all_states_aligned/audio_segments/sentence_5/new-jersey-8_whisper.mp3"

# Extract ohio-3_whisper - 38.88s to 43.68s
ffmpeg -i "audio/ohio/ohio-3.mp3" -ss 38.88 -t 4.80 -c copy "all_states_aligned/audio_segments/sentence_5/ohio-3_whisper.mp3"

# Extract oregon-4_whisper - 38.88s to 45.04s
ffmpeg -i "audio/oregon/oregon-4.mp3" -ss 38.88 -t 6.16 -c copy "all_states_aligned/audio_segments/sentence_5/oregon-4_whisper.mp3"

# Extract minnesota-9_whisper - 37.40s to 43.80s
ffmpeg -i "audio/minnesota/minnesota-9.mp3" -ss 37.40 -t 6.40 -c copy "all_states_aligned/audio_segments/sentence_5/minnesota-9_whisper.mp3"

# Extract pennsylvania-5_whisper - 36.50s to 41.50s
ffmpeg -i "audio/pennsylvania/pennsylvania-5.mp3" -ss 36.50 -t 5.00 -c copy "all_states_aligned/audio_segments/sentence_5/pennsylvania-5_whisper.mp3"

# Then she put on a plain yellow dress and a fleece jacket, picked up her kit and headed for work
mkdir -p all_states_aligned/audio_segments/sentence_6

# Extract montana-2_whisper - 49.52s to 55.28s
ffmpeg -i "audio/montana/montana-2.mp3" -ss 49.52 -t 5.76 -c copy "all_states_aligned/audio_segments/sentence_6/montana-2_whisper.mp3"

# Extract north-dakota-1_whisper - 43.00s to 49.00s
ffmpeg -i "audio/north-dakota/north-dakota-1.mp3" -ss 43.00 -t 6.00 -c copy "all_states_aligned/audio_segments/sentence_6/north-dakota-1_whisper.mp3"

# Extract north-carolina-10_whisper - 32.00s to 38.00s
ffmpeg -i "audio/north-carolina/north-carolina-10.mp3" -ss 32.00 -t 6.00 -c copy "all_states_aligned/audio_segments/sentence_6/north-carolina-10_whisper.mp3"

# Extract south-carolina-9_whisper - 58.00s to 68.00s
ffmpeg -i "audio/south-carolina/south-carolina-9.mp3" -ss 58.00 -t 10.00 -c copy "all_states_aligned/audio_segments/sentence_6/south-carolina-9_whisper.mp3"

# Extract oklahoma-9_whisper - 39.00s to 45.00s
ffmpeg -i "audio/oklahoma/oklahoma-9.mp3" -ss 39.00 -t 6.00 -c copy "all_states_aligned/audio_segments/sentence_6/oklahoma-9_whisper.mp3"

# Extract mississippi-9_whisper - 46.00s to 53.00s
ffmpeg -i "audio/mississippi/mississippi-9.mp3" -ss 46.00 -t 7.00 -c copy "all_states_aligned/audio_segments/sentence_6/mississippi-9_whisper.mp3"

# Extract nebraska-2_whisper - 41.00s to 49.00s
ffmpeg -i "audio/nebraska/nebraska-2.mp3" -ss 41.00 -t 8.00 -c copy "all_states_aligned/audio_segments/sentence_6/nebraska-2_whisper.mp3"

# Extract new-mexico-4_whisper - 42.00s to 48.00s
ffmpeg -i "audio/new-mexico/new-mexico-4.mp3" -ss 42.00 -t 6.00 -c copy "all_states_aligned/audio_segments/sentence_6/new-mexico-4_whisper.mp3"

# Extract michigan-15_whisper - 35.04s to 39.36s
ffmpeg -i "audio/michigan/michigan-15.mp3" -ss 35.04 -t 4.32 -c copy "all_states_aligned/audio_segments/sentence_6/michigan-15_whisper.mp3"

# Extract south-dakota-1_whisper - 40.50s to 46.50s
ffmpeg -i "audio/south-dakota/south-dakota-1.mp3" -ss 40.50 -t 6.00 -c copy "all_states_aligned/audio_segments/sentence_6/south-dakota-1_whisper.mp3"

# Extract rhode-island-1_whisper - 47.56s to 51.56s
ffmpeg -i "audio/rhode-island/rhode-island-1.mp3" -ss 47.56 -t 4.00 -c copy "all_states_aligned/audio_segments/sentence_6/rhode-island-1_whisper.mp3"

# Extract received-pronunciation-4_whisper - 40.60s to 46.80s
ffmpeg -i "audio/received-pronunciation/received-pronunciation-4.mp3" -ss 40.60 -t 6.20 -c copy "all_states_aligned/audio_segments/sentence_6/received-pronunciation-4_whisper.mp3"

# Extract nevada-1_whisper - 38.44s to 41.72s
ffmpeg -i "audio/nevada/nevada-1.mp3" -ss 38.44 -t 3.28 -c copy "all_states_aligned/audio_segments/sentence_6/nevada-1_whisper.mp3"

# Extract new-jersey-8_whisper - 38.08s to 42.08s
ffmpeg -i "audio/new-jersey/new-jersey-8.mp3" -ss 38.08 -t 4.00 -c copy "all_states_aligned/audio_segments/sentence_6/new-jersey-8_whisper.mp3"

# Extract ohio-3_whisper - 43.68s to 50.04s
ffmpeg -i "audio/ohio/ohio-3.mp3" -ss 43.68 -t 6.36 -c copy "all_states_aligned/audio_segments/sentence_6/ohio-3_whisper.mp3"

# Extract oregon-4_whisper - 45.04s to 51.44s
ffmpeg -i "audio/oregon/oregon-4.mp3" -ss 45.04 -t 6.40 -c copy "all_states_aligned/audio_segments/sentence_6/oregon-4_whisper.mp3"

# Extract minnesota-9_whisper - 43.80s to 48.52s
ffmpeg -i "audio/minnesota/minnesota-9.mp3" -ss 43.80 -t 4.72 -c copy "all_states_aligned/audio_segments/sentence_6/minnesota-9_whisper.mp3"

# Extract pennsylvania-5_whisper - 41.50s to 47.50s
ffmpeg -i "audio/pennsylvania/pennsylvania-5.mp3" -ss 41.50 -t 6.00 -c copy "all_states_aligned/audio_segments/sentence_6/pennsylvania-5_whisper.mp3"

# When she got there, there was a woman with a goose waiting for her
mkdir -p all_states_aligned/audio_segments/sentence_7

# Extract montana-2_whisper - 55.28s to 62.40s
ffmpeg -i "audio/montana/montana-2.mp3" -ss 55.28 -t 7.12 -c copy "all_states_aligned/audio_segments/sentence_7/montana-2_whisper.mp3"

# Extract north-dakota-1_whisper - 49.00s to 53.00s
ffmpeg -i "audio/north-dakota/north-dakota-1.mp3" -ss 49.00 -t 4.00 -c copy "all_states_aligned/audio_segments/sentence_7/north-dakota-1_whisper.mp3"

# Extract north-carolina-10_whisper - 38.00s to 41.00s
ffmpeg -i "audio/north-carolina/north-carolina-10.mp3" -ss 38.00 -t 3.00 -c copy "all_states_aligned/audio_segments/sentence_7/north-carolina-10_whisper.mp3"

# Extract south-carolina-9_whisper - 68.00s to 74.00s
ffmpeg -i "audio/south-carolina/south-carolina-9.mp3" -ss 68.00 -t 6.00 -c copy "all_states_aligned/audio_segments/sentence_7/south-carolina-9_whisper.mp3"

# Extract oklahoma-9_whisper - 45.00s to 49.00s
ffmpeg -i "audio/oklahoma/oklahoma-9.mp3" -ss 45.00 -t 4.00 -c copy "all_states_aligned/audio_segments/sentence_7/oklahoma-9_whisper.mp3"

# Extract mississippi-9_whisper - 53.00s to 61.00s
ffmpeg -i "audio/mississippi/mississippi-9.mp3" -ss 53.00 -t 8.00 -c copy "all_states_aligned/audio_segments/sentence_7/mississippi-9_whisper.mp3"

# Extract nebraska-2_whisper - 49.00s to 54.00s
ffmpeg -i "audio/nebraska/nebraska-2.mp3" -ss 49.00 -t 5.00 -c copy "all_states_aligned/audio_segments/sentence_7/nebraska-2_whisper.mp3"

# Extract new-mexico-4_whisper - 48.00s to 51.00s
ffmpeg -i "audio/new-mexico/new-mexico-4.mp3" -ss 48.00 -t 3.00 -c copy "all_states_aligned/audio_segments/sentence_7/new-mexico-4_whisper.mp3"

# Extract michigan-15_whisper - 39.36s to 42.08s
ffmpeg -i "audio/michigan/michigan-15.mp3" -ss 39.36 -t 2.72 -c copy "all_states_aligned/audio_segments/sentence_7/michigan-15_whisper.mp3"

# Extract south-dakota-1_whisper - 46.50s to 50.50s
ffmpeg -i "audio/south-dakota/south-dakota-1.mp3" -ss 46.50 -t 4.00 -c copy "all_states_aligned/audio_segments/sentence_7/south-dakota-1_whisper.mp3"

# Extract rhode-island-1_whisper - 54.20s to 58.72s
ffmpeg -i "audio/rhode-island/rhode-island-1.mp3" -ss 54.20 -t 4.52 -c copy "all_states_aligned/audio_segments/sentence_7/rhode-island-1_whisper.mp3"

# Extract received-pronunciation-4_whisper - 46.80s to 50.20s
ffmpeg -i "audio/received-pronunciation/received-pronunciation-4.mp3" -ss 46.80 -t 3.40 -c copy "all_states_aligned/audio_segments/sentence_7/received-pronunciation-4_whisper.mp3"

# Extract nevada-1_whisper - 43.08s to 46.00s
ffmpeg -i "audio/nevada/nevada-1.mp3" -ss 43.08 -t 2.92 -c copy "all_states_aligned/audio_segments/sentence_7/nevada-1_whisper.mp3"

# Extract new-jersey-8_whisper - 43.56s to 46.80s
ffmpeg -i "audio/new-jersey/new-jersey-8.mp3" -ss 43.56 -t 3.24 -c copy "all_states_aligned/audio_segments/sentence_7/new-jersey-8_whisper.mp3"

# Extract ohio-3_whisper - 50.04s to 54.08s
ffmpeg -i "audio/ohio/ohio-3.mp3" -ss 50.04 -t 4.04 -c copy "all_states_aligned/audio_segments/sentence_7/ohio-3_whisper.mp3"

# Extract oregon-4_whisper - 51.44s to 57.36s
ffmpeg -i "audio/oregon/oregon-4.mp3" -ss 51.44 -t 5.92 -c copy "all_states_aligned/audio_segments/sentence_7/oregon-4_whisper.mp3"

# Extract minnesota-9_whisper - 49.52s to 53.28s
ffmpeg -i "audio/minnesota/minnesota-9.mp3" -ss 49.52 -t 3.76 -c copy "all_states_aligned/audio_segments/sentence_7/minnesota-9_whisper.mp3"

# Extract pennsylvania-5_whisper - 47.50s to 51.50s
ffmpeg -i "audio/pennsylvania/pennsylvania-5.mp3" -ss 47.50 -t 4.00 -c copy "all_states_aligned/audio_segments/sentence_7/pennsylvania-5_whisper.mp3"

# The woman gave Sarah an official letter from the vet
mkdir -p all_states_aligned/audio_segments/sentence_8

# Extract montana-2_whisper - 62.40s to 70.16s
ffmpeg -i "audio/montana/montana-2.mp3" -ss 62.40 -t 7.76 -c copy "all_states_aligned/audio_segments/sentence_8/montana-2_whisper.mp3"

# Extract north-dakota-1_whisper - 53.00s to 56.00s
ffmpeg -i "audio/north-dakota/north-dakota-1.mp3" -ss 53.00 -t 3.00 -c copy "all_states_aligned/audio_segments/sentence_8/north-dakota-1_whisper.mp3"

# Extract south-carolina-9_whisper - 74.00s to 79.00s
ffmpeg -i "audio/south-carolina/south-carolina-9.mp3" -ss 74.00 -t 5.00 -c copy "all_states_aligned/audio_segments/sentence_8/south-carolina-9_whisper.mp3"

# Extract oklahoma-9_whisper - 49.00s to 52.00s
ffmpeg -i "audio/oklahoma/oklahoma-9.mp3" -ss 49.00 -t 3.00 -c copy "all_states_aligned/audio_segments/sentence_8/oklahoma-9_whisper.mp3"

# Extract mississippi-9_whisper - 53.00s to 61.00s
ffmpeg -i "audio/mississippi/mississippi-9.mp3" -ss 53.00 -t 8.00 -c copy "all_states_aligned/audio_segments/sentence_8/mississippi-9_whisper.mp3"

# Extract michigan-15_whisper - 42.08s to 44.32s
ffmpeg -i "audio/michigan/michigan-15.mp3" -ss 42.08 -t 2.24 -c copy "all_states_aligned/audio_segments/sentence_8/michigan-15_whisper.mp3"

# Extract south-dakota-1_whisper - 50.50s to 53.50s
ffmpeg -i "audio/south-dakota/south-dakota-1.mp3" -ss 50.50 -t 3.00 -c copy "all_states_aligned/audio_segments/sentence_8/south-dakota-1_whisper.mp3"

# Extract rhode-island-1_whisper - 58.72s to 62.12s
ffmpeg -i "audio/rhode-island/rhode-island-1.mp3" -ss 58.72 -t 3.40 -c copy "all_states_aligned/audio_segments/sentence_8/rhode-island-1_whisper.mp3"

# Extract received-pronunciation-4_whisper - 50.20s to 53.30s
ffmpeg -i "audio/received-pronunciation/received-pronunciation-4.mp3" -ss 50.20 -t 3.10 -c copy "all_states_aligned/audio_segments/sentence_8/received-pronunciation-4_whisper.mp3"

# Extract nevada-1_whisper - 46.00s to 48.60s
ffmpeg -i "audio/nevada/nevada-1.mp3" -ss 46.00 -t 2.60 -c copy "all_states_aligned/audio_segments/sentence_8/nevada-1_whisper.mp3"

# Extract new-jersey-8_whisper - 46.80s to 49.48s
ffmpeg -i "audio/new-jersey/new-jersey-8.mp3" -ss 46.80 -t 2.68 -c copy "all_states_aligned/audio_segments/sentence_8/new-jersey-8_whisper.mp3"

# Extract ohio-3_whisper - 54.08s to 58.56s
ffmpeg -i "audio/ohio/ohio-3.mp3" -ss 54.08 -t 4.48 -c copy "all_states_aligned/audio_segments/sentence_8/ohio-3_whisper.mp3"

# Extract oregon-4_whisper - 57.36s to 62.96s
ffmpeg -i "audio/oregon/oregon-4.mp3" -ss 57.36 -t 5.60 -c copy "all_states_aligned/audio_segments/sentence_8/oregon-4_whisper.mp3"

# Extract minnesota-9_whisper - 53.28s to 56.28s
ffmpeg -i "audio/minnesota/minnesota-9.mp3" -ss 53.28 -t 3.00 -c copy "all_states_aligned/audio_segments/sentence_8/minnesota-9_whisper.mp3"

# Extract pennsylvania-5_whisper - 51.50s to 54.50s
ffmpeg -i "audio/pennsylvania/pennsylvania-5.mp3" -ss 51.50 -t 3.00 -c copy "all_states_aligned/audio_segments/sentence_8/pennsylvania-5_whisper.mp3"

# The letter implied that the animal could be suffering from a rare form of foot and mouth disease, which was surprising, because normally you would only expect to see it in a dog or a goat
mkdir -p all_states_aligned/audio_segments/sentence_9

# Extract montana-2_whisper - 70.16s to 76.24s
ffmpeg -i "audio/montana/montana-2.mp3" -ss 70.16 -t 6.08 -c copy "all_states_aligned/audio_segments/sentence_9/montana-2_whisper.mp3"

# Extract north-dakota-1_whisper - 56.00s to 67.00s
ffmpeg -i "audio/north-dakota/north-dakota-1.mp3" -ss 56.00 -t 11.00 -c copy "all_states_aligned/audio_segments/sentence_9/north-dakota-1_whisper.mp3"

# Extract north-carolina-10_whisper - 44.00s to 49.00s
ffmpeg -i "audio/north-carolina/north-carolina-10.mp3" -ss 44.00 -t 5.00 -c copy "all_states_aligned/audio_segments/sentence_9/north-carolina-10_whisper.mp3"

# Extract south-carolina-9_whisper - 79.00s to 89.00s
ffmpeg -i "audio/south-carolina/south-carolina-9.mp3" -ss 79.00 -t 10.00 -c copy "all_states_aligned/audio_segments/sentence_9/south-carolina-9_whisper.mp3"

# Extract oklahoma-9_whisper - 52.00s to 61.00s
ffmpeg -i "audio/oklahoma/oklahoma-9.mp3" -ss 52.00 -t 9.00 -c copy "all_states_aligned/audio_segments/sentence_9/oklahoma-9_whisper.mp3"

# Extract mississippi-9_whisper - 61.00s to 73.00s
ffmpeg -i "audio/mississippi/mississippi-9.mp3" -ss 61.00 -t 12.00 -c copy "all_states_aligned/audio_segments/sentence_9/mississippi-9_whisper.mp3"

# Extract nebraska-2_whisper - 58.00s to 71.00s
ffmpeg -i "audio/nebraska/nebraska-2.mp3" -ss 58.00 -t 13.00 -c copy "all_states_aligned/audio_segments/sentence_9/nebraska-2_whisper.mp3"

# Extract new-mexico-4_whisper - 63.00s to 68.00s
ffmpeg -i "audio/new-mexico/new-mexico-4.mp3" -ss 63.00 -t 5.00 -c copy "all_states_aligned/audio_segments/sentence_9/new-mexico-4_whisper.mp3"

# Extract michigan-15_whisper - 44.32s to 48.40s
ffmpeg -i "audio/michigan/michigan-15.mp3" -ss 44.32 -t 4.08 -c copy "all_states_aligned/audio_segments/sentence_9/michigan-15_whisper.mp3"

# Extract south-dakota-1_whisper - 53.50s to 63.50s
ffmpeg -i "audio/south-dakota/south-dakota-1.mp3" -ss 53.50 -t 10.00 -c copy "all_states_aligned/audio_segments/sentence_9/south-dakota-1_whisper.mp3"

# Extract rhode-island-1_whisper - 62.12s to 68.36s
ffmpeg -i "audio/rhode-island/rhode-island-1.mp3" -ss 62.12 -t 6.24 -c copy "all_states_aligned/audio_segments/sentence_9/rhode-island-1_whisper.mp3"

# Extract received-pronunciation-4_whisper - 53.30s to 58.60s
ffmpeg -i "audio/received-pronunciation/received-pronunciation-4.mp3" -ss 53.30 -t 5.30 -c copy "all_states_aligned/audio_segments/sentence_9/received-pronunciation-4_whisper.mp3"

# Extract new-jersey-8_whisper - 57.40s to 59.40s
ffmpeg -i "audio/new-jersey/new-jersey-8.mp3" -ss 57.40 -t 2.00 -c copy "all_states_aligned/audio_segments/sentence_9/new-jersey-8_whisper.mp3"

# Extract ohio-3_whisper - 58.56s to 66.08s
ffmpeg -i "audio/ohio/ohio-3.mp3" -ss 58.56 -t 7.52 -c copy "all_states_aligned/audio_segments/sentence_9/ohio-3_whisper.mp3"

# Extract oregon-4_whisper - 62.96s to 69.44s
ffmpeg -i "audio/oregon/oregon-4.mp3" -ss 62.96 -t 6.48 -c copy "all_states_aligned/audio_segments/sentence_9/oregon-4_whisper.mp3"

# Extract pennsylvania-5_whisper - 54.50s to 59.50s
ffmpeg -i "audio/pennsylvania/pennsylvania-5.mp3" -ss 54.50 -t 5.00 -c copy "all_states_aligned/audio_segments/sentence_9/pennsylvania-5_whisper.mp3"

# Sarah was sentimental, so this made her feel sorry for the beautiful bird
mkdir -p all_states_aligned/audio_segments/sentence_10

# Extract montana-2_whisper - 76.24s to 83.68s
ffmpeg -i "audio/montana/montana-2.mp3" -ss 76.24 -t 7.44 -c copy "all_states_aligned/audio_segments/sentence_10/montana-2_whisper.mp3"

# Extract north-dakota-1_whisper - 67.00s to 72.00s
ffmpeg -i "audio/north-dakota/north-dakota-1.mp3" -ss 67.00 -t 5.00 -c copy "all_states_aligned/audio_segments/sentence_10/north-dakota-1_whisper.mp3"

# Extract south-carolina-9_whisper - 95.00s to 102.00s
ffmpeg -i "audio/south-carolina/south-carolina-9.mp3" -ss 95.00 -t 7.00 -c copy "all_states_aligned/audio_segments/sentence_10/south-carolina-9_whisper.mp3"

# Extract oklahoma-9_whisper - 61.00s to 65.00s
ffmpeg -i "audio/oklahoma/oklahoma-9.mp3" -ss 61.00 -t 4.00 -c copy "all_states_aligned/audio_segments/sentence_10/oklahoma-9_whisper.mp3"

# Extract mississippi-9_whisper - 73.00s to 79.00s
ffmpeg -i "audio/mississippi/mississippi-9.mp3" -ss 73.00 -t 6.00 -c copy "all_states_aligned/audio_segments/sentence_10/mississippi-9_whisper.mp3"

# Extract nebraska-2_whisper - 71.00s to 76.00s
ffmpeg -i "audio/nebraska/nebraska-2.mp3" -ss 71.00 -t 5.00 -c copy "all_states_aligned/audio_segments/sentence_10/nebraska-2_whisper.mp3"

# Extract new-mexico-4_whisper - 68.00s to 73.00s
ffmpeg -i "audio/new-mexico/new-mexico-4.mp3" -ss 68.00 -t 5.00 -c copy "all_states_aligned/audio_segments/sentence_10/new-mexico-4_whisper.mp3"

# Extract michigan-15_whisper - 52.64s to 56.00s
ffmpeg -i "audio/michigan/michigan-15.mp3" -ss 52.64 -t 3.36 -c copy "all_states_aligned/audio_segments/sentence_10/michigan-15_whisper.mp3"

# Extract south-dakota-1_whisper - 63.50s to 69.00s
ffmpeg -i "audio/south-dakota/south-dakota-1.mp3" -ss 63.50 -t 5.50 -c copy "all_states_aligned/audio_segments/sentence_10/south-dakota-1_whisper.mp3"

# Extract rhode-island-1_whisper - 74.40s to 79.40s
ffmpeg -i "audio/rhode-island/rhode-island-1.mp3" -ss 74.40 -t 5.00 -c copy "all_states_aligned/audio_segments/sentence_10/rhode-island-1_whisper.mp3"

# Extract received-pronunciation-4_whisper - 64.10s to 69.00s
ffmpeg -i "audio/received-pronunciation/received-pronunciation-4.mp3" -ss 64.10 -t 4.90 -c copy "all_states_aligned/audio_segments/sentence_10/received-pronunciation-4_whisper.mp3"

# Extract nevada-1_whisper - 56.60s to 60.36s
ffmpeg -i "audio/nevada/nevada-1.mp3" -ss 56.60 -t 3.76 -c copy "all_states_aligned/audio_segments/sentence_10/nevada-1_whisper.mp3"

# Extract new-jersey-8_whisper - 59.40s to 64.32s
ffmpeg -i "audio/new-jersey/new-jersey-8.mp3" -ss 59.40 -t 4.92 -c copy "all_states_aligned/audio_segments/sentence_10/new-jersey-8_whisper.mp3"

# Extract ohio-3_whisper - 71.28s to 77.16s
ffmpeg -i "audio/ohio/ohio-3.mp3" -ss 71.28 -t 5.88 -c copy "all_states_aligned/audio_segments/sentence_10/ohio-3_whisper.mp3"

# Extract oregon-4_whisper - 69.44s to 76.56s
ffmpeg -i "audio/oregon/oregon-4.mp3" -ss 69.44 -t 7.12 -c copy "all_states_aligned/audio_segments/sentence_10/oregon-4_whisper.mp3"

# Extract minnesota-9_whisper - 66.20s to 71.44s
ffmpeg -i "audio/minnesota/minnesota-9.mp3" -ss 66.20 -t 5.24 -c copy "all_states_aligned/audio_segments/sentence_10/minnesota-9_whisper.mp3"

# Extract pennsylvania-5_whisper - 64.50s to 68.50s
ffmpeg -i "audio/pennsylvania/pennsylvania-5.mp3" -ss 64.50 -t 4.00 -c copy "all_states_aligned/audio_segments/sentence_10/pennsylvania-5_whisper.mp3"

# Before long, that itchy goose began to strut around the office like a lunatic, which made an unsanitary mess
mkdir -p all_states_aligned/audio_segments/sentence_11

# Extract montana-2_whisper - 83.68s to 90.64s
ffmpeg -i "audio/montana/montana-2.mp3" -ss 83.68 -t 6.96 -c copy "all_states_aligned/audio_segments/sentence_11/montana-2_whisper.mp3"

# Extract north-dakota-1_whisper - 72.00s to 79.00s
ffmpeg -i "audio/north-dakota/north-dakota-1.mp3" -ss 72.00 -t 7.00 -c copy "all_states_aligned/audio_segments/sentence_11/north-dakota-1_whisper.mp3"

# Extract north-carolina-10_whisper - 58.00s to 63.00s
ffmpeg -i "audio/north-carolina/north-carolina-10.mp3" -ss 58.00 -t 5.00 -c copy "all_states_aligned/audio_segments/sentence_11/north-carolina-10_whisper.mp3"

# Extract south-carolina-9_whisper - 103.00s to 115.00s
ffmpeg -i "audio/south-carolina/south-carolina-9.mp3" -ss 103.00 -t 12.00 -c copy "all_states_aligned/audio_segments/sentence_11/south-carolina-9_whisper.mp3"

# Extract oklahoma-9_whisper - 65.00s to 71.00s
ffmpeg -i "audio/oklahoma/oklahoma-9.mp3" -ss 65.00 -t 6.00 -c copy "all_states_aligned/audio_segments/sentence_11/oklahoma-9_whisper.mp3"

# Extract mississippi-9_whisper - 79.00s to 87.00s
ffmpeg -i "audio/mississippi/mississippi-9.mp3" -ss 79.00 -t 8.00 -c copy "all_states_aligned/audio_segments/sentence_11/mississippi-9_whisper.mp3"

# Extract nebraska-2_whisper - 76.00s to 84.00s
ffmpeg -i "audio/nebraska/nebraska-2.mp3" -ss 76.00 -t 8.00 -c copy "all_states_aligned/audio_segments/sentence_11/nebraska-2_whisper.mp3"

# Extract new-mexico-4_whisper - 73.00s to 82.00s
ffmpeg -i "audio/new-mexico/new-mexico-4.mp3" -ss 73.00 -t 9.00 -c copy "all_states_aligned/audio_segments/sentence_11/new-mexico-4_whisper.mp3"

# Extract michigan-15_whisper - 56.08s to 61.72s
ffmpeg -i "audio/michigan/michigan-15.mp3" -ss 56.08 -t 5.64 -c copy "all_states_aligned/audio_segments/sentence_11/michigan-15_whisper.mp3"

# Extract south-dakota-1_whisper - 69.00s to 76.00s
ffmpeg -i "audio/south-dakota/south-dakota-1.mp3" -ss 69.00 -t 7.00 -c copy "all_states_aligned/audio_segments/sentence_11/south-dakota-1_whisper.mp3"

# Extract rhode-island-1_whisper - 79.40s to 84.36s
ffmpeg -i "audio/rhode-island/rhode-island-1.mp3" -ss 79.40 -t 4.96 -c copy "all_states_aligned/audio_segments/sentence_11/rhode-island-1_whisper.mp3"

# Extract received-pronunciation-4_whisper - 69.00s to 75.90s
ffmpeg -i "audio/received-pronunciation/received-pronunciation-4.mp3" -ss 69.00 -t 6.90 -c copy "all_states_aligned/audio_segments/sentence_11/received-pronunciation-4_whisper.mp3"

# Extract nevada-1_whisper - 60.36s to 64.32s
ffmpeg -i "audio/nevada/nevada-1.mp3" -ss 60.36 -t 3.96 -c copy "all_states_aligned/audio_segments/sentence_11/nevada-1_whisper.mp3"

# Extract new-jersey-8_whisper - 64.32s to 68.64s
ffmpeg -i "audio/new-jersey/new-jersey-8.mp3" -ss 64.32 -t 4.32 -c copy "all_states_aligned/audio_segments/sentence_11/new-jersey-8_whisper.mp3"

# Extract ohio-3_whisper - 77.16s to 83.40s
ffmpeg -i "audio/ohio/ohio-3.mp3" -ss 77.16 -t 6.24 -c copy "all_states_aligned/audio_segments/sentence_11/ohio-3_whisper.mp3"

# Extract oregon-4_whisper - 77.04s to 82.56s
ffmpeg -i "audio/oregon/oregon-4.mp3" -ss 77.04 -t 5.52 -c copy "all_states_aligned/audio_segments/sentence_11/oregon-4_whisper.mp3"

# Extract minnesota-9_whisper - 71.44s to 76.46s
ffmpeg -i "audio/minnesota/minnesota-9.mp3" -ss 71.44 -t 5.02 -c copy "all_states_aligned/audio_segments/sentence_11/minnesota-9_whisper.mp3"

# Extract pennsylvania-5_whisper - 68.50s to 73.50s
ffmpeg -i "audio/pennsylvania/pennsylvania-5.mp3" -ss 68.50 -t 5.00 -c copy "all_states_aligned/audio_segments/sentence_11/pennsylvania-5_whisper.mp3"

# The goose's owner, Mary Harrison, kept calling, "Comma, Comma," which Sarah thought was an odd choice for a name
mkdir -p all_states_aligned/audio_segments/sentence_12

# Extract montana-2_whisper - 91.28s to 97.68s
ffmpeg -i "audio/montana/montana-2.mp3" -ss 91.28 -t 6.40 -c copy "all_states_aligned/audio_segments/sentence_12/montana-2_whisper.mp3"

# Extract north-dakota-1_whisper - 79.00s to 86.00s
ffmpeg -i "audio/north-dakota/north-dakota-1.mp3" -ss 79.00 -t 7.00 -c copy "all_states_aligned/audio_segments/sentence_12/north-dakota-1_whisper.mp3"

# Extract north-carolina-10_whisper - 63.00s to 66.00s
ffmpeg -i "audio/north-carolina/north-carolina-10.mp3" -ss 63.00 -t 3.00 -c copy "all_states_aligned/audio_segments/sentence_12/north-carolina-10_whisper.mp3"

# Extract south-carolina-9_whisper - 115.00s to 126.00s
ffmpeg -i "audio/south-carolina/south-carolina-9.mp3" -ss 115.00 -t 11.00 -c copy "all_states_aligned/audio_segments/sentence_12/south-carolina-9_whisper.mp3"

# Extract oklahoma-9_whisper - 71.00s to 78.00s
ffmpeg -i "audio/oklahoma/oklahoma-9.mp3" -ss 71.00 -t 7.00 -c copy "all_states_aligned/audio_segments/sentence_12/oklahoma-9_whisper.mp3"

# Extract mississippi-9_whisper - 87.00s to 99.00s
ffmpeg -i "audio/mississippi/mississippi-9.mp3" -ss 87.00 -t 12.00 -c copy "all_states_aligned/audio_segments/sentence_12/mississippi-9_whisper.mp3"

# Extract nebraska-2_whisper - 84.00s to 93.00s
ffmpeg -i "audio/nebraska/nebraska-2.mp3" -ss 84.00 -t 9.00 -c copy "all_states_aligned/audio_segments/sentence_12/nebraska-2_whisper.mp3"

# Extract new-mexico-4_whisper - 82.00s to 91.00s
ffmpeg -i "audio/new-mexico/new-mexico-4.mp3" -ss 82.00 -t 9.00 -c copy "all_states_aligned/audio_segments/sentence_12/new-mexico-4_whisper.mp3"

# Extract michigan-15_whisper - 61.72s to 67.12s
ffmpeg -i "audio/michigan/michigan-15.mp3" -ss 61.72 -t 5.40 -c copy "all_states_aligned/audio_segments/sentence_12/michigan-15_whisper.mp3"

# Extract south-dakota-1_whisper - 76.00s to 83.00s
ffmpeg -i "audio/south-dakota/south-dakota-1.mp3" -ss 76.00 -t 7.00 -c copy "all_states_aligned/audio_segments/sentence_12/south-dakota-1_whisper.mp3"

# Extract rhode-island-1_whisper - 87.16s to 91.20s
ffmpeg -i "audio/rhode-island/rhode-island-1.mp3" -ss 87.16 -t 4.04 -c copy "all_states_aligned/audio_segments/sentence_12/rhode-island-1_whisper.mp3"

# Extract received-pronunciation-4_whisper - 75.90s to 83.70s
ffmpeg -i "audio/received-pronunciation/received-pronunciation-4.mp3" -ss 75.90 -t 7.80 -c copy "all_states_aligned/audio_segments/sentence_12/received-pronunciation-4_whisper.mp3"

# Extract nevada-1_whisper - 67.72s to 71.68s
ffmpeg -i "audio/nevada/nevada-1.mp3" -ss 67.72 -t 3.96 -c copy "all_states_aligned/audio_segments/sentence_12/nevada-1_whisper.mp3"

# Extract new-jersey-8_whisper - 70.56s to 76.12s
ffmpeg -i "audio/new-jersey/new-jersey-8.mp3" -ss 70.56 -t 5.56 -c copy "all_states_aligned/audio_segments/sentence_12/new-jersey-8_whisper.mp3"

# Extract ohio-3_whisper - 88.76s to 93.28s
ffmpeg -i "audio/ohio/ohio-3.mp3" -ss 88.76 -t 4.52 -c copy "all_states_aligned/audio_segments/sentence_12/ohio-3_whisper.mp3"

# Extract oregon-4_whisper - 83.44s to 92.96s
ffmpeg -i "audio/oregon/oregon-4.mp3" -ss 83.44 -t 9.52 -c copy "all_states_aligned/audio_segments/sentence_12/oregon-4_whisper.mp3"

# Extract minnesota-9_whisper - 78.16s to 84.36s
ffmpeg -i "audio/minnesota/minnesota-9.mp3" -ss 78.16 -t 6.20 -c copy "all_states_aligned/audio_segments/sentence_12/minnesota-9_whisper.mp3"

# Extract pennsylvania-5_whisper - 76.50s to 80.50s
ffmpeg -i "audio/pennsylvania/pennsylvania-5.mp3" -ss 76.50 -t 4.00 -c copy "all_states_aligned/audio_segments/sentence_12/pennsylvania-5_whisper.mp3"

# Comma was strong and huge, so it would take some force to trap her, but Sarah had a different idea
mkdir -p all_states_aligned/audio_segments/sentence_13

# Extract montana-2_whisper - 98.32s to 105.12s
ffmpeg -i "audio/montana/montana-2.mp3" -ss 98.32 -t 6.80 -c copy "all_states_aligned/audio_segments/sentence_13/montana-2_whisper.mp3"

# Extract north-dakota-1_whisper - 86.00s to 92.00s
ffmpeg -i "audio/north-dakota/north-dakota-1.mp3" -ss 86.00 -t 6.00 -c copy "all_states_aligned/audio_segments/sentence_13/north-dakota-1_whisper.mp3"

# Extract north-carolina-10_whisper - 70.00s to 79.00s
ffmpeg -i "audio/north-carolina/north-carolina-10.mp3" -ss 70.00 -t 9.00 -c copy "all_states_aligned/audio_segments/sentence_13/north-carolina-10_whisper.mp3"

# Extract south-carolina-9_whisper - 126.00s to 132.00s
ffmpeg -i "audio/south-carolina/south-carolina-9.mp3" -ss 126.00 -t 6.00 -c copy "all_states_aligned/audio_segments/sentence_13/south-carolina-9_whisper.mp3"

# Extract oklahoma-9_whisper - 78.00s to 84.00s
ffmpeg -i "audio/oklahoma/oklahoma-9.mp3" -ss 78.00 -t 6.00 -c copy "all_states_aligned/audio_segments/sentence_13/oklahoma-9_whisper.mp3"

# Extract mississippi-9_whisper - 99.00s to 107.00s
ffmpeg -i "audio/mississippi/mississippi-9.mp3" -ss 99.00 -t 8.00 -c copy "all_states_aligned/audio_segments/sentence_13/mississippi-9_whisper.mp3"

# Extract nebraska-2_whisper - 93.00s to 98.00s
ffmpeg -i "audio/nebraska/nebraska-2.mp3" -ss 93.00 -t 5.00 -c copy "all_states_aligned/audio_segments/sentence_13/nebraska-2_whisper.mp3"

# Extract new-mexico-4_whisper - 91.00s to 93.00s
ffmpeg -i "audio/new-mexico/new-mexico-4.mp3" -ss 91.00 -t 2.00 -c copy "all_states_aligned/audio_segments/sentence_13/new-mexico-4_whisper.mp3"

# Extract michigan-15_whisper - 67.12s to 71.72s
ffmpeg -i "audio/michigan/michigan-15.mp3" -ss 67.12 -t 4.60 -c copy "all_states_aligned/audio_segments/sentence_13/michigan-15_whisper.mp3"

# Extract south-dakota-1_whisper - 83.00s to 89.00s
ffmpeg -i "audio/south-dakota/south-dakota-1.mp3" -ss 83.00 -t 6.00 -c copy "all_states_aligned/audio_segments/sentence_13/south-dakota-1_whisper.mp3"

# Extract rhode-island-1_whisper - 95.60s to 100.16s
ffmpeg -i "audio/rhode-island/rhode-island-1.mp3" -ss 95.60 -t 4.56 -c copy "all_states_aligned/audio_segments/sentence_13/rhode-island-1_whisper.mp3"

# Extract received-pronunciation-4_whisper - 83.70s to 91.00s
ffmpeg -i "audio/received-pronunciation/received-pronunciation-4.mp3" -ss 83.70 -t 7.30 -c copy "all_states_aligned/audio_segments/sentence_13/received-pronunciation-4_whisper.mp3"

# Extract nevada-1_whisper - 74.24s to 77.92s
ffmpeg -i "audio/nevada/nevada-1.mp3" -ss 74.24 -t 3.68 -c copy "all_states_aligned/audio_segments/sentence_13/nevada-1_whisper.mp3"

# Extract new-jersey-8_whisper - 78.08s to 82.20s
ffmpeg -i "audio/new-jersey/new-jersey-8.mp3" -ss 78.08 -t 4.12 -c copy "all_states_aligned/audio_segments/sentence_13/new-jersey-8_whisper.mp3"

# Extract ohio-3_whisper - 98.72s to 103.48s
ffmpeg -i "audio/ohio/ohio-3.mp3" -ss 98.72 -t 4.76 -c copy "all_states_aligned/audio_segments/sentence_13/ohio-3_whisper.mp3"

# Extract oregon-4_whisper - 92.96s to 99.60s
ffmpeg -i "audio/oregon/oregon-4.mp3" -ss 92.96 -t 6.64 -c copy "all_states_aligned/audio_segments/sentence_13/oregon-4_whisper.mp3"

# Extract minnesota-9_whisper - 85.84s to 91.94s
ffmpeg -i "audio/minnesota/minnesota-9.mp3" -ss 85.84 -t 6.10 -c copy "all_states_aligned/audio_segments/sentence_13/minnesota-9_whisper.mp3"

# Extract pennsylvania-5_whisper - 84.50s to 91.50s
ffmpeg -i "audio/pennsylvania/pennsylvania-5.mp3" -ss 84.50 -t 7.00 -c copy "all_states_aligned/audio_segments/sentence_13/pennsylvania-5_whisper.mp3"

# First she tried gently stroking the goose's lower back with her palm, then singing a tune to her
mkdir -p all_states_aligned/audio_segments/sentence_14

# Extract montana-2_whisper - 114.24s to 119.84s
ffmpeg -i "audio/montana/montana-2.mp3" -ss 114.24 -t 5.60 -c copy "all_states_aligned/audio_segments/sentence_14/montana-2_whisper.mp3"

# Extract north-dakota-1_whisper - 93.00s to 99.00s
ffmpeg -i "audio/north-dakota/north-dakota-1.mp3" -ss 93.00 -t 6.00 -c copy "all_states_aligned/audio_segments/sentence_14/north-dakota-1_whisper.mp3"

# Extract north-carolina-10_whisper - 70.00s to 79.00s
ffmpeg -i "audio/north-carolina/north-carolina-10.mp3" -ss 70.00 -t 9.00 -c copy "all_states_aligned/audio_segments/sentence_14/north-carolina-10_whisper.mp3"

# Extract south-carolina-9_whisper - 135.00s to 141.00s
ffmpeg -i "audio/south-carolina/south-carolina-9.mp3" -ss 135.00 -t 6.00 -c copy "all_states_aligned/audio_segments/sentence_14/south-carolina-9_whisper.mp3"

# Extract oklahoma-9_whisper - 84.00s to 90.00s
ffmpeg -i "audio/oklahoma/oklahoma-9.mp3" -ss 84.00 -t 6.00 -c copy "all_states_aligned/audio_segments/sentence_14/oklahoma-9_whisper.mp3"

# Extract mississippi-9_whisper - 107.00s to 117.00s
ffmpeg -i "audio/mississippi/mississippi-9.mp3" -ss 107.00 -t 10.00 -c copy "all_states_aligned/audio_segments/sentence_14/mississippi-9_whisper.mp3"

# Extract nebraska-2_whisper - 98.00s to 105.00s
ffmpeg -i "audio/nebraska/nebraska-2.mp3" -ss 98.00 -t 7.00 -c copy "all_states_aligned/audio_segments/sentence_14/nebraska-2_whisper.mp3"

# Extract new-mexico-4_whisper - 99.00s to 106.00s
ffmpeg -i "audio/new-mexico/new-mexico-4.mp3" -ss 99.00 -t 7.00 -c copy "all_states_aligned/audio_segments/sentence_14/new-mexico-4_whisper.mp3"

# Extract michigan-15_whisper - 71.72s to 75.64s
ffmpeg -i "audio/michigan/michigan-15.mp3" -ss 71.72 -t 3.92 -c copy "all_states_aligned/audio_segments/sentence_14/michigan-15_whisper.mp3"

# Extract south-dakota-1_whisper - 89.00s to 95.00s
ffmpeg -i "audio/south-dakota/south-dakota-1.mp3" -ss 89.00 -t 6.00 -c copy "all_states_aligned/audio_segments/sentence_14/south-dakota-1_whisper.mp3"

# Extract rhode-island-1_whisper - 102.52s to 106.92s
ffmpeg -i "audio/rhode-island/rhode-island-1.mp3" -ss 102.52 -t 4.40 -c copy "all_states_aligned/audio_segments/sentence_14/rhode-island-1_whisper.mp3"

# Extract received-pronunciation-4_whisper - 91.00s to 97.20s
ffmpeg -i "audio/received-pronunciation/received-pronunciation-4.mp3" -ss 91.00 -t 6.20 -c copy "all_states_aligned/audio_segments/sentence_14/received-pronunciation-4_whisper.mp3"

# Extract nevada-1_whisper - 78.92s to 82.68s
ffmpeg -i "audio/nevada/nevada-1.mp3" -ss 78.92 -t 3.76 -c copy "all_states_aligned/audio_segments/sentence_14/nevada-1_whisper.mp3"

# Extract new-jersey-8_whisper - 83.20s to 87.72s
ffmpeg -i "audio/new-jersey/new-jersey-8.mp3" -ss 83.20 -t 4.52 -c copy "all_states_aligned/audio_segments/sentence_14/new-jersey-8_whisper.mp3"

# Extract ohio-3_whisper - 109.16s to 112.80s
ffmpeg -i "audio/ohio/ohio-3.mp3" -ss 109.16 -t 3.64 -c copy "all_states_aligned/audio_segments/sentence_14/ohio-3_whisper.mp3"

# Extract oregon-4_whisper - 104.08s to 109.28s
ffmpeg -i "audio/oregon/oregon-4.mp3" -ss 104.08 -t 5.20 -c copy "all_states_aligned/audio_segments/sentence_14/oregon-4_whisper.mp3"

# Extract minnesota-9_whisper - 93.34s to 98.08s
ffmpeg -i "audio/minnesota/minnesota-9.mp3" -ss 93.34 -t 4.74 -c copy "all_states_aligned/audio_segments/sentence_14/minnesota-9_whisper.mp3"

# Extract pennsylvania-5_whisper - 91.50s to 97.50s
ffmpeg -i "audio/pennsylvania/pennsylvania-5.mp3" -ss 91.50 -t 6.00 -c copy "all_states_aligned/audio_segments/sentence_14/pennsylvania-5_whisper.mp3"

# Finally, she administered ether
mkdir -p all_states_aligned/audio_segments/sentence_15

# Extract montana-2_whisper - 119.84s to 127.20s
ffmpeg -i "audio/montana/montana-2.mp3" -ss 119.84 -t 7.36 -c copy "all_states_aligned/audio_segments/sentence_15/montana-2_whisper.mp3"

# Extract north-dakota-1_whisper - 99.00s to 102.00s
ffmpeg -i "audio/north-dakota/north-dakota-1.mp3" -ss 99.00 -t 3.00 -c copy "all_states_aligned/audio_segments/sentence_15/north-dakota-1_whisper.mp3"

# Extract oklahoma-9_whisper - 90.00s to 92.00s
ffmpeg -i "audio/oklahoma/oklahoma-9.mp3" -ss 90.00 -t 2.00 -c copy "all_states_aligned/audio_segments/sentence_15/oklahoma-9_whisper.mp3"

# Extract michigan-15_whisper - 75.64s to 78.28s
ffmpeg -i "audio/michigan/michigan-15.mp3" -ss 75.64 -t 2.64 -c copy "all_states_aligned/audio_segments/sentence_15/michigan-15_whisper.mp3"

# Extract received-pronunciation-4_whisper - 97.20s to 101.90s
ffmpeg -i "audio/received-pronunciation/received-pronunciation-4.mp3" -ss 97.20 -t 4.70 -c copy "all_states_aligned/audio_segments/sentence_15/received-pronunciation-4_whisper.mp3"

# Extract nevada-1_whisper - 84.08s to 86.28s
ffmpeg -i "audio/nevada/nevada-1.mp3" -ss 84.08 -t 2.20 -c copy "all_states_aligned/audio_segments/sentence_15/nevada-1_whisper.mp3"

# Extract new-jersey-8_whisper - 88.72s to 90.92s
ffmpeg -i "audio/new-jersey/new-jersey-8.mp3" -ss 88.72 -t 2.20 -c copy "all_states_aligned/audio_segments/sentence_15/new-jersey-8_whisper.mp3"

# Extract ohio-3_whisper - 115.00s to 119.48s
ffmpeg -i "audio/ohio/ohio-3.mp3" -ss 115.00 -t 4.48 -c copy "all_states_aligned/audio_segments/sentence_15/ohio-3_whisper.mp3"

# Extract oregon-4_whisper - 109.28s to 118.24s
ffmpeg -i "audio/oregon/oregon-4.mp3" -ss 109.28 -t 8.96 -c copy "all_states_aligned/audio_segments/sentence_15/oregon-4_whisper.mp3"

# Extract minnesota-9_whisper - 99.08s to 102.52s
ffmpeg -i "audio/minnesota/minnesota-9.mp3" -ss 99.08 -t 3.44 -c copy "all_states_aligned/audio_segments/sentence_15/minnesota-9_whisper.mp3"

# Extract pennsylvania-5_whisper - 97.50s to 100.50s
ffmpeg -i "audio/pennsylvania/pennsylvania-5.mp3" -ss 97.50 -t 3.00 -c copy "all_states_aligned/audio_segments/sentence_15/pennsylvania-5_whisper.mp3"

# Her efforts were not futile
mkdir -p all_states_aligned/audio_segments/sentence_16

# Extract montana-2_whisper - 119.84s to 127.20s
ffmpeg -i "audio/montana/montana-2.mp3" -ss 119.84 -t 7.36 -c copy "all_states_aligned/audio_segments/sentence_16/montana-2_whisper.mp3"

# Extract north-dakota-1_whisper - 102.00s to 105.00s
ffmpeg -i "audio/north-dakota/north-dakota-1.mp3" -ss 102.00 -t 3.00 -c copy "all_states_aligned/audio_segments/sentence_16/north-dakota-1_whisper.mp3"

# Extract north-carolina-10_whisper - 79.00s to 81.00s
ffmpeg -i "audio/north-carolina/north-carolina-10.mp3" -ss 79.00 -t 2.00 -c copy "all_states_aligned/audio_segments/sentence_16/north-carolina-10_whisper.mp3"

# Extract south-carolina-9_whisper - 148.00s to 151.00s
ffmpeg -i "audio/south-carolina/south-carolina-9.mp3" -ss 148.00 -t 3.00 -c copy "all_states_aligned/audio_segments/sentence_16/south-carolina-9_whisper.mp3"

# Extract mississippi-9_whisper - 117.00s to 127.00s
ffmpeg -i "audio/mississippi/mississippi-9.mp3" -ss 117.00 -t 10.00 -c copy "all_states_aligned/audio_segments/sentence_16/mississippi-9_whisper.mp3"

# Extract nebraska-2_whisper - 105.00s to 114.00s
ffmpeg -i "audio/nebraska/nebraska-2.mp3" -ss 105.00 -t 9.00 -c copy "all_states_aligned/audio_segments/sentence_16/nebraska-2_whisper.mp3"

# Extract michigan-15_whisper - 78.28s to 85.40s
ffmpeg -i "audio/michigan/michigan-15.mp3" -ss 78.28 -t 7.12 -c copy "all_states_aligned/audio_segments/sentence_16/michigan-15_whisper.mp3"

# Extract south-dakota-1_whisper - 95.00s to 101.00s
ffmpeg -i "audio/south-dakota/south-dakota-1.mp3" -ss 95.00 -t 6.00 -c copy "all_states_aligned/audio_segments/sentence_16/south-dakota-1_whisper.mp3"

# Extract rhode-island-1_whisper - 111.92s to 113.68s
ffmpeg -i "audio/rhode-island/rhode-island-1.mp3" -ss 111.92 -t 1.76 -c copy "all_states_aligned/audio_segments/sentence_16/rhode-island-1_whisper.mp3"

# Extract received-pronunciation-4_whisper - 97.20s to 101.90s
ffmpeg -i "audio/received-pronunciation/received-pronunciation-4.mp3" -ss 97.20 -t 4.70 -c copy "all_states_aligned/audio_segments/sentence_16/received-pronunciation-4_whisper.mp3"

# Extract nevada-1_whisper - 86.28s to 88.04s
ffmpeg -i "audio/nevada/nevada-1.mp3" -ss 86.28 -t 1.76 -c copy "all_states_aligned/audio_segments/sentence_16/nevada-1_whisper.mp3"

# Extract new-jersey-8_whisper - 90.92s to 92.68s
ffmpeg -i "audio/new-jersey/new-jersey-8.mp3" -ss 90.92 -t 1.76 -c copy "all_states_aligned/audio_segments/sentence_16/new-jersey-8_whisper.mp3"

# Extract oregon-4_whisper - 109.28s to 118.24s
ffmpeg -i "audio/oregon/oregon-4.mp3" -ss 109.28 -t 8.96 -c copy "all_states_aligned/audio_segments/sentence_16/oregon-4_whisper.mp3"

# Extract minnesota-9_whisper - 102.52s to 106.20s
ffmpeg -i "audio/minnesota/minnesota-9.mp3" -ss 102.52 -t 3.68 -c copy "all_states_aligned/audio_segments/sentence_16/minnesota-9_whisper.mp3"

# Extract pennsylvania-5_whisper - 100.50s to 102.50s
ffmpeg -i "audio/pennsylvania/pennsylvania-5.mp3" -ss 100.50 -t 2.00 -c copy "all_states_aligned/audio_segments/sentence_16/pennsylvania-5_whisper.mp3"

# In no time, the goose began to tire, so Sarah was able to hold onto Comma and give her a relaxing bath
mkdir -p all_states_aligned/audio_segments/sentence_17

# Extract montana-2_whisper - 119.84s to 127.20s
ffmpeg -i "audio/montana/montana-2.mp3" -ss 119.84 -t 7.36 -c copy "all_states_aligned/audio_segments/sentence_17/montana-2_whisper.mp3"

# Extract north-dakota-1_whisper - 105.00s to 112.00s
ffmpeg -i "audio/north-dakota/north-dakota-1.mp3" -ss 105.00 -t 7.00 -c copy "all_states_aligned/audio_segments/sentence_17/north-dakota-1_whisper.mp3"

# Extract north-carolina-10_whisper - 81.00s to 86.00s
ffmpeg -i "audio/north-carolina/north-carolina-10.mp3" -ss 81.00 -t 5.00 -c copy "all_states_aligned/audio_segments/sentence_17/north-carolina-10_whisper.mp3"

# Extract south-carolina-9_whisper - 151.00s to 162.00s
ffmpeg -i "audio/south-carolina/south-carolina-9.mp3" -ss 151.00 -t 11.00 -c copy "all_states_aligned/audio_segments/sentence_17/south-carolina-9_whisper.mp3"

# Extract oklahoma-9_whisper - 94.00s to 100.00s
ffmpeg -i "audio/oklahoma/oklahoma-9.mp3" -ss 94.00 -t 6.00 -c copy "all_states_aligned/audio_segments/sentence_17/oklahoma-9_whisper.mp3"

# Extract mississippi-9_whisper - 117.00s to 127.00s
ffmpeg -i "audio/mississippi/mississippi-9.mp3" -ss 117.00 -t 10.00 -c copy "all_states_aligned/audio_segments/sentence_17/mississippi-9_whisper.mp3"

# Extract nebraska-2_whisper - 105.00s to 114.00s
ffmpeg -i "audio/nebraska/nebraska-2.mp3" -ss 105.00 -t 9.00 -c copy "all_states_aligned/audio_segments/sentence_17/nebraska-2_whisper.mp3"

# Extract new-mexico-4_whisper - 114.00s to 122.00s
ffmpeg -i "audio/new-mexico/new-mexico-4.mp3" -ss 114.00 -t 8.00 -c copy "all_states_aligned/audio_segments/sentence_17/new-mexico-4_whisper.mp3"

# Extract michigan-15_whisper - 78.28s to 85.40s
ffmpeg -i "audio/michigan/michigan-15.mp3" -ss 78.28 -t 7.12 -c copy "all_states_aligned/audio_segments/sentence_17/michigan-15_whisper.mp3"

# Extract south-dakota-1_whisper - 102.00s to 109.00s
ffmpeg -i "audio/south-dakota/south-dakota-1.mp3" -ss 102.00 -t 7.00 -c copy "all_states_aligned/audio_segments/sentence_17/south-dakota-1_whisper.mp3"

# Extract rhode-island-1_whisper - 113.68s to 121.84s
ffmpeg -i "audio/rhode-island/rhode-island-1.mp3" -ss 113.68 -t 8.16 -c copy "all_states_aligned/audio_segments/sentence_17/rhode-island-1_whisper.mp3"

# Extract received-pronunciation-4_whisper - 102.00s to 109.40s
ffmpeg -i "audio/received-pronunciation/received-pronunciation-4.mp3" -ss 102.00 -t 7.40 -c copy "all_states_aligned/audio_segments/sentence_17/received-pronunciation-4_whisper.mp3"

# Extract nevada-1_whisper - 88.04s to 91.86s
ffmpeg -i "audio/nevada/nevada-1.mp3" -ss 88.04 -t 3.82 -c copy "all_states_aligned/audio_segments/sentence_17/nevada-1_whisper.mp3"

# Extract new-jersey-8_whisper - 92.68s to 97.24s
ffmpeg -i "audio/new-jersey/new-jersey-8.mp3" -ss 92.68 -t 4.56 -c copy "all_states_aligned/audio_segments/sentence_17/new-jersey-8_whisper.mp3"

# Extract ohio-3_whisper - 119.48s to 124.48s
ffmpeg -i "audio/ohio/ohio-3.mp3" -ss 119.48 -t 5.00 -c copy "all_states_aligned/audio_segments/sentence_17/ohio-3_whisper.mp3"

# Extract oregon-4_whisper - 109.28s to 118.24s
ffmpeg -i "audio/oregon/oregon-4.mp3" -ss 109.28 -t 8.96 -c copy "all_states_aligned/audio_segments/sentence_17/oregon-4_whisper.mp3"

# Extract minnesota-9_whisper - 106.20s to 112.08s
ffmpeg -i "audio/minnesota/minnesota-9.mp3" -ss 106.20 -t 5.88 -c copy "all_states_aligned/audio_segments/sentence_17/minnesota-9_whisper.mp3"

# Extract pennsylvania-5_whisper - 102.50s to 109.50s
ffmpeg -i "audio/pennsylvania/pennsylvania-5.mp3" -ss 102.50 -t 7.00 -c copy "all_states_aligned/audio_segments/sentence_17/pennsylvania-5_whisper.mp3"

# Once Sarah had managed to bathe the goose, she wiped her off with a cloth and laid her on her right side
mkdir -p all_states_aligned/audio_segments/sentence_18

# Extract montana-2_whisper - 133.44s to 139.60s
ffmpeg -i "audio/montana/montana-2.mp3" -ss 133.44 -t 6.16 -c copy "all_states_aligned/audio_segments/sentence_18/montana-2_whisper.mp3"

# Extract north-dakota-1_whisper - 112.00s to 119.00s
ffmpeg -i "audio/north-dakota/north-dakota-1.mp3" -ss 112.00 -t 7.00 -c copy "all_states_aligned/audio_segments/sentence_18/north-dakota-1_whisper.mp3"

# Extract south-carolina-9_whisper - 162.00s to 171.00s
ffmpeg -i "audio/south-carolina/south-carolina-9.mp3" -ss 162.00 -t 9.00 -c copy "all_states_aligned/audio_segments/sentence_18/south-carolina-9_whisper.mp3"

# Extract oklahoma-9_whisper - 100.00s to 107.00s
ffmpeg -i "audio/oklahoma/oklahoma-9.mp3" -ss 100.00 -t 7.00 -c copy "all_states_aligned/audio_segments/sentence_18/oklahoma-9_whisper.mp3"

# Extract mississippi-9_whisper - 127.00s to 134.00s
ffmpeg -i "audio/mississippi/mississippi-9.mp3" -ss 127.00 -t 7.00 -c copy "all_states_aligned/audio_segments/sentence_18/mississippi-9_whisper.mp3"

# Extract michigan-15_whisper - 85.40s to 89.96s
ffmpeg -i "audio/michigan/michigan-15.mp3" -ss 85.40 -t 4.56 -c copy "all_states_aligned/audio_segments/sentence_18/michigan-15_whisper.mp3"

# Extract south-dakota-1_whisper - 109.00s to 117.00s
ffmpeg -i "audio/south-dakota/south-dakota-1.mp3" -ss 109.00 -t 8.00 -c copy "all_states_aligned/audio_segments/sentence_18/south-dakota-1_whisper.mp3"

# Extract rhode-island-1_whisper - 121.84s to 128.96s
ffmpeg -i "audio/rhode-island/rhode-island-1.mp3" -ss 121.84 -t 7.12 -c copy "all_states_aligned/audio_segments/sentence_18/rhode-island-1_whisper.mp3"

# Extract received-pronunciation-4_whisper - 109.40s to 115.50s
ffmpeg -i "audio/received-pronunciation/received-pronunciation-4.mp3" -ss 109.40 -t 6.10 -c copy "all_states_aligned/audio_segments/sentence_18/received-pronunciation-4_whisper.mp3"

# Extract nevada-1_whisper - 93.40s to 97.20s
ffmpeg -i "audio/nevada/nevada-1.mp3" -ss 93.40 -t 3.80 -c copy "all_states_aligned/audio_segments/sentence_18/nevada-1_whisper.mp3"

# Extract new-jersey-8_whisper - 99.32s to 103.12s
ffmpeg -i "audio/new-jersey/new-jersey-8.mp3" -ss 99.32 -t 3.80 -c copy "all_states_aligned/audio_segments/sentence_18/new-jersey-8_whisper.mp3"

# Extract ohio-3_whisper - 130.80s to 136.64s
ffmpeg -i "audio/ohio/ohio-3.mp3" -ss 130.80 -t 5.84 -c copy "all_states_aligned/audio_segments/sentence_18/ohio-3_whisper.mp3"

# Extract oregon-4_whisper - 124.24s to 129.92s
ffmpeg -i "audio/oregon/oregon-4.mp3" -ss 124.24 -t 5.68 -c copy "all_states_aligned/audio_segments/sentence_18/oregon-4_whisper.mp3"

# Extract minnesota-9_whisper - 113.36s to 120.80s
ffmpeg -i "audio/minnesota/minnesota-9.mp3" -ss 113.36 -t 7.44 -c copy "all_states_aligned/audio_segments/sentence_18/minnesota-9_whisper.mp3"

# Extract pennsylvania-5_whisper - 109.50s to 116.50s
ffmpeg -i "audio/pennsylvania/pennsylvania-5.mp3" -ss 109.50 -t 7.00 -c copy "all_states_aligned/audio_segments/sentence_18/pennsylvania-5_whisper.mp3"

# Then Sarah confirmed the vet's diagnosis
mkdir -p all_states_aligned/audio_segments/sentence_19

# Almost immediately, she remembered an effective treatment that required her to measure out a lot of medicine
mkdir -p all_states_aligned/audio_segments/sentence_20

# Extract montana-2_whisper - 139.60s to 145.92s
ffmpeg -i "audio/montana/montana-2.mp3" -ss 139.60 -t 6.32 -c copy "all_states_aligned/audio_segments/sentence_20/montana-2_whisper.mp3"

# Extract north-dakota-1_whisper - 123.00s to 128.00s
ffmpeg -i "audio/north-dakota/north-dakota-1.mp3" -ss 123.00 -t 5.00 -c copy "all_states_aligned/audio_segments/sentence_20/north-dakota-1_whisper.mp3"

# Extract north-carolina-10_whisper - 90.00s to 96.00s
ffmpeg -i "audio/north-carolina/north-carolina-10.mp3" -ss 90.00 -t 6.00 -c copy "all_states_aligned/audio_segments/sentence_20/north-carolina-10_whisper.mp3"

# Extract south-carolina-9_whisper - 176.00s to 186.00s
ffmpeg -i "audio/south-carolina/south-carolina-9.mp3" -ss 176.00 -t 10.00 -c copy "all_states_aligned/audio_segments/sentence_20/south-carolina-9_whisper.mp3"

# Extract oklahoma-9_whisper - 110.00s to 115.00s
ffmpeg -i "audio/oklahoma/oklahoma-9.mp3" -ss 110.00 -t 5.00 -c copy "all_states_aligned/audio_segments/sentence_20/oklahoma-9_whisper.mp3"

# Extract mississippi-9_whisper - 134.00s to 144.00s
ffmpeg -i "audio/mississippi/mississippi-9.mp3" -ss 134.00 -t 10.00 -c copy "all_states_aligned/audio_segments/sentence_20/mississippi-9_whisper.mp3"

# Extract nebraska-2_whisper - 118.00s to 127.00s
ffmpeg -i "audio/nebraska/nebraska-2.mp3" -ss 118.00 -t 9.00 -c copy "all_states_aligned/audio_segments/sentence_20/nebraska-2_whisper.mp3"

# Extract michigan-15_whisper - 92.16s to 96.88s
ffmpeg -i "audio/michigan/michigan-15.mp3" -ss 92.16 -t 4.72 -c copy "all_states_aligned/audio_segments/sentence_20/michigan-15_whisper.mp3"

# Extract south-dakota-1_whisper - 117.00s to 124.00s
ffmpeg -i "audio/south-dakota/south-dakota-1.mp3" -ss 117.00 -t 7.00 -c copy "all_states_aligned/audio_segments/sentence_20/south-dakota-1_whisper.mp3"

# Extract rhode-island-1_whisper - 131.80s to 138.68s
ffmpeg -i "audio/rhode-island/rhode-island-1.mp3" -ss 131.80 -t 6.88 -c copy "all_states_aligned/audio_segments/sentence_20/rhode-island-1_whisper.mp3"

# Extract received-pronunciation-4_whisper - 118.60s to 124.70s
ffmpeg -i "audio/received-pronunciation/received-pronunciation-4.mp3" -ss 118.60 -t 6.10 -c copy "all_states_aligned/audio_segments/sentence_20/received-pronunciation-4_whisper.mp3"

# Extract nevada-1_whisper - 101.48s to 104.52s
ffmpeg -i "audio/nevada/nevada-1.mp3" -ss 101.48 -t 3.04 -c copy "all_states_aligned/audio_segments/sentence_20/nevada-1_whisper.mp3"

# Extract new-jersey-8_whisper - 107.24s to 111.28s
ffmpeg -i "audio/new-jersey/new-jersey-8.mp3" -ss 107.24 -t 4.04 -c copy "all_states_aligned/audio_segments/sentence_20/new-jersey-8_whisper.mp3"

# Extract ohio-3_whisper - 140.12s to 145.44s
ffmpeg -i "audio/ohio/ohio-3.mp3" -ss 140.12 -t 5.32 -c copy "all_states_aligned/audio_segments/sentence_20/ohio-3_whisper.mp3"

# Extract oregon-4_whisper - 129.92s to 134.88s
ffmpeg -i "audio/oregon/oregon-4.mp3" -ss 129.92 -t 4.96 -c copy "all_states_aligned/audio_segments/sentence_20/oregon-4_whisper.mp3"

# Extract minnesota-9_whisper - 125.28s to 129.40s
ffmpeg -i "audio/minnesota/minnesota-9.mp3" -ss 125.28 -t 4.12 -c copy "all_states_aligned/audio_segments/sentence_20/minnesota-9_whisper.mp3"

# Extract pennsylvania-5_whisper - 119.50s to 125.50s
ffmpeg -i "audio/pennsylvania/pennsylvania-5.mp3" -ss 119.50 -t 6.00 -c copy "all_states_aligned/audio_segments/sentence_20/pennsylvania-5_whisper.mp3"

# Sarah warned that this course of treatment might be expensive—either five or six times the cost of penicillin
mkdir -p all_states_aligned/audio_segments/sentence_21

# Extract montana-2_whisper - 145.92s to 152.40s
ffmpeg -i "audio/montana/montana-2.mp3" -ss 145.92 -t 6.48 -c copy "all_states_aligned/audio_segments/sentence_21/montana-2_whisper.mp3"

# Extract north-dakota-1_whisper - 128.00s to 134.00s
ffmpeg -i "audio/north-dakota/north-dakota-1.mp3" -ss 128.00 -t 6.00 -c copy "all_states_aligned/audio_segments/sentence_21/north-dakota-1_whisper.mp3"

# Extract north-carolina-10_whisper - 98.00s to 101.00s
ffmpeg -i "audio/north-carolina/north-carolina-10.mp3" -ss 98.00 -t 3.00 -c copy "all_states_aligned/audio_segments/sentence_21/north-carolina-10_whisper.mp3"

# Extract south-carolina-9_whisper - 186.00s to 196.00s
ffmpeg -i "audio/south-carolina/south-carolina-9.mp3" -ss 186.00 -t 10.00 -c copy "all_states_aligned/audio_segments/sentence_21/south-carolina-9_whisper.mp3"

# Extract oklahoma-9_whisper - 115.00s to 121.00s
ffmpeg -i "audio/oklahoma/oklahoma-9.mp3" -ss 115.00 -t 6.00 -c copy "all_states_aligned/audio_segments/sentence_21/oklahoma-9_whisper.mp3"

# Extract mississippi-9_whisper - 144.00s to 151.00s
ffmpeg -i "audio/mississippi/mississippi-9.mp3" -ss 144.00 -t 7.00 -c copy "all_states_aligned/audio_segments/sentence_21/mississippi-9_whisper.mp3"

# Extract nebraska-2_whisper - 127.00s to 133.00s
ffmpeg -i "audio/nebraska/nebraska-2.mp3" -ss 127.00 -t 6.00 -c copy "all_states_aligned/audio_segments/sentence_21/nebraska-2_whisper.mp3"

# Extract michigan-15_whisper - 96.88s to 101.36s
ffmpeg -i "audio/michigan/michigan-15.mp3" -ss 96.88 -t 4.48 -c copy "all_states_aligned/audio_segments/sentence_21/michigan-15_whisper.mp3"

# Extract south-dakota-1_whisper - 124.00s to 129.00s
ffmpeg -i "audio/south-dakota/south-dakota-1.mp3" -ss 124.00 -t 5.00 -c copy "all_states_aligned/audio_segments/sentence_21/south-dakota-1_whisper.mp3"

# Extract rhode-island-1_whisper - 138.68s to 142.68s
ffmpeg -i "audio/rhode-island/rhode-island-1.mp3" -ss 138.68 -t 4.00 -c copy "all_states_aligned/audio_segments/sentence_21/rhode-island-1_whisper.mp3"

# Extract received-pronunciation-4_whisper - 124.70s to 131.10s
ffmpeg -i "audio/received-pronunciation/received-pronunciation-4.mp3" -ss 124.70 -t 6.40 -c copy "all_states_aligned/audio_segments/sentence_21/received-pronunciation-4_whisper.mp3"

# Extract nevada-1_whisper - 106.44s to 109.32s
ffmpeg -i "audio/nevada/nevada-1.mp3" -ss 106.44 -t 2.88 -c copy "all_states_aligned/audio_segments/sentence_21/nevada-1_whisper.mp3"

# Extract new-jersey-8_whisper - 113.24s to 117.28s
ffmpeg -i "audio/new-jersey/new-jersey-8.mp3" -ss 113.24 -t 4.04 -c copy "all_states_aligned/audio_segments/sentence_21/new-jersey-8_whisper.mp3"

# Extract ohio-3_whisper - 145.44s to 149.52s
ffmpeg -i "audio/ohio/ohio-3.mp3" -ss 145.44 -t 4.08 -c copy "all_states_aligned/audio_segments/sentence_21/ohio-3_whisper.mp3"

# Extract oregon-4_whisper - 134.88s to 140.24s
ffmpeg -i "audio/oregon/oregon-4.mp3" -ss 134.88 -t 5.36 -c copy "all_states_aligned/audio_segments/sentence_21/oregon-4_whisper.mp3"

# Extract minnesota-9_whisper - 130.64s to 136.40s
ffmpeg -i "audio/minnesota/minnesota-9.mp3" -ss 130.64 -t 5.76 -c copy "all_states_aligned/audio_segments/sentence_21/minnesota-9_whisper.mp3"

# Extract pennsylvania-5_whisper - 125.50s to 132.50s
ffmpeg -i "audio/pennsylvania/pennsylvania-5.mp3" -ss 125.50 -t 7.00 -c copy "all_states_aligned/audio_segments/sentence_21/pennsylvania-5_whisper.mp3"

# I can't imagine paying so much
mkdir -p all_states_aligned/audio_segments/sentence_22
