# Python Scripts for processing RDRSegmenter word segmentation

This is a summary of the important scripts (scripts that are not mentioned are considered deprecated):

- `analyse_wfreqs.py input_folder output_file`
  - Analyze word frequencies in a folder text files and outputs it to a output csv with format `word,count`
- `generate_freq_plot.py input_file [--log10]`
  - Generates a plot for the distribution of the word frequencies using a provided file.
  - Optionally can be plotted in log10 scale
- `get_master_dict_list.py`
  - Merges dicts in the kaikki.org Wiktionary dump format to a master dict file, containing only word definitions.
  - Paths are hard coded sorry.
- `merge_extract_wfreqs.py [--master_dict] file1 file2 ...`
  - Merges multiple extracted word frequencies into a single file
  - Optionally filters by a master dict file (only words containing in this file will be included)
  - Will be written to `merged_word_frequencies.csv`
