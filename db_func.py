# -*- coding: utf-8 -*-
"""
Created on Mon May 23 17:24:00 2024

@author: Pherenice
"""

import mysql.connector

# User用户表操作
def user_add(json_data, db_config):
    data = json_data
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    
    userName_value = data["username"]
    pwd_value = data["password"]    
    
    query = f"insert into user (name, pwd) values('{userName_value}', '{pwd_value}')"
    cursor.execute(query)
    connection.commit()
    
    id_value = cursor.lastrowid
    for val in data["permissions"]:
        if val == "change_password":
            query = f"update user set c_p = true where id = {id_value}"
            cursor.execute(query)
        elif val == "change_data":
            query = f"update user set c_d = true where id = {id_value}"
            cursor.execute(query)
        elif val == "predict":
            query = f"update user set predict = true where id = {id_value}"
            cursor.execute(query)
    connection.commit()
        
    
    cursor.close()
    connection.close()
    return

def user_del(json_data, db_config):
    data = json_data
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    
    name = data["username"]

    query = f"delete from user where name = '{name}'"
    cursor.execute(query)
    connection.commit()
    
    cursor.close()
    connection.close()
    return

def user_update(json_data, db_config):
    data = json_data
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    
    userID_value = int(data["ID"])
    c_p_v = data["change_password"]
    c_d_v = data["change_data"]
    p_v = data["predict"]
    
    for k, j in zip(['username','password'],['name','pwd']):
        v = data[k]
        query = f"update user set {j} = '{v}' where id = {userID_value}"
        cursor.execute(query)
        
    query = f"update user set c_p = {c_p_v}, c_d = {c_d_v}, predict = {p_v} where id = {userID_value}"
    cursor.execute(query)
    connection.commit()
    
    cursor.close()
    connection.close()
    return
    
def user_login(json_data, db_config):
    data = json_data
    
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    
    userName_value = data["username"]
    pwd_value = data["password"]   
    
    query = f"SELECT pwd, c_p, c_d, predict FROM user WHERE name = '{userName_value}'"
    cursor.execute(query)
    result = cursor.fetchone()

    if result:
        db_password, change_password, change_data, predict = result
        if db_password == pwd_value:
            privileges = []
            if change_password:
                privileges.append('change_password')
            if change_data:
                privileges.append('change_data')
            if predict:
                privileges.append('predict')
                
            cursor.close()
            connection.close()
            return 200, privileges
        
    elif str(result == 'None'):
        cursor.close()
        connection.close()
        err = ['err']
        return 420, err
        
    err = ['err']
    cursor.close()
    connection.close()
    return 400, err
    
def user_getall(db_config):  
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    query = "select id, name, pwd, c_p, c_d, predict from user"
    cursor.execute(query)
    result = cursor.fetchall()
    
    data = []
    for row in result:
        data.append([str(row[0]), row[1], row[2], row[3], row[4], row[5]])

    cursor.close()
    connection.close()
    
    return data


# Materials原料表操作
def mat_add(json_data, db_config):
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        data = json_data
        
        
        query = "INSERT INTO `mat` () VALUES ();"
        print(query)
        cursor.execute(query)
        
        connection.commit()
        cursor.execute("SELECT LAST_INSERT_ID();")
        last_insert_id = cursor.fetchone()[0]

        fields_and_values = {
            'CAS' : data['CAS'],
            'code' : data['code'],
            'ccn' : data['ccn'],
            'ecn' : data['ecn'],
            'rmm' : data['rmm'],
            'ob' : data['ob'],
            'ofr' : data['ofr'],
            'density' : data['density'],
            'granu' : data['granu'],
            'sen_p' : data['sen_p'],
        }

        for field, value in fields_and_values.items():
            update_query = f"UPDATE `mat` SET {field} = %s WHERE id = %s"
            try:
                cursor.execute(update_query, (value, last_insert_id))
                connection.commit()
            except Exception as update_error:
                print(f"mat_add: Failed to update {field}: {str(update_error)}")

        connection.commit()
        cursor.close()
        connection.close()

        return 0
    
def update_mat(json_data, db_config, privileges):
    if 'change_data' in privileges:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        data = json_data
        
        id = data["id"]
        for key, value in data.items():
            if key == 'id':
                continue
            
            query = f"UPDATE mat SET `{key}` = '{value}' WHERE id = {id}"
            # print(query)
            cursor.execute(query)
            connection.commit()    
        
        cursor.close()
        connection.close()
        return 200, 'ok'
        
    else:
        err = "Current user do not have the permission to modify the table Materials"
        return 400, err

def del_mat(json_data, db_config, privileges):
    if 'change_data' in privileges:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        data = json_data
        
        id = data["id"]
        for key, value in data.items():
            if key == 'id':
                continue
            
            query = f"UPDATE mat SET `{key}` = '{value}' WHERE id = {id}"
            # print(query)
            cursor.execute(query)
            connection.commit()    
        
        status = "Update data in Materials: Success."
        cursor.close()
        connection.close()
        return 200, status
        
    else:
        err = "Current user do not have the permission to delete the data in Materials"
        return 400, err

def get_mat(db_config):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        query = "select * from mat"
        cursor.execute(query)
        rows = cursor.fetchall()

        cursor.close()
        connection.close()

        return rows
    except Exception as e:
        return f"Error occurred: {str(e)}"
    
    
    
