# -*- coding: utf-8 -*-
"""
Created on Mon May 23 17:24:00 2024

@author: Pherenice
"""

import mysql.connector
sep = "|||"

#功能性函数
def convert(input1, input2):
    ids = [int(num.strip()) for num in input1.split(",")]
    conts = [f"{num.strip()}" for num in input2.split(",")]
    result = [{"id": id_val, "cont": cont_val} for id_val, cont_val in zip(ids, conts)]

    return result

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
def add_mat(json_data, db_config):
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
    
def update_mat(json_data, db_config):
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
    return

def del_mat(json_data, db_config):
    data = json_data
    id = data["Mat_ID"]
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    query = "delete from mat where id = %s"
    value = (id,)
    cursor.execute(query, value)

    connection.commit()
    cursor.close()
    connection.close()
    return

def get_mat_one(json_data, db_config):
    data = json_data
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    keys = list(data.keys())
    if len(keys) == 1:
        str = keys[0]
    else:
        raise ValueError("json_data必须包含且仅包含一个键")
    
    query = f"SELECT * FROM mat WHERE {str} = %s"
    cursor.execute(query, (data[str],))
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows
    
def get_mat_all(db_config):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    query = "select * from mat"
    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows
    
    
#I_M_Midium中间表操作
def getall_mat_for_ingre(json_data, db_config):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    
    data = json_data
    ingre_id = data['Ingre_ID']

    query = f"SELECT * FROM in_ma WHERE in_id={ingre_id}"
    cursor.execute(query)
    rows_in_ma = cursor.fetchall()
    
    outList = []
    for rDict in rows_in_ma:
        ma_id = rDict['ma_id']
        subQuery = f"SELECT * FROM mat WHERE id={ma_id}"
        cursor.execute(subQuery)
        ma_info = cursor.fetchone()
        mat_name = ma_info['ccn']
        outList.append({'id': ma_id, 'mat_name': mat_name, 'cont': rDict['cont']})
    out_dict = {'data': outList}
    
    cursor.close()
    connection.close()

    return out_dict
    
    
# Ingredients配方表操作

def add_or_update_ingre(json_data, db_config):
    data = json_data
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    
    str1 = data["mat_ids"]
    str2 = data["conts"]
    
    data["data"] = convert(str1, str2)

    ch_fo_value = data['ch_fo']
    formula_value = data['formula']
    mol_we_value = data['mol_we']
    name_value = data['name']
    ingre_id_value = data.get('ingre_id')  # 获取ingre_id，如果存在的话

    id_values_list = [int(i["id"]) for i in data["data"]]
    cont_values_list = [i["cont"] for i in data["data"]]

    if ingre_id_value: 
        update_ingre_query = f"""
        UPDATE ingre SET ch_fo = '{ch_fo_value}', formula = '{formula_value}', mol_we = '{mol_we_value}', name = '{name_value}'
        WHERE id = {ingre_id_value}
        """
        cursor.execute(update_ingre_query)
        connection.commit()
        
        delete_in_ma_query = f"DELETE FROM in_ma WHERE in_id = {ingre_id_value}"
        cursor.execute(delete_in_ma_query)
        connection.commit()
        
        for mat_id, cont in zip(id_values_list, cont_values_list):
            insert_into_in_ma_query = f"INSERT INTO in_ma (in_id, ma_id, cont) VALUES ({ingre_id_value}, {mat_id}, '{cont}')"
            cursor.execute(insert_into_in_ma_query)
            connection.commit()
    else:  
        insert_into_ingre_query = f"INSERT INTO ingre (ch_fo, formula, mol_we, name) VALUES ('{ch_fo_value}', '{formula_value}', '{mol_we_value}', '{name_value}')"
        cursor.execute(insert_into_ingre_query)
        connection.commit()

        ingre_id = int(cursor.lastrowid)
        for mat_id, cont in zip(id_values_list, cont_values_list):
            insert_into_in_ma_query = f"INSERT INTO in_ma (in_id, ma_id, cont) VALUES ({ingre_id}, {mat_id}, '{cont}')"
            cursor.execute(insert_into_in_ma_query)
            connection.commit()

    cursor.close()
    connection.close()
    return

def del_ingre(json_data, db_config):
    data = json_data
    id = data["Ingre_ID"]
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    query = "delete from ingre where id = %s"
    value = (id,)
    cursor.execute(query, value)

    connection.commit()
    cursor.close()
    connection.close()
    return

def get_ingre_one(json_data, db_config):
    data = json_data
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    keys = list(data.keys())
    if len(keys) == 1:
        str = keys[0]
    else:
        raise ValueError("json_data必须包含且仅包含一个键")
    
    query = f"SELECT * FROM ingre WHERE {str} = %s"
    cursor.execute(query, (data[str],))
    rows = cursor.fetchall()

    cursor.close()
    connection.close()
    return rows

    
def get_ingre_all(db_config):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        query = "select * from ingre"
        cursor.execute(query)
        rows = cursor.fetchall()

        cursor.close()
        connection.close()

        return rows
    except Exception as e:
        return f"Error occurred: {str(e)}"

#efed实验燃素数据表
def add_or_update_efed(json_data, db_config):
    connection = None
    cursor = None
    data = json_data
    
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    
    in_id_value = int(data['Ingre_ID'])
    count_value = int(data['count'])
           
    query = f"""
    select code, pre, rate from efed where in_id = {in_id_value};
    """
    cursor.execute(query)
    result = cursor.fetchone()
    
    if result:
        code_values_list = result[0].split(sep)
        pre_values_list = result[1].split(sep)
        rate_values_list = result[2].split(sep)
        
        for item in data['data']:
           code_values_list.append(item['code'])
           pre_values_list.append(item['pre'])
           rate_values_list.append(item['rate'])
            
        code_values_str = sep.join(code_values_list)   
        pre_values_str = sep.join(pre_values_list)
        rate_values_str = sep.join(rate_values_list)
    else:
        code_values_str = sep.join([item['code'] for item in data['data']])
        pre_values_str = sep.join([item['pre'] for item in data['data']])
        rate_values_str = sep.join([item['rate'] for item in data['data']])

    query = f"""
    insert into efed (in_id, count, code, pre, rate)
    values ({in_id_value}, {count_value}, '{code_values_str}', '{pre_values_str}', '{rate_values_str}')
    on duplicate key update code=values(code), pre=values(pre), rate=values(rate);
    """
    cursor.execute(query)
    connection.commit()
    print("efed表：数据保存成功！")
   
    if cursor:
       cursor.close()
    if connection:
       connection.close()  
    return

def del_efed(json_data, db_config):
    data = json_data
    
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    
    in_id = int(data['Ingre_ID'])
    
    query = "delete from efed where in_id = %(in_id)s"
    value = {"in_id": in_id}
    cursor.execute(query, value)
    connection.commit()
    cursor.close()
    connection.close()
    print("efed表：数据删除成功")

def get_efed(json_data, db_config):
    d_data = json_data
    
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    
    in_id = int(d_data['Ingre_ID'])
    
    query = "SELECT * FROM efed WHERE in_id = %(in_id)s"
    value = {"in_id": in_id}
    cursor.execute(query, value)
    result = cursor.fetchone()
    row = list(result)
    
    in_id = row[1]
    count = row[2]
    code_values = row[3].split(sep)
    pre_values = row[4].split(sep)
    rate_values = row[5].split(sep)
    

    data = [
        {"count": count},
    ]
    for i in range(len(code_values)):
        item = {
            "code": code_values[i].strip('""'),
            "pre": pre_values[i].strip('""'),
            "rate": rate_values[i].strip('""'),
        }
        data.append(item)

    result = { 
        "data": data
    }
    connection.commit()
    cursor.close()
    connection.close()

    return result

def get_all_efed(db_config):
    import mysql.connector

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    query = "SELECT * FROM efed"
    cursor.execute(query)
    results = cursor.fetchall()

    # 获取列名
    column_names = [i[0] for i in cursor.description]

    # 将结果转换为字典列表
    data = [dict(zip(column_names, row)) for row in results]

    cursor.close()
    connection.close()

    return data



#bre燃素方程表
def add_or_update_bre(json_data, db_config):
    connection = None
    cursor = None
    data = json_data
    
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    
    in_id_value = int(data['Ingre_ID'])

    query = f"""
    SELECT p, A, B, N, Err, rfs, comment FROM bre WHERE in_id = {in_id_value};
    """
    cursor.execute(query)
    result = cursor.fetchone()

    if result:
        p_values_list = result[0].split(sep) #返回字符串列表， 将每个索引所对的字符串进行切割
        a_values_list = result[1].split(sep)
        b_values_list = result[2].split(sep)
        n_values_list = result[3].split(sep)
        err_values_list = result[4].split(sep)
        rf_values_list = result[5].split(sep)
        comment_values_list = result[6].split(sep)

        for item in data['data']:
            p_values_list.append(item['P'])
            a_values_list.append(item['A'])
            b_values_list.append(item['B'])
            n_values_list.append(item['N'])
            err_values_list.append(item['Err'])
            rf_values_list.append(item['Rfs'])
            comment_values_list.append(item['Comment'])

        p_values_str = sep.join(p_values_list)
        a_values_str = sep.join(a_values_list)
        b_values_str = sep.join(b_values_list)
        n_values_str = sep.join(n_values_list)
        err_values_str = sep.join(err_values_list)
        rf_values_str = sep.join(rf_values_list)
        comment_values_str = sep.join(comment_values_list)
    else:
        p_values_str = sep.join([item['P'] for item in data['data']])
        a_values_str = sep.join([item['A'] for item in data['data']])
        b_values_str = sep.join([item['B'] for item in data['data']])
        n_values_str = sep.join([item['N'] for item in data['data']])
        err_values_str = sep.join([item['Err'] for item in data['data']])
        rf_values_str = sep.join([item['Rfs'] for item in data['data']])
        comment_values_str = sep.join([item['Comment'] for item in data['data']])
    
    query = f"""
    INSERT INTO bre (in_id, p, A, B, N, Err, rfs, comment)
    VALUES ({in_id_value}, '{p_values_str}', '{a_values_str}', '{b_values_str}',
    '{n_values_str}', '{err_values_str}', '{rf_values_str}', '{comment_values_str}')
    ON DUPLICATE KEY UPDATE p=VALUES(p), A=VALUES(A), B=VALUES(B), N=VALUES(N),
                            Err=VALUES(Err), rfs=VALUES(rfs), comment=VALUES(comment);
    """
    cursor.execute(query)
    # 提交事务
    connection.commit()
    print("bre表：数据保存成功！")

    # 关闭数据库连接
    if cursor:
       cursor.close()
    if connection:
       connection.close()  
       
def del_bre(json_data, db_config):
    data = json_data
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    
    in_id = int(data['Ingre_ID'])
    
    query = "delete from bre where in_id = %(in_id)s"
    value = {"in_id": in_id}
    cursor.execute(query, value)
    connection.commit()
    cursor.close()
    connection.close()
    return

def get_bre(json_data, db_config):
    data = json_data
    
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    
    in_id = int(data['Ingre_ID'])  # 确保ID为整数，如果数据库查询需要
    
    query = "SELECT * FROM bre WHERE in_id = %(in_id)s"
    params = {"in_id": in_id}  # 使用参数化查询来防止SQL注入
    cursor.execute(query, params)
    result = cursor.fetchone()
    row = list(result)
    
    # 直接从row中读取，不再重新赋值in_id，因为原代码中的该行似乎是多余的
    p_values = row[2].split(sep)
    a_values = row[3].split(sep)
    b_values = row[4].split(sep)
    n_values = row[5].split(sep)
    err_values = row[6].split(sep)
    rf_values = row[7].split(sep)
    comment_values = row[8].split(sep)

    data_list = []  # 更改变量名以避免与外部传入的"data"重名
    for i in range(len(p_values)):
        item = {
            "P": p_values[i].strip('""'),
            "A": a_values[i].strip('""'),
            "B": b_values[i].strip('""'),
            "N": n_values[i].strip('""'),
            "Err": err_values[i].strip('""'),
            "rfs": rf_values[i].strip('""'),
            "Comment": comment_values[i].strip('""'),
        }
        data_list.append(item)  # 使用append方法添加字典到列表中

    result = {
        "data": data_list,
    }
    
    cursor.close()
    connection.close()

    return result

def get_all_bre(db_config):
    import mysql.connector

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    query = "SELECT * FROM bre"
    cursor.execute(query)
    results = cursor.fetchall()

    # 获取列名
    column_names = [i[0] for i in cursor.description]

    # 将结果转换为字典列表
    data = [dict(zip(column_names, row)) for row in results]

    cursor.close()
    connection.close()

    return data