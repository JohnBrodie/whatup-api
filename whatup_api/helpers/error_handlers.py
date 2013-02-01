from flask import jsonify


def configure_error_handlers(app):

    @app.errorhandler(401)
    def return_unauthorized(e):
        return jsonify(url='/login'), 401

    @app.errorhandler(404)
    def return_not_found_json(e):
        return jsonify(error=e.message), 404

    @app.errorhandler(405)
    def return_method_not_allowed_json(e):
        return jsonify(error=e.message), 405

    @app.errorhandler(500)
    def return_bad_request_json(e):
        return jsonify(error='400 Bad Request'), 400
