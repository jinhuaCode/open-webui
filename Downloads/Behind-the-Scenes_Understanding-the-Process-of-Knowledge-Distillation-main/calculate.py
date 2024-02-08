# coding:utf-8
"""
@file: calculate.py
@author: cjx
@createTime: 2023/12/18
@Functioon: 描述作用
"""


import os
import sys
import glob
import logging
import argparse
import pickle

import random
import numpy as np
import pandas as pd
import torch
from torch.utils.data import SequentialSampler
from tqdm import tqdm
from shapely.geometry import MultiPoint
import scipy.spatial

from envs import PROJECT_FOLDER, HOME_DATA_FOLDER
from BERT.pytorch_pretrained_bert.modeling import BertConfig
from BERT.pytorch_pretrained_bert.tokenization import BertTokenizer
from src.data_processing import init_model, get_task_dataloader
from src.utils import count_parameters, load_model, eval_model_dataloader, fill_tensor
from convex.reduce_dimension import reduce_dimension
from convex.utils import generate_numpy_key
from convex.calculate_to_csv import calculate_to_csv


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def find_epoch(eval_log_file, task):
    data = []
    with open(eval_log_file, 'r') as file:
        # 读取文件内容并按行分割
        lines = file.readlines()

        # 解析每一行的数据
        for line in lines[1:]:  # 跳过表头
            if task == 'MRPC':
                epoch, f1, acc, loss = map(float, line.strip().split(',')) #将f1的值给acc
            elif task == 'QQP':
                epoch, acc, f1, loss = map(float, line.strip().split(','))
            else:
                epoch, acc, loss = map(float, line.strip().split(','))
            data.append({'epoch': epoch, 'acc': acc, 'loss': loss})

    max_acc_entry = max(data, key=lambda x: x['acc'])
    max_acc_epoch = max_acc_entry['epoch']

    return max_acc_epoch

# 该函数接受教师模型（teacher_knowledge）、学生模型（student_ft_knowledge、student_kd_knowledge、student_pkd_knowledge）的知识，以及一个前缀作为参数。
# 将输入的知识转换为 NumPy 数组，然后使用 Shapely 库的 MultiPoint 类构建点的集合。
# 计算教师和每个学生模型知识的凸包，并计算凸包的一些几何性质，如重心之间的距离、凸包的面积等。
# 对每个模型的凸包进行降维，得到其边界点的顺序（spw）。
# 最后，返回一个包含各种特征的字典。
def calculate_each(teacher_knowledge, student_ft_knowledge, student_kd_knowledge, student_pkd_knowledge, student_ckd_knowledge, prefix):

    teacher_knowledge_np = np.array(teacher_knowledge)
    student_ft_knowledge_np = np.array(student_ft_knowledge)
    student_kd_knowledge_np = np.array(student_kd_knowledge)
    student_pkd_knowledge_np = np.array(student_pkd_knowledge)
    student_ckd_knowledge_np = np.array(student_ckd_knowledge)

    teacher_knowledge_mp = MultiPoint(teacher_knowledge_np)
    student_ft_knowledge_mp = MultiPoint(student_ft_knowledge_np)
    student_kd_knowledge_mp = MultiPoint(student_kd_knowledge_np)
    student_pkd_knowledge_mp = MultiPoint(student_pkd_knowledge_np)
    student_ckd_knowledge_mp = MultiPoint(student_ckd_knowledge_np)

    teacher_knowledge_convex = teacher_knowledge_mp.convex_hull
    student_ft_knowledge_convex = student_ft_knowledge_mp.convex_hull
    student_kd_knowledge_convex = student_kd_knowledge_mp.convex_hull
    student_pkd_knowledge_convex = student_pkd_knowledge_mp.convex_hull
    student_ckd_knowledge_convex = student_ckd_knowledge_mp.convex_hull

    # 两个凸包重心的距离
    centroid_distance_teacher_student_ft = teacher_knowledge_convex.centroid.distance(
        student_ft_knowledge_convex.centroid)
    centroid_distance_teacher_student_kd = teacher_knowledge_convex.centroid.distance(
        student_kd_knowledge_convex.centroid)
    centroid_distance_teacher_student_pkd = teacher_knowledge_convex.centroid.distance(
        student_pkd_knowledge_convex.centroid)
    centroid_distance_teacher_student_ckd = teacher_knowledge_convex.centroid.distance(
        student_ckd_knowledge_convex.centroid)

    # 凸包的面积
    area_teacher_knowledge = teacher_knowledge_convex.area
    area_student_ft_knowledge = student_ft_knowledge_convex.area
    area_student_kd_knowledge = student_kd_knowledge_convex.area
    area_student_pkd_knowledge = student_pkd_knowledge_convex.area
    area_student_ckd_knowledge = student_ckd_knowledge_convex.area

    # 两个凸包交集面积
    area_intersection_teacher_student_ft = teacher_knowledge_convex.intersection(student_ft_knowledge_convex).area
    area_intersection_teacher_student_kd = teacher_knowledge_convex.intersection(student_kd_knowledge_convex).area
    area_intersection_teacher_student_pkd = teacher_knowledge_convex.intersection(student_pkd_knowledge_convex).area
    area_intersection_teacher_student_ckd = teacher_knowledge_convex.intersection(student_ckd_knowledge_convex).area

    # spw of model
    teacher_knowledge_convex_hull = scipy.spatial.ConvexHull(teacher_knowledge_np)
    teacher_knowledge_convex_hull = teacher_knowledge_convex_hull.vertices.tolist()
    teacher_knowledge_convex_hull.sort()
    spw_teacher_knowledge = teacher_knowledge_convex_hull

    student_ft_knowledge_convex_hull = scipy.spatial.ConvexHull(student_ft_knowledge_np)
    student_ft_knowledge_convex_hull = student_ft_knowledge_convex_hull.vertices.tolist()
    student_ft_knowledge_convex_hull.sort()
    spw_student_ft__knowledge = student_ft_knowledge_convex_hull

    student_kd_knowledge_convex_hull = scipy.spatial.ConvexHull(student_kd_knowledge_np)
    student_kd_knowledge_convex_hull = student_kd_knowledge_convex_hull.vertices.tolist()
    student_kd_knowledge_convex_hull.sort()
    spw_student_kd__knowledge = student_kd_knowledge_convex_hull

    student_pkd_knowledge_convex_hull = scipy.spatial.ConvexHull(student_pkd_knowledge_np)
    student_pkd_knowledge_convex_hull = student_pkd_knowledge_convex_hull.vertices.tolist()
    student_pkd_knowledge_convex_hull.sort()
    spw_student_pkd__knowledge = student_pkd_knowledge_convex_hull

    student_ckd_knowledge_convex_hull = scipy.spatial.ConvexHull(student_ckd_knowledge_np)
    student_ckd_knowledge_convex_hull = student_ckd_knowledge_convex_hull.vertices.tolist()
    student_ckd_knowledge_convex_hull.sort()
    spw_student_ckd__knowledge = student_ckd_knowledge_convex_hull

    # 两个模型spw的交集
    spw_intersection_teacher_student_ft = list(set(spw_teacher_knowledge) & set(spw_student_ft__knowledge))
    spw_intersection_teacher_student_kd = list(set(spw_teacher_knowledge) & set(spw_student_kd__knowledge))
    spw_intersection_teacher_student_pkd = list(set(spw_teacher_knowledge) & set(spw_student_pkd__knowledge))
    spw_intersection_teacher_student_ckd = list(set(spw_teacher_knowledge) & set(spw_student_ckd__knowledge))


    return {
        f'{prefix}-teacher_area': area_teacher_knowledge,
        f'{prefix}-student_ft_area': area_student_ft_knowledge,
        f'{prefix}-student_kd_area': area_student_kd_knowledge,
        f'{prefix}-student_pkd_area': area_student_pkd_knowledge,
        f'{prefix}-student_ckd_area': area_student_ckd_knowledge,
        f'{prefix}-centroid_distance_teacher_student_ft': centroid_distance_teacher_student_ft,
        f'{prefix}-centroid_distance_teacher_student_kd': centroid_distance_teacher_student_kd,
        f'{prefix}-centroid_distance_teacher_student_pkd': centroid_distance_teacher_student_pkd,
        f'{prefix}-centroid_distance_teacher_student_ckd': centroid_distance_teacher_student_ckd,
        f'{prefix}-area_intersection_teacher_student_ft': area_intersection_teacher_student_ft,
        f'{prefix}-area_intersection_teacher_student_kd': area_intersection_teacher_student_kd,
        f'{prefix}-area_intersection_teacher_student_pkd': area_intersection_teacher_student_pkd,
        f'{prefix}-area_intersection_teacher_student_ckd': area_intersection_teacher_student_ckd,
        f'{prefix}-spw_teacher': len(spw_teacher_knowledge),
        f'{prefix}-spw_student_ft': len(spw_student_ft__knowledge),
        f'{prefix}-spw_student_kd': len(spw_student_kd__knowledge),
        f'{prefix}-spw_student_pkd': len(spw_student_pkd__knowledge),
        f'{prefix}-spw_student_ckd': len(spw_student_ckd__knowledge),
        f'{prefix}-spw_intersection_teacher_student_ft': len(spw_intersection_teacher_student_ft),
        f'{prefix}-spw_intersection_teacher_student_kd': len(spw_intersection_teacher_student_kd),
        f'{prefix}-spw_intersection_teacher_student_pkd': len(spw_intersection_teacher_student_pkd),
        f'{prefix}-spw_intersection_teacher_student_ckd': len(spw_intersection_teacher_student_ckd),
    }


random.seed(1234)
np.random.seed(1234)
torch.manual_seed(1234)
torch.cuda.manual_seed_all(1234)




DEBUG = True

if DEBUG:
    task = 'QNLI'
    stu_nlayer = 6
    calculate_mode_input = 'teacher,student-ft,student-kd,student-pkd,student-ckd'
    bert_model = 'bert-base-uncased'
    output_all_layers= 'ckd'
    model_file = os.path.join(PROJECT_FOLDER, 'result/glue/result_summary/teacher_student_all.csv')
else:
    task = sys.argv[1].split(',')
    calculate_mode_input = sys.argv[2]
    bert_model = sys.argv[3]
    output_all_layers = sys.argv[4]
    model_file = sys.argv[5]


KD_DIR = os.path.join(HOME_DATA_FOLDER, 'outputs/KD/')

sub_dir = 'teacher_12layer'

output_dir = os.path.join(PROJECT_FOLDER, f'result/glue/teacher_student_calculate/student_{stu_nlayer}layer')

bert_model = os.path.join(HOME_DATA_FOLDER, f'models/pretrained/{bert_model}')
config = BertConfig(os.path.join(bert_model, 'bert_config.json'))
tokenizer = BertTokenizer.from_pretrained(bert_model, do_lower_case=True)
device = torch.device("cuda:1" if torch.cuda.is_available() else "cpu")
args = argparse.Namespace(n_gpu=1,
                          device=device,
                          fp16=False,
                          eval_batch_size=1,
                          max_seq_length=128)

model_df = pd.read_csv(model_file)

# loading model


args.raw_data_dir = os.path.join(HOME_DATA_FOLDER, 'data_raw', task)

calculate_result_file = f'{output_dir}/{task}_calculate_result.pkl'
calculate_result_csv_file = f'{output_dir}/{task}_calculate_result.csv'

logger.info('***** loading teacher model *****')

teacher_folder = f'kd_{task}_nlayer.12_lr.1e-05_T.10.0_alpha.0.0_beta.0.0_bs.32-run-1'
eval_log_file = os.path.join(KD_DIR, task, sub_dir, teacher_folder, 'eval_log.txt')
teacher_epoch = find_epoch(eval_log_file, task) - 1
teacher_information = teacher_folder.split('_')
teacher_n_layer = 12

teacher_folder = os.path.join(KD_DIR, task, sub_dir, teacher_folder)
# Your existing code

teacher_encoder_file = glob.glob(teacher_folder + '/*e.%d.encoder.pkl' % teacher_epoch)
teacher_cls_file = glob.glob(teacher_folder + '/*e.%d.cls.pkl' % teacher_epoch)
assert len(teacher_encoder_file) == 1 and len(teacher_cls_file) == 1, f'encoder/cls file error: {teacher_encoder_file}, {teacher_cls_file}'
teacher_encoder_file, teacher_cls_file = teacher_encoder_file[0], teacher_cls_file[0]

teacher_encoder_bert, teacher_classifier = init_model(task, output_all_layers, teacher_n_layer, config)
teacher_encoder_bert = load_model(teacher_encoder_bert, teacher_encoder_file, args, 'exact', verbose=True)
teacher_encoder_bert.eval()
teacher_classifier = load_model(teacher_classifier, teacher_cls_file, args, 'exact', verbose=True)

logger.info('***** loading student-ft model *****')

student_ft_folder = f'kd_{task}_nlayer.{stu_nlayer}_lr.1e-05_T.10.0_alpha.0.0_beta.0.0_bs.32-run-1'
eval_log_file = os.path.join(KD_DIR, task, sub_dir, student_ft_folder, 'eval_log.txt')
student_ft_epoch = find_epoch(eval_log_file,task) - 1
student_ft_n_layer = 6

student_ft_folder = os.path.join(KD_DIR, task, sub_dir, student_ft_folder)
student_ft_encoder_file = glob.glob(student_ft_folder + '/*e.%d.encoder.pkl' % student_ft_epoch)
student_ft_cls_file = glob.glob(student_ft_folder + '/*e.%d.cls.pkl' % student_ft_epoch)
assert len(student_ft_encoder_file) == 1 and len(
    student_ft_cls_file) == 1, f'encoder/cls file error: {student_ft_encoder_file}, {student_ft_cls_file}'
student_ft_encoder_file, student_ft_cls_file = student_ft_encoder_file[0], student_ft_cls_file[0]

student_ft_encoder_bert, student_ft_classifier = init_model(task, output_all_layers, student_ft_n_layer, config)
student_ft_encoder_bert = load_model(student_ft_encoder_bert, student_ft_encoder_file, args, 'exact', verbose=True)
student_ft_encoder_bert.eval()
student_ft_classifier = load_model(student_ft_classifier, student_ft_cls_file, args, 'exact', verbose=True)

logger.info('***** loading student-kd model *****')

student_kd_folder = f'kd_{task}_nlayer.{stu_nlayer}_lr.1e-05_T.4.0_alpha.0.7_beta.0.0_bs.32-run-1'
eval_log_file = os.path.join(KD_DIR, task, sub_dir, student_kd_folder, 'eval_log.txt')
student_kd_epoch = find_epoch(eval_log_file, task)-1
student_kd_n_layer = 6

student_kd_folder = os.path.join(KD_DIR, task, sub_dir, student_kd_folder)
student_kd_encoder_file = glob.glob(student_kd_folder + '/*e.%d.encoder.pkl' % student_kd_epoch)
student_kd_cls_file = glob.glob(student_kd_folder + '/*e.%d.cls.pkl' % student_kd_epoch)
assert len(student_kd_encoder_file) == 1 and len(
    student_kd_cls_file) == 1, f'encoder/cls file error: {student_kd_encoder_file}, {student_kd_cls_file}'
student_kd_encoder_file, student_kd_cls_file = student_kd_encoder_file[0], student_kd_cls_file[0]

student_kd_encoder_bert, student_kd_classifier = init_model(task, output_all_layers, student_kd_n_layer, config)
student_kd_encoder_bert = load_model(student_kd_encoder_bert, student_kd_encoder_file, args, 'exact', verbose=True)
student_kd_encoder_bert.eval()
student_kd_classifier = load_model(student_kd_classifier, student_kd_cls_file, args, 'exact', verbose=True)

logger.info('***** loading student-pkd model *****')

student_pkd_folder = f'kd.cls.True_{task}_nlayer.{stu_nlayer}_lr.1e-05_T.4.0_alpha.0.7_beta.500.0_bs.32-run-1'
eval_log_file = os.path.join(KD_DIR, task, sub_dir, student_pkd_folder, 'eval_log.txt')
student_pkd_epoch = find_epoch(eval_log_file, task)-1
student_pkd_information = student_pkd_folder.split('_')
student_pkd_n_layer = int(student_pkd_information[2].split('.')[1])

student_pkd_folder = os.path.join(KD_DIR, task, sub_dir, student_pkd_folder)
student_pkd_encoder_file = glob.glob(student_pkd_folder + '/*e.%d.encoder.pkl' % student_pkd_epoch)
student_pkd_cls_file = glob.glob(student_pkd_folder + '/*e.%d.cls.pkl' % student_pkd_epoch)
assert len(student_pkd_encoder_file) == 1 and len(
    student_pkd_cls_file) == 1, f'encoder/cls file error: {student_pkd_encoder_file}, {student_pkd_cls_file}'
student_pkd_encoder_file, student_pkd_cls_file = student_pkd_encoder_file[0], student_pkd_cls_file[0]

student_pkd_encoder_bert, student_pkd_classifier = init_model(task, output_all_layers, student_pkd_n_layer, config)
student_pkd_encoder_bert = load_model(student_pkd_encoder_bert, student_pkd_encoder_file, args, 'exact', verbose=True)
student_pkd_encoder_bert.eval()
student_pkd_classifier = load_model(student_pkd_classifier, student_pkd_cls_file, args, 'exact', verbose=True)

logger.info('***** loading student-ckd model *****')

student_ckd_folder = f'ckd_{task}_nlayer.{stu_nlayer}_lr.1e-05_T.4.0_alpha.0.7_beta.500.0_bs.32-run-1'
eval_log_file = os.path.join(KD_DIR, task, sub_dir, student_ckd_folder, 'eval_log.txt')
student_ckd_epoch = find_epoch(eval_log_file, task)-1
student_ckd_information = student_ckd_folder.split('_')
student_ckd_n_layer = int(student_ckd_information[2].split('.')[1])

student_ckd_folder = os.path.join(KD_DIR, task, sub_dir, student_ckd_folder)
student_ckd_encoder_file = glob.glob(student_ckd_folder + '/*e.%d.encoder.pkl' % student_ckd_epoch)
student_ckd_cls_file = glob.glob(student_ckd_folder + '/*e.%d.cls.pkl' % student_ckd_epoch)
assert len(student_ckd_encoder_file) == 1 and len(
    student_ckd_cls_file) == 1, f'encoder/cls file error: {student_ckd_encoder_file}, {student_ckd_cls_file}'
student_ckd_encoder_file, student_ckd_cls_file = student_ckd_encoder_file[0], student_ckd_cls_file[0]

student_ckd_encoder_bert, student_ckd_classifier = init_model(task, output_all_layers, student_ckd_n_layer, config)
student_ckd_encoder_bert = load_model(student_ckd_encoder_bert, student_ckd_encoder_file, args, 'exact', verbose=True)
student_ckd_encoder_bert.eval()
student_ckd_classifier = load_model(student_ckd_classifier, student_ckd_cls_file, args, 'exact', verbose=True)


logger.info('***** loading dev_data *****')

dev_examples, dev_dataloader, dev_label_ids = get_task_dataloader(task.lower(), 'dev', tokenizer, args,
                                                                  SequentialSampler, args.eval_batch_size)

logger.info('***** start reduce dimension *****')


#########  分模型降维  ############
teacher_knowledge_high_all = None
student_ft_knowledge_high_all = None
student_kd_knowledge_high_all = None
student_pkd_knowledge_high_all = None
student_ckd_knowledge_high_all = None

for idx, batch in enumerate(tqdm(dev_dataloader, desc="Iteration")):
    batch = tuple(t.to(device) for t in batch)
    if len(batch) > 4:
        input_ids, input_mask, segment_ids, label_ids, *ignore = batch
    else:
        input_ids, input_mask, segment_ids, label_ids = batch


    sentence_len = torch.sum(input_mask == 1).item()

    teacher_knowledge_high = teacher_encoder_bert.getKnowledge(input_ids, segment_ids, input_mask)
    teacher_knowledge_high = torch.squeeze(teacher_knowledge_high, dim=0).cpu().detach().numpy()
    teacher_knowledge_high = teacher_knowledge_high[1:sentence_len-1, :]

    if teacher_knowledge_high_all is None:
        teacher_knowledge_high_all = teacher_knowledge_high
    else:
        teacher_knowledge_high_all = np.vstack((teacher_knowledge_high_all, teacher_knowledge_high))

    student_ft_knowledge_high = student_ft_encoder_bert.getKnowledge(input_ids, segment_ids, input_mask)
    student_ft_knowledge_high = torch.squeeze(student_ft_knowledge_high, dim=0).cpu().detach().numpy()
    student_ft_knowledge_high = student_ft_knowledge_high[1:sentence_len - 1, :]

    if student_ft_knowledge_high_all is None:
        student_ft_knowledge_high_all = student_ft_knowledge_high
    else:
        student_ft_knowledge_high_all = np.vstack((student_ft_knowledge_high_all, student_ft_knowledge_high))

    student_kd_knowledge_high = student_kd_encoder_bert.getKnowledge(input_ids, segment_ids, input_mask)
    student_kd_knowledge_high = torch.squeeze(student_kd_knowledge_high, dim=0).cpu().detach().numpy()
    student_kd_knowledge_high = student_kd_knowledge_high[1:sentence_len - 1, :]

    if student_kd_knowledge_high_all is None:
        student_kd_knowledge_high_all = student_kd_knowledge_high
    else:
        student_kd_knowledge_high_all = np.vstack((student_kd_knowledge_high_all, student_kd_knowledge_high))

    student_pkd_knowledge_high = student_pkd_encoder_bert.getKnowledge(input_ids, segment_ids, input_mask)
    student_pkd_knowledge_high = torch.squeeze(student_pkd_knowledge_high, dim=0).cpu().detach().numpy()
    student_pkd_knowledge_high = student_pkd_knowledge_high[1:sentence_len - 1, :]

    if student_pkd_knowledge_high_all is None:
        student_pkd_knowledge_high_all = student_pkd_knowledge_high
    else:
        student_pkd_knowledge_high_all = np.vstack((student_pkd_knowledge_high_all, student_pkd_knowledge_high))

    student_ckd_knowledge_high = student_ckd_encoder_bert.getKnowledge(input_ids, segment_ids, input_mask)
    student_ckd_knowledge_high = torch.squeeze(student_ckd_knowledge_high, dim=0).cpu().detach().numpy()
    student_ckd_knowledge_high = student_ckd_knowledge_high[1:sentence_len - 1, :]

    if student_ckd_knowledge_high_all is None:
        student_ckd_knowledge_high_all = student_ckd_knowledge_high
    else:
        student_ckd_knowledge_high_all = np.vstack((student_ckd_knowledge_high_all, student_ckd_knowledge_high))

    # knowledge_high = np.vstack((teacher_knowledge_high, student_ft_knowledge_high, student_kd_knowledge_high, student_pkd_knowledge_high))

# use pca method to reduce dimension to 2-dimension
teacher_knowledge_low_all = reduce_dimension(teacher_knowledge_high_all, 2, 'pca')
student_ft_knowledge_low_all = reduce_dimension(student_ft_knowledge_high_all, 2, 'pca')
student_kd_knowledge_low_all = reduce_dimension(student_kd_knowledge_high_all, 2, 'pca')
student_pkd_knowledge_low_all = reduce_dimension(student_pkd_knowledge_high_all, 2, 'pca')
student_ckd_knowledge_low_all = reduce_dimension(student_ckd_knowledge_high_all, 2, 'pca')

teacher_knowledge_high_dict = {}
for i, _ in enumerate(teacher_knowledge_high_all):
    teacher_knowledge_high_dict[generate_numpy_key(_)] = i

student_ft_knowledge_high_dict = {}
for i, _ in enumerate(student_ft_knowledge_high_all):
    student_ft_knowledge_high_dict[generate_numpy_key(_)] = i

student_kd_knowledge_high_dict = {}
for i, _ in enumerate(student_kd_knowledge_high_all):
    student_kd_knowledge_high_dict[generate_numpy_key(_)] = i

student_pkd_knowledge_high_dict = {}
for i, _ in enumerate(student_pkd_knowledge_high_all):
    student_pkd_knowledge_high_dict[generate_numpy_key(_)] = i

student_ckd_knowledge_high_dict = {}
for i, _ in enumerate(student_ckd_knowledge_high_all):
    student_ckd_knowledge_high_dict[generate_numpy_key(_)] = i


logger.info('***** calculating *****')

calculate_result = []
for idx, batch in enumerate(tqdm(dev_dataloader, desc="Iteration")):
    batch = tuple(t.to(device) for t in batch)
    if len(batch) > 4:
        input_ids, input_mask, segment_ids, label_ids, *ignore = batch
    else:
        input_ids, input_mask, segment_ids, label_ids = batch


    sentence_len = torch.sum(input_mask == 1).item()

    teacher_knowledge_high = teacher_encoder_bert.getKnowledge(input_ids, segment_ids, input_mask)
    teacher_knowledge_high = torch.squeeze(teacher_knowledge_high, dim=0).cpu().detach().numpy()
    teacher_knowledge_high = teacher_knowledge_high[1:sentence_len-1, :]

    student_ft_knowledge_high = student_ft_encoder_bert.getKnowledge(input_ids, segment_ids, input_mask)
    student_ft_knowledge_high = torch.squeeze(student_ft_knowledge_high, dim=0).cpu().detach().numpy()
    student_ft_knowledge_high = student_ft_knowledge_high[1:sentence_len - 1, :]

    student_kd_knowledge_high = student_kd_encoder_bert.getKnowledge(input_ids, segment_ids, input_mask)
    student_kd_knowledge_high = torch.squeeze(student_kd_knowledge_high, dim=0).cpu().detach().numpy()
    student_kd_knowledge_high = student_kd_knowledge_high[1:sentence_len - 1, :]

    student_pkd_knowledge_high = student_pkd_encoder_bert.getKnowledge(input_ids, segment_ids, input_mask)
    student_pkd_knowledge_high = torch.squeeze(student_pkd_knowledge_high, dim=0).cpu().detach().numpy()
    student_pkd_knowledge_high = student_pkd_knowledge_high[1:sentence_len - 1, :]

    student_ckd_knowledge_high = student_ckd_encoder_bert.getKnowledge(input_ids, segment_ids, input_mask)
    student_ckd_knowledge_high = torch.squeeze(student_ckd_knowledge_high, dim=0).cpu().detach().numpy()
    student_ckd_knowledge_high = student_ckd_knowledge_high[1:sentence_len - 1, :]

    if len(np.unique(np.array(teacher_knowledge_high), axis=0)) > 2 and len(
            np.unique(np.array(student_ft_knowledge_high), axis=0)) > 2 and len(np.unique(np.array(student_kd_knowledge_high), axis=0)) > 2 and len(np.unique(np.array(student_pkd_knowledge_high), axis=0)) > 2  and len(np.unique(np.array(student_ckd_knowledge_high), axis=0)) > 2:

        teacher_knowledge_low = []
        for _ in teacher_knowledge_high:
            teacher_knowledge_low.append(teacher_knowledge_high_dict[generate_numpy_key(_)])

        teacher_knowledge_low = teacher_knowledge_low_all[teacher_knowledge_low]

        student_ft_knowledge_low = []
        for _ in student_ft_knowledge_high:
            student_ft_knowledge_low.append(student_ft_knowledge_high_dict[generate_numpy_key(_)])

        student_ft_knowledge_low = student_ft_knowledge_low_all[student_ft_knowledge_low]

        student_kd_knowledge_low = []
        for _ in student_kd_knowledge_high:
            student_kd_knowledge_low.append(student_kd_knowledge_high_dict[generate_numpy_key(_)])

        student_kd_knowledge_low = student_kd_knowledge_low_all[student_kd_knowledge_low]

        student_pkd_knowledge_low = []
        for _ in student_pkd_knowledge_high:
            student_pkd_knowledge_low.append(student_pkd_knowledge_high_dict[generate_numpy_key(_)])

        student_pkd_knowledge_low = student_pkd_knowledge_low_all[student_pkd_knowledge_low]

        student_ckd_knowledge_low = []
        for _ in student_ckd_knowledge_high:
            student_ckd_knowledge_low.append(student_ckd_knowledge_high_dict[generate_numpy_key(_)])

        student_ckd_knowledge_low = student_ckd_knowledge_low_all[student_ckd_knowledge_low]

        # calculate area, centroid, spw...
        feature = calculate_each(teacher_knowledge_low, student_ft_knowledge_low, student_kd_knowledge_low, student_pkd_knowledge_low, student_ckd_knowledge_low, task)

        calculate_result.append(feature)


with open(calculate_result_file, 'wb') as wf:
    pickle.dump(calculate_result, wf)

calculate_to_csv(calculate_result_file, calculate_result_csv_file)


