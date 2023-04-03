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

        return f(*args, **kwargs, current_user=current_user)
    return decorated


def access_to_exercise(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        exercise = mongo.exercises.find_one({
            '_id': ObjectId(kwargs['exercise_id']),
            'owner': kwargs['current_user']['_id']
        })
        if exercise is None:
            return {'message': 'No access to file!'}, 403
        return f(*args, **kwargs, exercise=exercise)
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
    files = request.files.getlist("files")
    body = json.loads(request.form["body"])

    # check if body is empty
    length_files = len(files)

    index_correct = "thumbnailIndex" in body and length_files > body['thumbnailIndex'] >= 0
    thumbnail_index = body['thumbnailIndex'] if index_correct else 0

    exercise_files = []
    for i in range(len(files)):
        file = files[i]
        content = file.read()
        file_name = file.filename

        img, points = transform_image(content)
        file_id = fs.put(img, filename=file_name)

        if i == thumbnail_index:
            first_frame = image_get_first_frame(img)
            thumbnail_id = fs.put(first_frame)

        exercise_files.append({
            'file_id': str(file_id),
            # 'points': points,
        })

    mongo.exercises.insert_one({
        'owner': current_user['_id'],
        'created': datetime.datetime.utcnow(),
        'name': body['name'],
        'type': body['type'],
        'thumbnail_id': str(thumbnail_id),
        'files': exercise_files
    })

    return {"message": "Upload of video was successful!"}, 300


@app.route('/exercises', methods=['GET'])
@token_required
def load_exercises(current_user):
    exercises = mongo.exercises.find({'owner': current_user['_id']})

    payload = []
    for exercise in exercises:
        byte_file = fs.get(ObjectId(exercise['thumbnail_id'])).read()

        payload.append({
            'id': str(exercise['_id']),
            'created': exercise['created'],
            'name': exercise['name'],
            'type': exercise['type'],
            'thumbnail': base64.b64encode(byte_file).decode(),
        })
    return {'data': payload}, 200


@app.route('/exercises/<exercise_id>', methods=['GET'])
@token_required
@access_to_exercise
def load_exercise(current_user, exercise_id, exercise):
    files = []
    for file in exercise['files']:
        byte_file = fs.get(ObjectId(file['file_id'])).read()
        content = base64.b64encode(byte_file).decode()

        files.append({
            'file': content
        })

    return {
        'data': {
            'name': exercise['name'],
            'type': exercise['type'],
            'files': files
        }
    }, 200


@app.route('/exercises/<exercise_id>', methods=['DELETE'])
@token_required
@access_to_exercise
def delete_upload(current_user, exercise_id, exercise):
    fs.delete(ObjectId(exercise['thumbnail_id']))
    for file in exercise['files']:
        fs.delete(ObjectId(file['file_id']))
    mongo.exercises.delete_one({'_id': ObjectId(exercise_id)})
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

        users.insert_one({
            'name': name,
            'password': hashpass
        })
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
        raise Exception('Invalid JWT token.')


if __name__ == '__main__':
    app.run(debug=True)
