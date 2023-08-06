from typing import List, Dict

import tensorflow as tf
from tensorflow.python.framework import errors


def read_tf_event_file(event_file: str) -> List[Dict]:
    """
    read single tf event file

    :param event_file: a tf event file
    :return: list of dict, each dict is a record
    """

    summary = tf.train.summary_iterator(event_file)

    all_records = []
    try:
        for event in summary:
            record = {"step": event.step, "wall_time": event.wall_time, "summary": {}}
            for v in event.summary.value:
                record["summary"][v.tag] = v.simple_value

            # if not record["summary"]:
            #     continue

            all_records.append(record)
    except errors.DataLossError:
        return all_records

    return all_records


if __name__ == "__main__":
    # data = "./data/eval/events.out.tfevents.1565339243.howl-MS-7A67"
    # data = "./data/events.out.tfevents.1565338134.howl-MS-7A67"
    data = "./data/events.out.tfevents.1565338566.howl-MS-7A67"

    result = read_tf_event_file(data)
    print(result)
