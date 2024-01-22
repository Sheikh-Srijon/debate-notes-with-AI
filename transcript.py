from youtube_transcript_api import YouTubeTranscriptApi
import sys
import json
import os 
# class inputs : video_id, start_time


# @get_end_time takes start in seconds.
def get_end_time(start):
    seconds_in_a_minute = 60
    return start + seconds_in_a_minute * 8


def speech(start, end, obj_list):
    result = ""
    
    for obj in obj_list:
        obj_start = obj["start"]
        if obj_start >= start and obj_start <= end:
            result += obj["text"] + " "

    return result.strip()



def write_output(all_speeches, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    output_data = []
    speaker_number = 1
    for speech in all_speeches:
        output_data.append({
            "speaker": speaker_number,
            "speech": speech
        })
        speaker_number += 1
    
    with open(output_file, "w") as json_file:
        json.dump(output_data, json_file)
# Todo error check when transcript not available in the api
def main(video_id="", start_time=200.0, output_file="output.txt"):
    # video_id = "https://www.youtube.com/watch?v=Ys0Sgicnjz4" is the part after v= in the parameters of url
    # Schema of transcript[0] :
    # {'text': 'going to define a marxist revolution in', 'start': 247.05, 'duration': 4.5},
    start_time = float(start_time)
    transcript = None 
    try:
      transcript = YouTubeTranscriptApi.get_transcript(video_id)  
    except:
      print("Transcript not available for video id: ", video_id)
      return
    # todo: error check for invalid video id
    # get all 8 speeches
    all_starts = [start_time]
    for i in range(8):
        end_time = get_end_time(start_time)
        all_starts.append(get_end_time(start_time))
        start_time = end_time
    # print(all_starts)

    all_speeches = []

    for i in range(1, len(all_starts)):
        start_time = all_starts[i - 1]
        end_time = all_starts[i]
        current_speech = speech(start_time, end_time, transcript)
        all_speeches.append(current_speech)
    # result = speech(start_time, end_time, transcript)
    write_output(
        all_speeches,
        output_file
    )

# * we give the video id and start time as input, for each video we have to hardcode the start time
if __name__ == "__main__":
    # should take video_id, start_time as input
    if len(sys.argv) != 4:
        raise ValueError("Usage: python script_name.py <video_id> <start_time>")
    main(video_id=sys.argv[1], start_time=sys.argv[2], output_file=sys.argv[3])

    
   
    # main(video_id=sys.argv[1], start_time=sys.argv[2], output_file=sys.argv[4])
