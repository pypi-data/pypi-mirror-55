# -*- coding: utf-8 -*-

# @Time   : 2019/7/13 19:27
# @Author : Administrator
# @Project : feature_toolbox
# @FileName: sum.py
# @Software: PyCharm

"""
USM
this is a union select method for feature subsets.
key:
1.gather performance of different model
2.raise the best one from similar learning performance subsets
3.rank the raised subsets and penalty the size of subsets

node == feature subset
"""
import numpy as np

from featurebox.selection.ugs import UGS


def _kamada_kawai_solve(dist_mtx, dim=2):
    # Anneal node locations based on the Kamada-Kawai cost-function,
    # using the supplied matrix of preferred inter-node distances,
    # and starting locations.
    from networkx import circular_layout
    pos = circular_layout(list(range(dist_mtx.shape[0])), dim=dim)
    pos_arr = np.array([pos[n] for n in list(range(dist_mtx.shape[0]))])

    from scipy.optimize import minimize

    meanwt = 1e-3
    costargs = (np, 1 / (dist_mtx + np.eye(dist_mtx.shape[0]) * 1e-3),
                meanwt, dim)

    optresult = minimize(_kamada_kawai_costfn, pos_arr.ravel(),
                         method='L-BFGS-B', args=costargs, jac=True)

    return optresult.x.reshape((-1, dim))


def _kamada_kawai_costfn(pos_vec, np, invdist, meanweight, dim):
    # Cost-function and gradient for Kamada-Kawai layout algorithm
    nNodes = invdist.shape[0]
    pos_arr = pos_vec.reshape((nNodes, dim))

    delta = pos_arr[:, np.newaxis, :] - pos_arr[np.newaxis, :, :]
    nodesep = np.linalg.norm(delta, axis=-1)
    direction = np.einsum('ijk,ij->ijk',
                          delta,
                          1 / (nodesep + np.eye(nNodes) * 1e-3))

    offset = nodesep * invdist - 1.0
    offset[np.diag_indices(nNodes)] = 0

    cost = 0.5 * np.sum(offset ** 2)
    grad = (np.einsum('ij,ij,ijk->ik', invdist, offset, direction) -
            np.einsum('ij,ij,ijk->jk', invdist, offset, direction))

    # Additional parabolic term to encourage mean position to be near origin:
    sumpos = np.sum(pos_arr, axis=0)
    cost += 0.5 * meanweight * np.sum(sumpos ** 2)
    grad += meanweight * sumpos

    return cost, grad.ravel()


class SUM(UGS):
    """

    """

    def __init__(self, estimator, slices, estimator_n=None, n_jobs=2):
        """

        Parameters
        ----------
        estimator : list
            list of base estimator or GridSearchCV from sklearn
        slices: list
            the lists of the index of feature subsets, each feature subset is a node,each int is the index of X
            Examples 3 nodes
            [[1,4,5],[1,4,6],[1,2,7]]
        estimator_n: list
            default indexes of estimator
        """
        super().__init__(estimator, slices, estimator_n=estimator_n, n_jobs=n_jobs)

    def distance_method(self):
        cal_binary_distance_all_model = [self.cal_binary_distance_all(estimator_i=i) for i in self.estimator_n]
        score_all_model = [self.score_all(estimator_i=i)[:, 0] for i in self.estimator_n]
        max_node = [[np.argmax(_)] for _ in score_all_model]
        l = len(score_all_model[0])
        iter_ = np.linspace(np.min(np.array(cal_binary_distance_all_model)),
                            np.max(np.array(cal_binary_distance_all_model)), num=100 * l)

        # unify = [np.max(_) for _ in cal_binary_distance_all_model]
        # cal_binary_distance_all_model = [i / j for i, j in zip(cal_binary_distance_all_model, unify)]

        rank = []
        distance = []
        for steps in iter_:
            circle = set(list(range(l)))
            for dis_all, score_all, max_node_i in zip(cal_binary_distance_all_model, score_all_model, max_node):
                circle_i = set(np.where(dis_all[:, max_node_i[0]] <= steps)[0])
                circle &= circle_i
            print(circle, steps)
            addd = list(circle - set(rank))
            if addd:
                rank.extend(list(circle - set(rank)))
                distance.extend([steps] * len(addd))
        return rank

    def kk_distance_method(self):
        cal_binary_distance_all_model = [self.cal_binary_distance_all(estimator_i=i) for i in self.estimator_n]
        score_all_model = [self.score_all(estimator_i=i)[:, 0] for i in self.estimator_n]
        KK_dis_all_model = [_kamada_kawai_solve(_, dim=2) for _ in cal_binary_distance_all_model]

        def cal_r(kk):
            r_matrix = []
            for i in kk:
                r_matrix.append(np.sqrt(np.sum((kk - i) ** 2, axis=1)))
            return np.array(r_matrix)

        cal_binary_distance_all_model = [cal_r(_) for _ in KK_dis_all_model]

        # unify = [np.max(_) for _ in cal_binary_distance_all_model]
        # cal_binary_distance_all_model = [i / j for i, j in zip(cal_binary_distance_all_model, unify)]

        max_node = [[np.argmax(_)] for _ in score_all_model]
        l = len(score_all_model[0])
        iter_ = np.linspace(np.min(np.array(cal_binary_distance_all_model)),
                            np.max(np.array(cal_binary_distance_all_model)), num=100 * l)

        rank = []
        distance = []
        for steps in iter_:
            circle = set(list(range(l)))
            for dis_all, score_all, max_node_i in zip(cal_binary_distance_all_model, score_all_model, max_node):
                circle_i = set(np.where(dis_all[:, max_node_i[0]] <= steps)[0])
                circle &= circle_i
            print(circle, steps)
            addd = list(circle - set(rank))
            if addd:
                rank.extend(list(circle - set(rank)))
                distance.extend([steps] * len(addd))

        return list(zip(rank, distance))

    def pareto_method(self, sign=None):
        y = np.array([self.score_all(estimator_i=i)[:, 0] for i in self.estimator_n]).T
        std_ = np.std(y, axis=1)
        m = y.shape[0]
        n = y.shape[1]
        print(m, n)
        if not sign:
            sign = np.array([1] * n)
        y = y * sign
        front_point = []
        for i in range(m):
            data_new = y[i, :].reshape(1, -1) - y
            data_max = np.max(data_new, axis=1)
            data_in = np.min(data_max)
            if data_in >= 0:
                front_point.append(i)
        front_point = np.array(front_point)
        std_front = std_[front_point]
        rank_ = np.argsort(std_front)
        front_point_rank = front_point[rank_]
        std_front_rank = std_front[rank_]

        return list(zip(front_point_rank, std_front_rank))

    def mean_max_method(self):
        score_all = np.array([self.score_all(estimator_i=i)[:, 0] for i in self.estimator_n]).T
        score = np.mean(score_all, axis=1)
        rank = np.argsort(score)[::-1]
        score_ranked = score[rank]
        return list(zip(rank, score_ranked))
