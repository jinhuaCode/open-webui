# coding:utf-8
"""
@file: envs.py
@author: cjx
@createTime: 2023/12/4
@Functioon: 描述作用
"""


import os
import logging


logger = logging.getLogger(__name__)


PROJECT_FOLDER = os.path.dirname(__file__)
HOME_DATA_FOLDER = os.path.join(PROJECT_FOLDER, 'data')
HOME_OUTPUT_FOLDER = os.path.join(HOME_DATA_FOLDER, 'outputs/KD')
PREDICTION_FOLDER = os.path.join(HOME_DATA_FOLDER, 'outputs/predictions')