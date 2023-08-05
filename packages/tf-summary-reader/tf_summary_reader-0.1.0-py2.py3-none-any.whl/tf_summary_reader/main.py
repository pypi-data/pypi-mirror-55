# -*- coding: utf-8 -*-
import sys
import time

from tf_summary_reader.get_summary_data import get_summary_data

summary_dir = sys.argv[1]
time_interval_in_seconds = 10

while True:
    result = get_summary_data(summary_dir)
    print(result)

    time.sleep(time_interval_in_seconds)
