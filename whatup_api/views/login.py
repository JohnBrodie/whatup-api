from flask import (
    abort, flash, g, redirect,
    render_template, request, jsonify,
    url_for,
)

from whatup_api.app import app
from whatup_api import models as m

from flask.ext.login import login_required, login_user, logout_user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST" and "username" in request.form and "password" in request.form:
        username = request.form["username"]
        password = request.form["password"]
        user = m.User.query.filter(m.User.alias == username).first()
        if user is None:
            return jsonify(error='Invalid username.'), 400
        if not user.check_password(password):
            return jsonify(error='Invalid password.'), 400
        remember = request.form.get("remember", "no") == "yes"
        if login_user(user, remember=remember):
            flash("Logged in!")
            return redirect(request.args.get("next") or request.url_root)
        else:
            return jsonify(error='Error logging in.'), 400
    return render_template("login.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'You have been signed out')
    return(redirect(url_for('login')))
