"""This file import the main functions to use metrics.
Functions here are slightly modified according to our needs from
 https://github.com/explainablerecsys/ecir2024/tree/main/Hands-On."""

import pickle

from typing import Dict, Tuple
from tqdm import tqdm

from metrics_alone.beyond_accuracy_metrics import COVERAGE, PFAIRNESS, coverage, \
    serendipity_at_k, diversity_at_k, novelty_at_k, get_item_genre, get_item_count, get_item_pop, SERENDIPITY, \
    DIVERSITY, NOVELTY
from metrics_alone.eval_utils import compute_mostpop_topk, get_precomputed_topks, REC_QUALITY_METRICS_TOPK
from metrics_alone.utility_metrics import *
from metrics_alone.data_utils import get_set

# def evaluate_rec_quality(dataset_name: str, topk_items: Dict[int, List[int]], test_labels: Dict[int, List[int]],
def evaluate_rec_quality(dataset_name: str, topk_items: Dict[int, List[int]],
                         k: int = 10, method_name=None, metrics: List[str] = REC_QUALITY_METRICS_TOPK) -> Tuple[Dict[str, float], Dict[str, List[float]]]:
    """
    This function computes all the recommendation quality metrics for a given set of topk items, please note that the topk items and test set are
    expressed using the original ids of the dataset (e.g. the ids of the movies in the MovieLens dataset).
    """
    test_labels = get_set("ml1m", set_str='test')
    
    rec_quality_metrics = {metric: list() for metric in metrics}
    recommended_items_all_user_set = set()

    n_items_in_catalog = get_item_count(dataset_name)  # Needed for coverage
    pid2popularity = get_item_pop(dataset_name)  # Needed for novelty
    pid2genre = get_item_genre(dataset_name)  # Needed for diversity
    mostpop_topk = compute_mostpop_topk(dataset_name, k)  # Needed for serendipity

    topk_sizes = []
    # Evaluate recommendation quality for users' topk
    with tqdm(desc=f"Evaluating rec quality for {method_name}", total=len(topk_items.keys())) as pbar:
        for uid, topk in topk_items.items():
            hits = []
            for pid in topk[:k]:
                hits.append(1 if pid in test_labels[uid] else 0)

            # If the model has predicted less than 10 items pad with zeros
            while len(hits) < k:
                hits.append(0)
            for metric in REC_QUALITY_METRICS_TOPK:
                if len(topk) == 0:
                    metric_value = 0.0
                else:
                    if metric == NDCG:
                        metric_value = ndcg_at_k(hits, k)
                    if metric == MRR:
                        metric_value = mmr_at_k(hits, k)
                    if metric == PRECISION:
                        metric_value = precision_at_k(hits, k)
                    if metric == RECALL:
                        test_set_len = max(max(1, len(topk)), len(test_labels[uid]))
                        metric_value = recall_at_k(hits, k, test_set_len)
                    if metric == SERENDIPITY:
                        metric_value = serendipity_at_k(topk, mostpop_topk[uid], k)
                    if metric == DIVERSITY:
                        metric_value = diversity_at_k(topk, pid2genre)
                    if metric == NOVELTY:
                        metric_value = novelty_at_k(topk, pid2popularity)
                    if metric == PFAIRNESS:
                        continue  # Skip for now
                rec_quality_metrics[metric].append(metric_value)

            # For coverage
            recommended_items_all_user_set.update(set(topk))
            topk_sizes.append(len(topk))
            pbar.update(1)

    # Compute average values for evaluation
    avg_rec_quality_metrics = {metric: np.mean(values) for metric, values in rec_quality_metrics.items()}
    avg_rec_quality_metrics[COVERAGE] = coverage(recommended_items_all_user_set, n_items_in_catalog)

    # Print results
    print(f'Number of users: {len(topk_items.keys())}, average topk size: {np.array(topk_sizes).mean():.2f}')
    print_rec_quality_metrics(avg_rec_quality_metrics)
    # print(generate_latex_row(args.model, avg_rec_quality_metrics, "rec"))
    # Save as csv if specified
    return rec_quality_metrics, avg_rec_quality_metrics


def print_rec_quality_metrics(avg_rec_quality_metrics: Dict[str, float], method='inline'):
    """
    args:
        avg_rec_quality_metrics: a dictionary containing the average value of each metric
    """
    if method=='latex':
        print(' & '.join(list(avg_rec_quality_metrics.keys())))
        print(' & '.join([str(round(value, 2)) for value in avg_rec_quality_metrics.values()]))
    elif method=='inline':
        print(', '.join([f'{metric}: {round(value, 2)}' for metric, value in avg_rec_quality_metrics.items()]))
    elif method=='endline':
        for metric, value in avg_rec_quality_metrics.items():
            print(f'{metric}: {round(value, 2)}')

            
### HOW TO USE ###

# RECOMMENDATION_PATH = "/home_nfs/stassinsed/MA2/Q2/PhD/TRAIL_6/Lisbonne2024/ecir2024/Hands-On/results/ml1m/cafe/top10_items.pkl"

# PROVIDE recommendation for all users in the following format: 
# {int(k): [int(v) for v in topk_items[k]] for k in topk_items}

# Loading here from the ecir2024 github : 
# with open(RECOMMENDATION_PATH, 'rb') as f:
#     topk_items = pickle.load(f)
# # print("Initial topk:", topk_items)
# topk_items = {int(k): [int(v) for v in topk_items[k]] for k in topk_items}
# print("Topk: ", topk_items[0:3])

# # Obtaining labels from the ml1m test set
# test_labels = get_set("ml1m", set_str='test')

# out = evaluate_rec_quality(dataset_name="ml1m", 
#                      topk_items=topk_items, 
#                      test_labels=test_labels)