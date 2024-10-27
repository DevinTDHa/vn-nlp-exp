# Shell Scripts for processing RDRSegmenter word segmentation

- `only_words.sh input_file`
  - Extracts only the first column of the output file to an output file
- `split_evenly.sh input_file output_folder lines_per_chunk`
  - Splits a large file to evenly sized ones. Useful to extract the first n-thousand words.
