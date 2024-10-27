import os
import argparse
import multiprocessing
import queue
from tqdm import tqdm
from vws import RDRSegmenter, Tokenizer
import re

os.environ["JVM_PATH"] = (
    "/usr/lib/jvm/java-8-openjdk-amd64/jre/lib/amd64/server/libjvm.so"
)


class Worker(multiprocessing.Process):
    def __init__(self, task_queue, output_folder, bar_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.output_folder = output_folder
        # self.result_queue = result_queue
        self.rdrsegment = RDRSegmenter.RDRSegmenter()
        self.tokenizer = Tokenizer.Tokenizer()
        self.bar_queue = bar_queue
        clean_pattern = r"[^_A-Za-zÀ-ỹĐđ ]"
        self.clean_pattern = re.compile(clean_pattern)

    def run(self):
        while True:
            try:
                file_path = self.task_queue.get(timeout=1)
                if file_path is None:  # We're done
                    break
                try:
                    self.execute_task(file_path, self.output_folder)
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")
                    # Print the backtrace
                    import traceback

                    traceback.print_exc()

                self.bar_queue.put(1)
            except queue.Empty:
                continue

    def remove_all_other_chars(self, text):
        cleaned = re.sub(self.clean_pattern, " ", text)
        cleaned = re.sub(r"\s+", " ", cleaned)
        return cleaned

    def execute_task(self, input_file, output_folder):
        output_file = os.path.join(output_folder, os.path.basename(input_file))
        if os.path.exists(output_file):
            return

        out_string = ""
        with open(input_file, "r") as f:
            for line in f:
                if not line:
                    continue
                result = self.rdrsegment.segmentRawSentences(self.tokenizer, line)
                result = self.remove_all_other_chars(result)
                if result:
                    out_string += result.strip() + "\n"

        with open(output_file, "w+") as output_f:
            output_f.write(out_string)


def update_bar(q, total):
    pbar = tqdm(total=total, desc="Processing files")

    while True:
        x = q.get()
        pbar.update(x)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Annotate a folder of files using VnCoreNLP."
    )
    parser.add_argument("input_folder", type=str, help="Path to the input folder.")
    parser.add_argument("output_folder", type=str, help="Path to the output folder.")
    parser.add_argument(
        "--num_workers", type=int, default=6, help="Number of worker processes."
    )
    args = parser.parse_args()

    num_workers = args.num_workers

    total_files = len(os.listdir(args.input_folder))
    bar_queue = multiprocessing.Queue()

    bar_process = multiprocessing.Process(
        target=update_bar, args=(bar_queue, total_files), daemon=True
    )
    bar_process.start()

    os.makedirs(args.output_folder, exist_ok=True)

    task_queue = multiprocessing.Queue()
    # Create and start worker processes
    workers = []
    for _ in range(num_workers):
        worker = Worker(
            task_queue, output_folder=args.output_folder, bar_queue=bar_queue
        )
        worker.start()
        workers.append(worker)

    # Add tasks to the queue
    for file_name in os.listdir(args.input_folder):
        file_path = os.path.join(args.input_folder, file_name)
        task_queue.put(file_path)

    # Add termination signals
    for _ in range(num_workers):
        task_queue.put(None)

    # Wait for all workers to finish
    for worker in workers:
        worker.join()

    # Collect results
    print("All tasks completed")
