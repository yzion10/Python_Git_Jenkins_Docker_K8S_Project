# This rest_app.py defines routes with rest api for create, read, update, and delete user
# from/to the MySQL

from flask import Flask, request, jsonify, render_template
from db_connector import DBConnector
import os
import signal

host='devopsdb.cu3hwstmvfmq.eu-north-1.rds.amazonaws.com'
port=3306
user='admin'
password='oren123456'
database='test'
Err200 = 200
Err400 = 400
Err500 = 500

# initialize the DBConnector class
db = DBConnector(host,port,user,password,database)

# initialize the Flask (constructor)
app = Flask(__name__)

# 1 - POST
@app.route('/users/<user_id>', methods=['POST'])
def add_user(user_id):
    userName = request.json.get("user_name")
    if userName is None:
        return jsonify({'status': 'error', 'reason': 'there is no user_name'}), Err400

    if db.getUserName(user_id) is not None:
        return jsonify({'status': 'error', 'reason': 'id already exists'}), Err500

    db.addUser(user_id, userName)
    return jsonify({'status': 'ok', 'user_added': userName}), Err200

# 2 - GET
@app.route('/users/<user_id>', methods=['GET'])
def getUserName(user_id):
    userName = db.getUserName(user_id)
    if userName is None:
        return jsonify({'status': 'error', 'reason': 'no such id'}), Err500

    return jsonify({'status': 'ok', 'user_name': userName}), Err200

# 3 - PUT
@app.route('/users/<user_id>', methods=['PUT'])
def updateUserName(user_id):
    userName = request.json.get('user_name')
    if userName is None:
        return jsonify({'status': 'error', 'reason': 'there is no user_name'}), Err400

    if db.getUserName(user_id) is None:
        return jsonify({'status': 'error', 'reason': 'no such id'}), Err500

    db.updateUserName(user_id, userName)
    return jsonify({'status': 'ok', 'user_updated': userName}), Err200

# 4 - DELETE
@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    if db.getUserName(user_id) is None:
        return jsonify({'status': 'error', 'reason': 'no such id'}), Err500

    db.deleteUser(user_id)
    return jsonify({'status': 'ok', 'user_deleted': user_id}), Err200

# 5 - Stop the flask server
@app.route('/stop_server')
def stop_server():
    os.kill(os.getpid(), signal.CTRL_C_EVENT)
    return 'Server stopped'
    # return jsonify({'status': 'ok', 'message': 'Server stopped'}), Err200

# Extra
# route error handler for non-existing routes
# return page not found 404
@app.errorhandler(404)
def page_not_found(error):
    return render_template("PageNotFount.html")

# Run the Flask application
app.run(host='0.0.0.0', port=5000)

























