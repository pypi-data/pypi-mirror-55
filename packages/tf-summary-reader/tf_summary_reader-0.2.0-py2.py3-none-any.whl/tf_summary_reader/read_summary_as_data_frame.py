import collections
import datetime
from typing import List

import pandas as pd

from tf_summary_reader.process_record import process_record
from tf_summary_reader.read_summay import read_summary


def collect_tag_from_record(record_list) -> List[str]:
    """
    get all the metrics name

    :param record_list: list of records
    :return: list of metrics name
    """

    tags = set()
    for record in record_list:
        tags.update(set(record["summary"].keys()))

    return sorted(list(tags))


def read_summary_as_data_frame(summary_dir: str) -> pd.DataFrame:
    raw_records = read_summary(summary_dir)
    records = process_record(raw_records)

    wall_time = [i["wall_time"] for i in records]
    step = [i["step"] for i in records]

    wall_datetime = [datetime.datetime.fromtimestamp(i) for i in wall_time]

    wall_date_index = pd.to_datetime(wall_datetime)

    tags = collect_tag_from_record(records)

    data = collections.OrderedDict()  # column view of dataframe: dict of column (list)
    data["step"] = step

    for tag in tags:
        # create a column if needed
        if tag not in data:
            data[tag] = []

        for record in records:
            v = record["summary"].get(tag)
            data[tag].append(v)

    ts = pd.DataFrame(data, index=wall_date_index)

    return ts


if __name__ == "__main__":
    ts = read_summary_as_data_frame("./data")

    from dateutil import parser

    start_time = parser.parse("2019-08-09 19:00:00")
    end_time = datetime.datetime.now()
    selected_ts = ts[start_time: end_time]
    print("")
