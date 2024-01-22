import transcript
import json

# Script: YouTube Video Transcription Generator

'''
This script is designed to generate debate transcripts from YouTube videos.

It reads a JSON file containing information about YouTube video URLs, start times, and output file paths.
For each video in the JSON data, it processes the video to generate a transcript.

'''


# Todo: Currently hardcoded url path -- should take it from the commandline maybe?
# Load JSON data from urls.json. Every tournament/dir/urls.json has a list of youtube videos
with open('tournaments/wudc_korea_2023_part_2/urls.json', 'r') as json_file:
    data = json.load(json_file)# schema of this is url, start_time, output_file

# Iterate through the JSON dataEach item is one youtube debate video
for item in data:
    video_id = item['video_id']
    start_time = item['start_time']
    output_file = item['output_file']

    # Your code to process each item goes here
    print(f"Video ID: {video_id}")
    print(f"Start Time: {start_time}")
    print(f"Output File: {output_file}")
    
    transcript.main(video_id, start_time, output_file)
