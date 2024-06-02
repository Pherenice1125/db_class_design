import mysql.connector
from db_Config import db_config

def create_table_Materials():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        check_table_query = "show tables like 'mat'"
        cursor.execute(check_table_query)

        if cursor.fetchone():
            print("mat原料表已存在。")
        else:
            create_table_query = '''
                CREATE TABLE mat (
                    id bigint primary key auto_increment comment 'ID',
                    ccn varchar(255) unique comment '中文化学名(Chinese chemical name)' DEFAULT '',
                    ecn varchar(255) comment '英文化学名(English chemical name)' DEFAULT '',
                    rmm varchar(255) comment '相对分子质量(relative molecular mass)' DEFAULT '',
                    ofr varchar(255) comment '氧燃比(Oxygen-fuel ratio)' DEFAULT '',
                    ob varchar(255) comment '氧平衡' DEFAULT '',
                    density double comment '密度',
                    granu varchar(255) comment '粒度(granularity)' DEFAULT '',
                    sen_p varchar(255) comment '感度性能(Sensitivity performance)' DEFAULT ''
                ) comment '原料';
                '''

            cursor.execute(create_table_query)
            print("mat原料表创建成功！")

        connection.commit()
        cursor.close()
        connection.close()

    except mysql.connector.Error as error:
        print(f"mat原料表生成失败: {error}")

      
def create_table_Ingredients():
    try:
       connection = mysql.connector.connect(**db_config)
       cursor = connection.cursor()

       check_table_query = "show tables like 'ingre'"
       cursor.execute(check_table_query)

       if cursor.fetchone():
           print("ingre配方表已存在。")
       else:
           create_table_query = '''
                CREATE TABLE ingre (
                    id bigint comment 'ID' primary key auto_increment,
                    ch_fo varchar(255) comment '化学式' DEFAULT '',
                    formula varchar(255) comment '分子式' DEFAULT '',
                    mol_we varchar(255) comment '分子量FW' DEFAULT '',
                    name varchar(1000) comment '名称' DEFAULT ''
                ) comment '配方';
                '''
           cursor.execute(create_table_query)
           print("ingre配方表创建成功！")

       connection.commit()
       cursor.close()
       connection.close()

    except mysql.connector.Error as error:
       print(f"ingre配方表创建失败: {error}")
     
   
def crete_table_I_M_Midium():
    try:
       connection = mysql.connector.connect(**db_config)
       cursor = connection.cursor()

       check_table_query = "show tables like 'in_ma'"
       cursor.execute(check_table_query)

       if cursor.fetchone():
           print("in_ma中间表已存在。")
       else:
           create_table_query = '''
                CREATE TABLE in_ma (
                    id bigint primary key not null auto_increment comment 'ID',
                    in_id bigint comment '对应配方id',
                    ma_id bigint comment '对应组分id',
                    cont varchar(30) comment '含量' DEFAULT '0',
                    UNIQUE (in_id, ma_id),
                    constraint `fk_in_id` foreign key (in_id) references ingre(id) on delete cascade,
                    constraint `fk_ma_id` foreign key (ma_id) references mat(id) on delete cascade
                ) comment '配方-原料中间表';
                '''

           cursor.execute(create_table_query)
           print("in_ma中间表创建成功！")

       connection.commit()
       cursor.close()
       connection.close()
       
    except mysql.connector.Error as error:
       print(f"in_ma中间表创建失败: {error}")


def create_table_Efed():
    try:
       connection = mysql.connector.connect(**db_config)
       cursor = connection.cursor()

       check_table_query = "show tables like 'efed'"
       cursor.execute(check_table_query)

       if cursor.fetchone():
           print("efed实验燃速数据表已存在。")
       else:
           create_table_query = '''
            CREATE TABLE efed (
                id int auto_increment not null primary key comment 'ID',
                in_id int unique comment '相对应的配方id',
                count int comment '数目' DEFAULT 0,
                code varchar(1000) comment '编号' DEFAULT '',
                pre varchar(1000) comment '压强' DEFAULT '',
                rate varchar(1000) comment '速率' DEFAULT '',
                constraint fk_ef_in_id foreign key (in_id) references ingre(id) on delete cascade
            ) comment '实验燃速数据';
            '''

           cursor.execute(create_table_query)
           print("efed实验燃速数据表创建成功！")

       connection.commit()
       cursor.close()
       connection.close()
       
    except mysql.connector.Error as error:
       print(f"efed实验燃速数据表创建失败: {error}")


def create_table_Bre():       
    try:
       connection = mysql.connector.connect(**db_config)
       cursor = connection.cursor()

       check_table_query = "show tables like 'bre'"
       cursor.execute(check_table_query)

       if cursor.fetchone():
           print("bre燃速方程表已存在。")
       else:
           create_table_query = '''
            CREATE TABLE bre (
                id bigint auto_increment primary key not null comment 'ID',
                in_id bigint unique comment '相对应配方id',
                p varchar(1000) comment 'p' DEFAULT '',
                A varchar(1000) comment 'A' DEFAULT '',
                B varchar(1000) comment 'A' DEFAULT '',
                N varchar(1000) comment 'N' DEFAULT '',
                Err varchar(1000) comment 'Err' DEFAULT '',
                rfs varchar(1000) comment 'references' DEFAULT '',
                comment varchar(1000) comment 'comment' DEFAULT '',
                constraint fk_br_in_id foreign key (in_id) references ingre(id) on delete cascade
            ) comment '燃速方程表（Burning rate equation table）';
            '''

           cursor.execute(create_table_query)
           print("bre燃速方程表创建成功！")

       connection.commit()
       cursor.close()
       connection.close()
       
    except mysql.connector.Error as error:
       print(f"bre燃速方程表创建失败: {error}")
       
       
def create_table_User():       
    try:
       connection = mysql.connector.connect(**db_config)
       cursor = connection.cursor()

       check_table_query = "show tables like 'user'"
       cursor.execute(check_table_query)

       if cursor.fetchone():
           print("User用户表已存在。")
       else:
           create_table_query = '''
            create table user(
                id bigint primary key auto_increment,
                name varchar(20) unique comment '用户名',
                pwd varchar(50) comment '密码',
                c_d boolean default 0 comment 'change_data',
                c_p boolean default 0 comment 'change_password',
                predict boolean default 0 comment 'predict'
                );
            '''

           cursor.execute(create_table_query)
           print("User用户表创建成功！")

       connection.commit()
       cursor.close()
       connection.close()
       
    except mysql.connector.Error as error:
       print(f"User用户表创建失败: {error}")
       


def create_ALL():
    create_table_Ingredients()
    create_table_Materials()
    crete_table_I_M_Midium()
    create_table_Efed()
    create_table_Bre()
    create_table_User()
    
if __name__ == '__main__':
    create_ALL()    