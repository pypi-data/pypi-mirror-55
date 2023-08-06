import datetime

import pandas as pd

from tf_summary_reader.read_summary_as_data_frame import read_summary_as_data_frame

previous_time = None


def get_summary_data(summary_dir: str) -> pd.DataFrame:
    """
    get summary data-frame since previous call

    :param summary_dir: directory of tf event files
    :return: pandas data frame of metrics
    """

    global previous_time

    ts = read_summary_as_data_frame(summary_dir)

    if previous_time is None:
        start_time = datetime.datetime(1970, 1, 1, 0, 0, 0)
    else:
        start_time = previous_time

    end_time = datetime.datetime.now()
    previous_time = end_time

    selected_ts = ts[start_time:end_time]

    return selected_ts


if __name__ == "__main__":
    result = get_summary_data("./data")
    print("")
    result = get_summary_data("./data")
    print("")
