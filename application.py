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
import os

from video.video_util import image_get_first_frame, trim_video
from pose_analyze.pose_analyzer import pose_analyze

app = Flask(__name__)
CORS(app)

client = pymongo.MongoClient(
    f'mongodb://{os.environ["MONGO_HOST"]}:{os.environ["MONGO_PORT"]}', 
    serverSelectionTimeoutMS=0
)
mongo = client.get_database(os.environ["DB_NAME"])
fs = gridfs.GridFS(mongo)

with open("exercises.json", "r") as read_file:
    config = json.load(read_file)

def mongo_check(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            client.server_info()
        except pymongo.errors.ServerSelectionTimeoutError:
            return {"message": "Error occured during the connection to database!"}, 500

        return f(*args, **kwargs)
    return decorated


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

        except jwt.PyJWTError as e:
            return {"message": str(e)}, 401
        except pymongo.errors.ConnectionFailure:
            return {"message": "Error occured during the connection to database!"}, 500
        except Exception as e:
            return {"message": str(e)}, 500

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
    exercise_type = request.args.get('exerciseType')
    file = request.files["file"]

    file_size = int(request.headers['Content-length'])/(1024 * 1024)
    if file_size > 40:
        return {"message": "File is too big! Maximum file size is 40MB"}, 413
    if file.content_type != 'video/mp4':
        return {"message": "Unsupported file extension! Only MP4 is accepted"}, 415

    trimmed_file, points = trim_video(
        file.read(), 
        start,
        end, 
        None if (exercise_type is None or exercise_type == 'undefined') else config[exercise_type]['points']
    )

    return {
        'message': 'Trim of video was successful!',
        'data': {
            'movement': base64.b64encode(trimmed_file).decode(),
            'points': points
        }
    }, 200


@app.route('/upload', methods=['POST'])
@token_required
def upload_exercise(current_user):
    try:
        files = request.files.getlist("files")
        body = json.loads(request.form["body"])
        all_points = body['points']
        length_files = len(files)
        name = body['name']

        if length_files == 0:
            return {"message": "No file was included!"}, 400
        if len(name) < 5:
            return {"message": "Exercise name needs to be minimum 5 characters!"}, 400

        index_correct = "thumbnailIndex" in body and length_files > body['thumbnailIndex'] >= 0
        thumbnail_index = body['thumbnailIndex'] if index_correct else 0

        exercise_files = []
        for i in range(len(files)):
            file = files[i]
            img = file.read()
            points = all_points[i]
            file_name = file.filename

            file_id = fs.put(img, filename=file_name)

            if i == thumbnail_index:
                first_frame = image_get_first_frame(img)
                thumbnail_id = fs.put(first_frame)

            view = file_name.split('.')[0]
            exercise_type = body['type']

            exercise_files.append({
                'file_id': file_id,
                'view': view,
                'analyze': pose_analyze(points,exercise_type, view),
                'points': points
            })

        _id = mongo.exercises.insert_one({
            'owner': current_user['_id'],
            'created': datetime.datetime.utcnow(),
            'name': name,
            'type': exercise_type,
            'thumbnail_id': thumbnail_id,
            'files': exercise_files
        })

        return {
            "message": "Upload of video was successful!",
            "data": str(_id.inserted_id)
        }, 200
    except KeyError as e:
        return {"message": "Request body error: " + str(e)}, 400


@app.route('/exercises/<exercise_id>/files', methods=['POST'])
@token_required
@access_to_exercise
def add_exercise_file(current_user, exercise_id, exercise):
    file = request.files["file"]
    body = json.loads(request.form["body"])

    img = file.read()
    points = body['points']
    view = body['view']
    file_name = file.filename

    file_id = fs.put(img, filename=file_name)

    mongo.exercises.update(
        {'_id': ObjectId(exercise_id)},
        {'$push': {
            'files': {
                'file_id': file_id,
                'view': view,
                'analyze': pose_analyze(points, exercise['type'], view),
                'points': points
            }
        }}
    )

    return {'message': 'File added to exercise'}, 200


@app.route('/exercises', methods=['GET'])
@token_required
def load_exercises(current_user):
    exercise_type = request.args.get('exerciseType')

    query = {
        'owner': current_user['_id'],
    }
    if exercise_type:
        query['type'] = exercise_type

    exercises = mongo.exercises\
        .find(query)\
        .sort("created", pymongo.DESCENDING)

    payload = []
    for exercise in exercises:
        byte_file = fs.get(exercise['thumbnail_id']).read()

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
        byte_file = fs.get(file['file_id']).read()
        content = base64.b64encode(byte_file).decode()

        files.append({
            'file_id': str(file['file_id']),
            'file': content,
            'view': file['view'],
            'analyze': file['analyze']
        })

    return {
        'data': {
            'name': exercise['name'],
            'type': exercise['type'],
            'created': exercise['created'],
            'files': files
        }
    }, 200


@app.route('/exercises/<exercise_id>', methods=['DELETE'])
@token_required
@access_to_exercise
def delete_exercise(current_user, exercise_id, exercise):
    fs.delete(exercise['thumbnail_id'])
    for file in exercise['files']:
        fs.delete(file['file_id'])
    mongo.exercises.delete_one({'_id': ObjectId(exercise_id)})
    return {'message': 'Exercise deleted'}, 200


@app.route('/exercises/<exercise_id>/files/<file_id>', methods=['DELETE'])
@token_required
@access_to_exercise
def delete_exercise_file(current_user, exercise_id, file_id, exercise):
    fs.delete(ObjectId(file_id))
    mongo.exercises.update(
        {'_id': ObjectId(exercise_id)},
        {'$pull': {
            'files': {
                'file_id': ObjectId(file_id),
            }
        }}
    )
    return {'message': 'File for exercise deleted'}, 200


@app.route('/config/posetypes', methods=['GET'])
def load_pose_types():
    return {
        'data': {exercise: config[exercise]['views'] for exercise in config}
    }, 200


@app.route('/benchmark/<exercise_type>/<view>', methods=['GET'])
def get_benchmark_video(exercise_type, view):
    with open(f"./benchmark_exercises/gif/{exercise_type}-{view}.gif", "rb") as image_file:
        image_data = image_file.read()

    encoded_data = base64.b64encode(image_data)
    base64_string = encoded_data.decode("utf-8")

    return {'data': base64_string}, 200


@app.route('/exercises/<exercise_id>/test/<idx>', methods=['GET'])
@token_required
@access_to_exercise
def test(current_user, exercise_id, idx, exercise):
    spec_exercise = exercise['files'][int(idx)]

    result = pose_analyze(spec_exercise['points'],
                          exercise['type'],
                          spec_exercise['view'])

    return {'data': result}, 200


@app.route('/login', methods=['POST'])
@mongo_check
def login():
    payload = request.json

    name = payload['name']
    login_user = mongo.users.find_one({'name': name})

    if login_user:
        if bcrypt.checkpw(payload['password'].encode('utf-8'), login_user['password']):
            return {
                'message': 'User logged in!',
                'data': create_token(str(login_user['_id']), name)
            }, 200
    return {'message': 'Invalid login credentials'}, 403


@app.route('/register', methods=['POST'])
@mongo_check
def register():
    users = mongo.users
    payload = request.json
    name = payload['name']
    password = payload['password']

    if len(name) < 5:
        return {"message": "Username needs to be minimum 5 characters!"}, 400
    if len(password) < 5:
        return {"message": "Password needs to be minimum 5 characters!"}, 400
    
    
    existing_user = users.find_one({'name': name})

    if existing_user is None:
        hashpass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        user = users.insert_one({
            'name': name,
            'password': hashpass
        })
        user_id = str(user.inserted_id)
        return {
            'message': f'User {name} created successfully!',
            'data': create_token(user_id, name)
        }, 200

    return {'message': f'User {name} already exists!'}, 409


@app.route('/ping', methods=['GET'])
@token_required
def ping(current_user):
    return {'message': 'Works'}, 200


@staticmethod
def create_token(user_id, name):
    return jwt.encode(
        {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=1000),
            'iat': datetime.datetime.utcnow(),
            'user_id': user_id,
            'name': name
        },
        os.environ["SECRET_KEY"],
        algorithm='HS256'
    )


@staticmethod
def decode_auth_token(token):
    try:
        return jwt.decode(
            token,
            os.environ["SECRET_KEY"],
            algorithms='HS256'
        )
    except jwt.ExpiredSignatureError:
        raise jwt.PyJWTError('JWT signature expired.')
    except jwt.InvalidTokenError as e:
        raise jwt.PyJWTError('Invalid JWT token.')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
