# coding:utf-8
"""
@file: analysis.py
@author: cjx
@createTime: 2023/12/22
@Functioon: 描述作用
"""
import os

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import csv


ROOT_DIR = '/home/jingxu/project/PKD/result/glue/teacher_student_calculate/analysis_layer_n'

def max_acc(eval_log_file):

    max_acc = 0.0  # 初始最大acc值

    with open(eval_log_file, 'r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            acc = float(row['acc'])

            if acc > max_acc:
                max_acc = acc
    return max_acc


analysis_result = []
for layer in range(1, 12):
    student_kd_folder = f'kd_RTE_nlayer.{layer}_lr.1e-05_T.4.0_alpha.0.7_beta.0.0_bs.32-run-1'
    eval_log_file = os.path.join('/home/jingxu/project/PKD/data/outputs/KD/RTE/teacher_12layer', student_kd_folder, 'eval_log.txt')
    acc = max_acc(eval_log_file)

    file_name = f'{layer}_calculate_result.csv'
    result_file = os.path.join(ROOT_DIR, file_name)

    result_data = pd.read_csv(result_file)
    result_data.columns = [col.replace(str(layer) + '-', '') for col in result_data.columns]
    ## 计算KTR,KAR,KLR,KED,KCD
    result_data['KTR-kd'] = (
            result_data['area_intersection_teacher_student_kd'] /
            result_data['teacher_area'] * 100
    )
    # KAR
    result_data['KAR-kd'] = (
            result_data['area_intersection_teacher_student_kd'] /
            result_data['student_kd_area'] * 100
    )
    # KLR
    result_data['KLR-kd'] = (
            result_data['spw_intersection_teacher_student_kd'] /
            result_data['spw_student_kd'] * 100
    )

    _ = result_data.mean()
    _ = _.round(2)
    _['acc'] = acc
    _['layer'] = layer

    analysis_result.append(_)

analysis_result = pd.DataFrame(analysis_result)
selected_columns = ['layer', 'acc', 'student_kd_area', 'area_intersection_teacher_student_kd', 'KTR-kd', 'KAR-kd', 'KLR-kd']

# 创建新的DataFrame
new_df = analysis_result[selected_columns]
analysis_result.to_csv('analysis_result_n_all.csv', index=False)
new_df.to_csv('analysis_result_n.csv', index=False)
