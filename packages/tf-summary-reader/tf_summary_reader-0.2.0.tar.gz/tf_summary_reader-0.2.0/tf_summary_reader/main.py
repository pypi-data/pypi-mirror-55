# -*- coding: utf-8 -*-
import sys

from tf_summary_reader.read_summary_data_periodically import read_summary_data_periodically

summary_dir = sys.argv[1]

for result in read_summary_data_periodically(summary_dir):
    for timestamp, item in result.iterrows():
        keys = item.keys()
        step = item["step"]
        del item["step"]
        for metric_name, metric_val in item.items():
            print(timestamp, step, metric_name, metric_val)
