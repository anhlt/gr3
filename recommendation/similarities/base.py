import numpy as np


class BaseSimilarity(object):
    """docstring for BaseSimilarity"""

    def __init__(self, model, distance, num_best=None):
        self.model = model
        self.distance = distance
        self._set_num_best(num_best)

    def _set_num_best(self, num_best):
        self.num_best = num_best

    def get_similarity(self, source_id, target_id):
        raise NotImplementedError("cannot instantiate Abstract Base Class")

    def get_similarities(self, source_id):
        '''
        Return similarity of source_id to all source in the model
        '''

        raise NotImplementedError("cannot instantiate Abstract Base Class")

    def __getitem__(self, source_id):
        all_sims = self.get_similarities(source_id)

        tops = sorted(all_sims, key=lambda x: -x[1])

        if all_sims:
            item_ids, preferences = zip(*all_sims)
            preferences = np.array(preferences).flatten()
            item_ids = np.array(item_ids).flatten()
            sorted_prefs = np.argsort(-preferences)
            tops = zip(item_ids[sorted_prefs], preferences[sorted_prefs])

        return tops[:self.num_best] if self.num_best is not None else tops

