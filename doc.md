
# 接口文档

## 用户接口

**用户登录**
- URL: `/users/login`
- Method: `POST`
- Input:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- Output:
  ```json
  {
    "access_token": "string",
    "Priviliges": ["string"],
    "Message": "Login success"
  }
  ```

**创建用户**
- URL: `/users/create`
- Method: `POST`
- Input:
  ```json
  {
    "username": "string",
    "password": "string",
    "permissions": ["string"]
  }
  ```
- Output:
  ```json
  {
    "current_user": "string",
    "Message": "Create Success"
  }
  ```

**删除用户**
- URL: `/users/delete`
- Method: `POST`
- Input:
  ```json
  {
    "username": "string"
  }
  ```
- Output:
  ```json
  {
    "current_user": "string",
    "Message": "Delete Success"
  }
  ```

**编辑用户**
- URL: `/users/edit`
- Method: `POST`
- Input:
  ```json
  {
    "ID": "int",
    "username": "string",
    "password": "string",
    "change_password": "boolean",
    "change_data": "boolean",
    "predict": "boolean"
  }
  ```
- Output:
  ```json
  {
    "current_user": "string",
    "Message": "Edit Success"
  }
  ```

**获取所有用户**
- URL: `/users/getall`
- Method: `GET`
- Output:
  ```json
  {
    "current_user": "string",
    "data": [
      {
        "id": "int",
        "name": "string",
        "pwd": "string",
        "c_p": "boolean",
        "c_d": "boolean",
        "predict": "boolean"
      }
    ]
  }
  ```

## 原料接口

**添加原料**
- URL: `/mat/add`
- Method: `POST`
- Input:
  ```json
  {
    "CAS": "string",
    "code": "string",
    "ccn": "string",
    "ecn": "string",
    "rmm": "string",
    "ob": "string",
    "ofr": "string",
    "density": "float",
    "granu": "string",
    "sen_p": "string"
  }
  ```
- Output:
  ```json
  {
    "message": "Data successfully inserted into `mat`"
  }
  ```

**删除原料**
- URL: `/mat/del`
- Method: `POST`
- Input:
  ```json
  {
    "id": "int"
  }
  ```
- Output:
  ```json
  {
    "message": "Data successfully deleted."
  }
  ```

**获取单个原料**
- URL: `/mat/getone`
- Method: `POST`
- Input:
  ```json
  {
    "id": "int"
  }
  ```
- Output:
  ```json
  {
    "message": "Data get from `mat` successfully",
    "value": [
      {
        "id": "int",
        "ccn": "string",
        "ecn": "string",
        "rmm": "string",
        "ob": "string",
        "ofr": "string",
        "density": "float",
        "granu": "string",
        "sen_p": "string"
      }
    ]
  }
  ```

**获取所有原料**
- URL: `/mat/getall`
- Method: `GET`
- Output:
  ```json
  {
    "message": "Data get from `mat` successfully",
    "value": [
      {
        "id": "int",
        "ccn": "string",
        "ecn": "string",
        "rmm": "string",
        "ob": "string",
        "ofr": "string",
        "density": "float",
        "granu": "string",
        "sen_p": "string"
      }
    ]
  }
  ```

**更新原料**
- URL: `/mat/update`
- Method: `POST`
- Input:
  ```json
  {
    "id": "int",
    "ccn": "string",
    "ecn": "string",
    "rmm": "string",
    "ob": "string",
    "ofr": "string",
    "density": "float",
    "granu": "string",
    "sen_p": "string"
  }
  ```
- Output:
  ```json
  {
    "message": "Data in `mat` updated successfully"
  }
  ```

## 配方接口

**添加或更新配方**
- URL: `/ingre/add`
- Method: `POST`
- Input:
  ```json
  {
    "ch_fo": "string",
    "formula": "string",
    "mol_we": "string",
    "data": [
      {
        "id": "int",
        "cont": "string"
      }
    ]
  }
  ```
- Output:
  ```json
  {
    "message": "Data added into `ingre` successfully"
  }
  ```

**删除配方**
- URL: `/ingre/del`
- Method: `POST`
- Input:
  ```json
  {
    "Ingre_ID": "int"
  }
  ```
- Output:
  ```json
  {
    "message": "Data deleted from `ingre` successfully"
  }
  ```

**获取所有配方**
- URL: `/ingre/get`
- Method: `GET`
- Output:
  ```json
  {
    "message": "Data get from `ingre` successfully",
    "value": [
      {
        "id": "int",
        "ch_fo": "string",
        "formula": "string",
        "mol_we": "string",
        "name": "string"
      }
    ]
  }
  ```

**更新配方**
- URL: `/ingre/update`
- Method: `POST`
- Input:
  ```json
  {
    "ID": "int",
    "ch_fo": "string",
    "formula": "string",
    "mol_we": "string",
    "name": "string"
  }
  ```
- Output:
  ```json
  {
    "message": "Data update in `ingre` successfully"
  }
  ```

## 中间表接口

**获取单个配方的所有原料**
- URL: `/gmfi`
- Method: `POST`
- Input:
  ```json
  {
    "Ingre_ID": "int"
  }
  ```
- Output:
  ```json
  {
    "message": "Get all mat from single ingre successfully",
    "value": {
      "data": [
        {
          "原料名称": "string",
          "含量": "string"
        }
      ]
    }
  }
  ```

## 实验燃素数据表接口

**添加或更新实验燃素数据**
- URL: `/efed/addAndUpdate`
- Method: `POST`
- Input:
  ```json
  {
    "Ingre_ID": "int",
    "count": "int",
    "data": [
      {
        "pre": "string",
        "rate": "string"
      },...
    ]
  }
  ```
- Output:
  ```json
  {
    "message": "Data successfully inserted into `efed`"
  }
  ```

**删除实验燃素数据**
- URL: `/efed_del`
- Method: `POST`
- Input:
  ```json
  {
    "Ingre_ID": "int"
  }
  ```
- Output:
  ```json
  {
    "message": "Data successfully deleted from `efed`"
  }
  ```

**获取单个实验燃素数据**
- URL: `/efed_get`
- Method: `POST`
- Input:
  ```json
  {
    "Ingre_ID": "int"
  }
  ```
- Output:
  ```json
  {
    "message": "Data successfully get from `efed`",
    "value": {
      "data": [
        {
          "count": "int",
          "ref_num": "string",
          "note": "string",
          "code": "string",
          "pre": "string",
          "rate": "string"
        }
      ]
    }
  }
  ```

**获取所有实验燃素数据**
- URL: `/efedget_all`
- Method: `GET`
- Output:
  ```json
  {
    "message": "Successfully get all data from `efed`",
    "value": [
      {
        "id": "int",
        "in_id": "int",
        "count": "int",
        "pre": "string",
        "rate": "string"
      }
    ]
  }
  ```

## 燃素方程表接口

**添加或更新燃素方程数据**
- URL: `/bre_addAndUpdate`
- Method: `POST`
- Input:
  ```json
  {
    "Ingre_ID": "int",
    "data": [

      {
        "P": "string",
        "A": "string",
        "B": "string",
        "N": "string",
        "Err": "string",
        "Rfs": "string",
        "Comment": "string"
      },...
    ]
  }
  ```
- Output:
  ```json
  {
    "message": "Data successfully inserted into `bre`"
  }
  ```

**删除燃素方程数据**
- URL: `/bre_del`
- Method: `POST`
- Input:
  ```json
  {
    "Ingre_ID": "int"
  }
  ```
- Output:
  ```json
  {
    "message": "Data successfully deleted from `bre`"
  }
  ```

**获取单个燃素方程数据**
- URL: `/bre_get`
- Method: `POST`
- Input:
  ```json
  {
    "Ingre_ID": "int"
  }
  ```
- Output:
  ```json
  {
    "message": "Data successfully get from `bre`",
    "value": [
      {
        "P": "string",
        "A": "string",
        "B": "string",
        "N": "string",
        "Err": "string",
        "rfs": "string",
        "Comment": "string"
      }
    ]
  }
  ```

**获取所有燃素方程数据**
- URL: `/breget_all`
- Method: `GET`
- Output:
  ```json
  {
    "message": "Successfully get all data from `bre`",
    "value": [
      {
        "id": "int",
        "in_id": "int",
        "p": "string",
        "A": "string",
        "B": "string",
        "N": "string",
        "Err": "string",
        "rfs": "string",
        "comment": "string"
      }
    ]
  }
  ```
