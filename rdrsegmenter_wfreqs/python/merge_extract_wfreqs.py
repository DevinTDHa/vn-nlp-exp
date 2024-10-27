import pandas as pd
import sys
import argparse


def merge_word_frequencies(file_list):
    combined_df = pd.DataFrame()

    for file in file_list:
        df = pd.read_csv(file, names=["word", "count"])
        if combined_df.empty:
            combined_df = df
        else:
            combined_df = pd.concat([combined_df, df])

    combined_df = combined_df.groupby("word", as_index=False).sum()
    return combined_df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Merge word frequencies from multiple CSV files."
    )
    parser.add_argument(
        "--master_dict",
        type=str,
        default=None,
        help="Master dictionary list to filter words by",
    )
    parser.add_argument(
        "files", metavar="FILE", type=str, nargs="+", help="CSV files to merge"
    )

    args = parser.parse_args()

    file_list = args.files

    if args.master_dict:
        print("Loading master dictionary list...")
        master_dict_list = pd.read_csv(args.master_dict)

    print("Merging word frequencies...")
    result_df = merge_word_frequencies(file_list)

    if args.master_dict:
        print("Filtering out words not in the master dictionary list...")
        result_df = result_df[result_df["word"].isin(master_dict_list["word"])]

    sorted_result_df = result_df.sort_values(by="count", ascending=False)
    sorted_result_df.to_csv("merged_word_frequencies.csv", index=False, header=False)
    print("Merged word frequencies saved to 'merged_word_frequencies.csv'")
