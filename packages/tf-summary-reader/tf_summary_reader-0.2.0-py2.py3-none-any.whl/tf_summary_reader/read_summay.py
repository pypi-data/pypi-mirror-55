from tf_summary_reader.collect_tf_event_files import collect_tf_event_files
from tf_summary_reader.read_tf_event_file import read_tf_event_file


def read_summary(event_dir, recursive=False):
    event_files = collect_tf_event_files(event_dir, recursive)

    all_record = []
    for event_file in event_files:
        file_record = read_tf_event_file(event_file)
        all_record.extend(file_record)

    return all_record


if __name__ == "__main__":
    records = read_summary("./data")
    print(records)
