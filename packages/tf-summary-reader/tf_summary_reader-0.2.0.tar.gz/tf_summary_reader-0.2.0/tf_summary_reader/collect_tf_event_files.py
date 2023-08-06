import glob
import os
from typing import List


def collect_tf_event_files(event_dir: str, recursive=False) -> List[str]:
    """
    get all the event files from specific directory

    :param event_dir: the directory from which search the tf event files
    :param recursive: Bool, if recursive search sub directory
    :return: list of event files
    """

    event_dir = os.path.abspath(event_dir)
    glob_pattern = os.path.join(event_dir, "*.tfevents.*")
    relative_files = glob.glob(glob_pattern, recursive=recursive)
    files = [os.path.join(event_dir, i) for i in relative_files]
    return files


if __name__ == "__main__":
    event_files = collect_tf_event_files("./data")
    print(event_files)
