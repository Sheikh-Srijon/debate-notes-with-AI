from pytube import Playlist
import json 

# Replace 'YOUR_PLAYLIST_URL' with the URL of the YouTube playlist you want to scrape
playlist_url = 'https://www.youtube.com/playlist?list=PLCAT23LupiCqHa_SST3O0IkFeY_L7Xi1L'
def extract_video_id(youtube_url):
    # Split the URL by "v="
    parts = youtube_url.split("v=")
    
    # Check if there are at least two parts (before and after "v=")
    if len(parts) >= 2:
        # Extract and return the second part (the video ID)
        video_id = parts[1]
        return video_id
    else:
        # If there are not enough parts, return None or raise an exception, as needed
        return None

try:
    # Create a Playlist object
    playlist = Playlist(playlist_url)

    # Print the title of the playlist
    print("Playlist Title:", playlist.title)

    # Initialize lists to store video URLs and titles
    video_urls = []
    video_titles = []

    # Loop through each video in the playlist
    video_json = []
    dir_prefix ="tournaments/wudc_korea_2023_part_2"
    
    for video in playlist.videos:
        # Append the video URL and title to their respective lists
        video_id = extract_video_id(video.watch_url)
        video_urls.append(video_id)
        # process video.title
        parts = video.title.split("Korea WUDC 2021")
        custom_video_title = parts[1].strip()
        video_titles.append(custom_video_title)
        video_json.append({
            "video_id": video_id,
            "start_time": 0,
            "output_file": f"{dir_prefix}/{custom_video_title}.json"
        })
except Exception as e:
    print("Error:", str(e))
    # Print the video URLs and titles
#!  Write the video_json array to a JSON file
# Specify the directory where you want to save the JSON file
output_dir = "tournaments/wudc_korea_2023_part_2"  # Replace with your desired directory path

# Create the full file path for the JSON file
json_file_path = f"{output_dir}/urls.json"
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(video_json, json_file, ensure_ascii=False, indent=4)

print(f"Video data written to {json_file_path}")
    


