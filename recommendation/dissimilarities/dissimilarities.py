from base import BaseDissimilarities


class Dissimilarity(BaseDissimilarities):
    """docstring for Dissimilarity"""

    def __init__(self, model, dis_function):
        self.model = model
        self.dis_function = dis_function

    def get_dissimilarity(self):
        return self.dis_function(self.model.index)