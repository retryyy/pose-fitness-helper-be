from flask import Flask, request
from flask_cors import CORS
from functools import wraps

import pymongo
import gridfs
from bson.objectid import ObjectId

import jwt
import bcrypt
import jwt
import datetime
import base64

from service import trim_video

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
    start = request.args.get('start')
    end = request.args.get('end')
    file = request.files["file"]

    file.save(file.filename)

    trim_video(file.filename, 'out.mp4', start, end)

    return {'message': 'All good'}, 200


@token_required
def upload_file(current_user):
    file = request.files["file"]

    content = file.read()
    file_name = file.filename

    file_id = fs.put(content, filename=file_name)

    mongo.users.update(
        {'_id': ObjectId(current_user['_id'])},
        {'$push': {
            'docs': {
                'file_id': str(file_id)
            }
        }}
    )


@app.route('/load', methods=['GET'])
@token_required
def load_file(current_user):
    docs = current_user['docs'] if 'docs' in current_user else []

    for doc in docs:
        byte_file = fs.get(ObjectId(doc['file'])).read()
        doc['file'] = base64.b64encode(byte_file).decode()
    return {'data': docs}, 200


@app.route('/login', methods=['POST'])
def login():
    users = mongo.users
    payload = request.json

    name = payload['name']
    login_user = users.find_one({'name': name})

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
