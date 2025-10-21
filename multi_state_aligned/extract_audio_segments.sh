#!/bin/bash
# Generated script to extract comma story audio segments
# Output directory: multi_state_aligned/audio_segments

set -e

mkdir -p multi_state_aligned/audio_segments

# Well, here's a story for you
mkdir -p multi_state_aligned/audio_segments/sentence_0

# Extract north-carolina-10_whisper - 10.00s to 17.00s
ffmpeg -i "audio/north-carolina/north-carolina-10.mp3" -ss 10.00 -t 7.00 -c copy "multi_state_aligned/audio_segments/sentence_0/north-carolina-10_whisper.mp3"

# Extract oklahoma-9_whisper - 12.00s to 21.00s
ffmpeg -i "audio/oklahoma/oklahoma-9.mp3" -ss 12.00 -t 9.00 -c copy "multi_state_aligned/audio_segments/sentence_0/oklahoma-9_whisper.mp3"

# Extract mississippi-9_whisper - 13.00s to 24.00s
ffmpeg -i "audio/mississippi/mississippi-9.mp3" -ss 13.00 -t 11.00 -c copy "multi_state_aligned/audio_segments/sentence_0/mississippi-9_whisper.mp3"

# Extract new-mexico-4_whisper - 12.00s to 23.00s
ffmpeg -i "audio/new-mexico/new-mexico-4.mp3" -ss 12.00 -t 11.00 -c copy "multi_state_aligned/audio_segments/sentence_0/new-mexico-4_whisper.mp3"

# Extract ohio-3_whisper - 10.96s to 17.00s
ffmpeg -i "audio/ohio/ohio-3.mp3" -ss 10.96 -t 6.04 -c copy "multi_state_aligned/audio_segments/sentence_0/ohio-3_whisper.mp3"

# Sarah Perry was a veterinary nurse who had been working daily at an old zoo in a deserted district of the territory
mkdir -p multi_state_aligned/audio_segments/sentence_1

# Extract north-carolina-10_whisper - 10.00s to 17.00s
ffmpeg -i "audio/north-carolina/north-carolina-10.mp3" -ss 10.00 -t 7.00 -c copy "multi_state_aligned/audio_segments/sentence_1/north-carolina-10_whisper.mp3"

# Extract oklahoma-9_whisper - 12.00s to 21.00s
ffmpeg -i "audio/oklahoma/oklahoma-9.mp3" -ss 12.00 -t 9.00 -c copy "multi_state_aligned/audio_segments/sentence_1/oklahoma-9_whisper.mp3"

# Extract mississippi-9_whisper - 13.00s to 24.00s
ffmpeg -i "audio/mississippi/mississippi-9.mp3" -ss 13.00 -t 11.00 -c copy "multi_state_aligned/audio_segments/sentence_1/mississippi-9_whisper.mp3"

# Extract new-mexico-4_whisper - 12.00s to 23.00s
ffmpeg -i "audio/new-mexico/new-mexico-4.mp3" -ss 12.00 -t 11.00 -c copy "multi_state_aligned/audio_segments/sentence_1/new-mexico-4_whisper.mp3"

# Extract ohio-3_whisper - 10.96s to 17.00s
ffmpeg -i "audio/ohio/ohio-3.mp3" -ss 10.96 -t 6.04 -c copy "multi_state_aligned/audio_segments/sentence_1/ohio-3_whisper.mp3"

# so she was very happy to start a new job at a superb private practice in north square near the Duke Street Tower
mkdir -p multi_state_aligned/audio_segments/sentence_2

# Extract north-carolina-10_whisper - 17.00s to 22.00s
ffmpeg -i "audio/north-carolina/north-carolina-10.mp3" -ss 17.00 -t 5.00 -c copy "multi_state_aligned/audio_segments/sentence_2/north-carolina-10_whisper.mp3"

# Extract oklahoma-9_whisper - 21.00s to 28.00s
ffmpeg -i "audio/oklahoma/oklahoma-9.mp3" -ss 21.00 -t 7.00 -c copy "multi_state_aligned/audio_segments/sentence_2/oklahoma-9_whisper.mp3"

# Extract mississippi-9_whisper - 24.00s to 32.00s
ffmpeg -i "audio/mississippi/mississippi-9.mp3" -ss 24.00 -t 8.00 -c copy "multi_state_aligned/audio_segments/sentence_2/mississippi-9_whisper.mp3"

# Extract new-mexico-4_whisper - 23.00s to 28.00s
ffmpeg -i "audio/new-mexico/new-mexico-4.mp3" -ss 23.00 -t 5.00 -c copy "multi_state_aligned/audio_segments/sentence_2/new-mexico-4_whisper.mp3"

# Extract ohio-3_whisper - 21.16s to 29.16s
ffmpeg -i "audio/ohio/ohio-3.mp3" -ss 21.16 -t 8.00 -c copy "multi_state_aligned/audio_segments/sentence_2/ohio-3_whisper.mp3"

# That area was much nearer for her and more to her liking
mkdir -p multi_state_aligned/audio_segments/sentence_3

# Extract north-carolina-10_whisper - 22.00s to 26.00s
ffmpeg -i "audio/north-carolina/north-carolina-10.mp3" -ss 22.00 -t 4.00 -c copy "multi_state_aligned/audio_segments/sentence_3/north-carolina-10_whisper.mp3"

# Extract oklahoma-9_whisper - 28.00s to 31.00s
ffmpeg -i "audio/oklahoma/oklahoma-9.mp3" -ss 28.00 -t 3.00 -c copy "multi_state_aligned/audio_segments/sentence_3/oklahoma-9_whisper.mp3"

# Extract mississippi-9_whisper - 32.00s to 39.00s
ffmpeg -i "audio/mississippi/mississippi-9.mp3" -ss 32.00 -t 7.00 -c copy "multi_state_aligned/audio_segments/sentence_3/mississippi-9_whisper.mp3"

# Extract new-mexico-4_whisper - 28.00s to 33.00s
ffmpeg -i "audio/new-mexico/new-mexico-4.mp3" -ss 28.00 -t 5.00 -c copy "multi_state_aligned/audio_segments/sentence_3/new-mexico-4_whisper.mp3"

# Extract ohio-3_whisper - 29.16s to 38.88s
ffmpeg -i "audio/ohio/ohio-3.mp3" -ss 29.16 -t 9.72 -c copy "multi_state_aligned/audio_segments/sentence_3/ohio-3_whisper.mp3"

# Even so, on her first morning, she felt stressed
mkdir -p multi_state_aligned/audio_segments/sentence_4

# Extract north-carolina-10_whisper - 26.00s to 32.00s
ffmpeg -i "audio/north-carolina/north-carolina-10.mp3" -ss 26.00 -t 6.00 -c copy "multi_state_aligned/audio_segments/sentence_4/north-carolina-10_whisper.mp3"

# Extract oklahoma-9_whisper - 31.00s to 34.00s
ffmpeg -i "audio/oklahoma/oklahoma-9.mp3" -ss 31.00 -t 3.00 -c copy "multi_state_aligned/audio_segments/sentence_4/oklahoma-9_whisper.mp3"

# Extract mississippi-9_whisper - 32.00s to 39.00s
ffmpeg -i "audio/mississippi/mississippi-9.mp3" -ss 32.00 -t 7.00 -c copy "multi_state_aligned/audio_segments/sentence_4/mississippi-9_whisper.mp3"

# Extract new-mexico-4_whisper - 33.00s to 37.00s
ffmpeg -i "audio/new-mexico/new-mexico-4.mp3" -ss 33.00 -t 4.00 -c copy "multi_state_aligned/audio_segments/sentence_4/new-mexico-4_whisper.mp3"

# Extract ohio-3_whisper - 29.16s to 38.88s
ffmpeg -i "audio/ohio/ohio-3.mp3" -ss 29.16 -t 9.72 -c copy "multi_state_aligned/audio_segments/sentence_4/ohio-3_whisper.mp3"

# She ate a bowl of porridge, checked herself in the mirror and washed her face in a hurry
mkdir -p multi_state_aligned/audio_segments/sentence_5

# Extract north-carolina-10_whisper - 26.00s to 32.00s
ffmpeg -i "audio/north-carolina/north-carolina-10.mp3" -ss 26.00 -t 6.00 -c copy "multi_state_aligned/audio_segments/sentence_5/north-carolina-10_whisper.mp3"

# Extract oklahoma-9_whisper - 34.00s to 39.00s
ffmpeg -i "audio/oklahoma/oklahoma-9.mp3" -ss 34.00 -t 5.00 -c copy "multi_state_aligned/audio_segments/sentence_5/oklahoma-9_whisper.mp3"

# Extract mississippi-9_whisper - 39.00s to 46.00s
ffmpeg -i "audio/mississippi/mississippi-9.mp3" -ss 39.00 -t 7.00 -c copy "multi_state_aligned/audio_segments/sentence_5/mississippi-9_whisper.mp3"

# Extract new-mexico-4_whisper - 37.00s to 42.00s
ffmpeg -i "audio/new-mexico/new-mexico-4.mp3" -ss 37.00 -t 5.00 -c copy "multi_state_aligned/audio_segments/sentence_5/new-mexico-4_whisper.mp3"

# Extract ohio-3_whisper - 38.88s to 43.68s
ffmpeg -i "audio/ohio/ohio-3.mp3" -ss 38.88 -t 4.80 -c copy "multi_state_aligned/audio_segments/sentence_5/ohio-3_whisper.mp3"

# Then she put on a plain yellow dress and a fleece jacket, picked up her kit and headed for work
mkdir -p multi_state_aligned/audio_segments/sentence_6

# Extract north-carolina-10_whisper - 32.00s to 38.00s
ffmpeg -i "audio/north-carolina/north-carolina-10.mp3" -ss 32.00 -t 6.00 -c copy "multi_state_aligned/audio_segments/sentence_6/north-carolina-10_whisper.mp3"

# Extract oklahoma-9_whisper - 39.00s to 45.00s
ffmpeg -i "audio/oklahoma/oklahoma-9.mp3" -ss 39.00 -t 6.00 -c copy "multi_state_aligned/audio_segments/sentence_6/oklahoma-9_whisper.mp3"

# Extract mississippi-9_whisper - 46.00s to 53.00s
ffmpeg -i "audio/mississippi/mississippi-9.mp3" -ss 46.00 -t 7.00 -c copy "multi_state_aligned/audio_segments/sentence_6/mississippi-9_whisper.mp3"

# Extract new-mexico-4_whisper - 42.00s to 48.00s
ffmpeg -i "audio/new-mexico/new-mexico-4.mp3" -ss 42.00 -t 6.00 -c copy "multi_state_aligned/audio_segments/sentence_6/new-mexico-4_whisper.mp3"

# Extract ohio-3_whisper - 43.68s to 50.04s
ffmpeg -i "audio/ohio/ohio-3.mp3" -ss 43.68 -t 6.36 -c copy "multi_state_aligned/audio_segments/sentence_6/ohio-3_whisper.mp3"

# When she got there, there was a woman with a goose waiting for her
mkdir -p multi_state_aligned/audio_segments/sentence_7

# Extract north-carolina-10_whisper - 38.00s to 41.00s
ffmpeg -i "audio/north-carolina/north-carolina-10.mp3" -ss 38.00 -t 3.00 -c copy "multi_state_aligned/audio_segments/sentence_7/north-carolina-10_whisper.mp3"

# Extract oklahoma-9_whisper - 45.00s to 49.00s
ffmpeg -i "audio/oklahoma/oklahoma-9.mp3" -ss 45.00 -t 4.00 -c copy "multi_state_aligned/audio_segments/sentence_7/oklahoma-9_whisper.mp3"

# Extract mississippi-9_whisper - 53.00s to 61.00s
ffmpeg -i "audio/mississippi/mississippi-9.mp3" -ss 53.00 -t 8.00 -c copy "multi_state_aligned/audio_segments/sentence_7/mississippi-9_whisper.mp3"

# Extract new-mexico-4_whisper - 48.00s to 51.00s
ffmpeg -i "audio/new-mexico/new-mexico-4.mp3" -ss 48.00 -t 3.00 -c copy "multi_state_aligned/audio_segments/sentence_7/new-mexico-4_whisper.mp3"

# Extract ohio-3_whisper - 50.04s to 54.08s
ffmpeg -i "audio/ohio/ohio-3.mp3" -ss 50.04 -t 4.04 -c copy "multi_state_aligned/audio_segments/sentence_7/ohio-3_whisper.mp3"

# The woman gave Sarah an official letter from the vet
mkdir -p multi_state_aligned/audio_segments/sentence_8

# Extract oklahoma-9_whisper - 49.00s to 52.00s
ffmpeg -i "audio/oklahoma/oklahoma-9.mp3" -ss 49.00 -t 3.00 -c copy "multi_state_aligned/audio_segments/sentence_8/oklahoma-9_whisper.mp3"

# Extract mississippi-9_whisper - 53.00s to 61.00s
ffmpeg -i "audio/mississippi/mississippi-9.mp3" -ss 53.00 -t 8.00 -c copy "multi_state_aligned/audio_segments/sentence_8/mississippi-9_whisper.mp3"

# Extract ohio-3_whisper - 54.08s to 58.56s
ffmpeg -i "audio/ohio/ohio-3.mp3" -ss 54.08 -t 4.48 -c copy "multi_state_aligned/audio_segments/sentence_8/ohio-3_whisper.mp3"

# The letter implied that the animal could be suffering from a rare form of foot and mouth disease, which was surprising, because normally you would only expect to see it in a dog or a goat
mkdir -p multi_state_aligned/audio_segments/sentence_9

# Extract north-carolina-10_whisper - 44.00s to 49.00s
ffmpeg -i "audio/north-carolina/north-carolina-10.mp3" -ss 44.00 -t 5.00 -c copy "multi_state_aligned/audio_segments/sentence_9/north-carolina-10_whisper.mp3"

# Extract oklahoma-9_whisper - 52.00s to 61.00s
ffmpeg -i "audio/oklahoma/oklahoma-9.mp3" -ss 52.00 -t 9.00 -c copy "multi_state_aligned/audio_segments/sentence_9/oklahoma-9_whisper.mp3"

# Extract mississippi-9_whisper - 61.00s to 73.00s
ffmpeg -i "audio/mississippi/mississippi-9.mp3" -ss 61.00 -t 12.00 -c copy "multi_state_aligned/audio_segments/sentence_9/mississippi-9_whisper.mp3"

# Extract new-mexico-4_whisper - 63.00s to 68.00s
ffmpeg -i "audio/new-mexico/new-mexico-4.mp3" -ss 63.00 -t 5.00 -c copy "multi_state_aligned/audio_segments/sentence_9/new-mexico-4_whisper.mp3"

# Extract ohio-3_whisper - 58.56s to 66.08s
ffmpeg -i "audio/ohio/ohio-3.mp3" -ss 58.56 -t 7.52 -c copy "multi_state_aligned/audio_segments/sentence_9/ohio-3_whisper.mp3"

# Sarah was sentimental, so this made her feel sorry for the beautiful bird
mkdir -p multi_state_aligned/audio_segments/sentence_10

# Extract oklahoma-9_whisper - 61.00s to 65.00s
ffmpeg -i "audio/oklahoma/oklahoma-9.mp3" -ss 61.00 -t 4.00 -c copy "multi_state_aligned/audio_segments/sentence_10/oklahoma-9_whisper.mp3"

# Extract mississippi-9_whisper - 73.00s to 79.00s
ffmpeg -i "audio/mississippi/mississippi-9.mp3" -ss 73.00 -t 6.00 -c copy "multi_state_aligned/audio_segments/sentence_10/mississippi-9_whisper.mp3"

# Extract new-mexico-4_whisper - 68.00s to 73.00s
ffmpeg -i "audio/new-mexico/new-mexico-4.mp3" -ss 68.00 -t 5.00 -c copy "multi_state_aligned/audio_segments/sentence_10/new-mexico-4_whisper.mp3"

# Extract ohio-3_whisper - 71.28s to 77.16s
ffmpeg -i "audio/ohio/ohio-3.mp3" -ss 71.28 -t 5.88 -c copy "multi_state_aligned/audio_segments/sentence_10/ohio-3_whisper.mp3"

# Before long, that itchy goose began to strut around the office like a lunatic, which made an unsanitary mess
mkdir -p multi_state_aligned/audio_segments/sentence_11

# Extract north-carolina-10_whisper - 58.00s to 63.00s
ffmpeg -i "audio/north-carolina/north-carolina-10.mp3" -ss 58.00 -t 5.00 -c copy "multi_state_aligned/audio_segments/sentence_11/north-carolina-10_whisper.mp3"

# Extract oklahoma-9_whisper - 65.00s to 71.00s
ffmpeg -i "audio/oklahoma/oklahoma-9.mp3" -ss 65.00 -t 6.00 -c copy "multi_state_aligned/audio_segments/sentence_11/oklahoma-9_whisper.mp3"

# Extract mississippi-9_whisper - 79.00s to 87.00s
ffmpeg -i "audio/mississippi/mississippi-9.mp3" -ss 79.00 -t 8.00 -c copy "multi_state_aligned/audio_segments/sentence_11/mississippi-9_whisper.mp3"

# Extract new-mexico-4_whisper - 73.00s to 82.00s
ffmpeg -i "audio/new-mexico/new-mexico-4.mp3" -ss 73.00 -t 9.00 -c copy "multi_state_aligned/audio_segments/sentence_11/new-mexico-4_whisper.mp3"

# Extract ohio-3_whisper - 77.16s to 83.40s
ffmpeg -i "audio/ohio/ohio-3.mp3" -ss 77.16 -t 6.24 -c copy "multi_state_aligned/audio_segments/sentence_11/ohio-3_whisper.mp3"

# The goose's owner, Mary Harrison, kept calling, "Comma, Comma," which Sarah thought was an odd choice for a name
mkdir -p multi_state_aligned/audio_segments/sentence_12

# Extract north-carolina-10_whisper - 63.00s to 66.00s
ffmpeg -i "audio/north-carolina/north-carolina-10.mp3" -ss 63.00 -t 3.00 -c copy "multi_state_aligned/audio_segments/sentence_12/north-carolina-10_whisper.mp3"

# Extract oklahoma-9_whisper - 71.00s to 78.00s
ffmpeg -i "audio/oklahoma/oklahoma-9.mp3" -ss 71.00 -t 7.00 -c copy "multi_state_aligned/audio_segments/sentence_12/oklahoma-9_whisper.mp3"

# Extract mississippi-9_whisper - 87.00s to 99.00s
ffmpeg -i "audio/mississippi/mississippi-9.mp3" -ss 87.00 -t 12.00 -c copy "multi_state_aligned/audio_segments/sentence_12/mississippi-9_whisper.mp3"

# Extract new-mexico-4_whisper - 82.00s to 91.00s
ffmpeg -i "audio/new-mexico/new-mexico-4.mp3" -ss 82.00 -t 9.00 -c copy "multi_state_aligned/audio_segments/sentence_12/new-mexico-4_whisper.mp3"

# Extract ohio-3_whisper - 88.76s to 93.28s
ffmpeg -i "audio/ohio/ohio-3.mp3" -ss 88.76 -t 4.52 -c copy "multi_state_aligned/audio_segments/sentence_12/ohio-3_whisper.mp3"

# Comma was strong and huge, so it would take some force to trap her, but Sarah had a different idea
mkdir -p multi_state_aligned/audio_segments/sentence_13

# Extract north-carolina-10_whisper - 70.00s to 79.00s
ffmpeg -i "audio/north-carolina/north-carolina-10.mp3" -ss 70.00 -t 9.00 -c copy "multi_state_aligned/audio_segments/sentence_13/north-carolina-10_whisper.mp3"

# Extract oklahoma-9_whisper - 78.00s to 84.00s
ffmpeg -i "audio/oklahoma/oklahoma-9.mp3" -ss 78.00 -t 6.00 -c copy "multi_state_aligned/audio_segments/sentence_13/oklahoma-9_whisper.mp3"

# Extract mississippi-9_whisper - 99.00s to 107.00s
ffmpeg -i "audio/mississippi/mississippi-9.mp3" -ss 99.00 -t 8.00 -c copy "multi_state_aligned/audio_segments/sentence_13/mississippi-9_whisper.mp3"

# Extract new-mexico-4_whisper - 91.00s to 93.00s
ffmpeg -i "audio/new-mexico/new-mexico-4.mp3" -ss 91.00 -t 2.00 -c copy "multi_state_aligned/audio_segments/sentence_13/new-mexico-4_whisper.mp3"

# Extract ohio-3_whisper - 98.72s to 103.48s
ffmpeg -i "audio/ohio/ohio-3.mp3" -ss 98.72 -t 4.76 -c copy "multi_state_aligned/audio_segments/sentence_13/ohio-3_whisper.mp3"

# First she tried gently stroking the goose's lower back with her palm, then singing a tune to her
mkdir -p multi_state_aligned/audio_segments/sentence_14

# Extract north-carolina-10_whisper - 70.00s to 79.00s
ffmpeg -i "audio/north-carolina/north-carolina-10.mp3" -ss 70.00 -t 9.00 -c copy "multi_state_aligned/audio_segments/sentence_14/north-carolina-10_whisper.mp3"

# Extract oklahoma-9_whisper - 84.00s to 90.00s
ffmpeg -i "audio/oklahoma/oklahoma-9.mp3" -ss 84.00 -t 6.00 -c copy "multi_state_aligned/audio_segments/sentence_14/oklahoma-9_whisper.mp3"

# Extract mississippi-9_whisper - 107.00s to 117.00s
ffmpeg -i "audio/mississippi/mississippi-9.mp3" -ss 107.00 -t 10.00 -c copy "multi_state_aligned/audio_segments/sentence_14/mississippi-9_whisper.mp3"

# Extract new-mexico-4_whisper - 99.00s to 106.00s
ffmpeg -i "audio/new-mexico/new-mexico-4.mp3" -ss 99.00 -t 7.00 -c copy "multi_state_aligned/audio_segments/sentence_14/new-mexico-4_whisper.mp3"

# Extract ohio-3_whisper - 109.16s to 112.80s
ffmpeg -i "audio/ohio/ohio-3.mp3" -ss 109.16 -t 3.64 -c copy "multi_state_aligned/audio_segments/sentence_14/ohio-3_whisper.mp3"

# Finally, she administered ether
mkdir -p multi_state_aligned/audio_segments/sentence_15

# Extract oklahoma-9_whisper - 90.00s to 92.00s
ffmpeg -i "audio/oklahoma/oklahoma-9.mp3" -ss 90.00 -t 2.00 -c copy "multi_state_aligned/audio_segments/sentence_15/oklahoma-9_whisper.mp3"

# Extract ohio-3_whisper - 115.00s to 119.48s
ffmpeg -i "audio/ohio/ohio-3.mp3" -ss 115.00 -t 4.48 -c copy "multi_state_aligned/audio_segments/sentence_15/ohio-3_whisper.mp3"

# Her efforts were not futile
mkdir -p multi_state_aligned/audio_segments/sentence_16

# Extract north-carolina-10_whisper - 79.00s to 81.00s
ffmpeg -i "audio/north-carolina/north-carolina-10.mp3" -ss 79.00 -t 2.00 -c copy "multi_state_aligned/audio_segments/sentence_16/north-carolina-10_whisper.mp3"

# Extract mississippi-9_whisper - 117.00s to 127.00s
ffmpeg -i "audio/mississippi/mississippi-9.mp3" -ss 117.00 -t 10.00 -c copy "multi_state_aligned/audio_segments/sentence_16/mississippi-9_whisper.mp3"

# In no time, the goose began to tire, so Sarah was able to hold onto Comma and give her a relaxing bath
mkdir -p multi_state_aligned/audio_segments/sentence_17

# Extract north-carolina-10_whisper - 81.00s to 86.00s
ffmpeg -i "audio/north-carolina/north-carolina-10.mp3" -ss 81.00 -t 5.00 -c copy "multi_state_aligned/audio_segments/sentence_17/north-carolina-10_whisper.mp3"

# Extract oklahoma-9_whisper - 94.00s to 100.00s
ffmpeg -i "audio/oklahoma/oklahoma-9.mp3" -ss 94.00 -t 6.00 -c copy "multi_state_aligned/audio_segments/sentence_17/oklahoma-9_whisper.mp3"

# Extract mississippi-9_whisper - 117.00s to 127.00s
ffmpeg -i "audio/mississippi/mississippi-9.mp3" -ss 117.00 -t 10.00 -c copy "multi_state_aligned/audio_segments/sentence_17/mississippi-9_whisper.mp3"

# Extract new-mexico-4_whisper - 114.00s to 122.00s
ffmpeg -i "audio/new-mexico/new-mexico-4.mp3" -ss 114.00 -t 8.00 -c copy "multi_state_aligned/audio_segments/sentence_17/new-mexico-4_whisper.mp3"

# Extract ohio-3_whisper - 119.48s to 124.48s
ffmpeg -i "audio/ohio/ohio-3.mp3" -ss 119.48 -t 5.00 -c copy "multi_state_aligned/audio_segments/sentence_17/ohio-3_whisper.mp3"

# Once Sarah had managed to bathe the goose, she wiped her off with a cloth and laid her on her right side
mkdir -p multi_state_aligned/audio_segments/sentence_18

# Extract oklahoma-9_whisper - 100.00s to 107.00s
ffmpeg -i "audio/oklahoma/oklahoma-9.mp3" -ss 100.00 -t 7.00 -c copy "multi_state_aligned/audio_segments/sentence_18/oklahoma-9_whisper.mp3"

# Extract mississippi-9_whisper - 127.00s to 134.00s
ffmpeg -i "audio/mississippi/mississippi-9.mp3" -ss 127.00 -t 7.00 -c copy "multi_state_aligned/audio_segments/sentence_18/mississippi-9_whisper.mp3"

# Extract ohio-3_whisper - 130.80s to 136.64s
ffmpeg -i "audio/ohio/ohio-3.mp3" -ss 130.80 -t 5.84 -c copy "multi_state_aligned/audio_segments/sentence_18/ohio-3_whisper.mp3"

# Then Sarah confirmed the vet's diagnosis
mkdir -p multi_state_aligned/audio_segments/sentence_19

# Almost immediately, she remembered an effective treatment that required her to measure out a lot of medicine
mkdir -p multi_state_aligned/audio_segments/sentence_20

# Extract north-carolina-10_whisper - 90.00s to 96.00s
ffmpeg -i "audio/north-carolina/north-carolina-10.mp3" -ss 90.00 -t 6.00 -c copy "multi_state_aligned/audio_segments/sentence_20/north-carolina-10_whisper.mp3"

# Extract oklahoma-9_whisper - 110.00s to 115.00s
ffmpeg -i "audio/oklahoma/oklahoma-9.mp3" -ss 110.00 -t 5.00 -c copy "multi_state_aligned/audio_segments/sentence_20/oklahoma-9_whisper.mp3"

# Extract mississippi-9_whisper - 134.00s to 144.00s
ffmpeg -i "audio/mississippi/mississippi-9.mp3" -ss 134.00 -t 10.00 -c copy "multi_state_aligned/audio_segments/sentence_20/mississippi-9_whisper.mp3"

# Extract ohio-3_whisper - 140.12s to 145.44s
ffmpeg -i "audio/ohio/ohio-3.mp3" -ss 140.12 -t 5.32 -c copy "multi_state_aligned/audio_segments/sentence_20/ohio-3_whisper.mp3"

# Sarah warned that this course of treatment might be expensive—either five or six times the cost of penicillin
mkdir -p multi_state_aligned/audio_segments/sentence_21

# Extract north-carolina-10_whisper - 98.00s to 101.00s
ffmpeg -i "audio/north-carolina/north-carolina-10.mp3" -ss 98.00 -t 3.00 -c copy "multi_state_aligned/audio_segments/sentence_21/north-carolina-10_whisper.mp3"

# Extract oklahoma-9_whisper - 115.00s to 121.00s
ffmpeg -i "audio/oklahoma/oklahoma-9.mp3" -ss 115.00 -t 6.00 -c copy "multi_state_aligned/audio_segments/sentence_21/oklahoma-9_whisper.mp3"

# Extract mississippi-9_whisper - 144.00s to 151.00s
ffmpeg -i "audio/mississippi/mississippi-9.mp3" -ss 144.00 -t 7.00 -c copy "multi_state_aligned/audio_segments/sentence_21/mississippi-9_whisper.mp3"

# Extract ohio-3_whisper - 145.44s to 149.52s
ffmpeg -i "audio/ohio/ohio-3.mp3" -ss 145.44 -t 4.08 -c copy "multi_state_aligned/audio_segments/sentence_21/ohio-3_whisper.mp3"

# I can't imagine paying so much
mkdir -p multi_state_aligned/audio_segments/sentence_22
