#!/bin/bash

# Set the source directory and the destination directory
src_dir="/app/downloads/"
dst_dir="/app/downloads/proc/"

# Set the API endpoint here
INSTANCE="https://files.serverboi.org"
# Set the filestash share id here
SHARE="4NSIb7U"
# Set the API key here
KEY="uploaderapp0585719131"

# Create the destination directory if it doesn't exist
mkdir -p "$dst_dir"

# Find all video files in subdirectories of the source directory
find "$src_dir" -type f \( -iname "*.mp4" -o -iname "*.avi" -o -iname "*.mkv" \) -print0 |
while read -d $'\0' video_file; do
  # Get the relative path of the video file
  relative_path="${video_file#$src_dir}"
  # Extract the file name from the relative path
  file_name="$(basename "$relative_path")"
  # Copy the video file to the destination directory
  mkdir -p "$dst_dir/$(dirname "$relative_path")"
  mv "$video_file" "$dst_dir/$relative_path"

  # Send the file to the server
  file_size=$(stat -c%s "$dst_dir/$relative_path")
  if (( $file_size > 100000000 )); then
    # Split the file into 100MB parts
    split -b 100M "$dst_dir/$relative_path" "$dst_dir/$file_name.part"

    # Send each part to the server
    for part_file in "$dst_dir/$file_name.part"*; do
      part_name=$(basename "$part_file")
      curl "$INSTANCE/api/files/cat?share=$SHARE&key=$KEY&path=$file_name.$part_name" -X POST --data-binary @"$part_file"
    done

    # Remove the split parts
    rm "$dst_dir/$file_name.part"*
  else
    # Send the whole file to the server
    curl "$INSTANCE/api/files/cat?share=$SHARE&key=$KEY&path=$file_name" -X POST --data-binary @"$dst_dir/$relative_path"
  fi
done
rm -rf /app/downloads/*



















