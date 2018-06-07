#!/usr/bin/env python3
# @Time    : 18-1-18 上午11:32
# @Author  : ys
# @Email   : youngs@yeah.net

import re
import datetime


def id_card_check(id_number):
    """
    二代身份证校验算法
    :param id_number: 
    :return: bool
    """
    id_code_list = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    check_code_list = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
    if len(id_number) != 18:
        return False
    if not re.match(r"^\d{17}(\d|X|x)$", id_number):
        return False
    try:
        datetime.date(int(id_number[6:10]), int(id_number[10:12]), int(id_number[12:14]))
    except ValueError:
        return False
    if check_code_list[sum([a * b for a, b in zip(id_code_list, [
            int(a) for a in id_number[0:-1]])]) % 11] != id_number.upper()[-1]:
        return False
    return True


if __name__ == '__main__':
    id_number_list = ['410482198804138128', '342422199103016689',
                      '530121198207183746', '530121198408214246']
    for id_number in id_number_list:
        print(id_card_check(id_number))
