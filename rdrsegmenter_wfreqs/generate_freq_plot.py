import numpy as np
import pandas as pd
import argparse

import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("Agg")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Generate frequency plot from CSV file."
    )
    parser.add_argument("input_file", type=str, help="Path to the input CSV file")

    args = parser.parse_args()
    # Load the CSV file
    df = pd.read_csv(args.input_file, names=["word", "frequency"])

    # Sort by frequency in descending order
    df = df.sort_values(by="frequency", ascending=False).reset_index(drop=True)

    # Plot the frequencies
    plt.figure(figsize=(10, 5))
    plt.bar(
        df.index + 1, df["frequency"].apply(lambda x: np.log(x + 1)), width=1
    )  # Apply logarithmic scale to the frequency
    plt.xlabel("Word Index (most frequent to least frequent)")
    plt.ylabel("Log(Frequency)")
    plt.title("Word Frequencies (Log Scale)")

    # Calculate the cumulative sum and find the 80% coverage point
    cumulative_sum = df["frequency"].cumsum()
    total_sum = df["frequency"].sum()

    # https://forum.language-learners.org/viewtopic.php?t=16463
    eighty_percent_index = (cumulative_sum <= 0.8 * total_sum).sum()
    ninety_five_percent_index = (cumulative_sum <= 0.95 * total_sum).sum()
    print(f"80% coverage at index {eighty_percent_index}")
    print(f"95% coverage at index {ninety_five_percent_index}")

    # Draw a vertical line at the 80% coverage point
    plt.axvline(
        x=eighty_percent_index,
        color="r",
        linestyle="--",
        label=f"80% coverage at index {eighty_percent_index}",
    )
    plt.axvline(
        x=ninety_five_percent_index,
        color="orange",
        linestyle="--",
        label=f"95% coverage at index {ninety_five_percent_index}",
    )
    plt.legend()

    print("Saving plot to 'word_frequencies.png'")
    plt.savefig("word_frequencies.png", dpi=300)
