import os
import json
# from llm import write_md, prompting_independently
from llm import write_md, prompting_independently
#reads every json file of debate transcript
def load_and_print_json_files(directory):
  all_data = []
  all_filenames = []
  for root, _, files in os.walk(directory):
    for file_name in files:
        if file_name.endswith('.json'):
          file_path = os.path.join(root, file_name)
          with open(file_path, 'r') as json_file:
              try:
                  data = json.load(json_file)
                  all_filenames.append(file_name)
                  all_data.append(data)
                  print(f"Successfully loaded {file_path}")
              except json.JSONDecodeError as e:
                  print(f"Error loading {file_path}: {e}")
              except Exception as e:
                  print(f"An error occurred while processing {file_path}: {e}")
  return all_data, all_filenames
# Example usage:


#Todo cal

def write_summaries(directory_path):
  all_data, all_filenames = load_and_print_json_files(directory_path)
  for i, data in enumerate(all_data):
    
  
    transcript_dir_prefix = "tournaments/wudc_korea_2023_part_2/"
    
    filename = transcript_dir_prefix +  all_filenames[i]
    notes = prompting_independently(filename)
    dir = "output/" + filename
    dir = dir.split(".")[0] + ".md"
    write_md(notes, dir)
    print(f"processed {filename} ", i)
    # debug 
    
# Todo should be passing this path as a command line argument
if __name__ == "__main__":
  directory_path = "tournaments/wudc_korea_2023_part_2"
  write_summaries(directory_path)