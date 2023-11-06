from flask import jsonify
from models import db

def get_model_by_id(model, model_id):
    instance = db.session.get(model, model_id)
    if not instance:
        return None
    return instance

def error_response(message, status_code):
    response = {"error": message}
    return jsonify(response), status_code

def commit_to_db(data):
    db.session.add(data)
    db.session.commit()