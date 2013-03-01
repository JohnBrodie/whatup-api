import os

from flask import request, abort, jsonify, redirect
from sqlalchemy.exc import IntegrityError

from whatup_api.app import app
from whatup_api import models as m
from whatup_api.helpers.app_helpers import (
    check_login,
    create_attachment_from_url,
    create_attachment_from_file
)


@app.route('/', methods=['GET'])
@app.route('/api', methods=['GET'])
def api_root():
    """Redirect to API docs."""
    return redirect('http://projectwhatup.us')
    #return 'TODO: Replace with API Docs'


@app.route('/check_login', methods=['GET'])
def is_logged_in():
    """Return true if user is logged in, else false."""
    is_logged_in = check_login()
    return jsonify(is_logged_in=is_logged_in)


@app.route('/attachments/<int:attachment_id>', methods=['DELETE'])
def delete_attachment(attachment_id):
    if not check_login():
        abort(401)

    attachment = m.Attachment.query.get(attachment_id)
    if attachment is None:
        return jsonify(error='There is no attachment with id ' + str(attachment_id)), 400

    upload_dir = app.config['ATTACHMENTS_DIR']
    filename = attachment.location
    try:
        os.remove('/'.join([upload_dir, filename]))
    except OSError:
        return jsonify(error='Could not find file'), 400

    try:
        m.db.session.delete(attachment)
        m.db.session.commit()
    except IntegrityError:
        abort(400)
    return jsonify(status='File deleted'), 200

@app.route('/upload', methods=['POST'])
def upload():
    """When a file is POSTed to this endpoint, it is given
    a random name and a new Attachment object is saved.

    """
    if not check_login():
        abort(401)

    if len(request.files):
        attachment = create_attachment_from_file(
            request.files['file'],
            app.config
        )
    elif 'url' in request.form:
        try:
            attachment = create_attachment_from_url(
                request.form['url'],
                app.config
            )
        except IOError:
            return jsonify(error='Failed to download file'), 400
        except ValueError:
            return jsonify(error='Invalid URL'), 400
    else:
        return jsonify(error='No files in request'), 400

    m.db.session.add(attachment)
    try:
        m.db.session.commit()
    except IntegrityError:
        abort(400)

    response = jsonify(
        id=attachment.id,
        created_at=str(attachment.created_at),
        modified_at=str(attachment.modified_at),
        user_id=attachment.user_id,
        name=attachment.name,
        location=attachment.location,
    )
    return response
