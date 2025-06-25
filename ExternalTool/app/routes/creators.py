
from flask import Blueprint, request, jsonify
from flasgger import swag_from
from marshmallow import ValidationError
from app.services.creator_service import generate_creators, list_creators, delete_all_creators, create_indexes
from app.schemas.creator_schema import CreatorBatchRequestSchema
from bson.json_util import dumps

creators_bp = Blueprint('creators', __name__)

@creators_bp.route('/creators', methods=['POST'])
@swag_from({
    'tags': ['Creators'],
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'schema': {
            'type': 'object',
            'properties': {
                'size': {
                    'type': 'string',
                    'enum': ['small', 'medium', 'large'],
                    'example': 'small',
                    'description': 'Tamanho do lote a ser criado'
                }
            },
            'required': ['size']
        }
    }],
    'responses': {
        201: {'description': 'Criadores gerados'},
        400: {'description': 'Erro de validação'}
    }
})
def create_creators():
    try:
        data = request.get_json()
        CreatorBatchRequestSchema().load(data)
        count = generate_creators(data['size'])
        return jsonify({"message": f"{count} content creators generated.", "size": data['size']}), 201
    except ValidationError as ve:
        return jsonify({"error": ve.messages}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@creators_bp.route('/creators', methods=['GET'])
@swag_from({
    'tags': ['Creators'],
    'parameters': [
        {'name': 'page', 'in': 'query', 'type': 'integer', 'default': 1},
        {'name': 'per_page', 'in': 'query', 'type': 'integer', 'default': 100}
    ],
    'responses': {200: {'description': 'List of creators'}}
})
def get_creators():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 100))
        if page < 1 or per_page < 1 or per_page > 1000:
            raise ValueError("Invalid pagination values.")
        creators = list_creators(page, per_page)
        return dumps(creators), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@creators_bp.route('/creators', methods=['DELETE'])
@swag_from({
    'tags': ['Creators'],
    'responses': {
        200: {'description': 'Deleted all creators'}
    }
})
def remove_creators():
    count = delete_all_creators()
    return jsonify({"message": f"Deleted {count} creators from MongoDB."}), 200

@creators_bp.route('/configurate-indexes', methods=['POST'])
@swag_from({
    'tags': ['Indexes'],
    'responses': {
        200: {'description': 'Indexes created'}
    }
})
def configure_indexes():
    idx = create_indexes()
    return jsonify({"message": "Indexes created successfully.", "created-indexes": idx}), 200
