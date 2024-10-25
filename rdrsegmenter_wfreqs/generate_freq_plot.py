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
    parser.add_argument("--log10", action="store_true", help="Use log10 scale")

    args = parser.parse_args()
    # Load the CSV file
    df = pd.read_csv(args.input_file, names=["word", "frequency"])

    # Sort by frequency in descending order
    df = df.sort_values(by="frequency", ascending=False).reset_index(drop=True)

    # Plot the frequencies
    plt.figure(figsize=(10, 5))
    if not args.log10:
        # Limit the number of points to plot
        max_points = 10_000  # You can adjust this value as needed
        df = df.head(max_points)
        plt.bar(df.index + 1, df["frequency"], width=1)
        plt.xlabel("Word Index (most frequent to least frequent)")
        plt.ylabel("Frequency")
        plt.title("Word Frequencies")
    else:
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

    # Choose colors from a colormap
    cmap = plt.get_cmap("plasma")
    colors = [cmap(i / len(coverage_points)) for i in range(len(coverage_points))]

    # Draw vertical lines at the coverage points and add sideways strings on the x-axis
    for i, point in enumerate(coverage_points):
        plt.axvline(
            x=coverage_indices[point],
            color=colors[i],
            linestyle="--",
            label=f"{point:>4}% coverage at index {coverage_indices[point]}",
        )
        plt.text(
            coverage_indices[point],
            plt.ylim()[0]
            + (plt.ylim()[1] - plt.ylim()[0]) * 0.01,  # Add a small margin
            f"{point}%",
            color=colors[i],
            rotation=90,
            verticalalignment="bottom",
            horizontalalignment="right",
        )

    plt.legend()

    out_name = (
        "word_frequencies.png" if not args.log10 else "word_frequencies_log10.png"
    )
    print(f"Saving plot to '{out_name}'")
    plt.savefig(out_name, dpi=300)
