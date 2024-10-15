import pandas as pd
import argparse
from tqdm import tqdm
import os


def process_folder(input_folder):
    # Read all files in the folder
    wfreqs = {}
    for file in tqdm(os.listdir(input_folder)):
        if file.endswith(".txt"):
            with open(os.path.join(input_folder, file), "r") as f:
                text = f.read().replace("\n", " ").lower()  # test if this lower is ok
                words = text.split(" ")
                for word in words:
                    word = word.replace("_", " ")
                    if word in wfreqs:
                        wfreqs[word] += 1
                    else:
                        wfreqs[word] = 1

    # Create a DataFrame from the word frequencies
    wfreqs_df = pd.DataFrame.from_dict(wfreqs, orient="index", columns=["frequency"])
    wfreqs_df = wfreqs_df.sort_values(by="frequency", ascending=False)
    return wfreqs_df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analyze word frequencies in text files."
    )
    parser.add_argument(
        "input_folder", type=str, help="Path to the input folder containing text files."
    )
    args = parser.parse_args()

    input_folder = args.input_folder

    wfreqs_df = process_folder(input_folder)

    wfreqs_df.to_csv("word_frequencies.csv", header=False)
