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


# ALL_TASKS = ['RTE', 'SST-2','MNLI']
# Layers = ['6', '3']
task = 'QNLI'
layer = '6'
ROOT_DIR = '/home/jingxu/project/PKD/result/glue/teacher_student_calculate'


def max_acc(eval_log_file):

    max_acc = 0.0  # 初始最大acc值

    with open(eval_log_file, 'r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            if task == "MRPC":
                acc = float(row['f1'])
            elif task == 'CoLA':
                acc = float(row['mcc'])
            elif task == 'STS-B':
                acc = float(row['spearmanr'])
            else:
                acc = float(row['acc'])

            if acc > max_acc:
                max_acc = acc
    return max_acc

analysis_result = []

result_dir = os.path.join(ROOT_DIR, 'student_' + layer + 'layer')

file_name = f'{task}_calculate_result.csv'
result_file = os.path.join(result_dir, file_name)

result_data = pd.read_csv(result_file)
result_data.columns = [col.replace(task + '-', '') for col in result_data.columns]
## 计算KTR,KAR,KLR,KED,KCD
result_data['KTR-ft'] = (
        result_data['area_intersection_teacher_student_ft'] /
        result_data['teacher_area'] * 100
)
result_data['KTR-kd'] = (
        result_data['area_intersection_teacher_student_kd'] /
        result_data['teacher_area'] * 100
)
result_data['KTR-pkd'] = (
        result_data['area_intersection_teacher_student_pkd'] /
        result_data['teacher_area'] * 100
)
result_data['KTR-ckd'] = (
        result_data['area_intersection_teacher_student_ckd'] /
        result_data['teacher_area'] * 100
)
# KAR
result_data['KAR-ft'] = (
        result_data['area_intersection_teacher_student_ft'] /
        result_data['student_ft_area'] * 100
)
result_data['KAR-kd'] = (
        result_data['area_intersection_teacher_student_kd'] /
        result_data['student_kd_area'] * 100
)
result_data['KAR-pkd'] = (
        result_data['area_intersection_teacher_student_pkd'] /
        result_data['student_pkd_area'] * 100
)
result_data['KAR-ckd'] = (
        result_data['area_intersection_teacher_student_ckd'] /
        result_data['student_ckd_area'] * 100
)
# KLR
result_data['KLR-ft'] = (
        result_data['spw_intersection_teacher_student_ft'] /
        result_data['spw_student_ft'] * 100
)
result_data['KLR-kd'] = (
        result_data['spw_intersection_teacher_student_kd'] /
        result_data['spw_student_kd'] * 100
)
result_data['KLR-pkd'] = (
        result_data['spw_intersection_teacher_student_pkd'] /
        result_data['spw_student_pkd'] * 100
)
result_data['KLR-ckd'] = (
        result_data['spw_intersection_teacher_student_ckd'] /
        result_data['spw_student_ckd'] * 100
)

_ = result_data.mean()
_ = _.round(2)
_['task'] = task + '_' + layer
analysis_result.append(_)


analysis_result = pd.DataFrame(analysis_result)
analysis_result = analysis_result.rename(columns={'student_ft_area': 'student_area-ft',
                                                  'student_kd_area': 'student_area-kd',
                                                  'student_pkd_area': 'student_area-pkd',
                                                  'student_ckd_area': 'student_area-ckd',
                                                  'centroid_distance_teacher_student_ft': 'centroid_distance_teacher_student-ft',
                                                  'centroid_distance_teacher_student_kd': 'centroid_distance_teacher_student-kd',
                                                  'centroid_distance_teacher_student_pkd': 'centroid_distance_teacher_student-pkd',
                                                  'centroid_distance_teacher_student_ckd': 'centroid_distance_teacher_student-ckd'
                                                  })


stu_types = ['ft', 'kd', 'pkd', 'ckd']

for s_t in stu_types:
    if s_t == 'ft':
        folder = f'kd_{task}_nlayer.{layer}_lr.1e-05_T.10.0_alpha.0.0_beta.0.0_bs.32-run-1'
    elif s_t == 'kd':
        folder = f'kd_{task}_nlayer.{layer}_lr.1e-05_T.4.0_alpha.0.7_beta.0.0_bs.32-run-1'
    elif s_t == 'pkd':
        folder = f'kd.cls.True_{task}_nlayer.{layer}_lr.1e-05_T.4.0_alpha.0.7_beta.500.0_bs.32-run-1'
    else:
        folder = f'ckd_{task}_nlayer.{layer}_lr.1e-05_T.4.0_alpha.0.7_beta.500.0_bs.32-run-1'

    eval_log_file = os.path.join(f'/home/jingxu/project/PKD/data/outputs/KD/{task}/teacher_12layer', folder,
                                 'eval_log.txt')
    acc = max_acc(eval_log_file)
    analysis_result[f'acc-{s_t}'] = acc

print(analysis_result)

types = ['acc', 'student_area', 'centroid_distance_teacher_student', 'KTR', 'KAR', 'KLR']

result_df = []
for s_t in stu_types:
    _ = []
    _.append(s_t)
    for t in types:
        _.append(analysis_result[f'{t}-{s_t}'].values.item())

    result_df.append(_)
result_df = pd.DataFrame(result_df)
result_df.columns = ['type', 'acc', 'student_area', 'centroid_distance', 'KTR', 'KAR', 'KLR']
print(result_df)

analysis_result.to_csv(f'{task}_analysis_result_all.csv', index=False)
result_df.to_csv(f'{task}_analysis_result.csv', index=False)