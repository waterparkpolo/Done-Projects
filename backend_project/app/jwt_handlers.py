
from flask import jsonify

def register_jwt_error_handlers(jwt):
    @jwt.invalid_token_loader
    def invalid_token(msg):
        return jsonify(error="invalid_token", message=msg, status=401), 401

    @jwt.unauthorized_loader
    def missing_auth(msg):
        return jsonify(error="missing_authorization", message=msg, status=401), 401

    @jwt.expired_token_loader
    def expired_token(jwt_header, jwt_payload):
        return jsonify(error="token_expired", message="Token has expired.", status=401), 401

    @jwt.needs_fresh_token_loader
    def needs_fresh(jwt_header, jwt_payload):
        return jsonify(error="fresh_token_required", message="Fresh token required.", status=401), 401
