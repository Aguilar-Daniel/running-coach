from flask import jsonify


def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(err):
        return jsonify({"error": getattr(err, "description", "bad request")}), 400

    @app.errorhandler(401)
    def unauthorized(err):
        return jsonify({"error": getattr(err, "description", "unauthorized")}), 401

    @app.errorhandler(404)
    def not_found(err):
        return jsonify({"error": getattr(err, "description", "not found")}), 404

    @app.errorhandler(500)
    def server_error(err):
        return jsonify({"error": "internal server error"}), 500
