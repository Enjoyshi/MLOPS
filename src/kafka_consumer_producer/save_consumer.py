from kafka import KafkaConsumer
import json
import mysql.connector
from utils import Consumer

# data col : age,sex,cp,trtbps,chol,fbs,restecg,thalachh,exng,oldpeak,slp,caa,thall
# data : 57,1,0,150,276,0,0,112,1,0.6,1,1,1

def init_db():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="11111111",
        port="3309"
    )
    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE IF NOT EXISTS kafka")
    mycursor.execute("USE kafka")
    return mydb, mycursor

def create_table(mycursor):
    mycursor.execute("CREATE TABLE IF NOT EXISTS Patient (id INT AUTO_INCREMENT PRIMARY KEY, age INT, sex INT, cp INT, trtbps INT, chol INT, fbs INT, restecg INT, thalachh INT, exng INT, oldpeak FLOAT, slp INT, caa INT, thall INT, prediction INT)")

def insert_data(mycursor, data):
    sql = "INSERT INTO Patient (age, sex, cp, trtbps, chol, fbs, restecg, thalachh, exng, oldpeak, slp, caa, thall, prediction) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = data["age"], data["sex"], data["cp"], data["trtbps"], data["chol"], data["fbs"], data["restecg"], data["thalachh"], data["exng"], data["oldpeak"], data["slp"], data["caa"], data["thall"], data["prediction"]
    mycursor.execute(sql, val)



if __name__ == "__main__":
    server = '0.0.0.0:29092'
    topic = 'Save'

    consumer = Consumer(server, topic).consumer
    mydb, mycursor = init_db()
    create_table(mycursor)
    for msg in consumer:
        value = msg.value
        insert_data(mycursor, value)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")

