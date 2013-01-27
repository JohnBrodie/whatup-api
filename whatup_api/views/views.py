import os
from base64 import urlsafe_b64encode
from flask import request, abort, jsonify, g
from sqlalchemy.exc import IntegrityError

from whatup_api.app import app
from whatup_api import models as m
from whatup_api.helpers.app_helpers import check_login


@app.route('/', methods=['GET'])
@app.route('/api', methods=['GET'])
def api_root():
    """Redirect to API docs."""
    return 'TODO: Replace with API Docs'


@app.route('/upload', methods=['POST'])
def upload():
    """When a file is POSTed to this endpoint, it is given
    a random name and a new Attachment object is saved.

    """
    if not check_login():
        abort(401)

    if not len(request.files):
        return jsonify(error='No files in request'), 400

    uploaded_file = request.files['file']
    upload_dir = app.config['ATTACHMENTS_DIR']

    user_id = g.user.id
    original_name = uploaded_file.filename.rpartition('/')[2]

    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    while True:
        filename = urlsafe_b64encode(os.urandom(30))
        try:
            f = open('/'.join([upload_dir, filename]))
            continue
        except IOError:
            f = open('/'.join([upload_dir, filename]), b'w')
            break
    uploaded_file.save(f)

    attachment = m.Attachment(
        user_id=user_id,
        name=original_name,
        location=filename,
    )

    m.db.session.add(attachment)
    try:
        m.db.session.commit()
    except IntegrityError:
        abort(400)

    response = jsonify(
        id=attachment.id,
        created_at=str(attachment.created_at),
        modified_at=str(attachment.modified_at),
        user_id=user_id,
        name=attachment.name,
        location=attachment.location,
    )
    return response
