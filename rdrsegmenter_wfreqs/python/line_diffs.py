import sys

def read_file_to_set(file_path):
    with open(file_path, 'r') as file:
        return set(line.strip() for line in file)

def main(file1, file2):
    set1 = read_file_to_set(file1)
    set2 = read_file_to_set(file2)
    
    differences = set1.symmetric_difference(set2)
    
    print("Differences:")
    for item in differences:
        print(item)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python line_diffs.py <file1> <file2>")
    else:
        main(sys.argv[1], sys.argv[2])