#!/bin/bash

# Check if the input file is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <input_file>"
    exit 1
fi

input_file="$1"
output_file="${input_file%.*}_only_words.${input_file##*.}"

# Extract the first column (words) and write to the output file
awk -F, '{print $1}' "$input_file" >"$output_file"

echo "Output written to $output_file"
