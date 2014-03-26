class BaseRecommender():
    """
    Base Class for Recommenders that suggest items for users.

    Should not be used directly, use derived classes instead

    Attributes
    ----------
     model:  DataModel
          Defines the data model where data is fetched.

     with_preference: bool
          Defines if the recommendations come along with the
          estimated preferences. (default= False)

    """

    def __init__(self, model, with_preference=False):
        self.model = model
        self.with_preference = with_preference

    def recommend(self, user_id, how_many):
        '''
        Parameters
        ----------
        user_id: int or string
                 User for which recommendations are to be computed.
        how_many: int
                 Desired number of recommendations
        Returns
        ---------
        Return a list of recommended items, ordered from most strongly
        recommend to least.

        '''
        raise NotImplementedError("BaseRecommender is an abstract class.")

    def estimate_preference(self, user_id, item_id):
        '''
        Parameters
        ----------
        user_id: int or string
                 User for which recommendations are to be computed.

        item_id: int or string
                Item for which recommendations are to be computed.

        Returns
        -------
        Return an estimated preference if the user has not expressed a
        preference for the item, or else the user's actual preference for the
        item. If a preference cannot be estimated, returns None.
        '''
        raise NotImplementedError("BaseRecommender is an abstract class.")

    def all_other_items(self, user_id):
        '''
        Parameters
        ----------
        user_id: int or string
                 User for which recommendations are to be computed.

        Returns
        --------
        Return all items in the `model` for which the user has not expressed
        the preference and could possibly be recommended to the user.
        '''
        raise NotImplementedError("BaseRecommender is an abstract class.")

    def set_preference(self, user_id, item_id, value):
        '''
        Set a new preference of a user for a specific item with a certain
        magnitude.

        Parameters
        ----------
        user_id: int or string
                 User for which the preference will be updated.

        item_id: int or string
                 Item that will be updated.

        value:  The new magnitude for the preference of a item_id from a
                user_id.

        '''
        self.model.set_preference(user_id, item_id, value)

    def remove_preference(self, user_id, item_id):
        '''
        Remove a preference of a user for a specific item

        Parameters
        ----------
        user_id: int or string
                 User for which recommendations are to be computed.
        item_id: int or string
                 Item that will be removed the preference for the user_id.

        '''
        self.model.remove_preference(user_id, item_id)


class ItemRecommender(BaseRecommender):
    def __init__(self, arg):
        super(ItemRecommender, self).__init__()
        self.arg = arg


    def most_similar_item(self, item_id, how_many=None):
        """
        Tra ve gia nhung item giong vs item duoc dua ra nhat

        Parameters
        ----------
        item_id : int / string
            Id cua item
        how_many : int
            Chi ra so item giong vs item da chi ra nhat

        """
        raise NotImplementedError("ItemRecommender is an abstract class ")


    def recommended_because(self, user_id, item_id, how_many):
        '''
        Dua ra item ma anh huong lon nhat den item da recommended cho nguoi dung

        Parameters
        ----------
        user_id : int / string
            Id cua user
        item_id :
            id cua item da dc recommended
        how_many:
            so luong toi da item tra ve

        returns
        -------

        Danh sach nhung item sap xep theo thu tu anh huong lon nhat den it nhat
        '''

        raise NotImplementedError("ItemRecommender is an abstract class")

#User-base interface


class UserRecommender(BaseRecommender):
    """docstring for UserRecommender"""

    def __init__(self, arg):
        super(UserRecommender, self).__init__()
        self.arg = arg

    def most_similar_user(self, user_id, how_many=None):
        """
        Return the most similar user to the given user_id, ordered from the most to least

        Parameters
        ----------
        user_id : int
            ID of user
        how_many : int
            Desired number of most most_similar_user to find

        """

        raise NotImplementedError("UserRecommender is abstract class")

    def recommended_because(self, user_id, item_id, how_many):
        """
        Returns the users that were most influential in recommending a given item to a given user

        Parameters:
        -----------
        user_id : int
            ID of the user who recommended item_id

        item_id : int
            ID of the item that was recommended

        how_many : int
            maximum number of item to returns

        Returns:
        ----------
        The list of users ordered from most influential to least


        """
        raise NotImplementedError("UserRecommender is an abstract class")


class BaseCandidateItemStrategy(object):
    """
    Base implementation for retrieving
    all item that could possibly be recommended to user
    """

    def __init__(self, arg):
        super(BaseCandidateItemStrategy, self).__init__()
        self.arg = arg


    def candidate_items(self, user_id, data_model):
        '''
        Returns the candidate_items that could possibly be recommended to the user


        Parameters:
        -----------
        user_id :int
            ID of user for which to find most similar other users

        data_model:
            The DataModel that will be the source for the possibly candidate_items
        '''

        raise NotImplementedError("BaseCandidateItemStrategy is abstract class")


class BaseUserNeighborhoodStrategy(object):
    '''
    Base implementation for retrieving
    all users that could possibly be select as part of the neighborhood.
    '''

    def user_neighborhood(self, user_id, data_model, n_similarity='user_similarity',
                          distance=None, n_users=None):
        '''
        Computes a neighborhood consisting of the  n users to a given user based on the
        strategy implemented in this method.
        Parameters
        -----------
        user_id:  int or string
            ID of user for which to find most similar other users

        data_model: DataModel instance
            The data model that will be the source for the possible
            candidates

        n_similarity: string
            The similarity to compute the neighborhood (default = user_similarity)

        distance: function
            Pairwise metric to compute the similarity between the users.

        nhood_size: int
            The neighborhood size (default = None all users)

        '''
        raise NotImplementedError("BaseCandidateItemsStrategy is an abstract class.")
