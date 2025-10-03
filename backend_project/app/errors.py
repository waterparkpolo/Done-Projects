
from flask import jsonify
from werkzeug.exceptions import HTTPException

def _json_error(message, status, code):
    return jsonify(error=code, message=message, status=status), status

def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(e):
        return _json_error("Bad request", 400, "bad_request")

    @app.errorhandler(401)
    def unauthorized(e):
        return _json_error("Unauthorized", 401, "unauthorized")

    @app.errorhandler(403)
    def forbidden(e):
        return _json_error("Forbidden", 403, "forbidden")

    @app.errorhandler(404)
    def not_found(e):
        return _json_error("Not found", 404, "not_found")

    @app.errorhandler(405)
    def method_not_allowed(e):
        return _json_error("Method not allowed", 405, "method_not_allowed")

    @app.errorhandler(422)
    def validation_error(e):
        # If you attach field errors, you can also put them under "detail"
        return _json_error("Validation failed", 422, "validation_error")

    @app.errorhandler(Exception)
    def internal_error(e):
        # Preserve HTTPExceptions with their original codes
        if isinstance(e, HTTPException):
            code = (e.name or "HTTPException").lower().replace(" ", "_")
            return _json_error(e.description or "HTTP error", e.code or 500, code)
        app.logger.exception(e)
        return _json_error("Internal server error", 500, "internal_error")
