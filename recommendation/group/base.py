class BaseGroupRecommender(object):
    """docstring for BaseGroupRecommender"""

    def __init__(self, model, user_list, expertise, social, dissimmilarity):
        self.model = model
        self.user_list = user_list
        self.expertise = expertise
        self.social = social
        self.dissimmilarity = dissimmilarity


    def build_model():
        raise NotImplementedError("cannot instantiate Abstract Base Class")

