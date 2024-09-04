import torch
import pickle
from tqdm import tqdm
import pandas as pd
import os
import sys
import argparse
import subprocess

root_dir = '/home/LafiscaL/TRAIL_2023/rep-path-reasoning-recsys'
path_to_transe = os.path.join(root_dir, 'models/embeddings/transe/')
path_to_pgpr = os.path.join(root_dir, 'models/PGPR')
path_to_trained_model = os.path.join(root_dir, 'data/ml1m/preprocessed/pgpr/tmp')
path_to_data = os.path.join(root_dir, 'data/ml1m/preprocessed')

os.chdir(path_to_pgpr)

from kg_env import BatchKGEnvironment
from train_agent import ActorCritic
from pgpr_utils import *    
from test_agent import batch_beam_search

from functools import reduce


def add_new_user_data(new_user_info, new_user_ratings, users, ratings, path_to_data):
    
    # Replace uid = 0 rows with new user info column by column
    users.loc[users['uid'] == '0', 'uid'] = new_user_info['uid']
    users.loc[users['uid'] == '0', 'gender'] = new_user_info['gender']
    users.loc[users['uid'] == '0', 'age'] = new_user_info['age']
    
    ratings = ratings[ratings['uid'] != 0]

    for i in range(len(new_user_ratings['pid'])):
        new_row = {
            'uid': new_user_ratings['uid'],
            'pid': new_user_ratings['pid'][i],
            'rating': new_user_ratings['rating'][i],
            'timestamp': new_user_ratings['timestamp'][i]
        }
        new_row_df = pd.DataFrame([new_row])
        ratings = pd.concat([ratings, new_row_df], ignore_index=True)

    users.to_csv(f'{path_to_data}/users.txt', sep='\t', index=False, header=False)
    ratings.to_csv(f'{path_to_data}/ratings.txt', sep='\t', index=False, header=False)
    
    return users, ratings


# Modified predict_paths function to include a specific user
def predict_paths_for_user(policy_file, args, new_user_id):
    print('Predicting paths...')
    env = BatchKGEnvironment(args.dataset, args.max_acts, max_path_len=args.max_path_len,
                             state_history=args.state_history)

    pretrain_sd = torch.load(policy_file)
    model = ActorCritic(env.state_dim, env.act_dim, gamma=args.gamma, hidden_sizes=args.hidden).to(args.device)
    model_sd = model.state_dict()
    model_sd.update(pretrain_sd)
    model.load_state_dict(model_sd)

    # Use the new user ID directly
    batch_uids = [new_user_id]
    
    # Assuming batch_size of 1 since we are predicting for a single user
    paths, probs = batch_beam_search(env, model, batch_uids, args.device, topk=args.topk)
    predicts = {'paths': paths, 'probs': probs}

    return predicts

def get_rec_paths(predicts, k=5):
    pred_paths = {}
    for path, probs in zip(predicts['paths'], predicts['probs']):
        pid = path[-1][2]
        if pid not in pred_paths:
            pred_paths[pid] = []
        path_prob = reduce(lambda x, y: x * y, probs)
        pred_paths[pid].append((path_prob, path))

    best_pred_paths = []

    for pid in pred_paths:
        # Get the path with highest probability
        sorted_path = sorted(pred_paths[pid], key=lambda x: x[1], reverse=True)
        best_pred_paths.append(sorted_path[0])

    sorted_path = sorted(best_pred_paths, key=lambda x: x[0], reverse=True)

    topk_products = [p[-1][2] for _, p in sorted_path[:k]]
    topk_paths = [p for _, p in sorted_path[:k]]
    topk_probs = [p for p, _ in sorted_path[:k]]

    print("Path proba", topk_probs)
    print("paths")
    for i in range(k):
        print(topk_paths[i])

    return topk_paths


def extract_recommendation_path(pid_list, gender='M', age='25-34', number_of_paths=1):
    ### INPUTS ###
    # pid_list : list of all watched movies. e.g., [1193, 1197, 1287, 2804, 594]
    # number_of_paths : the number of paths we want as output (1 by default)
    ### OUTPUTS ###
    # recommendation paths with movie eid. e.g., [('self_loop', 'user', 0), ('watched', 'product', 1930), ('watched', 'user', 3914), ('watched', 'product', 2585)]

    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=str, default=ML1M, help='One of {cloth, beauty, cell, cd}')
    parser.add_argument('--name', type=str, default='train_agent', help='directory name.')
    parser.add_argument('--seed', type=int, default=123, help='random seed.')
    parser.add_argument('--gpu', type=str, default='0', help='gpu device.')
    parser.add_argument('--epochs', type=int, default=50, help='num of epochs.')
    parser.add_argument('--max_acts', type=int, default=250, help='Max number of actions.')
    parser.add_argument('--max_path_len', type=int, default=3, help='Max path length.')
    parser.add_argument('--gamma', type=float, default=0.99, help='reward discount factor.')
    parser.add_argument('--state_history', type=int, default=1, help='state history length')
    parser.add_argument('--hidden', type=int, nargs='*', default=[512, 256], help='number of samples')
    parser.add_argument('--add_products', type=boolean, default=True, help='Add predicted products up to 10')
    parser.add_argument('--topk', type=list, nargs='*', default=[25, 5, 1], help='number of samples')
    parser.add_argument('--run_path', type=boolean, default=True, help='Generate predicted path? (takes long time)')
    parser.add_argument('--run_eval', type=boolean, default=True, help='Run evaluation?')
    parser.add_argument('--save_paths', type=boolean, default=True, help='Save paths')
    parser.add_argument('--new_user', type=boolean, default=True, help='Allow prediction on new user')

    args = parser.parse_args()

    os.environ['CUDA_VISIBLE_DEVICES'] = args.gpu
    args.device = torch.device('cuda:0') if torch.cuda.is_available() else 'cpu'
    args.log_dir = os.path.join(path_to_trained_model, args.name)
    
    # New user information
    new_user_id = '0'
    new_user_info = {'uid': [new_user_id], 'gender': [gender], 'age': [age]}
    new_user_ratings = {'uid': new_user_id,
                        'pid': pid_list,
                        'rating': [5] * len(pid_list),
                        'timestamp': [11111] * len(pid_list)}
    
    # Load existing users and ratings data
    users = pd.read_csv(f'{path_to_data}/init_users.txt', sep='\t', names=['uid', 'gender', 'age'])
    ratings = pd.read_csv(f'{path_to_data}/init_ratings.txt', sep='\t', names=['uid', 'pid', 'rating', 'timestamp'])

    # Add the new user data and overwrite the path
    users, ratings = add_new_user_data(new_user_info, new_user_ratings, users, ratings, path_to_data)

    # Change to the directory and run the first script
    os.chdir(path_to_transe)
    subprocess.run(['python', 'train_transe_NU.py', '--epochs=1'])

    # Change back to the root directory and run the second script
    os.chdir(root_dir)
    subprocess.run(['python', 'prepare_datasets_NU.py'])

    # Change to the PGPR directory and run the third script
    os.chdir(path_to_pgpr)
    subprocess.run(['python', 'train_agent_NU.py', '--epochs=1'])

    policy_file = args.log_dir + '/policy_model_new_user.ckpt'

    predicts = predict_paths_for_user(policy_file, args, new_user_id)

    rec_paths = get_rec_paths(predicts, k=number_of_paths)

    return rec_paths
