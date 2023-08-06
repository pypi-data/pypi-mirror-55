from typing import List, Dict

from tf_summary_reader.preprocess.process_record_clean_empty_summary import process_record_clean_empty_summary
from tf_summary_reader.preprocess.process_record_merge_summary import process_record_merge_summary


def process_record(record_list: List[Dict]) -> List[Dict]:
    """
    clean and merge records

    :param record_list: list of records
    :return: list of records
    """
    intermediate_result = process_record_clean_empty_summary(record_list)
    result = process_record_merge_summary(intermediate_result)

    return result
