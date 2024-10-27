#!/bin/bash
# Check if the correct number of arguments is provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <file> <output_folder> <lines_per_chunk>"
    exit 1
fi

input_file=$1
output_folder=$2
lines_per_chunk=$3

# Check if the input file exists
if [ ! -f "$input_file" ]; then
    echo "File not found: $input_file"
    exit 1
fi

# Create the output folder if it doesn't exist
mkdir -p "$output_folder"

# Split the file into chunks and save them in the output folder
split --numeric-suffixes=1 --additional-suffix=".txt" -l "$lines_per_chunk" "$input_file" "$output_folder/most_frequent_"

echo "File has been split into chunks of $lines_per_chunk lines each and saved in $output_folder."
