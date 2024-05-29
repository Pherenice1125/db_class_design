# -*- coding: utf-8 -*-
"""
Created on Mon May 27 17:42:21 2024

@author: Pherenice
"""

import db_func
from db_Config import db_config
from flask import Flask, request, jsonify, make_response, render_template
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager


app=Flask(__name__)

# User表操作
@app.route('/users/login', methods=['POST'])
def user_login():
    json_data = request.get_json()
    code, priviliges = db_func.user_login(json_data, db_config)
    if code == 200:
        access_token = create_access_token(identity=json_data["username"])
        return make_response(jsonify({"access_token": access_token,"Priviliges": priviliges, "Message": "Login success"}), 200)
    if code == 400:
        return make_response(jsonify({"error": "Wrong username or password"}), 400)
    if code == 420:
        return make_response(jsonify({"error": "Unknown username or password"}), 400)
    
@app.route('/users/create', methods=['POST'])
@jwt_required()
def create_user():
    json_data = request.get_json()
    try:
        current_user = get_jwt_identity()
        db_func.user_add(json_data, db_config)
        return make_response(jsonify({"current_user":current_user, "Message":"Create Success"}), 200)
    except Exception as e:
        return make_response(jsonify({"current_user":current_user, "Error":"Create fail: "+str(e)}), 400)
    
@app.route('/users/delete', methods=['POST'])
@jwt_required()
def delete_user():
    json_data = request.get_json()
    try:
        current_user = get_jwt_identity()
        db_func.user_del(json_data, db_config)
        return make_response(jsonify({"current_user":current_user, "Message":"Delete Success"}), 200)
    except Exception as e:
        return make_response(jsonify({"current_user":current_user, "Error":"Delete fail: "+str(e)}), 400)


@app.route('/users/edit', methods=['POST'])
@jwt_required()
def edit_user():
    json_data = request.get_json()
    try:
        current_user = get_jwt_identity()
        db_func.user_update(json_data, db_config)
        return make_response(jsonify({"current_user":current_user, "Message":"Edit Success"}), 200)
    except Exception as e:
        return make_response(jsonify({"current_user":current_user, "Error":"Edit fail: "+str(e)}), 400)


@app.route('/users/getall', methods=['GET'])
@jwt_required()
def get_all_users():
    result = {}
    try:
        current_user = get_jwt_identity()
        result["data"] = db_func.user_getall(db_config)
        result["current_user"] = current_user
        return make_response(result, 200)
    except Exception as e:
        return make_response(jsonify({"current_user":current_user, "Error":"The user identity verification failed: "+str(e)}), 400)



# Materials表操作
@app.route("/matadd", methods=["POST"])
def mat_add():
    try:
        json_data = request.get_json()
        if 'file' in request.files:
            file = request.files['file']
        else:
            file = None
        db_func.add_mat(json_data, db_config, file)
        return make_response(jsonify({'message': 'Data successfully inserted into `mat`'}), 200)
    except Exception as e:
        return make_response(jsonify({'error': 'Failed to insert data into `mat`:' + str(e)}), 500)

@app.route("/matdel", methods=["POST"])
def mat_del():
    try:
        json_data = request.get_json()
        db_func.del_mat(json_data, db_config)     
        return make_response(jsonify({'message': 'Data successfully deleted.'}), 200)
    except Exception as e:
        return make_response(jsonify({'error': 'Data failed to deleted:' + str(e)}), 500)

@app.route("/matget", methods=["GET"])
def mat_get():
    try:
        rows = db_func.get_mat(db_config)      
        return make_response(jsonify({'message': 'Data get from `mat` successfully', 'value': rows}), 200)
    except Exception as e:
        return make_response(jsonify({'error': 'Data get unsuccessfully from `mat`:' + str(e)}), 500)
    
@app.route("/matupdate", methods=["POST"])
def mat_update():
    try:
        json_data = request.get_json()
        db_func.update_mat(json_data, db_config)
        return make_response(jsonify({'message': 'Data in `mat` updated successfully'}), 200)
    except Exception as e:
        return make_response(jsonify({'error': 'Data in `mat` updated unsuccessfully:' + str(e)}), 500)
if __name__ == "__main__":
    app.run(debug=False, host='127.0.0.1', port=9010)