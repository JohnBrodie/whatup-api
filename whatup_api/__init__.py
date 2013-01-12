"""Monkey patch flask-restless delete method to toggle
    is_deleted on a model instead of deleting the row.

"""

from flask.ext.restless import views


def delete(self, instid):
    self._check_authentication()
    inst = self._get_by(instid)
    if inst is not None:
        inst.is_deleted = True
        self.session.commit()
    return views.jsonify_status_code(204)

views.API.delete = delete
