import os
from base64 import urlsafe_b64encode
from flask import request, abort, jsonify
from sqlalchemy.exc import IntegrityError

from whatup_api.app import app
from whatup_api import models as m


@app.route('/', methods=['GET'])
@app.route('/api', methods=['GET'])
def api_root():
    """Redirect to API docs."""
    return 'TODO: Replace with API Docs'


@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files['file']
    upload_dir = app.config['ATTACHMENTS_DIR']
    if not request.values.get('user'):
        abort(500)
    user_id = request.values['user']
    original_name = uploaded_file.filename.rpartition('/')[2]

    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    while True:
        filename = urlsafe_b64encode(os.urandom(30))
        try:
            f = open(upload_dir + '/' + filename)
            continue
        except IOError:
            f = open(upload_dir + '/' + filename, b'w')
            break
    uploaded_file.save(f)

    attachment = m.Attachment(user_id=user_id,
                              name=original_name,
                              location=filename)

    m.db.session.add(attachment)
    try:
        m.db.session.commit()
        response = jsonify(id=attachment.id,
                           created_at=str(attachment.created_at),
                           modified_at=str(attachment.modified_at),
                           user_id=attachment.user_id,
                           name=attachment.name,
                           location=attachment.location)
    except IntegrityError:
        abort(500)
    return response
