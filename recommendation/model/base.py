"""
Base Data Models.
"""


class BaseDataModel(object):
    def user_ids(self):
        '''
        Returns
        --------
        Tra ve tat ca user trong model
        '''
        raise NotImplementedError("cannot instantiate Abstract Base Class")

    def item_ids(self):
        '''
        Returns
        -------

        tra ve tat ca cac item trong model
        '''
        raise NotImplementedError("cannot instantiate Abstract Base Class")

    def preferences_values_from_user(self, user_id, order_by_id=True):
        '''
        Parameters
        ----------
        user_id: user id 

        order_by_id: bool

        Returns
        ---------
        Tra ve gia tri rating cua user
        '''
        raise NotImplementedError("cannot instantiate Abstract Base Class")

    def preferences_from_user(self, user_id, order_by_id=True):
        '''
        Parameters
        ----------
        user_id: user id in the model

        order_by_id: bool

        Returns
        ---------
        '''
        raise NotImplementedError("cannot instantiate Abstract Base Class")

    def items_from_user(self, user_id):
        '''
        Parameters
        ----------
        user_id: user id in the model
                int or string

        Returns
        -------
        '''
        raise NotImplementedError("cannot instantiate Abstract Base Class")

    def preferences_for_item(self, item_id, order_by_id=True):
        '''
        Parameters
        ----------
        item_id: id of the item in the model
                string or int

        order_by_id: bool
                If True order by user_id otherwise by the preference values.
                default = True
        Returns
        ---------
        '''
        raise NotImplementedError("cannot instantiate Abstract Base Class")

    def preference_value(self, user_id, item_id):
        '''
        Parameters
        ----------
        user_id: user id in the model
                int or string

        item_id: id of the item in the model
                string or int

        Returns
        --------
        '''
        raise NotImplementedError("cannot instantiate Abstract Base Class")

    def users_count(self):
        '''
        Returns
        -------

        '''
        raise NotImplementedError("cannot instantiate Abstract Base Class")

    def items_count(self):
        '''
        Returns
        -------

        '''
        raise NotImplementedError("cannot instantiate Abstract Base Class")

    def set_preference(self, user_id, item_id, value=None):
        '''
        Parameters
        ----------
        user_id: 
        item_id: 

        '''
        raise NotImplementedError("cannot instantiate Abstract Base Class")

    def remove_preference(self, user_id, item_id):
        '''
        Parameters
        ----------
        user_id:
        item_id:
        '''
        raise NotImplementedError("cannot instantiate Abstract Base Class")


    def maximum_preference_value(self):
        '''
        Returns
        --------

        '''
        raise NotImplementedError("cannot instantiate Abstract Base Class")

    def minimum_preference_value(self):
        '''
        Returns
        --------

        '''
        raise NotImplementedError("cannot instantiate Abstract Base Class")
