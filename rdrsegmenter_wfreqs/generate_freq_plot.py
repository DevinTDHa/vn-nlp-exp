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
        df.index + 1, df["frequency"].apply(lambda x: np.log10(x + 1)), width=1
    )  # Apply logarithmic scale to the frequency
    plt.xlabel("Word Index (most frequent to least frequent)")
    plt.ylabel("Log10(Frequency)")
    plt.title("Word Frequencies (Log10 Scale)")

    # Calculate the cumulative sum and find the 80% coverage point
    cumulative_sum = df["frequency"].cumsum()
    total_sum = df["frequency"].sum()

    # Calculate the cumulative sum and find the coverage points
    coverage_points = [80, 90, 95, 98, 99, 99.5]
    coverage_indices = {}
    for point in coverage_points:
        coverage_indices[point] = (cumulative_sum <= (point / 100) * total_sum).sum()
        print(f"{point}% coverage at index {coverage_indices[point]}")

    # Choose colors from the viridis colormap
    cmap = plt.get_cmap("viridis")
    colors = [cmap(i / len(coverage_points)) for i in range(len(coverage_points))]

    # Draw vertical lines at the coverage points
    for i, point in enumerate(coverage_points):
        plt.axvline(
            x=coverage_indices[point],
            color=colors[i],
            linestyle="--",
            label=f"{point}% coverage at index {coverage_indices[point]}",
        )

    plt.legend()

    print("Saving plot to 'word_frequencies.*'")
    plt.savefig("word_frequencies.png", dpi=300)
    plt.savefig("word_frequencies.svg")
