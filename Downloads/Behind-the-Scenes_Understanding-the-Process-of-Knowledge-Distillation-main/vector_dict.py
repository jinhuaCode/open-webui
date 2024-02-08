import logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(name)s -  %(message)s',
    datefmt='%Y/%m/%d %H:%M:%S',
    level=logging.INFO,
    )
logger = logging.getLogger(__name__)


import os
import random
import pickle
import sys

import numpy as np
import torch
from torch.utils.data import RandomSampler, SequentialSampler
from tqdm import tqdm, trange

from src.argument_parser import default_parser, complete_argument
from envs import PROJECT_FOLDER, HOME_DATA_FOLDER


def get_reduce_word_vec(wait_reduce, reduce_type, low_dim):
    '''
    数据去重, 降维
    :param wait_reduce 等待降维的
    :param low_dim: 降低到的维数, 默认为2
    :return: all_vec_2_dimension, all_vec_unique
    '''
    print("开始整合坐标")
    # 去除重复行
    all_vec_unique = np.unique(wait_reduce, axis=0)
    # 对vector降维
    all_vec_n_dimension = reduce_dimension.reduce_dimension(all_vec_unique, low_dim, reduce_type)
    print("坐标整合完毕")
    return all_vec_unique, all_vec_n_dimension


def collect_vectors(args):
    """
    获取数据集中高位到低维的字典
    :return:
    """

    KD_DIR = os.path.join(HOME_DATA_FOLDER, 'outputs/KD/')


    parser = default_parser()
    args = parser.parse_args()
    args = complete_argument(args)

    args.raw_data_dir = os.path.join(HOME_DATA_FOLDER, 'data_raw', args.task_name)

    args.feat_data_dir = os.path.join(HOME_DATA_FOLDER, 'data_feat', args.task_name)

    logger.info('actual batch size on all GPU = %d' % args.train_batch_size)
    device, n_gpu = args.device, args.n_gpu

    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    if args.n_gpu > 0:
        torch.cuda.manual_seed_all(args.seed)

    logger.info('Input Argument Information')
    args_dict = vars(args)
    for a in args_dict:
        logger.info('%-28s  %s' % (a, args_dict[a]))


    torch.manual_seed(args.random_seed)
    torch.cuda.manual_seed_all(args.random_seed)
    np.random.seed(args.random_seed)
    random.seed(args.random_seed)

    device, n_gpu = args_check(args)

    #########################################################################
    # Prepare  Data
    ##########################################################################
    task_name = args.task_name.lower()

    if task_name not in processors and 'race' not in task_name:
        raise ValueError("Task not found: %s" % (task_name))

    if 'race' in task_name:
        pass
    else:
        processor = processors[task_name]()
        output_mode = output_modes[task_name]

        label_list = processor.get_labels()
        num_labels = len(label_list)

    tokenizer = BertTokenizer.from_pretrained(args.bert_model, do_lower_case=True)

    teachers_and_student = parse_model_config(args.model_config_json)  # 读取模型config

    processor = processors[args.task_name]()
    args.output_mode = output_modes[args.task_name]
    label_list = processor.get_labels()
    num_labels = len(label_list)

    logger.info("加载模型，教师模型，学生模型，传统模型")
    # 加载要使用的模型
    logger.info("Teacher Model loading")
    teacher = teachers_and_student['teachers'][0]
    model_type_T = teacher['model_type']
    model_config_T = teacher['config']
    checkpoint_T = teacher['checkpoint']

    _, _, model_class_T = MODEL_CLASSES[model_type_T]
    model_T = model_class_T(model_config_T, num_labels=num_labels)
    state_dict_T = torch.load(checkpoint_T, map_location='cpu')
    missing_keys, un_keys = model_T.load_state_dict(state_dict_T, strict=True)
    logger.info(f"missing keys:{missing_keys}")
    logger.info(f"unexpected keys:{un_keys}")
    logger.info(f"Teacher Model {model_type_T} loaded")
    model_T.to(device)
    model_T.eval()

    logger.info("Student Model loading")
    student = teachers_and_student['student']
    model_type_S = student['model_type']
    model_config_S = student['config']
    checkpoint_S = student['checkpoint']

    _, _, model_class_S = MODEL_CLASSES[model_type_S]
    model_S = model_class_S(model_config_S, num_labels=num_labels)
    state_dict_S = torch.load(checkpoint_S, map_location='cpu')
    missing_keys, un_keys = model_S.load_state_dict(state_dict_S, strict=False)
    logger.info(f"missing keys:{missing_keys}")
    logger.info(f"unexpected keys:{un_keys}")
    logger.info("Student Model loaded")
    model_S.to(device)
    model_S.eval()

    logger.info("Tradition Model loading")
    tradition = teachers_and_student['tradition']
    model_type_N = tradition['model_type']
    model_config_N = tradition['config']
    checkpoint_N = tradition['checkpoint']

    _, _, model_class_N = MODEL_CLASSES[model_type_N]
    model_N = model_class_N(model_config_N, num_labels=num_labels)
    state_dict_N = torch.load(checkpoint_N, map_location='cpu')
    missing_keys, un_keys = model_N.load_state_dict(state_dict_N, strict=False)
    logger.info(f"missing keys:{missing_keys}")
    logger.info(f"unexpected keys:{un_keys}")
    logger.info("Tradition Model loaded")
    model_N.to(device)
    model_N.eval()

    logger.info("加载数据集")
    train_dataset = None
    eval_datasets = None

    tokenizer_S = teachers_and_student['student']['tokenizer']
    prefix_S = teachers_and_student['student']['prefix']

    eval_datasets = []
    eval_task_names = ("mnli", "mnli-mm") if args.task_name == "mnli" else (args.task_name,)
    for eval_task in eval_task_names:
        eval_datasets.append(load_and_cache_examples(args, eval_task, tokenizer_S, prefix=prefix_S, evaluate=True))

    logger.info("Data loaded")

    # TODO: Embedding Tensor 实际上跟Hidden的维度可能是不同的
    hidden_high = None

    vectors_file = f'{args.output_dir}/vector_dict'
    for task_dataset in eval_datasets:
        hidden_high_task = None
        for data in tqdm(task_dataset):

            input_ids, attention_mask, token_type_ids, label_ids = data

            input_ids = torch.unsqueeze(input_ids, dim=0).to(device)
            attention_mask = torch.unsqueeze(attention_mask, dim=0).to(device)
            token_type_ids = torch.unsqueeze(token_type_ids, dim=0).to(device)

            # last_hidden_state_T = torch.squeeze(model_T.getmiddle(input_ids, attention_mask, token_type_ids), dim=0)
            # last_hidden_state_T = torch.unique(last_hidden_state_T, dim=0).cpu().detach().numpy()

            last_hidden_state_S = torch.squeeze(model_S.getmiddle(input_ids, attention_mask, token_type_ids), dim=0)
            last_hidden_state_S = torch.unique(last_hidden_state_S, dim=0).cpu().detach().numpy()

            # last_hidden_state_N = torch.squeeze(model_N.getmiddle(input_ids, attention_mask, token_type_ids), dim=0)
            # last_hidden_state_N = torch.unique(last_hidden_state_N, dim=0).cpu().detach().numpy()

            _ = last_hidden_state_S

            # _ = np.vstack((last_hidden_state_T, last_hidden_state_S, last_hidden_state_N))

            if hidden_high_task is None:
                hidden_high_task = _
            else:
                hidden_high_task = np.vstack((hidden_high_task, _))
        if hidden_high is None:
            hidden_high = hidden_high_task
        else:
            hidden_high = np.vstack((hidden_high, hidden_high_task))
    np.savez(vectors_file, hidden_high=hidden_high)


def generate_vector_dict():
    # parse arguments
    config.parse()
    args = config.args
    for k, v in vars(args).items():
        logger.info(f"{k}:{v}")

    collect_vectors(args)
    vectors_file_T = './output_calculate_dir/ag_news/ag_news_tea/vector_dict'
    vectors_file_S = f'{args.output_dir}/vector_dict'
    vectors_file_N = './output_calculate_dir/ag_news/ag_news_L6_tra/vector_dict'

    all_vectors_T = np.load('{}.npz'.format(vectors_file_T))
    all_vectors_S = np.load('{}.npz'.format(vectors_file_S))
    all_vectors_N = np.load('{}.npz'.format(vectors_file_N))

    all_vectors_np = np.vstack((all_vectors_T['hidden_high'], all_vectors_S['hidden_high'], all_vectors_N['hidden_high']))

    hidden_high_uni, hidden_low = get_reduce_word_vec(all_vectors_np, 'pca', 2)

    reduce_file = f'{args.output_dir}/vector_reduce'
    np.savez_compressed(reduce_file, high=hidden_high_uni, low=hidden_low)




if __name__ == '__main__':
    # collect_vectors()
    # generate_vector_dict('/home/PP/project/convex/logs/LSTM/imdb-10/version_0/checkpoints/epoch=12-step=1026.ckpt',
    #                      '/home/PP/project/convex/logs/LSTM/imdb-10/version_0/hparams.yaml',
    #                      'vector_dict', 'vector_reduce', 'pca')

    # all_vectors = np.load('{}.npz'.format('/home/jingxu/project/KD_bert/mnli_T12_S6/vector_dict'))
    # all_vectors_np = np.vstack((all_vectors['hidden_high_mnli'], all_vectors['hidden_high_mnli_mm']))
    #
    # hidden_high_uni, hidden_low = get_reduce_word_vec(all_vectors_np, 'pca', 2)
    # reduce_file = '/home/jingxu/project/KD_bert/mnli_T12_S6/vector_reduce'
    # np.savez_compressed(reduce_file, high=hidden_high_uni, low=hidden_low)

    DEBUG = True

    ALL_TASKS = ['MRPC', 'RTE', 'SST-2', 'MNLI', 'QQP', 'MNLI-mm', 'QNLI', 'CoLA', 'race-merge']

    if DEBUG:
        interested_task = 'RTE'.split(',')
        prediction_mode_input = 'teacher:train,dev,test'
        output_all_layers = False  # True for patient teacher and False for normal teacher
        bert_model = 'bert-base-uncased'
        result_file = os.path.join(PROJECT_FOLDER, 'result/glue/result_summary/teacher_12layer_all.csv')
    else:
        interested_task = sys.argv[1].split(',')
        prediction_mode_input = sys.argv[2]
        output_all_layers = sys.argv[3].lower() == 'true'
        bert_model = sys.argv[5]
        result_file = sys.argv[4]

    KD_DIR = os.path.join(HOME_DATA_FOLDER, 'outputs/KD/')

    sub_dir = '_'.join(os.path.basename(result_file).split('_')[:-1])

    prediction_mode, interested_set = prediction_mode_input.split(':')

    if prediction_mode == 'teacher':
        output_dir = os.path.join(HOME_DATA_FOLDER, 'outputs/KD')
    else:
        output_dir = os.path.join(PROJECT_FOLDER, f'result/glue/benchmark/{sub_dir}')

    bert_model = os.path.join(HOME_DATA_FOLDER, f'models/pretrained/{bert_model}')
    config = BertConfig(os.path.join(bert_model, 'bert_config.json'))
    tokenizer = BertTokenizer.from_pretrained(bert_model, do_lower_case=True)
    args = argparse.Namespace(n_gpu=1,
                              device=torch.device("cuda:1" if torch.cuda.is_available() else "cpu"),
                              fp16=False,
                              eval_batch_size=32,
                              max_seq_length=128)

    generate_vector_dict()

