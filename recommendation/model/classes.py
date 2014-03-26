import numpy as np
from .base import BaseDataModel
from .utils import UserNotFoundError, ItemNotFoundError
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('crab')


class MatrixPreferenceDataModel(BaseDataModel):
    """docstring for MatrixPreferenceDataModel"""

    def __init__(self, dataset):
        super(MatrixPreferenceDataModel, self).__init__()
        self.dataset = dataset
        self.build_model()

    def __getitem__(self, user_id):
        return self.preferences_from_user(user_id)

    def __iter__(self):
        for index, user in enumerate(self.user_ids()):
            yield user, self[user]

    def __len__(self):
        return self.index.shape


    def build_model(self):
        '''
        Return
        ------
        self:
            Build the data model
        '''

        self._user_ids = np.asanyarray(self.dataset.keys())
        self._user_ids.sort()

        self._item_ids = []
        for items in self.dataset.itervalues():
            self._item_ids.extend(items.keys())

        self._item_ids = np.unique(np.array(self._item_ids))
        self._item_ids.sort()

        self.max_pref = -np.inf
        self.min_pref = np.inf
        logger.info("Creating matrix for %d users and %d items" % (self._user_ids.size, self._item_ids.size))

        self.index = np.empty(shape=(self._user_ids.size, self._item_ids.size))

        for user_no, user_id in enumerate(self._user_ids):
            logger.debug("PROGRESS : at user_id #%i/%i" % (user_no, self._user_ids.size))
            for item_no, item_id in enumerate(self._item_ids):
                r = self.dataset[user_id].get(item_id, np.NaN)
                self.index[user_no, item_no] = r

        if self.index.size:
            self.max_pref = np.nanmax(self.index)
            self.min_pref = np.nanmin(self.index)


    def user_ids(self):
        '''
        Returns
        -------

        self._user_ids
        '''
        return self._user_ids

    def item_ids(self):

        '''
        Returns
        -------
        self._item_ids

        '''
        return self._item_ids

    def preferences_values_from_user(self, user_id):
        user_id_loc = np.where(self._user_ids == user_id)
        if not user_id_loc[0].size:
            raise UserNotFoundError
        preference = self.index[user_id_loc]
        return preference


    def preferences_from_user(self, user_id, order_by_id=True):

        preference = self.preferences_values_from_user(user_id)

        data = zip(self._item_ids, preference.flatten())

        if order_by_id:
            return [(item_id, preference) for item_id, preference in data if not np.isnan(preference)]
        else:
            return sorted([(item_id, preference) for item_id, preference in data if not np.isnan(preference)],
                          key=lambda item: -item[1])


    def maximum_preference_value(self):
        return self.max_pref


    def minimum_preference_value(self):
        return self.min_pref

    def users_count(self):

        return self._user_ids.size

    def items_count(self):
        return self._item_ids.size

    def items_from_user(self, user_id):
        preference = self.preferences_from_user(user_id)
        return [key for key, value in preference]

    def preferences_for_item(self, item_id, order_by_id=True):

        item_id_loc = np.where(self._item_ids == item_id)
        if not item_id_loc[0].size:
            raise ItemNotFoundError('Item not found')
        preference = self.index[:, item_id_loc]
        data = zip(self._user_ids, preference.flatten())
        if order_by_id:
            return [(user_id, preference) for user_id, preference in data if not np.isnan(preference)]

        else:
            return sorted([(user_id, preference) for user_id, preference in data if not np.isnan(preference)],
                          key=lambda user: -user[1])


    def preference_value(self, user_id, item_id):
        item_id_loc = np.where(self._item_ids == item_id)
        user_id_loc = np.where(self._user_ids == user_id)

        if not user_id_loc[0].size:
            raise UserNotFoundError('user_id in the model not found')

        if not item_id_loc[0].size:
            raise ItemNotFoundError('item_id in the model not found')

        return self.index[user_id_loc, item_id_loc].flatten()[0]


    def set_preference(self, user_id, item_id, value):


        user_id_loc = np.where(self._user_ids == user_id)
        if not user_id_loc[0].size:
            raise UserNotFoundError('user_id in the model not found')

        self.dataset[user_id][item_id] = value
        self.build_model()

    def remove_preference(self, user_id, item_id):

        user_id_loc = np.where(self._user_ids == user_id)
        item_id_loc = np.where(self._item_ids == item_id)

        if not user_id_loc[0].size:
            raise UserNotFoundError('user_id in the model not found')

        if not item_id_loc[0].size:
            raise ItemNotFoundError('item_id in the model not found')

        del self.dataset[user_id][item_id]
        self.build_model()

    def __repr__(self):
        return "<MatrixPreferenceDataModel (%d by %d)>" % (self.index.shape[0], self.index.shape[1])

    def _repr_matrix(self, matrix):
        s = ""
        cellWidth = 11
        shape = matrix.shape
        for i in range(shape[0]):
            for j in range(shape[1]):
                v = matrix[i, j]
                if np.isnan(v):
                    s += "---".center(cellWidth)
                else:
                    exp = np.log(abs(v))
                    if abs(exp) <= 4:
                        if exp < 0:
                            s += ("%9.6f" % v).ljust(cellWidth)
                        else:
                            s += ("%9.*f" % (6, v)).ljust(cellWidth)
                    else:
                        s += ("%9.2e" % v).ljust(cellWidth)
            s += "\n"
        return s[:-1]

    def __unicode__(self):

        matrix = self._repr_matrix(self.index[:20, :5])
        lines = matrix.split('\n')
        headers = [repr(self)[1:-1]]
        if self._item_ids.size:
            col_headers = [('%-8s' % unicode(item)[:8]) for item in self._item_ids[:5]]
            headers.append(' ' + ('   '.join(col_headers)))

        if self._user_ids.size:
            for (i, line) in enumerate(lines):
                lines[i] = ('%-8s' % unicode(self._user_ids[i])[:8]) + line
            for (i, line) in enumerate(headers):
                if i > 0:
                    headers[i] = ' ' * 8 + line
        lines = headers + lines
        if self.index.shape[1] > 5 and self.index.shape[0] > 0:
            lines[1] += ' ...'
        if self.index.shape[0] > 20:
            lines.append('...')

        return '\n'.join(line.rstrip() for line in lines)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def has_preference_values(self):
        return True