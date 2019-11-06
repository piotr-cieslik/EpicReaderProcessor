import textract
import sys
import os
import time
import json

# number of seconds between checks
pause = 15

# define paths to directories
directory_root = "/tmp/epic-reader/"
directory_queued = os.path.join(directory_root, "queued")
directory_processing = os.path.join(directory_root, "processing")
directory_processed = os.path.join(directory_root, "processed")
directory_result = os.path.join(directory_root, "result")

# Doesn't work for python2.
# Using python3 causes problem with encoding of textract result.
# make sure that directories exist
# os.makedirs(directory_queued, exist_ok=True)
# os.makedirs(directory_processing, exist_ok=True)
# os.makedirs(directory_processed, exist_ok=True)
# os.makedirs(directory_result, exist_ok=True)

def process_files():
  print("start processing files...")
  for file in os.listdir(directory_queued):
    processing_start_time = int(time.time())
    file_name = os.path.basename(file)
    file_path_queued = os.path.join(directory_queued, file_name)
    file_path_processing = os.path.join(directory_processing, file_name)
    file_path_processed = os.path.join(directory_processed, file_name)
    file_path_result = os.path.join(directory_result, file_name + ".json")
    
    # Ensure that no one else use this file.
    # Move is atomic operation in linux.
    os.rename(file_path_queued, file_path_processing)
    text = textract.process(file_path_processing, method="tesseract", language="pol")
    processing_end_time = int(time.time())

    # Create result
    result = {
      "status": "success",
      "text": text,
      "processingStartTime": processing_start_time,
      "processingEndTime": processing_end_time,
    }

    # Serialzie result to json
    json_result = json.dumps(result)
    
    # Write result to file
    file_result = open(file_path_result, "w")
    file_result.writelines(json_result)
    file_result.close()
    
    # Mark file as processed by moving it to processed directory
    os.rename(file_path_processing, file_path_processed)
  print("end processing files.")

while True:
  process_files()
  time.sleep(pause)