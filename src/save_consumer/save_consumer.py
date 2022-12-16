import mysql.connector
from utils import Consumer
import os
import time
import datetime

# data col : age,sex,cp,trtbps,chol,fbs,restecg,thalachh,exng,oldpeak,slp,caa,thall
# data : 57,1,0,150,276,0,0,112,1,0.6,1,1,1

def init_db():
    mydb = mysql.connector.connect(
        host="kafka-mysql",
        user="root",
        password="11111111"
    )
    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE IF NOT EXISTS kafka")
    mycursor.execute("USE kafka")
    return mydb, mycursor

def create_table(mycursor):
    mycursor.execute("CREATE TABLE IF NOT EXISTS Patient (id INT AUTO_INCREMENT PRIMARY KEY, age INT, sex INT, cp INT, trtbps INT, chol INT, fbs INT, restecg INT, thalachh INT, exng INT, oldpeak FLOAT, slp INT, caa INT, thall INT, prediction INT, timestamp TIMESTAMP)")

def insert_data(mycursor, data):
    sql = "INSERT INTO Patient (age, sex, cp, trtbps, chol, fbs, restecg, thalachh, exng, oldpeak, slp, caa, thall, prediction, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = data["age"], data["sex"], data["cp"], data["trtbps"], data["chol"], data["fbs"], data["restecg"], data["thalachh"], data["exng"], data["oldpeak"], data["slp"], data["caa"], data["thall"], data["prediction"], datetime.datetime.now().date()
    mycursor.execute(sql, val)

def check_data(data):
    # check data type
    if not (type(data['age']) is int or type(data['age']) is float):
        return False
    if not (type(data['sex']) is int or type(data['sex']) is float):
        return False
    if not (type(data['cp']) is int or type(data['cp']) is float):
        return False
    if not (type(data['trtbps']) is int or type(data['trtbps']) is float):
        return False
    if not (type(data['chol']) is int or type(data['chol']) is float):
        return False
    if not (type(data['fbs']) is int or type(data['fbs']) is float):
        return False
    if not (type(data['restecg']) is int or type(data['restecg']) is float):
        return False
    if not (type(data['thalachh']) is int or type(data['thalachh']) is float):
        return False
    if not (type(data['exng']) is int or type(data['exng']) is float):
        return False
    if not (type(data['oldpeak']) is int or type(data['oldpeak']) is float):
        return False
    if not (type(data['slp']) is int or type(data['slp']) is float):
        return False
    if not (type(data['caa']) is int or type(data['caa']) is float):
        return False
    if not (type(data['thall']) is int or type(data['thall']) is float):
        return False
    return True


if __name__ == "__main__":
    #server = '0.0.0.0:29092'
    server = os.environ['SERVERS_K']
    topic = os.environ['TOPIC_P']
    is_connected = False
    retry = 20
    while not is_connected and retry > 0:
        try:
            mydb, mycursor = init_db()
            is_connected = True
        except:
            print("Waiting for database...")
            time.sleep(5)
            retry -= 1
    if not is_connected:
        print("Database connection failed.")
        exit(1)
    mydb, mycursor = init_db()
    create_table(mycursor)
    consumer = Consumer(server, topic).consumer
    for msg in consumer:
        value = msg.value
        if not check_data(value):
            print("Wrong data format.")
            continue
        insert_data(mycursor, value)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")

