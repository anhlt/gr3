from base import BaseGroupRecommender
#from .MatrixPreferenceDataModel.classes import MatrixPreferenceDataModel as DataModel
from recommendation.model.classes import MatrixPreferenceDataModel as DataModel
from recommendation.dissimilarities.dissimilarities import Dissimilarity
import numpy as np


class GroupRecommender(BaseGroupRecommender):
    """docstring for GroupRecommender"""

    def __init__(self, model, user_list, expertise, social, dissimmilarity):
        super(GroupRecommender, self).__init__(model, user_list, expertise, social, dissimmilarity)
        self.build_model()
        self._dissimilarity = Dissimilarity(self.model, dissimmilarity)
        self.anpha = 0.5
        self.beta = 0.5

    def build_model(self):
        critics = {}
        for user in self.user_list:
            critics[user] = dict(self.model.preferences_from_user(user))
        self.model = DataModel(critics)
        print self.model

    def get_dissimilarity(self):
        return self._dissimilarity.get_dissimilarity()


    def recommend(self):
        a = self.model.index
        preference_values = self.anpha * np.mean(a, axis=0) + self.beta * (1 - self.get_dissimilarity())
        target_ids = self.model.item_ids()
        sorted_preferences = np.lexsort((preference_values,))[::-1]
        top_n_recs = [(target_ids[ind], preference_values[ind]) for ind in sorted_preferences]
        return top_n_recs
		
		
