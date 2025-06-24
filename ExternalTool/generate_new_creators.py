from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
from faker import Faker
from pymongo import MongoClient
import names
import random
import uuid
from datetime import datetime
from bson.json_util import dumps
import os
from pymongo import ASCENDING


mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/db_creators')
client = MongoClient(mongo_uri)
db = client.get_default_database()
collection = db.resume_creators_info

app = Flask(__name__)
swagger = Swagger(app)

fake = Faker('pt_BR')

CONTENT_TYPES = [
    'adult', 'sports', 'cooking', 'music', 'gaming', 'fitness', 'travel',
    'fashion', 'education', 'comedy', 'art', 'lifestyle', 'technology',
    'photography', 'beauty'
]

def generate_creator_name():
    adjective = ['Sexy', 'Cool', 'Hot', 'Mystic', 'Crazy', 'Sweet', 'Cute', 'Epic', 'Funky', 'Charming', 'Wild', 'Glam', 'Vivid', 'Bold', 'Daring', 'Fierce', 'Gorgeous', 'Radiant', 'Sassy', 'Trendy']
    names_list = ['Luna', 'Leo', 'Dark', 'Bella', 'Gabi', 'Thor', 'Neko', 'Max', 'Roxy', 'Jade', 'Kira', 'Nova', 'Milo', 'Zoe', 'Finn', 'Sky', 'Ace', 'Luna', 'Rex', 'Jax', 'Mia', 'Koda', 'Sage', 'Raven', 'Echo', 'Blaze', 'Storm', 'Faye', 'Juno', 'Zara', 'Gabi', 'Nina', 'Iza']
    numbers = str(random.randint(10, 9999))
    return random.choice(adjective) + random.choice(names_list) + numbers

def create_user():
    now = datetime.utcnow().isoformat() + "Z"
    return {
        "creatorName": generate_creator_name(),
        "realName": names.get_full_name(),
        "clientId": str(uuid.uuid4()),
        "totalFollowers": random.randint(100, 500000),
        "contentType": random.choice(CONTENT_TYPES),
        "revenue": round(random.uniform(100.0, 100000.0), 2),
        "email": fake.email(),
        "documentId": fake.cpf(),
        "isProcessed": False,
        "createdAt": now,
        "updatedAt": now
    }

@app.route('/creators', methods=['POST'])
@swag_from({
    'tags': ['Creators'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'size': {
                        'type': 'string',
                        'enum': ['small', 'medium', 'large'],
                        'example': 'small',
                        'description': 'Size of batch to generate (small=500, medium=5000, large=10000)'
                    }
                },
                'required': ['size']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Content creators generated',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'size': {'type': 'string'}
                }
            }
        },
        400: {'description': 'Invalid input'}
    }
})
def create_creators():
    data = request.get_json()
    if not data or 'size' not in data:
        return jsonify({"error": "Missing 'size' in JSON body. Use 'small', 'medium' or 'large'."}), 400

    size = data['size'].lower()
    size_map = {
        'small': 500,
        'medium': 5000,
        'large': 10000
    }

    quantity = size_map.get(size)
    if quantity is None:
        return jsonify({"error": "Invalid size. Use 'small', 'medium' or 'large'."}), 400

    users = [create_user() for _ in range(quantity)]
    collection.insert_many(users)

    return jsonify({
        "message": f"{quantity} content creators generated and saved to MongoDB.",
        "size": size
    }), 201

@app.route('/creators', methods=['GET'])
@swag_from({
    'tags': ['Creators'],
    'parameters': [
        {
            'name': 'page',
            'in': 'query',
            'type': 'integer',
            'default': 1,
            'required': False,
            'description': 'Page number for pagination'
        },
        {
            'name': 'per_page',
            'in': 'query',
            'type': 'integer',
            'default': 100,
            'required': False,
            'description': 'Number of items per page (max 1000)'
        }
    ],
    'responses': {
        200: {
            'description': 'List of content creators',
            'schema': {
                'type': 'array',
                'items': {'type': 'object'}
            }
        },
        400: {'description': 'Invalid parameters'}
    }
})
def list_creators():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 100))
    except ValueError:
        return jsonify({"error": "page and per_page must be integers."}), 400

    if page < 1 or per_page < 1 or per_page > 1000:
        return jsonify({"error": "page and per_page must be positive, per_page max 1000."}), 400

    skip = (page - 1) * per_page
    cursor = collection.find().skip(skip).limit(per_page)
    results = list(cursor)
    return dumps(results), 200, {'Content-Type': 'application/json'}

@app.route('/creators', methods=['DELETE'])
@swag_from({
    'tags': ['Creators'],
    'responses': {
        200: {
            'description': 'Deleted content creators',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        }
    }
})
def delete_creators():
    result = collection.delete_many({})
    return jsonify({"message": f"Deleted {result.deleted_count} creators from MongoDB."}), 200

@app.route('/configurate_indexes', methods=['POST'])
@swag_from({
    'tags': ['Indexes'],
    'responses': {
        200: {
            'description': 'Indexes created',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'created_indexes': {
                        'type': 'array',
                        'items': {'type': 'string'}
                    }
                }
            }
        }
    }
})
def configurate_mongo_indexes():
    indexes = []

    idx1 = collection.create_index(
        [("createdAt", ASCENDING), ("clientId", ASCENDING)],
        name="idx_createdAt_clientId"
    )
    indexes.append(idx1)

    idx2 = collection.create_index(
        [("updatedAt", ASCENDING), ("clientId", ASCENDING)],
        name="idx_updatedAt_clientId"
    )
    indexes.append(idx2)

    idx3 = collection.create_index(
        [("contentType", ASCENDING), ("createdAt", ASCENDING)],
        name="idx_contentType_createdAt"
    )
    indexes.append(idx3)

    return jsonify({
        "message": "Indexes created successfully.",
        "created_indexes": indexes
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
