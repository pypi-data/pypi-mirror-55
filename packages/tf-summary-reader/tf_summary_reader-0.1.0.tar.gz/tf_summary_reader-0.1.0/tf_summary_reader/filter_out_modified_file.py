import os

cache = {}


def filter_out_modified_file(file_list):
    modified_file_list = []
    for f in file_list:
        m_time = os.path.getmtime(f)

        if f not in cache:
            modified_file_list.append(f)
        else:
            last_m_time = cache[f]
            if m_time > last_m_time:
                modified_file_list.append(f)

        # update m_time
        cache[f] = m_time