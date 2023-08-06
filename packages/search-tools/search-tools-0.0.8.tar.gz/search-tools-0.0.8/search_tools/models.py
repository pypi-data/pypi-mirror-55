import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error
from scipy.sparse import coo_matrix

class ClickModel(object):

    def __init__(
            self,
            data,
            query_col='query',
            result_col='result',
            position_col='position',
            sessions_count='n_sessions',
            events_count='n_clicks',
            history=True,
            strategy='prior',
            val_frac=None,
            verbose=True,
            random_seed=42
        ):
        self.random_seed=random_seed
        if val_frac is not None:
            self.val_frac = val_frac
            self.val = True
        else:
            self.val = False
        self._init_graph(data, query_col, result_col, position_col, sessions_count, events_count)
        pos_size = len(self.pos_dict)
        qr_size = len(self.qr_dict)
        self._init_parameters(pos_size, qr_size, strategy=strategy)
        self.history = history
        if self.history:
            self.pos_diff_history = []
            self.qr_diff_history = []
            self.train_loss = []
            self.val_loss = []

        self.result_col = result_col
        self.query_col = query_col
        self.position_col = position_col
        self.verbose = verbose


    def _init_graph(self, data, query_col, result_col, position_col, sessions_count, events_count):
        """
        Initialize the sparse graph for more efficient computation.
        The resulting graph is written to self.graph and is an array like:
        [
            [position index, query-result index, number of positive events, number of negative events],
            [...],
            ...
        ]

        """
        df = data.copy()
        if 'float' in str(df[result_col].dtype):
            df[result_col] = df[result_col].astype(int)
        df['__qr_pair'] = df.apply(lambda row: str(row[query_col]) + '_' + str(row[result_col]), axis=1)
        pos_list = df[position_col].unique()
        pos_list.sort()
        self.pos_dict = {x:x for x in pos_list}

        qr_list = df['__qr_pair'].unique()
        self.qr_dict = {val:i for i,val in enumerate(qr_list)}
        df['__pos_idx'] = df[position_col].apply(lambda x: self.pos_dict[x])
        df['__qr_idx'] = df['__qr_pair'].apply(lambda x: self.qr_dict[x])
        df['__n_no_clicks'] = df[sessions_count] - df[events_count]
        graph = df[['__pos_idx', '__qr_idx', events_count, '__n_no_clicks']].values

        if self.val:
            #get validation set
            n_val_nodes = max(round(self.val_frac * len(graph)), 1)
            qrs, counts = np.unique(graph[:, 1], return_counts=True)
            to_take = qrs[np.where(counts>1, True, False)]
            try:
                np.random.seed(self.random_seed)
                to_take = np.random.choice(to_take, size=(n_val_nodes,), replace=False)
            except ValueError:
                msg = 'Cannot hold out this many nodes. Please reduce val_frac.'
                raise Exception(msg)
            val_idx = []
            for qr_idx in to_take:
                candidates = np.argwhere(graph[:,1]==qr_idx).flatten()
                idx = np.random.choice(candidates)
                val_idx.append(idx)
            val_idx = np.array(val_idx)

            self.val_graph = graph[val_idx]
            self.graph = graph[~np.isin(np.arange(0, len(graph)), val_idx)]
        else:
            self.graph=graph

    def _init_parameters(self, pos_size, qr_size, strategy):
        if isinstance(strategy, float):
            self.pos = np.array([strategy for _ in range(pos_size)])
            self.qr = np.array([.1 for _ in range(qr_size)])
        elif strategy == 'prior':
            pos_idx = self.graph[:, 0]
            qr_idx = self.graph[:, 1]
            n_clicks = self.graph[:, 2]
            nums = np.array(coo_matrix((n_clicks, (qr_idx, pos_idx))).sum(axis=0)).reshape(-1)
            n_no_clicks = self.graph[:, 3]
            denoms = np.array(coo_matrix((n_no_clicks, (qr_idx, pos_idx))).sum(axis=0)).reshape(-1)
            denoms = denoms + nums
            estimate = nums/denoms
            self.pos = estimate * (.99/estimate.max())

            ctrs = n_clicks / (n_clicks+n_no_clicks)
            P_inspect = self.pos[pos_idx]
            P_click = ctrs/P_inspect
            #constrain value between .01 and .99
            P_click = np.where(P_click > .99, .99, P_click)
            P_click = np.where(P_click < .01, .01, P_click)
            weights = n_clicks + n_no_clicks
            nums = np.array(coo_matrix((P_click * weights, (qr_idx, pos_idx))).sum(axis=1)).reshape(-1)
            denoms = np.array(coo_matrix((weights, (qr_idx, pos_idx))).sum(axis=1)).reshape(-1)

            self.qr = nums/denoms
        else:
            np.random.seed(self.random_seed)
            self.pos = np.random.random(size=(pos_size,))
            self.qr = np.random.random(size=(qr_size,))

    def _compute_update(self, kind=None):
        #these values are shared in both updates
        qr_idx = self.graph[:, 1]
        alpha = self.qr[qr_idx]
        pos_idx = self.graph[:, 0]
        gamma = self.pos[pos_idx]
        ctr = self.graph[:, 2]
        no_ctr = self.graph[:, 3]
        #these terms appears in both updates
        shared_term = (1 - gamma * alpha)
        denom = ctr + no_ctr
        denom_mat = coo_matrix((denom, (qr_idx, pos_idx)))

        if kind == 'qr' or kind is None:
            #here we compute update to alpha params
            qr_update = (ctr + (no_ctr * (((1 - gamma) * alpha) / shared_term)))
            qr_mat = coo_matrix((qr_update, (qr_idx, pos_idx)))
            qr_vec = qr_mat.sum(axis=1)

            denom_mat = coo_matrix((denom, (qr_idx, pos_idx)))
            qr_denom_vec = denom_mat.sum(axis=1)

            #this vector is the new set of alpha params
            new_qr = np.array(qr_vec / qr_denom_vec).reshape(-1)

            if kind == 'qr':
                return new_qr

        if kind == 'pos' or kind is None:

            #here we compute update to gamma params
            pos_update = (ctr + (no_ctr * (((1 - alpha) * gamma) / shared_term)))
            pos_mat = coo_matrix((pos_update, (qr_idx, pos_idx)))
            pos_vec = pos_mat.sum(axis=0)

            pos_denom_vec = denom_mat.sum(axis=0)

            #this vector is the new set of alpha params
            new_pos = np.array((pos_vec / pos_denom_vec)).reshape(-1)

            if kind == 'pos':
                return new_pos

        #return both if none specified
        return new_pos, new_qr

    def compute_diff(self, v0, v1):
        return np.linalg.norm(v0 - v1)

    def update_pos(self):
        new_pos = self._compute_update(kind='pos')
        self.pos = new_pos
        diff_pos = self.compute_diff(self.pos, new_pos)
        if self.history:
            self.pos_diff_history.append(diff_pos)

    def update_qr(self):
        new_qr = self._compute_update(kind='qr')
        self.qr = new_qr
        diff_qr = self.compute_diff(self.qr, new_qr)
        if self.history:
            self.qr_diff_history.append(diff_qr)

    def update_both(self):
        new_pos, new_qr = self._compute_update()
        diff_pos = self.compute_diff(self.pos, new_pos)
        diff_qr = self.compute_diff(self.qr, new_qr)
        if self.history:
            self.pos_diff_history.append(diff_pos)
            self.qr_diff_history.append(diff_qr)
        self.pos = new_pos
        self.qr = new_qr

    def validate(self, val_set=False):
        if val_set:
            graph = self.val_graph
        else:
            graph = self.graph
        total = graph[:, 2] + graph[:, 3]
        positive_outcomes = graph[:, 2]
        predicted_outcomes = (self.pos[graph[:, 0]] * self.qr[graph[:, 1]]) * total
        return mean_absolute_error(positive_outcomes, predicted_outcomes)

    def do_update(self, alternate=True):
        if alternate:
            self.update_pos()
            self.update_qr()
        else:
            self.update_both()

    def decode_qr_pairs(self, items):
        split = [x.split('_') for x in items]
        terms = ['_'.join(x[:-1]) for x in split]
        results = [x[-1] for x in split]
        return results, terms

    def fit(self, n_iterations=1000, alternate=True, stopping=None, min_iterations=20):
        if stopping is not None:
            prev = 1e99
        for i in range(n_iterations):
            self.do_update(alternate)
            val_loss = self.validate(val_set=self.val)
            if self.val:
                train_loss = self.validate(val_set=False)
            else:
                train_loss = val_loss
            if i%10 == 0 and self.verbose:
                print('validation loss at iteration {}: '.format(i), round(val_loss, 4))
            if self.history:
                self.train_loss.append(train_loss)
                self.val_loss.append(val_loss)
            if stopping is not None:
                diff = prev - val_loss
                if i > min_iterations and diff < stopping:
                    if self.verbose:
                        print('stopping early with ', str(i), ' iterations  and a val loss of ', val_loss)
                    break
                prev = val_loss

        qr_map = {self.qr_dict[key]:key for key in self.qr_dict}
        qr_keys = [qr_map[i] for i in range(len(self.qr))]
        pids, results = self.decode_qr_pairs(qr_keys)
        qr_values = self.qr
        qr_results = pd.DataFrame(columns=[self.result_col, self.query_col, 'attractiveness'])
        qr_results[self.result_col] = pids
        qr_results[self.query_col] = results
        qr_results['attractiveness'] = qr_values

        pos_results = pd.DataFrame(columns=[self.position_col, 'p_examine'])
        pos_results[self.position_col] = list(range(len(self.pos)))
        pos_results['p_examine'] = self.pos

        if self.history:
            history = {
                'val_loss':self.val_loss,
                'train_loss':self.train_loss,
                'delta_pos':self.pos_diff_history,
                'delta_qr':self.qr_diff_history
            }

        else:
            history = {}

        return qr_results, pos_results, history
