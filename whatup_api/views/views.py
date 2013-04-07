import os

from flask import request, abort, jsonify, redirect, g
from sqlalchemy.exc import IntegrityError
from flask.ext.login import login_required, current_user
from sqlalchemy import and_

from whatup_api.app import app
from whatup_api import models as m
from whatup_api.helpers.app_helpers import (
    admin_required,
    check_login,
    create_attachment_from_url,
    create_attachment_from_file,
    serialize_and_paginate,
)

from json import loads


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
@login_required
def delete_attachment(attachment_id):
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
@login_required
def upload():
    """When a file is POSTed to this endpoint, it is given
    a random name and a new Attachment object is saved.

    """
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

@app.route('/subscriptions', methods=['GET'])
@login_required
def subscriptions():
    user_id = current_user.id
    page = int(request.args.get('page', 1))
    user_subs = m.Subscription.query.filter(and_(m.Subscription.user_id==user_id, m.Subscription.is_deleted == False)).all()
    response = serialize_and_paginate(user_subs, app.config['PAGE_LENGTH'], page)
    return jsonify(response), 200

def isValidPassword(password):
    if not password:
        return False
    if len(password) < app.config['MIN_PASSWORD_LENGTH']:
        return False
    return True

@app.route('/users', methods=['POST'])
@login_required
@admin_required
def users():
    data = loads(request.data)
    username = data.get("name", None)
    password = data.get("password", None)
    if username is None:
        return jsonify(error='Invalid username'), 400
    numUsers = m.User.query.filter(m.User.name == username).count()
    if numUsers != 0:
        return jsonify(error='Username taken'), 400
    if password is None:
        return jsonify(error='No password provided'), 400
    if not isValidPassword(password):
        return jsonify(error='Invalid password'), 400
    user = m.User(name=username)
    user.set_password(password)
    m.db.session.add(user)
    try:
        m.db.session.commit()
    except IntegrityError:
        return jsonify(error='Could not add user'), 400
    response = jsonify(
        id=user.id,
        created_at=str(user.created_at),
        modified_at=str(user.modified_at),
        name=user.name,
    )
    return response, 201

@app.route('/subscribed', methods=['GET'])
@login_required
def subscribed():
    page = int(request.args.get('page', 1))
    page_length = app.config['PAGE_LENGTH']

    posts = set()

    user_id = current_user.id
    user_subs = m.Subscription.query.filter(and_(m.Subscription.user_id==user_id, m.Subscription.is_deleted == False)).all()
    for sub in user_subs:
        criteria = "true"
        for tag in sub.tags:
            criteria = and_(criteria, m.Post.tags.contains(tag))
        if sub.subscribee is not None:
            criteria = and_(criteria, m.Post.created_by_id == sub.subscribee.id)

        # if criteria is still "true", then no filters
        # were applied, and no posts should be returned
        if criteria == "true":
            criteria = "false"

        sub_posts = m.Post.query.filter(criteria).all()
        posts |= set(sub_posts)

    postlist = list(posts)
    response = serialize_and_paginate(postlist, page_length, page)
    return jsonify(response), 200

@app.route('/posts/<post_id>/revisions', methods=['GET'])
@login_required
def post_revisions(post_id):
    page = int(request.args.get('page', 1))
    page_length = app.config['PAGE_LENGTH']
    post = m.Post.query.get(post_id)
    if post is None:
        return jsonify(error='There is no post with id ' + str(post_id)), 400
    response = serialize_and_paginate(post.revisions, page_length, page)
    return jsonify(response), 200
