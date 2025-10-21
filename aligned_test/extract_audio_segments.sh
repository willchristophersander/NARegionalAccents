#!/bin/bash
# Generated script to extract comma story audio segments
# Output directory: aligned_test/audio_segments

set -e

mkdir -p aligned_test/audio_segments

# Well, here's a story for you
mkdir -p aligned_test/audio_segments/sentence_0

# Extract alaska-2_transcription - 11.68s to 20.64s
ffmpeg -i "audio/alaska/alaska-2.mp3" -ss 11.68 -t 8.96 -c copy "aligned_test/audio_segments/sentence_0/alaska-2_transcription.mp3"

# Extract alaska-5_transcription - 12.08s to 14.80s
ffmpeg -i "audio/alaska/alaska-5.mp3" -ss 12.08 -t 2.72 -c copy "aligned_test/audio_segments/sentence_0/alaska-5_transcription.mp3"

# Extract alaska-3_transcription - 12.00s to 15.00s
ffmpeg -i "audio/alaska/alaska-3.mp3" -ss 12.00 -t 3.00 -c copy "aligned_test/audio_segments/sentence_0/alaska-3_transcription.mp3"

# Extract nevada-1_whisper - 13.08s to 16.28s
ffmpeg -i "audio/nevada/nevada-1.mp3" -ss 13.08 -t 3.20 -c copy "aligned_test/audio_segments/sentence_0/nevada-1_whisper.mp3"

# Extract alaska-1_transcription - 12.08s to 17.68s
ffmpeg -i "audio/alaska/alaska-1.mp3" -ss 12.08 -t 5.60 -c copy "aligned_test/audio_segments/sentence_0/alaska-1_transcription.mp3"

# Sarah Perry was a veterinary nurse who had been working daily at an old zoo in a deserted district of the territory
mkdir -p aligned_test/audio_segments/sentence_1

# Extract alaska-2_transcription - 11.68s to 20.64s
ffmpeg -i "audio/alaska/alaska-2.mp3" -ss 11.68 -t 8.96 -c copy "aligned_test/audio_segments/sentence_1/alaska-2_transcription.mp3"

# Extract alaska-5_transcription - 14.80s to 22.00s
ffmpeg -i "audio/alaska/alaska-5.mp3" -ss 14.80 -t 7.20 -c copy "aligned_test/audio_segments/sentence_1/alaska-5_transcription.mp3"

# Extract alaska-3_transcription - 15.00s to 25.00s
ffmpeg -i "audio/alaska/alaska-3.mp3" -ss 15.00 -t 10.00 -c copy "aligned_test/audio_segments/sentence_1/alaska-3_transcription.mp3"

# Extract nevada-1_whisper - 16.28s to 20.32s
ffmpeg -i "audio/nevada/nevada-1.mp3" -ss 16.28 -t 4.04 -c copy "aligned_test/audio_segments/sentence_1/nevada-1_whisper.mp3"

# Extract alaska-1_transcription - 12.08s to 17.68s
ffmpeg -i "audio/alaska/alaska-1.mp3" -ss 12.08 -t 5.60 -c copy "aligned_test/audio_segments/sentence_1/alaska-1_transcription.mp3"

# so she was very happy to start a new job at a superb private practice in north square near the Duke Street Tower
mkdir -p aligned_test/audio_segments/sentence_2

# Extract alaska-2_transcription - 25.84s to 34.40s
ffmpeg -i "audio/alaska/alaska-2.mp3" -ss 25.84 -t 8.56 -c copy "aligned_test/audio_segments/sentence_2/alaska-2_transcription.mp3"

# Extract alaska-5_transcription - 22.00s to 25.92s
ffmpeg -i "audio/alaska/alaska-5.mp3" -ss 22.00 -t 3.92 -c copy "aligned_test/audio_segments/sentence_2/alaska-5_transcription.mp3"

# Extract alaska-3_transcription - 25.00s to 34.00s
ffmpeg -i "audio/alaska/alaska-3.mp3" -ss 25.00 -t 9.00 -c copy "aligned_test/audio_segments/sentence_2/alaska-3_transcription.mp3"

# Extract nevada-1_whisper - 24.62s to 27.84s
ffmpeg -i "audio/nevada/nevada-1.mp3" -ss 24.62 -t 3.22 -c copy "aligned_test/audio_segments/sentence_2/nevada-1_whisper.mp3"

# That area was much nearer for her and more to her liking
mkdir -p aligned_test/audio_segments/sentence_3

# Extract alaska-2_transcription - 34.40s to 44.72s
ffmpeg -i "audio/alaska/alaska-2.mp3" -ss 34.40 -t 10.32 -c copy "aligned_test/audio_segments/sentence_3/alaska-2_transcription.mp3"

# Extract alaska-5_transcription - 28.48s to 32.32s
ffmpeg -i "audio/alaska/alaska-5.mp3" -ss 28.48 -t 3.84 -c copy "aligned_test/audio_segments/sentence_3/alaska-5_transcription.mp3"

# Extract alaska-3_transcription - 34.00s to 40.00s
ffmpeg -i "audio/alaska/alaska-3.mp3" -ss 34.00 -t 6.00 -c copy "aligned_test/audio_segments/sentence_3/alaska-3_transcription.mp3"

# Extract nevada-1_whisper - 27.84s to 31.38s
ffmpeg -i "audio/nevada/nevada-1.mp3" -ss 27.84 -t 3.54 -c copy "aligned_test/audio_segments/sentence_3/nevada-1_whisper.mp3"

# Extract alaska-1_transcription - 31.44s to 36.00s
ffmpeg -i "audio/alaska/alaska-1.mp3" -ss 31.44 -t 4.56 -c copy "aligned_test/audio_segments/sentence_3/alaska-1_transcription.mp3"

# Even so, on her first morning, she felt stressed
mkdir -p aligned_test/audio_segments/sentence_4

# Extract alaska-2_transcription - 44.72s to 58.24s
ffmpeg -i "audio/alaska/alaska-2.mp3" -ss 44.72 -t 13.52 -c copy "aligned_test/audio_segments/sentence_4/alaska-2_transcription.mp3"

# Extract alaska-5_transcription - 32.32s to 36.08s
ffmpeg -i "audio/alaska/alaska-5.mp3" -ss 32.32 -t 3.76 -c copy "aligned_test/audio_segments/sentence_4/alaska-5_transcription.mp3"

# Extract alaska-3_transcription - 40.00s to 53.00s
ffmpeg -i "audio/alaska/alaska-3.mp3" -ss 40.00 -t 13.00 -c copy "aligned_test/audio_segments/sentence_4/alaska-3_transcription.mp3"

# Extract nevada-1_whisper - 31.38s to 34.72s
ffmpeg -i "audio/nevada/nevada-1.mp3" -ss 31.38 -t 3.34 -c copy "aligned_test/audio_segments/sentence_4/nevada-1_whisper.mp3"

# Extract alaska-1_transcription - 36.88s to 42.00s
ffmpeg -i "audio/alaska/alaska-1.mp3" -ss 36.88 -t 5.12 -c copy "aligned_test/audio_segments/sentence_4/alaska-1_transcription.mp3"

# She ate a bowl of porridge, checked herself in the mirror and washed her face in a hurry
mkdir -p aligned_test/audio_segments/sentence_5

# Extract alaska-2_transcription - 44.72s to 58.24s
ffmpeg -i "audio/alaska/alaska-2.mp3" -ss 44.72 -t 13.52 -c copy "aligned_test/audio_segments/sentence_5/alaska-2_transcription.mp3"

# Extract alaska-5_transcription - 36.08s to 40.32s
ffmpeg -i "audio/alaska/alaska-5.mp3" -ss 36.08 -t 4.24 -c copy "aligned_test/audio_segments/sentence_5/alaska-5_transcription.mp3"

# Extract alaska-3_transcription - 40.00s to 53.00s
ffmpeg -i "audio/alaska/alaska-3.mp3" -ss 40.00 -t 13.00 -c copy "aligned_test/audio_segments/sentence_5/alaska-3_transcription.mp3"

# Extract nevada-1_whisper - 34.72s to 38.44s
ffmpeg -i "audio/nevada/nevada-1.mp3" -ss 34.72 -t 3.72 -c copy "aligned_test/audio_segments/sentence_5/nevada-1_whisper.mp3"

# Extract alaska-1_transcription - 36.88s to 42.00s
ffmpeg -i "audio/alaska/alaska-1.mp3" -ss 36.88 -t 5.12 -c copy "aligned_test/audio_segments/sentence_5/alaska-1_transcription.mp3"

# Then she put on a plain yellow dress and a fleece jacket, picked up her kit and headed for work
mkdir -p aligned_test/audio_segments/sentence_6

# Extract alaska-2_transcription - 58.24s to 65.92s
ffmpeg -i "audio/alaska/alaska-2.mp3" -ss 58.24 -t 7.68 -c copy "aligned_test/audio_segments/sentence_6/alaska-2_transcription.mp3"

# Extract alaska-5_transcription - 40.88s to 43.84s
ffmpeg -i "audio/alaska/alaska-5.mp3" -ss 40.88 -t 2.96 -c copy "aligned_test/audio_segments/sentence_6/alaska-5_transcription.mp3"

# Extract alaska-3_transcription - 53.00s to 61.00s
ffmpeg -i "audio/alaska/alaska-3.mp3" -ss 53.00 -t 8.00 -c copy "aligned_test/audio_segments/sentence_6/alaska-3_transcription.mp3"

# Extract nevada-1_whisper - 38.44s to 41.72s
ffmpeg -i "audio/nevada/nevada-1.mp3" -ss 38.44 -t 3.28 -c copy "aligned_test/audio_segments/sentence_6/nevada-1_whisper.mp3"

# Extract alaska-1_transcription - 46.48s to 52.72s
ffmpeg -i "audio/alaska/alaska-1.mp3" -ss 46.48 -t 6.24 -c copy "aligned_test/audio_segments/sentence_6/alaska-1_transcription.mp3"

# When she got there, there was a woman with a goose waiting for her
mkdir -p aligned_test/audio_segments/sentence_7

# Extract alaska-2_transcription - 66.96s to 74.16s
ffmpeg -i "audio/alaska/alaska-2.mp3" -ss 66.96 -t 7.20 -c copy "aligned_test/audio_segments/sentence_7/alaska-2_transcription.mp3"

# Extract alaska-5_transcription - 46.40s to 49.84s
ffmpeg -i "audio/alaska/alaska-5.mp3" -ss 46.40 -t 3.44 -c copy "aligned_test/audio_segments/sentence_7/alaska-5_transcription.mp3"

# Extract alaska-3_transcription - 61.00s to 65.00s
ffmpeg -i "audio/alaska/alaska-3.mp3" -ss 61.00 -t 4.00 -c copy "aligned_test/audio_segments/sentence_7/alaska-3_transcription.mp3"

# Extract nevada-1_whisper - 43.08s to 46.00s
ffmpeg -i "audio/nevada/nevada-1.mp3" -ss 43.08 -t 2.92 -c copy "aligned_test/audio_segments/sentence_7/nevada-1_whisper.mp3"

# Extract alaska-1_transcription - 53.52s to 56.96s
ffmpeg -i "audio/alaska/alaska-1.mp3" -ss 53.52 -t 3.44 -c copy "aligned_test/audio_segments/sentence_7/alaska-1_transcription.mp3"

# The woman gave Sarah an official letter from the vet
mkdir -p aligned_test/audio_segments/sentence_8

# Extract alaska-2_transcription - 74.16s to 85.36s
ffmpeg -i "audio/alaska/alaska-2.mp3" -ss 74.16 -t 11.20 -c copy "aligned_test/audio_segments/sentence_8/alaska-2_transcription.mp3"

# Extract alaska-5_transcription - 49.84s to 52.88s
ffmpeg -i "audio/alaska/alaska-5.mp3" -ss 49.84 -t 3.04 -c copy "aligned_test/audio_segments/sentence_8/alaska-5_transcription.mp3"

# Extract alaska-3_transcription - 65.00s to 70.00s
ffmpeg -i "audio/alaska/alaska-3.mp3" -ss 65.00 -t 5.00 -c copy "aligned_test/audio_segments/sentence_8/alaska-3_transcription.mp3"

# Extract nevada-1_whisper - 46.00s to 48.60s
ffmpeg -i "audio/nevada/nevada-1.mp3" -ss 46.00 -t 2.60 -c copy "aligned_test/audio_segments/sentence_8/nevada-1_whisper.mp3"

# Extract alaska-1_transcription - 57.68s to 60.48s
ffmpeg -i "audio/alaska/alaska-1.mp3" -ss 57.68 -t 2.80 -c copy "aligned_test/audio_segments/sentence_8/alaska-1_transcription.mp3"

# The letter implied that the animal could be suffering from a rare form of foot and mouth disease, which was surprising, because normally you would only expect to see it in a dog or a goat
mkdir -p aligned_test/audio_segments/sentence_9

# Extract alaska-2_transcription - 85.36s to 92.24s
ffmpeg -i "audio/alaska/alaska-2.mp3" -ss 85.36 -t 6.88 -c copy "aligned_test/audio_segments/sentence_9/alaska-2_transcription.mp3"

# Extract alaska-5_transcription - 52.88s to 57.60s
ffmpeg -i "audio/alaska/alaska-5.mp3" -ss 52.88 -t 4.72 -c copy "aligned_test/audio_segments/sentence_9/alaska-5_transcription.mp3"

# Extract alaska-3_transcription - 70.00s to 80.00s
ffmpeg -i "audio/alaska/alaska-3.mp3" -ss 70.00 -t 10.00 -c copy "aligned_test/audio_segments/sentence_9/alaska-3_transcription.mp3"

# Sarah was sentimental, so this made her feel sorry for the beautiful bird
mkdir -p aligned_test/audio_segments/sentence_10

# Extract alaska-2_transcription - 93.36s to 102.40s
ffmpeg -i "audio/alaska/alaska-2.mp3" -ss 93.36 -t 9.04 -c copy "aligned_test/audio_segments/sentence_10/alaska-2_transcription.mp3"

# Extract alaska-5_transcription - 62.16s to 66.00s
ffmpeg -i "audio/alaska/alaska-5.mp3" -ss 62.16 -t 3.84 -c copy "aligned_test/audio_segments/sentence_10/alaska-5_transcription.mp3"

# Extract alaska-3_transcription - 85.00s to 92.00s
ffmpeg -i "audio/alaska/alaska-3.mp3" -ss 85.00 -t 7.00 -c copy "aligned_test/audio_segments/sentence_10/alaska-3_transcription.mp3"

# Extract nevada-1_whisper - 56.60s to 60.36s
ffmpeg -i "audio/nevada/nevada-1.mp3" -ss 56.60 -t 3.76 -c copy "aligned_test/audio_segments/sentence_10/nevada-1_whisper.mp3"

# Extract alaska-1_transcription - 74.40s to 79.76s
ffmpeg -i "audio/alaska/alaska-1.mp3" -ss 74.40 -t 5.36 -c copy "aligned_test/audio_segments/sentence_10/alaska-1_transcription.mp3"

# Before long, that itchy goose began to strut around the office like a lunatic, which made an unsanitary mess
mkdir -p aligned_test/audio_segments/sentence_11

# Extract alaska-2_transcription - 102.48s to 110.40s
ffmpeg -i "audio/alaska/alaska-2.mp3" -ss 102.48 -t 7.92 -c copy "aligned_test/audio_segments/sentence_11/alaska-2_transcription.mp3"

# Extract alaska-5_transcription - 66.88s to 71.76s
ffmpeg -i "audio/alaska/alaska-5.mp3" -ss 66.88 -t 4.88 -c copy "aligned_test/audio_segments/sentence_11/alaska-5_transcription.mp3"

# Extract alaska-3_transcription - 92.00s to 102.00s
ffmpeg -i "audio/alaska/alaska-3.mp3" -ss 92.00 -t 10.00 -c copy "aligned_test/audio_segments/sentence_11/alaska-3_transcription.mp3"

# Extract nevada-1_whisper - 60.36s to 64.32s
ffmpeg -i "audio/nevada/nevada-1.mp3" -ss 60.36 -t 3.96 -c copy "aligned_test/audio_segments/sentence_11/nevada-1_whisper.mp3"

# Extract alaska-1_transcription - 80.48s to 86.72s
ffmpeg -i "audio/alaska/alaska-1.mp3" -ss 80.48 -t 6.24 -c copy "aligned_test/audio_segments/sentence_11/alaska-1_transcription.mp3"

# The goose's owner, Mary Harrison, kept calling, "Comma, Comma," which Sarah thought was an odd choice for a name
mkdir -p aligned_test/audio_segments/sentence_12

# Extract alaska-2_transcription - 122.64s to 130.64s
ffmpeg -i "audio/alaska/alaska-2.mp3" -ss 122.64 -t 8.00 -c copy "aligned_test/audio_segments/sentence_12/alaska-2_transcription.mp3"

# Extract alaska-5_transcription - 73.92s to 78.08s
ffmpeg -i "audio/alaska/alaska-5.mp3" -ss 73.92 -t 4.16 -c copy "aligned_test/audio_segments/sentence_12/alaska-5_transcription.mp3"

# Extract nevada-1_whisper - 67.72s to 71.68s
ffmpeg -i "audio/nevada/nevada-1.mp3" -ss 67.72 -t 3.96 -c copy "aligned_test/audio_segments/sentence_12/nevada-1_whisper.mp3"

# Extract alaska-1_transcription - 87.20s to 95.92s
ffmpeg -i "audio/alaska/alaska-1.mp3" -ss 87.20 -t 8.72 -c copy "aligned_test/audio_segments/sentence_12/alaska-1_transcription.mp3"

# Comma was strong and huge, so it would take some force to trap her, but Sarah had a different idea
mkdir -p aligned_test/audio_segments/sentence_13

# Extract alaska-2_transcription - 130.72s to 138.64s
ffmpeg -i "audio/alaska/alaska-2.mp3" -ss 130.72 -t 7.92 -c copy "aligned_test/audio_segments/sentence_13/alaska-2_transcription.mp3"

# Extract alaska-5_transcription - 80.64s to 84.88s
ffmpeg -i "audio/alaska/alaska-5.mp3" -ss 80.64 -t 4.24 -c copy "aligned_test/audio_segments/sentence_13/alaska-5_transcription.mp3"

# Extract alaska-3_transcription - 113.00s to 120.00s
ffmpeg -i "audio/alaska/alaska-3.mp3" -ss 113.00 -t 7.00 -c copy "aligned_test/audio_segments/sentence_13/alaska-3_transcription.mp3"

# Extract nevada-1_whisper - 74.24s to 77.92s
ffmpeg -i "audio/nevada/nevada-1.mp3" -ss 74.24 -t 3.68 -c copy "aligned_test/audio_segments/sentence_13/nevada-1_whisper.mp3"

# Extract alaska-1_transcription - 95.92s to 102.24s
ffmpeg -i "audio/alaska/alaska-1.mp3" -ss 95.92 -t 6.32 -c copy "aligned_test/audio_segments/sentence_13/alaska-1_transcription.mp3"

# First she tried gently stroking the goose's lower back with her palm, then singing a tune to her
mkdir -p aligned_test/audio_segments/sentence_14

# Extract alaska-2_transcription - 139.60s to 145.92s
ffmpeg -i "audio/alaska/alaska-2.mp3" -ss 139.60 -t 6.32 -c copy "aligned_test/audio_segments/sentence_14/alaska-2_transcription.mp3"

# Extract alaska-5_transcription - 87.12s to 91.04s
ffmpeg -i "audio/alaska/alaska-5.mp3" -ss 87.12 -t 3.92 -c copy "aligned_test/audio_segments/sentence_14/alaska-5_transcription.mp3"

# Extract alaska-3_transcription - 123.00s to 130.00s
ffmpeg -i "audio/alaska/alaska-3.mp3" -ss 123.00 -t 7.00 -c copy "aligned_test/audio_segments/sentence_14/alaska-3_transcription.mp3"

# Extract nevada-1_whisper - 78.92s to 82.68s
ffmpeg -i "audio/nevada/nevada-1.mp3" -ss 78.92 -t 3.76 -c copy "aligned_test/audio_segments/sentence_14/nevada-1_whisper.mp3"

# Extract alaska-1_transcription - 109.20s to 114.08s
ffmpeg -i "audio/alaska/alaska-1.mp3" -ss 109.20 -t 4.88 -c copy "aligned_test/audio_segments/sentence_14/alaska-1_transcription.mp3"

# Finally, she administered ether
mkdir -p aligned_test/audio_segments/sentence_15

# Extract nevada-1_whisper - 84.08s to 86.28s
ffmpeg -i "audio/nevada/nevada-1.mp3" -ss 84.08 -t 2.20 -c copy "aligned_test/audio_segments/sentence_15/nevada-1_whisper.mp3"

# Her efforts were not futile
mkdir -p aligned_test/audio_segments/sentence_16

# Extract nevada-1_whisper - 86.28s to 88.04s
ffmpeg -i "audio/nevada/nevada-1.mp3" -ss 86.28 -t 1.76 -c copy "aligned_test/audio_segments/sentence_16/nevada-1_whisper.mp3"

# In no time, the goose began to tire, so Sarah was able to hold onto Comma and give her a relaxing bath
mkdir -p aligned_test/audio_segments/sentence_17

# Extract alaska-2_transcription - 164.40s to 173.36s
ffmpeg -i "audio/alaska/alaska-2.mp3" -ss 164.40 -t 8.96 -c copy "aligned_test/audio_segments/sentence_17/alaska-2_transcription.mp3"

# Extract alaska-3_transcription - 136.00s to 146.00s
ffmpeg -i "audio/alaska/alaska-3.mp3" -ss 136.00 -t 10.00 -c copy "aligned_test/audio_segments/sentence_17/alaska-3_transcription.mp3"

# Extract nevada-1_whisper - 88.04s to 91.86s
ffmpeg -i "audio/nevada/nevada-1.mp3" -ss 88.04 -t 3.82 -c copy "aligned_test/audio_segments/sentence_17/nevada-1_whisper.mp3"

# Extract alaska-1_transcription - 121.36s to 128.32s
ffmpeg -i "audio/alaska/alaska-1.mp3" -ss 121.36 -t 6.96 -c copy "aligned_test/audio_segments/sentence_17/alaska-1_transcription.mp3"

# Once Sarah had managed to bathe the goose, she wiped her off with a cloth and laid her on her right side
mkdir -p aligned_test/audio_segments/sentence_18

# Extract alaska-2_transcription - 164.40s to 173.36s
ffmpeg -i "audio/alaska/alaska-2.mp3" -ss 164.40 -t 8.96 -c copy "aligned_test/audio_segments/sentence_18/alaska-2_transcription.mp3"

# Extract alaska-3_transcription - 146.00s to 154.00s
ffmpeg -i "audio/alaska/alaska-3.mp3" -ss 146.00 -t 8.00 -c copy "aligned_test/audio_segments/sentence_18/alaska-3_transcription.mp3"

# Extract nevada-1_whisper - 93.40s to 97.20s
ffmpeg -i "audio/nevada/nevada-1.mp3" -ss 93.40 -t 3.80 -c copy "aligned_test/audio_segments/sentence_18/nevada-1_whisper.mp3"

# Extract alaska-1_transcription - 128.32s to 136.08s
ffmpeg -i "audio/alaska/alaska-1.mp3" -ss 128.32 -t 7.76 -c copy "aligned_test/audio_segments/sentence_18/alaska-1_transcription.mp3"

# Then Sarah confirmed the vet's diagnosis
mkdir -p aligned_test/audio_segments/sentence_19

# Almost immediately, she remembered an effective treatment that required her to measure out a lot of medicine
mkdir -p aligned_test/audio_segments/sentence_20

# Extract alaska-2_transcription - 181.60s to 189.04s
ffmpeg -i "audio/alaska/alaska-2.mp3" -ss 181.60 -t 7.44 -c copy "aligned_test/audio_segments/sentence_20/alaska-2_transcription.mp3"

# Extract alaska-3_transcription - 158.00s to 166.00s
ffmpeg -i "audio/alaska/alaska-3.mp3" -ss 158.00 -t 8.00 -c copy "aligned_test/audio_segments/sentence_20/alaska-3_transcription.mp3"

# Extract nevada-1_whisper - 101.48s to 104.52s
ffmpeg -i "audio/nevada/nevada-1.mp3" -ss 101.48 -t 3.04 -c copy "aligned_test/audio_segments/sentence_20/nevada-1_whisper.mp3"

# Extract alaska-1_transcription - 143.20s to 150.24s
ffmpeg -i "audio/alaska/alaska-1.mp3" -ss 143.20 -t 7.04 -c copy "aligned_test/audio_segments/sentence_20/alaska-1_transcription.mp3"

# Sarah warned that this course of treatment might be expensive—either five or six times the cost of penicillin
mkdir -p aligned_test/audio_segments/sentence_21

# Extract alaska-2_transcription - 190.16s to 197.60s
ffmpeg -i "audio/alaska/alaska-2.mp3" -ss 190.16 -t 7.44 -c copy "aligned_test/audio_segments/sentence_21/alaska-2_transcription.mp3"

# Extract alaska-5_transcription - 118.00s to 121.44s
ffmpeg -i "audio/alaska/alaska-5.mp3" -ss 118.00 -t 3.44 -c copy "aligned_test/audio_segments/sentence_21/alaska-5_transcription.mp3"

# Extract alaska-3_transcription - 166.00s to 176.00s
ffmpeg -i "audio/alaska/alaska-3.mp3" -ss 166.00 -t 10.00 -c copy "aligned_test/audio_segments/sentence_21/alaska-3_transcription.mp3"

# Extract nevada-1_whisper - 106.44s to 109.32s
ffmpeg -i "audio/nevada/nevada-1.mp3" -ss 106.44 -t 2.88 -c copy "aligned_test/audio_segments/sentence_21/nevada-1_whisper.mp3"

# Extract alaska-1_transcription - 151.20s to 157.68s
ffmpeg -i "audio/alaska/alaska-1.mp3" -ss 151.20 -t 6.48 -c copy "aligned_test/audio_segments/sentence_21/alaska-1_transcription.mp3"

# I can't imagine paying so much
mkdir -p aligned_test/audio_segments/sentence_22
