"""Monkey patch flask-restless delete method to toggle
    is_deleted on a model instead of deleting the row.

"""

from flask.ext.restless import views, search


def delete(self, instid):
    self._check_authentication()
    inst = self._get_by(instid)
    if inst is not None:
        inst.is_deleted = True
        self.session.commit()
    return views.jsonify_status_code(204)

views.API.delete = delete

def __init__(self, filters=None, limit=None, offset=None, order_by=None):
    """ Patch restless SearchParameters object to
    always exclude is_deleted rows.

    """
    self.filters = filters or []
    self.filters.append(search.Filter("is_deleted", "neq", 1))
    self.limit = limit
    self.offset = offset
    self.order_by = order_by or []

search.SearchParameters.__init__ = __init__
