# -*- coding:utf8 -*-

SPLIT_CHAR = " | "


# MORE_EMPTY = " "
def get_print_str(headers, keys, dicts):
    len_dict = initial_len_dict_by_headers(headers, keys)
    re_calc_len_by_values(len_dict, dicts, keys)
    h_s = printHeaders(headers, len_dict, keys)
    v_s = printValues(dicts, len_dict, keys)
    return h_s + '\n' + v_s


def print_list(headers, keys, dicts):
    len_dict = initial_len_dict_by_headers(headers, keys)
    re_calc_len_by_values(len_dict, dicts, keys)
    print printHeaders(headers, len_dict, keys)
    print printValues(dicts, len_dict, keys)


def printHeaders(headers, len_dict, keys):
    wait_print_header = " "
    for i in range(len(headers)):
        header = headers[i]
        last_char = SPLIT_CHAR if i < len(headers) -1 else " "
        wait_print_header += (header + (len_dict[keys[i]] - len(header)) * " " + last_char)
    # print wait_print_header
    # print len(wait_print_header) * "-"
    p_s = wait_print_header + '\n' + len(wait_print_header) * "-"
    return p_s


def printValues(dicts, len_dict, keys):
    p_s = ""
    for item in dicts:
        wait_print_item = " "
        for i in range(len(keys)):
            key = keys[i]
            last_char = SPLIT_CHAR if i < len(keys) - 1 else " "
            wait_print_item += (item[key] + (len_dict[key] - len(item[key])) * " " + last_char)
        # print wait_print_item
        p_s += wait_print_item + '\n'
    return p_s


def initial_len_dict_by_headers(headers, keys):
    res = {}
    for i in range(len(keys)):
        res[keys[i]] = len(headers[i])
    return res


def re_calc_len_by_values(len_dict, dicts, keys):
    for item in dicts:
        for key in keys:
            len_dict[key] = len_dict[key] if (len_dict[key] > len(item[key])) else len(item[key])
    return len_dict
