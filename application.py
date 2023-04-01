from flask import Flask, request
from flask_cors import CORS
from functools import wraps

import pymongo
import gridfs
from bson.objectid import ObjectId

import jwt
import bcrypt
import datetime
import base64
import json

from util import image_get_first_frame, transform_image, trim_video

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'key'

# client = pymongo.MongoClient('mongodb+srv://username:password@cluster0-xth9g.mongodb.net/Richard?retryWrites=true&w=majority')
client = pymongo.MongoClient('localhost', 27017)
mongo = client.get_database('pose-fitness-helper')
fs = gridfs.GridFS(mongo)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        request.files
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        else:
            return {"message": "Authentication token is missing!"}, 401

        try:
            data = decode_auth_token(token)
            current_user = mongo.users.find_one(
                {'_id': ObjectId(data['user_id'])})

            if current_user is None:
                return {"message": "User not found!"}, 401
        except Exception as e:
            return {"message": str(e)}, 401

        return f(current_user, *args, **kwargs)
    return decorated


@app.route('/trim', methods=['POST'])
@token_required
def trim_file(current_user):
    start = float(request.args.get('start'))
    end = float(request.args.get('end'))
    file = request.files["file"]

    trimmed_file = trim_video(file.read(), start, end)

    return {
        'message': 'Trim of video was successful!',
        'data': base64.b64encode(trimmed_file).decode()
    }, 200


@app.route('/upload', methods=['POST'])
@token_required
def upload_file(current_user):
    file = request.files["file"]

    # check if body is empty
    body = json.loads(request.form["body"])

    content = file.read()
    file_name = file.filename

    img, points = transform_image(content)

    file_id = fs.put(img, filename=file_name)

    first_frame = image_get_first_frame(img)
    thumbnail_id = fs.put(first_frame)

    mongo.users.update(
        {'_id': ObjectId(current_user['_id'])},
        {'$push': {
            'docs': {
                'file_id': str(file_id),
                'created': datetime.datetime.utcnow(),
                'thumbnail_id': str(thumbnail_id),
                'name': body['name'],
                'type': body['type'],
                'points': points,
            }
        }}
    )

    return {"message": "Upload of video was successful!"}, 300


@app.route('/load', methods=['GET'])
@token_required
def load_uploads(current_user):
    docs = current_user['docs'] if 'docs' in current_user else []

    for doc in docs:
        byte_file = fs.get(ObjectId(doc['thumbnail_id'])).read()
        doc['thumbnail'] = base64.b64encode(byte_file).decode()
    return {'data': docs}, 200


@app.route('/load/<file_id>', methods=['GET'])
@token_required
def load_upload(current_user, file_id):
    if not access_to_file(current_user, file_id):
        return {'message': 'No access to file!'}, 403

    doc = get_doc_by_fileid(current_user, file_id)

    byte_file = fs.get(ObjectId(file_id)).read()

    return {
        'data': {
            'file': base64.b64encode(byte_file).decode(),
            'name': doc["name"],
            'type': doc["type"]
        }
    }, 200


@app.route('/delete/<file_id>', methods=['DELETE'])
@token_required
def delete_upload(current_user, file_id):
    if not access_to_file(current_user, file_id):
        return {'message': 'No access to file!'}, 403

    doc = get_doc_by_fileid(current_user, file_id)

    fs.delete(ObjectId(file_id))
    fs.delete(ObjectId(doc['thumbnail_id']))

    mongo.users.update(
        {'_id': ObjectId(current_user['_id'])},
        {'$pull': {
            'docs': {
                'file_id': file_id,
            }
        }}
    )
    return {'message': 'File deleted'}, 200


@app.route('/login', methods=['POST'])
def login():
    payload = request.json

    name = payload['name']
    login_user = mongo.users.find_one({'name': name})

    if login_user:
        if bcrypt.checkpw(payload['password'].encode('utf-8'), login_user['password']):
            return {
                'message': 'User created!',
                'data': jwt.encode(
                    {
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=100),
                        'iat': datetime.datetime.utcnow(),
                        'user_id': str(login_user['_id']),
                        'name': name
                    },
                    app.config.get('SECRET_KEY'),
                    algorithm='HS256'
                )
            }, 200

    return {'message': 'Invalid login credentials'}, 401


@app.route('/register', methods=['POST'])
def register():
    users = mongo.users
    payload = request.json

    name = payload['name']
    existing_user = users.find_one({'name': name})

    if existing_user is None:
        hashpass = bcrypt.hashpw(
            payload['password'].encode('utf-8'), bcrypt.gensalt())

        user = {
            'name': name,
            'password': hashpass
        }

        users.insert_one(user)
        return {'message': f'User {name} created successfully!'}, 200

    return {'message': f'User {name} already exists!'}, 409


@staticmethod
def get_doc_by_fileid(current_user, file_id):
    return next((doc for doc in current_user['docs'] if doc['file_id'] == file_id), None)


@staticmethod
def access_to_file(current_user, file_id):
    for doc in current_user['docs']:
        if doc['file_id'] == file_id:
            return True
    return False


@staticmethod
def decode_auth_token(token):
    try:
        return jwt.decode(
            token,
            app.config.get('SECRET_KEY'),
            algorithms='HS256'
        )
    except jwt.ExpiredSignatureError:
        raise Exception('JWT signature expired.')
    except jwt.InvalidTokenError as e:
        print(e)
        raise Exception('Invalid JWT token.')


if __name__ == '__main__':
    app.run(debug=True)
