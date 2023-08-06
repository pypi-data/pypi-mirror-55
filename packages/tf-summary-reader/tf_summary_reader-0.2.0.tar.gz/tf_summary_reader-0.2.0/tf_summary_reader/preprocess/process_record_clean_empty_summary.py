from typing import List, Dict


def process_record_clean_empty_summary(record_list: List[Dict]) -> List[Dict]:
    """
    remove empty summary record from list

    :param record_list: list of record
    :return: list of record
    """

    processed_list = []
    for record in record_list:
        if not record["summary"]:
            continue

        processed_list.append(record)

    return processed_list


if __name__ == "__main__":
    data = [
        {"step": 0, "wall_time": 1565338566.0, "summary": {}},
        {"step": 0, "wall_time": 1565338566.6084208, "summary": {}},
        {"step": 0, "wall_time": 1565338567.1908352, "summary": {}},
        {"step": 0, "wall_time": 1565338617.0762944, "summary": {}},
        {"step": 0, "wall_time": 1565338617.420546, "summary": {}},
        {"step": 0, "wall_time": 1565338625.4887302, "summary": {}},
        {"step": 1, "wall_time": 1565338664.3173296, "summary": {}},
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

    result = process_record_clean_empty_summary(data)
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
