import copy
from typing import List, Dict


def process_record_merge_summary(record_list: List[Dict]) -> List[Dict]:
    """
    merge records that have same step summary into single one record

    :param record_list: list of record
    :return: list of record
    """
    record_dict = {}  # step -> record
    for record in record_list:
        step = record["step"]

        if step not in record_dict:
            record_dict[step] = record
        else:
            new_record = copy.deepcopy(
                record
            )  # new record have newer wall_time, record_list are ordered

            old_record = record_dict[step]

            old_key = set(old_record["summary"].keys())
            current_key = set(record["summary"].keys())
            if old_key & current_key:
                raise ValueError("{}, {} have same keys".format(old_record, record))

            old_summary = old_record["summary"]
            new_summary = record["summary"]
            new_summary.update(old_summary)

            new_record["summary"] = new_summary

            record_dict[step] = new_record

    return list(sorted(record_dict.values(), key=lambda x: x["step"]))


if __name__ == "__main__":
    data = [
        {
            "step": 1,
            "wall_time": 1565338664.317573,
            "summary": {
                "acc": 0.003722084453329444,
                "precision": 0.003722084453329444,
                "recall": 0.007317073177546263,
                "f1": 0.004934210795909166,
                "correct_rate": 0.0,
                "loss": 71.3306655883789,
            },
        },
        {
            "step": 101,
            "wall_time": 1565338673.0802393,
            "summary": {"global_step/sec": 11.410505294799805},
        },
        {
            "step": 101,
            "wall_time": 1565338673.080884,
            "summary": {
                "acc": 0.3448275923728943,
                "precision": 0.14387211203575134,
                "recall": 0.19194312393665314,
                "f1": 0.164466992020607,
                "correct_rate": 0.0078125,
                "loss": 19.875246047973633,
            },
        },
    ]

    result = process_record_merge_summary(data)

    print(result)

    expected = [
        {
            "step": 1,
            "wall_time": 1565338664.317573,
            "summary": {
                "acc": 0.003722084453329444,
                "precision": 0.003722084453329444,
                "recall": 0.007317073177546263,
                "f1": 0.004934210795909166,
                "correct_rate": 0.0,
                "loss": 71.3306655883789,
            },
        },
        {
            "step": 101,
            "wall_time": 1565338673.080884,
            "summary": {
                "acc": 0.3448275923728943,
                "precision": 0.14387211203575134,
                "recall": 0.19194312393665314,
                "f1": 0.164466992020607,
                "correct_rate": 0.0078125,
                "loss": 19.875246047973633,
                "global_step/sec": 11.410505294799805,
            },
        },
    ]
