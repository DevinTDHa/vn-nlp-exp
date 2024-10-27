import pandas as pd


if __name__ == "__main__":
    wikt_path = "/mnt/SSDSHARED/VN/dicts/wikt/kaikki.org-dictionary-Vietnamese.jsonl"
    witkionary_df = pd.read_json(wikt_path, lines=True)

    free_dict_path = "/mnt/SSDSHARED/VN/dicts/FreeVietnameseDictionaryProjectExport/data/vietanh.dict.jsonl"
    free_dict_df = pd.read_json(free_dict_path, lines=True)

    wikt_words = witkionary_df["word"]
    freed_words = free_dict_df["word"]

    merged = pd.concat([wikt_words, freed_words])
    merged = merged.drop_duplicates()

    merged.to_csv("master_dict_list.txt", index=False)
