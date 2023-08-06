# -*- coding: utf-8 -*-
import time

from tf_summary_reader.get_summary_data import get_summary_data


def read_summary_data_periodically(summary_dir, time_interval_in_seconds=10):
    while True:
        result = get_summary_data(summary_dir)
        yield result

        time.sleep(time_interval_in_seconds)
