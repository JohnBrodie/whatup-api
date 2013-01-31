from flask import (
    abort, flash, g, redirect,
    render_template, request, session,
)
from flask_openid import COMMON_PROVIDERS

from whatup_api.app import app, open_id
from whatup_api import models as m


@app.route('/login', methods=['GET', 'POST'])
@open_id.loginhandler
def login():
    if hasattr(g, 'user') and g.user is not None:
        return redirect(open_id.get_next_url())
    if request.method == 'POST':
        oid = request.form.get('openid')
        if oid:
            return open_id.try_login(oid, ask_for=['email', 'fullname',
                                                   'nickname'])

    next_url = request.args.get('redir', open_id.get_next_url())
    return render_template(
        'login.html',
        next=next_url,
        error=open_id.fetch_error(),
        providers=COMMON_PROVIDERS,
    )


@open_id.after_login
def create_or_login(resp):
    """This is called when login with OpenID succeeded and it's not
necessary to figure out if this is the users's first login or not.
This function has to redirect otherwise the user will be presented
with a terrible URL which we certainly don't want.
"""
    session['openid'] = resp.identity_url
    user = m.User.query.filter_by(openid=resp.identity_url).first()
    if user is not None:
        # User exists in db, sign them in
        flash(u'Successfully signed in')
        g.user = user
        return redirect(open_id.get_next_url())

    nickname = None
    fullname = None
    email = None

    try:
        fullname = resp.fullname
        email = resp.email
    except AttributeError:
        flash('Name and Email needed from OpenID provider')
        abort(401)

    try:
        nickname = resp.nickname
    except AttributeError:
        pass

    new_user = m.User(
        name=fullname,
        email=email,
        openid=session['openid'],
        alias=nickname,
    )
    try:
        m.db.session.add(new_user)
        m.db.session.commit()
    except Exception:
        abort(401)

    return redirect(open_id.get_next_url())


@app.route('/logout')
def logout():
    session.pop('openid', None)
    flash(u'You have been signed out')
    return redirect(open_id.get_next_url())
