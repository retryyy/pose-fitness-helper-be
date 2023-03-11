from flask import Flask, request
from flask_cors import CORS
from functools import wraps
import pymongo
import jwt
import bcrypt
import uuid
import jwt
import datetime

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'key'

# client = pymongo.MongoClient('mongodb+srv://username:password@cluster0-xth9g.mongodb.net/Richard?retryWrites=true&w=majority')
client = pymongo.MongoClient('localhost', 27017)
mongo = client.get_database('pose-fitness-helper')


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
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=1),
                        'iat': datetime.datetime.utcnow(),
                        'user_id': login_user['_id'],
                        'name': name
                    },
                    app.config.get('SECRET_KEY'),
                    algorithm='HS256'
                )
            }, 200

    return {'messgae': 'Invalid login credentials'}, 401


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
            '_id': uuid.uuid4().hex,
            'name': name,
            'password': hashpass
        }

        users.insert(user)
        return {'message': f'User {name} created successfully!'}, 200

    return {'message': f'User {name} already exists!'}, 409


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        else:
            return {"message": "Authentication token is missing!"}, 401

        try:
            print(token)
            data = decode_auth_token(token)
            current_user = mongo.users.find_one({'name': data['name']})

            if current_user is None:
                return {"message": "User not found!"}, 401
        except Exception as e:
            return {"message": str(e)}, 500

        return f(current_user, *args, **kwargs)
    return decorated


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


@app.route('/info', methods=['GET'])
@token_required
def info(current_user):
    return 'magic'


if __name__ == '__main__':
    app.run(debug=True)
