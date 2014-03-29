from base import ItemRecommender, UserRecommender
from item_strategies import AllPossibleItemsStrategy, ItemsNeighborhoodStrategy
#from neighborhood_strategies import NearestNeighborsStrategy
import numpy as np

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('recommended')


class ItemBasedRecommender(ItemRecommender):
    """
    Item Based Collaborative Filtering Recommender.
    """

    def __init__(self, model, similarity, arg, items_selection_strategy=None, capper=True, with_preference=False):
        self.similarity = similarity
        self.capper = capper
        self.model = model
        if items_selection_strategy is None:
            self.items_selection_strategy = ItemsNeighborhoodStrategy()
        else:
            self.items_selection_strategy = items_selection_strategy

    def recommended(self, user_id, how_many=None):
        candidate_items = self.all_other_items(user_id)
        recommendable_items = self._top_matches(user_id, candidate_items, how_many)

        return recommendable_items


    def estimate_preference(self, user_id, item_id):
        preference = self.model.preference_value(user_id, item_id)

        if not np.isnan(preference):
            return preference

        prefs = self.model.preferences_from_user(user_id)
        #lay cac gia tri da rating cuar user

        similarities = np.array([self.similarity.get_similarity(item_id, to_item_id) for to_item_id, pref in prefs if
                                 to_item_id != item_id]).flatten()
        #mang tra ve gia tri do giong nhau giua item vs candidate

        prefs = np.array([pref for it, pref in prefs])

        prefs_sim = np.sum(prefs[~np.isnan(similarities)] * similarities[~np.isnan(similarities)])

        total_similarity = np.sum(similarities)

        if total_similarity == 0.0 or not similarities[~np.isnan(similarities)].size:
            return np.nan

        estimated = prefs_sim / total_similarity

        if self.capper:
            max_p = self.model.maximum_preference_value()
            min_p = self.model.minimum_preference_value()
            estimated = max_p if estimated > max_p else min_p \
                if estimated < min_p else estimated
        return estimated


    def all_other_items(self, user_id):
        return self.items_selection_strategy.candidate_items(user_id, self.model)


    def _top_matches(self, source_id, target_ids, how_many=None):
        if target_ids.size == 0:
            return np.array([])
        preferences = np.array([self.estimate_preference(source_id, target_id) for target_id in target_ids])
        logger.debug(preferences)

        preference_values = preferences[~np.isnan(preferences)]
        target_ids = target_ids[~np.isnan(preferences)]

        sorted_preferences = np.lexsort((preference_values,))[::-1]

        sorted_preferences = sorted_preferences[0:how_many] \
            if how_many and sorted_preferences.size > how_many \
            else sorted_preferences
        top_n_recs = [(target_ids[ind], \
                       preferences[ind]) for ind in sorted_preferences]

        return top_n_recs