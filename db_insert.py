# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 16:00:35 2024

@author: Pherenice & Tianji
"""

import mysql.connector
from mysql.connector import Error
from db_Config import db_config

def insert_test_data(conf):
    try:
        # 连接到数据库
        connection = mysql.connector.connect(**conf)
        cursor = connection.cursor()

        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"Successfully connected to MySQL Server version {db_info}")
            
        mat_data = [
            ('硫酸铜', 'Copper Sulfate', '159.61 g/mol', '1.2:1', '正', '3.6 g/cm³', '300 mesh', '中'),
            ('硝酸钠', 'Sodium Nitrate', '84.99 g/mol', '1.5:1', '正', '2.26 g/cm³', '250 mesh', '高'),
            ('氢氧化钠', 'Sodium Hydroxide', '40.00 g/mol', '1.0:1', '负', '2.13 g/cm³', '片状', '高'),
            ('磷酸二氢钾', 'Potassium Dihydrogen Phosphate', '136.09 g/mol', '1:1', '正', '2.34 g/cm³', '粉末', '低'),
            ('氯化钙', 'Calcium Chloride', '110.98 g/mol', '1.1:1', '正', '2.15 g/cm³', '颗粒', '中'),
            ('乙醇', 'Ethanol', '46.07 g/mol', '0.8:1', '负', '0.789 g/cm³', '液态', '低'),
            ('丙酮', 'Acetone', '58.08 g/mol', '0.9:1', '负', '0.79 g/cm³', '液态', '低'),
            ('苯甲酸', 'Benzoic Acid', '122.12 g/mol', '1.1:1', '负', '1.27 g/cm³', '晶体', '中'),
            ('柠檬酸', 'Citric Acid', '192.12 g/mol', '1.2:1', '正', '1.66 g/cm³', '粉末', '低'),
            ('硫酸亚铁', 'Ferrous Sulfate', '151.91 g/mol', '1.3:1', '正', '2.84 g/cm³', '结晶', '中'),
            ('碳酸镁', 'Magnesium Carbonate', '84.32 g/mol', '1.0:1', '正', '3.0 g/cm³', '粉末', '低'),
            ('高锰酸钾', 'Potassium Permanganate', '158.04 g/mol', '1.4:1', '负', '2.7 g/cm³', '结晶', '高'),
            ('过氧化氢', 'Hydrogen Peroxide', '34.01 g/mol', '1.5:1', '正', '1.45 g/cm³', '液态', '高'),
            ('葡萄糖', 'Glucose', '180.16 g/mol', '1.2:1', '正', '1.54 g/cm³', '粉末', '低'),
            ('尿素', 'Urea', '60.06 g/mol', '1.0:1', '负', '1.33 g/cm³', '颗粒', '低'),
            ('醋酸', 'Acetic Acid', '60.05 g/mol', '1.1:1', '正', '1.05 g/cm³', '液态', '低'),
            ('硫酸铵', 'Ammonium Sulfate', '132.14 g/mol', '1.3:1', '负', '1.77 g/cm³', '结晶', '中'),
            ('碘化钾', 'Potassium Iodide', '166.01 g/mol', '1.4:1', '正', '3.12 g/cm³', '晶体', '低')
            ]   

        mat_insert_query = """
        INSERT INTO mat (ccn, ecn, rmm, ofr, ob, density, granu, sen_p)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.executemany(mat_insert_query, mat_data)
        print("Successfully insert data into table 'mat'.")

        # 插入ingre配方表数据
        ingre_data = [
            ('配方1', 'NaCl', '58.44 g/mol', 'C3H4O5N2'),
            ('配方2', 'CaCO3', '100.09 g/mol', 'C10H7O4N2'),
            ('配方3', 'H2SO4', '98.08 g/mol', 'C4H4O4N1'),
            ('配方4', 'KNO3', '101.11 g/mol', 'C10H7O4N1'),
            ('配方5', 'NH4NO3', '80.05 g/mol', 'C1H7O5N3'),
            ('配方6', 'Sucrose', '342.30 g/mol', 'C1H5O4N3'),
            ('配方7', 'Copper Sulfate', '159.61 g/mol', 'C1H10O2N2'),
            ('配方8', 'Iron(III) Nitrate', '241.87 g/mol', 'C1H6O2N2'),
            ('配方9', 'Aluminum Sulfate', '342.15 g/mol', 'C9H12O3N1'),
            ('配方10', 'Silver Nitrate', '169.88 g/mol', 'C9H14O5N1'),
            ('配方11', 'Barium Chloride', '208.23 g/mol', 'C1H22O3'),
            ('配方12', 'Acetic Acid', '60.05 g/mol', 'C7H17O4N1'),
            ('配方13', 'Glucose', '180.16 g/mol', 'C8H6O3N3'),
            ('配方14', '14Potassium Chlorate', '122.55 g/mol', 'C1H12O3N3'),
            ('配方15', 'Magnesium Sulfate', '120.37 g/mol', 'C1H12O5'),
            ('配方16', 'Sodium Bicarbonate', '84.01 g/mol', 'C3H19O5N1'),
            ('配方17', 'Sodium Carbonate', '105.99 g/mol', 'C10H20O3N1'),
            ('配方18', 'Zinc Chloride', '136.31 g/mol', 'C10H10O4N1')
        ]
        ingre_insert_query = """
        INSERT INTO ingre (ch_fo, formula, mol_we, name)
        VALUES (%s, %s, %s, %s)
        """
        cursor.executemany(ingre_insert_query, ingre_data)
        print("Successfully insert data into table 'ingre'.")

        # 插入in_ma中间表数据
        in_ma_data = [
            (1, 1, '50%'),
            (1, 2, '30%'),  
            (1, 3, '20%'),  
            (2, 2, '45%'),   
            (2, 5, '35%'),
            (2, 6, '20%'),
            (3, 17, '60%'),
            (3, 8, '40%'),
            (4, 9, '70%'),
            (4, 10, '30%'),
            (5, 11, '55%'),
            (5, 12, '45%'),
            (6, 1, '25%'),
            (6, 13, '50%'),
            (6, 14, '25%'),
            (7, 2, '30%'),
            (7, 15, '50%'),
            (7, 16, '20%'),
            (8, 3, '40%'),
            (8, 17, '45%'),
            (8, 18, '15%'),
            (9, 4, '60%'),
            (9, 15, '30%'),
            (10, 18, '10%'),
            (10, 2, '12%'),
            (10, 5, '24%'),
            (10, 9, '54%'),
            (11, 6, '10%'),  
            (11, 15, '90%'),  
            (12, 1, '19%'),  
            (12, 8, '81%'),  
            (13, 10, '33%'),  
            (13, 11, '33%'),  
            (13, 12, '34%'),  
            (14, 13, '19%'),
            (14, 1, '20%'),
            (14, 10, '21%'),
            (14, 2, '20%'),
            (15, 13, '1%'),
            (15, 1, '99%'),
            (16, 8, '17%'),
            (16, 12, '50%'),
            (16, 14, '33%'),
            (17, 15, '12%'),
            (17, 5, '31%'),
            (17, 7, '22%'),
            (17, 9, '5%'),
            (17, 17, '12%'),
            (17, 16, '18%'),
            (18, 6, '59%'),
            (18, 13, '41%'),
            ]

        in_ma_insert_query = """
        INSERT INTO in_ma (in_id, ma_id, cont)
        VALUES (%s, %s, %s)
        """
        cursor.executemany(in_ma_insert_query, in_ma_data)

        efed_data = [
            (1, 8, 'EXP002|||EXP012|||EXP022', '0.8 atm|||1.2 atm|||1.45 atm', '4.5 cm/s|||1.5 cm/s|||6.28 cm/s'),
            (3, 12, 'EXP003|||EXP013|||EXP023|||EXP033', '1.2 atm|||1.6 atm|||1.75 atm|||2.0 atm', '6.0 cm/s|||2.0 cm/s|||7.28 cm/s|||8.5 cm/s'),
            (4, 5, 'EXP004|||EXP014', '0.6 atm|||0.9 atm', '3.8 cm/s|||1.3 cm/s'),
            (5, 15, 'EXP005|||EXP015|||EXP025|||EXP035', '1.0 atm|||1.3 atm|||1.5 atm|||1.7 atm', '5.0 cm/s|||1.7 cm/s|||6.78 cm/s|||7.5 cm/s'),
            (6, 7, 'EXP006|||EXP016|||EXP026', '0.9 atm|||1.1 atm|||1.35 atm', '4.2 cm/s|||1.4 cm/s|||6.05 cm/s'),
            (9, 9, 'EXP007|||EXP017', '0.7 atm|||1.0 atm', '3.5 cm/s|||1.2 cm/s'),
            (11, 11, 'EXP008|||EXP018|||EXP028|||EXP038', '1.1 atm|||1.4 atm|||1.65 atm|||1.9 atm', '5.8 cm/s|||1.9 cm/s|||7.28 cm/s|||8.5 cm/s'),
            (12, 6, 'EXP009|||EXP019', '0.5 atm|||0.8 atm', '2.9 cm/s|||1.0 cm/s'),
            (17, 10, 'EXP010|||EXP020|||EXP030', '1.3 atm|||1.5 atm|||1.8 atm', '6.5 cm/s|||2.2 cm/s|||8.28 cm/s')
            ]   
        efed_insert_query = """
        INSERT INTO efed (in_id, count, code, pre, rate)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.executemany(efed_insert_query, efed_data)
        print("Successfully insert data into table 'in_ma'.")
        
        bre_data = [
            (2, '0.15|||0.25|||0.35', '1.8e-6|||2.3e-6|||2.8e-6', '1.3e-5|||1.4e-5|||1.5e-5', '1.1|||1.2|||1.3', '4%|||3.8%|||3.5%', 'Ref2345|||Ref3456|||Ref4567', '压力影响下测量|||不同温度影响|||不同湿度影响'),
            (3, '0.2|||0.3', '2.1e-6|||2.6e-6', '1.4e-5|||1.5e-5', '1.2|||1.3', '3%|||3.2%', 'Ref3456|||Ref4567', '室温条件下|||不同气压下'),
            (4, '0.3|||0.4|||0.5|||0.6', '2.4e-6|||2.9e-6|||3.4e-6|||3.9e-6', '1.5e-5|||1.6e-5|||1.7e-5|||1.8e-5', '1.3|||1.4|||1.5|||1.6', '3.5%|||3.6%|||3.7%|||3.8%', 'Ref4567|||Ref5678|||Ref6789|||Ref7890', '高湿度环境|||低湿度环境|||不同气压环境|||不同催化剂'),
            (5, '0.4|||0.5|||0.6', '2.7e-6|||3.2e-6|||3.7e-6', '1.6e-5|||1.7e-5|||1.8e-5', '1.4|||1.5|||1.6', '3.2%|||3.3%|||3.4%', 'Ref5678|||Ref6789|||Ref7890', '标准大气压|||不同催化剂下|||不同温度下'),
            (8, '0.5|||0.6|||0.7|||0.8', '3.0e-6|||3.5e-6|||4.0e-6|||4.5e-6', '1.7e-5|||1.8e-5|||1.9e-5|||2.0e-5', '1.5|||1.6|||1.7|||1.8', '3.8%|||3.9%|||4%|||4.1%', 'Ref6789|||Ref7890|||Ref8901|||Ref9012', '低温测试|||高温测试|||不同湿度测试|||长时间测试'),
            (11, '0.6|||0.7', '3.3e-6|||3.8e-6', '1.8e-5|||1.9e-5', '1.6|||1.7', '3.3%|||3.4%', 'Ref7890|||Ref8901', '高温模拟|||真空条件下'),
            (14, '0.7|||0.8|||0.9|||1.0', '3.6e-6|||4.1e-6|||4.6e-6|||5.1e-6', '1.9e-5|||2.0e-5|||2.1e-5|||2.2e-5', '1.7|||1.8|||1.9|||2.0', '3.6%|||3.7%|||3.8%|||3.9%', 'Ref8901|||Ref9012|||Ref0123|||Ref1234', '真空条件下|||长时间测试|||短时间测试|||不同压力下'),
            (15, '0.8|||0.9|||1.0', '3.9e-6|||4.4e-6|||4.9e-6', '2.0e-5|||2.1e-5|||2.2e-5', '1.8|||1.9|||2.0', '3.1%|||3.2%|||3.3%', 'Ref9012|||Ref0123|||Ref1234', '不同催化剂|||长时间持续燃烧|||短时间燃烧'),
            (18, '0.9|||1.0|||1.1|||1.2', '4.2e-6|||4.7e-6|||5.2e-6|||5.7e-6', '2.1e-5|||2.2e-5|||2.3e-5|||2.4e-5', '1.9|||2.0|||2.1|||2.2', '3.4%|||3.5%|||3.6%|||3.7%', 'Ref0123|||Ref1234|||Ref2345|||Ref3456', '长时间持续燃烧|||短时间燃烧|||不同压力下|||不同温度下')
            ]   
        bre_insert_query = """
        INSERT INTO bre (in_id, P, A, B, N, Err, rfs, comment)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.executemany(bre_insert_query, bre_data)
        print("Successfully insert data into table 'bre'.")
        
        # 提交事务
        connection.commit()
        print("数据插入成功。")

    except Error as e:
        print(f"数据插入失败: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("数据库连接已关闭。")
            
if __name__ == '__main__':
    insert_test_data(db_config)