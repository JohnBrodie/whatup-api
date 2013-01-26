from flask import jsonify, redirect, url_for


def configure_error_handlers(app):

    @app.errorhandler(404)
    def return_not_found_json(e):
        return jsonify(error=e.message), 404

    @app.errorhandler(405)
    def return_method_now_allowed_json(e):
        return jsonify(error=e.message), 405

    @app.errorhandler(500)
    def return_bad_request_json(e):
        return jsonify(error='400 Bad Request'), 400

    @app.errorhandler(401)
    def return_login_redirect(e):
        return redirect(url_for('login'))
