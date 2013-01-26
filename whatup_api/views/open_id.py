from flask import (
    flash, g, redirect, render_template,
    request, session, url_for,
)

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

    return render_template('login.html', next=open_id.get_next_url(),
                           error=open_id.fetch_error())


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
        flash(u'Successfully signed in')
        g.user = user
        return redirect(open_id.get_next_url())
    return redirect(url_for('create_profile', next=open_id.get_next_url(),
                            name=resp.fullname or resp.nickname,
                            email=resp.email))


@app.route('/create-profile', methods=['GET', 'POST'])
def create_profile():
    """If this is the user's first login, the create_or_login function
will redirect here so that the user can set up his profile.
"""
    if hasattr(g, 'user') and g.user is not None or 'openid' not in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        if not name:
            flash(u'Error: you have to provide a name')
        elif '@' not in email:
            flash(u'Error: you have to enter a valid email address')
        else:
            flash(u'Profile successfully created')
            #db_session.add(User(name, email, session['openid']))
            #db_session.commit()
            # TODO: check what fields we can get, modify user model
            # TODO: Expect ANY of these fields to be null!
            new_user = m.User(name=name, email=email, openid=session['openid'])
            m.db.session.add(new_user)
            # TODO: try/catch
            m.db.session.commit()

            return redirect(open_id.get_next_url())
    return render_template('create_profile.html', next_url=open_id.get_next_url())


@app.route('/logout')
def logout():
    session.pop('openid', None)
    flash(u'You have been signed out')
    return redirect(open_id.get_next_url())
