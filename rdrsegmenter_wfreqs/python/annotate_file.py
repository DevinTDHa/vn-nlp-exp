import os
import py_vncorenlp
import argparse

os.environ["JVM_PATH"] = (
    "/usr/lib/jvm/java-8-openjdk-amd64/jre/lib/amd64/server/libjvm.so"
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Annotate a file using VnCoreNLP.")
    parser.add_argument("input_file", type=str, help="Path to the input file.")
    parser.add_argument("output_file", type=str, help="Path to the output file.")
    args = parser.parse_args()

    data_path = "/mnt/SSDSHARED/VN/VnCoreNLP_Wrapper/data"

    # Automatically download VnCoreNLP components from the original repository
    # and save them in some local machine folder
    # py_vncorenlp.download_model(save_dir=data_path)

    rdrsegmenter = py_vncorenlp.VnCoreNLP(annotators=["wseg"], save_dir=data_path)

    rdrsegmenter.annotate_file(input_file=args.input_file, output_file=args.output_file)
