import os

from flask import request, abort, jsonify, redirect, g
from sqlalchemy.exc import IntegrityError
from flask.ext.login import login_required, current_user

from math import ceil

from whatup_api.app import app
from whatup_api import models as m
from whatup_api.helpers.app_helpers import (
    check_login,
    create_attachment_from_url,
    create_attachment_from_file
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
    user_subs = m.Subscription.query.filter(m.Subscription.user_id==user_id).all()
    return jsonify(objects=[i.serialize for i in user_subs]), 200

def isValidPassword(password):
    if not password: 
        return False
    if len(password) < app.config['MIN_PASSWORD_LENGTH']:
        return False
    return True

@app.route('/users', methods=['POST'])
@login_required
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
    page = request.args.get('page', 1)
    page_length = app.config['SUBS_PAGE_LENGTH']

    posts = set()

    user_id = current_user.id
    user_subs = m.Subscription.query.filter(m.Subscription.user_id==user_id).all()
    for sub in user_subs:
        if sub.tags:
            sub_posts = m.Post.query.join(m.Post.tags).filter(m.Tag.id.in_([s.id for s in sub.tags]))
        if sub.subscribee is not None:
            sub_posts = sub_posts.filter(m.Post.author == sub.subscribee)
        posts |= set(sub_posts.all())

    postlist = list(posts)
    postlist.sort(key=lambda x: x.created_at, reverse=True)
    postlist = postlist[page_length*(page-1):page_length*(page)]
    response = {}
    response['total_pages'] = int(ceil(len(postlist)/float(page_length)))
    response['num_results'] = len(postlist)
    response['page'] = page
    response['objects'] = [i.serialize for i in postlist]

    return jsonify(response), 200
