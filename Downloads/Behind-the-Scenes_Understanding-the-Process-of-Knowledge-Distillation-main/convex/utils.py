# coding:utf-8
"""
@file: utils.py
@author: cjx
@createTime: 2023/10/28
@Functioon:
"""


def generate_numpy_key(vec):
    return '&'.join([str(d) for d in list(vec)])