from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret key"
app.config["MONGO_URI"] = "mongodb://localhost:27017/users"
mongo = PyMongo(app)


# 'GET' = Returns a list of all users

@app.route('/GET/users', methods=['GET'])
def find_all_users():
    users = mongo.db.user.find()
    resp = dumps(users)
    return resp

# 'GET/<id>' = Returns the user the specified ID

@app.route('/GET/users/<id>', methods=['GET'])
def find_user_by_id(id):
    user = mongo.db.user.find_one({'_id': ObjectId(id)})
    resp = dumps(user)
    return resp


# 'POST' = Creates a new user with the specified data

@app.route('/POST/users', methods=['POST'])
def add_user():
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _password = _json['pwd']

    # validate the received values

    if _name and _email and _password and request.method == 'POST':
        # do not save password as a plain text
        _hashed_password = generate_password_hash(_password)
        # save details
        id = mongo.db.user.insert_one({'name': _name, 'email': _email, 'pwd': _hashed_password})
        resp = jsonify('User added successfully!')
        resp.status_code = 200
        return resp
    else:
        return not_found()


# 'PUT' = updates the user with the specified id with the new data

@app.route('/PUT/users/<id>', methods=['PUT'])
def update_user_by_id(id):
    _json = request.json
    _id = id
    _name = _json['name']
    _email = _json['email']
    _password = _json['pwd']

    if _name and _email and _password and request.method == 'PUT':
        # do not save password as a plain text
        _hashed_password = generate_password_hash(_password)
        # save details
        mongo.db.user.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'name': _name, 'email': _email, 'pwd': _hashed_password}})
        resp = jsonify('User updated successfully!')
        resp.status_code = 200
        return resp

# 'DELETE' = deletes the user with the specified id

@app.route('/DELETE/users/<id>', methods=['DELETE'])
def delete_user_by_id(id):
    user = mongo.db.user.delete_one({'_id': ObjectId(id)})
    resp = jsonify('user deleted successfully!')
    resp.status_code = 200
    return resp

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


if __name__ == "__main__":
    app.run(port=80, debug=True)


