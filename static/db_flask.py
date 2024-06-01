# -*- coding: utf-8 -*-
"""
Created on Mon May 27 17:42:21 2024

@author: Pherenice
"""

import db_func
from db_Config import db_config
from flask_cors import CORS
from flask import Flask, request, jsonify, make_response, render_template
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager


app=Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # 设置用于加密 JWT 的密钥
jwt = JWTManager(app)  


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
@app.route("/mat/add", methods=["POST"])
def mat_add():
    try:
        json_data = request.get_json()
        db_func.add_mat(json_data, db_config)
        return make_response(jsonify({'message': 'Data successfully inserted into `mat`'}), 200)
    except Exception as e:
        return make_response(jsonify({'error': 'Failed to insert data into `mat`:' + str(e)}), 500)

@app.route("/mat/del", methods=["POST"])
def mat_del():
    try:
        json_data = request.get_json()
        db_func.del_mat(json_data, db_config)     
        return make_response(jsonify({'message': 'Data successfully deleted.'}), 200)
    except Exception as e:
        return make_response(jsonify({'error': 'Data failed to deleted:' + str(e)}), 500)

@app.route("/mat/getone", methods=["POST"])
def mat_get_one():
    try:
        json_data = request.get_json()
        rows = db_func.get_mat_one(json_data, db_config)      
        return make_response(jsonify({'message': 'Data get from `mat` successfully', 'value': rows}), 200)
    except Exception as e:
        return make_response(jsonify({'error': 'Data get unsuccessfully from `mat`:' + str(e)}), 500)

@app.route("/mat/getall", methods=["GET"])
def mat_get_all():
    try:
        rows = db_func.get_mat_all(db_config)      
        return make_response(jsonify({'message': 'Data get from `mat` successfully', 'value': rows}), 200)
    except Exception as e:
        return make_response(jsonify({'error': 'Data get unsuccessfully from `mat`:' + str(e)}), 500)
    
@app.route("/mat/update", methods=["POST"])
def mat_update():
    try:
        json_data = request.get_json()
        db_func.update_mat(json_data, db_config)
        return make_response(jsonify({'message': 'Data in `mat` updated successfully'}), 200)
    except Exception as e:
        return make_response(jsonify({'error': 'Data in `mat` updated unsuccessfully:' + str(e)}), 500)
    
    
    
#Ingredients配方表操作
@app.route("/ingre/add", methods=["POST"])
def ingre_add():
    json_data = request.get_json()
    if json_data:
        try:
            db_func.add_ingre(json_data, db_config)
            return make_response(jsonify({'message': 'Data added into `ingre` successfully'}), 200)
        except Exception as e:
            return make_response(jsonify({'error': 'Data inserted failed：' + str(e)}), 500)
    else:
        return make_response(jsonify({'error': '未收到有效的json数据(add_ingre)：'}), 400)

@app.route("/ingre/del", methods=["POST"])
def ingre_del():
    try:
        json_data = request.get_json()
        db_func.del_ingre(json_data, db_config)
        
        return make_response(jsonify({'message': 'Data deleted from `ingre` successfully'}), 200)
    except Exception as e:
        return make_response(jsonify({'error': 'Data deleted from `ingre` unsuccsessfully:' + str(e)}), 500)

@app.route("/ingre/get", methods=["GET"])
def ingre_get():
    try:
        rows = db_func.get_ingre_all(db_config)        
        return make_response(jsonify({'message': 'Data get from `ingre` successfully', 'value': rows}), 200)
    except Exception as e:
        return make_response(jsonify({'error': 'Data get from `ingre` unsuccessfully:' + str(e)}), 500)

@app.route("/ingre/update", methods=["POST"])
def ingre_update():
    try:
        json_data = request.get_json()
        db_func.update_ingre(json_data, db_config)    
        return make_response(jsonify({'message': 'Data update in `ingre` successfully'}), 200)
    except Exception as d:
        return make_response(jsonify({'error': 'Data update in `ingre` unsuccessfully:' + str(d)}), 500)



#I_M_Midium中间表操作
@app.route("/gmfi", methods=['POST'])
def gmfi():
    try:
        json_data = request.get_json()
        rows = db_func.getall_mat_for_ingre(json_data, db_config)
        return make_response(jsonify({'message': 'Get all mat from single ingre successfully', 'value': rows}), 200)
    except Exception as e:
        return make_response(jsonify({'error': 'Get all mat from single ingre unsuccessfully:' + str(e)}), 500)



#efed实验燃素数据表操作
@app.route("/efed/addAndUpdate", methods=['POST'])
def efed_add_and_update():
    json_data = request.get_json()
    
    if json_data:
        try:
            db_func.add_efed(json_data, db_config)
            return make_response(jsonify({'message': 'Data successfully inserted into `efed`'}), 200)
        except Exception as e:
            return make_response(jsonify({'error': 'Data unsuccessfully inserted data into `efed`:' + str(e)}), 500)
    else:
        return make_response(jsonify({'error': 'Invalid json data(efed_add).'}), 400)
    
@app.route("/efed_del", methods=['POST'])
def efed_del():
    json_data = request.get_json()
    try:
        db_func.del_efed(json_data, db_config)
        return make_response(jsonify({'message': 'Data successfully deleted from `efed`'}), 200)
    except Exception as e:
        return make_response(jsonify({'error': 'Data unsuccessfully deleted from `efed`:' + str(e)}), 500)
    
@app.route("/efed_get", methods=['POST'])
def efed_get():
    try:
        json_data = request.get_json()
        rows = db_func.get_efed(json_data, db_config)   
        return make_response(jsonify({'message': 'Data successfully get from `efed`', 'value': rows}), 200)
    except Exception as e:
        return make_response(jsonify({'error': 'Data unsuccessfully get from `efed`:' + str(e)}), 500)

    
@app.route("/efedget_all", methods=['GET'])
def efed_get_all():
    try:
        rows = db_func.getall_efed_data_as_json(db_config)
        return make_response(jsonify({'message': 'Successfully get all data from `efed`', 'value': rows}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'Data successfully inserted into `efed`:' + str(e)}), 500)


#bre燃素方程表操作
@app.route("/bre_addAndUpdate", methods=['POST'])
def bre_add_and_update():
    json_data = request.get_json()
    
    if json_data:
        try:
            db_func.add_bre(json_data, db_config)
            return make_response(jsonify({'message': 'Data successfully inserted into `bre`'}), 200)
        except Exception as e:
            return make_response(jsonify({'error': 'Data unsuccessfully inserted into `bre`:' + str(e)}), 500)
    else:
        return make_response(jsonify({'error': 'Invalid json data(bre_add).'}), 400)
    
@app.route("/bre_del", methods=['POST'])
def bre_del():
    json_data = request.get_json()
    try:
        db_func.del_bre(json_data, db_config)
        return make_response(jsonify({'message': 'Data successfully deleted from `bre`'}), 200)
    except Exception as e:
        return make_response(jsonify({'error': 'Data unsuccessfully inserted into `bre`:' + str(e)}), 500)
    
@app.route("/bre_get", methods=['POST'])
def bre_get():
    try:
        json_data = request.get_json()
        rows = db_func.get_bre(json_data, db_config)     
        return make_response(jsonify({'message': 'Data successfully get from `bre`', 'value': rows}), 200)
    except Exception as e:
        return make_response(jsonify({'error': 'Data unsuccessfully inserted into `bre`:' + str(e)}), 500)


@app.route("/breget_all", methods=['GET'])
def bre_get_all():
    try:
        rows = db_func.getall_bre_data_as_json(db_config)
        return make_response(jsonify({'message': 'Successfully get all data from `bre`', 'value': rows}), 200)
    except Exception as e:
        return make_response(jsonify({'error': 'Unsuccessfully get all data from `bre`:' + str(e)}), 500)

if __name__ == "__main__":
    app.run(debug=False, host='127.0.0.1', port=9010)