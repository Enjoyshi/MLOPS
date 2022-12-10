from fastapi import FastAPI, Response
import mysql.connector
import pandas as pd
import numpy as np
# from eurybia import SmartDrift
from datetime import datetime
import os

app = FastAPI()

def connect_db():
    """
    mydb = mysql.connector.connect(
        host="kafka-mysql",
        user="root",
        password="11111111",
        database="kafka"
    )
    """
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="11111111",
        database="kafka",
        port="3309"
    )
    mycursor = mydb.cursor()
    return mydb, mycursor

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/data")
def read_data():
    mydb, mycursor = connect_db()
    mycursor.execute("SELECT * FROM Patient")
    myresult = mycursor.fetchall()
    return myresult

@app.get("/ref_data")
def read_ref_data():
    mydb, mycursor = connect_db()
    mycursor.execute("SELECT * FROM Ref")
    myresult = mycursor.fetchall()
    return myresult

@app.get("/fill_refdb")
def fill_db():
    mydb, mycursor = connect_db()
    df = pd.read_csv("train.csv")
    df.drop("output", axis=1, inplace=True)

    print('Connected to database')
    mycursor.execute("DROP TABLE IF EXISTS Ref")
    mycursor.execute("CREATE TABLE Ref (id INT AUTO_INCREMENT PRIMARY KEY, age INT, sex INT, cp INT, trtbps INT, chol INT, fbs INT, restecg INT, thalachh INT, exng INT, oldpeak FLOAT, slp INT, caa INT, thall INT)")
    print('Created table')
    for i, row in df.iterrows():
        sql = "INSERT INTO Ref (age, sex, cp, trtbps, chol, fbs, restecg, thalachh, exng, oldpeak, slp, caa, thall) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        mycursor.execute(sql, tuple(row))
        mydb.commit()
    print("Database filled")
    return Response(status_code=200)

"""

@app.post("/data_drift")
def data_drift(data: dict):
    download = data['Download']
    print(download)

    mydb, mycursor = connect_db()
    sql_current = "SELECT * FROM Patient"
    # check if Ref table exists
    mycursor.execute("SHOW TABLES LIKE 'Ref'")
    if mycursor.fetchone() is None:
        df = pd.read_csv("train.csv")
        df.drop("output", axis=1, inplace=True)
        mycursor.execute("CREATE TABLE Ref (id INT AUTO_INCREMENT PRIMARY KEY, age INT, sex INT, cp INT, trtbps INT, chol INT, fbs INT, restecg INT, thalachh INT, exng INT, oldpeak FLOAT, slp INT, caa INT, thall INT)")
        for i, row in df.iterrows():
            sql = "INSERT INTO Ref (age, sex, cp, trtbps, chol, fbs, restecg, thalachh, exng, oldpeak, slp, caa, thall) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            mycursor.execute(sql, tuple(row))
            mydb.commit()
    
    sql_base = "SELECT * FROM Ref"

    df_base = pd.read_sql(sql_base, mydb)
    df_current = pd.read_sql(sql_current, mydb)
    if df_current.empty:
        return Response(status_code=400)
    df_current.drop(["id", "prediction", "timestamp"], axis=1, inplace=True)
    df_base.drop("id", axis=1, inplace=True)

    drift = SmartDrift(df_current= df_current, df_baseline= df_base)

    date = datetime.now()
    date_timestamp = str(date.timestamp()).split('.')[0]

    drift.compile(full_validation=True, datadrift_file = "heartattack.csv")

    if download:
        html_file = f"../drift_report_{date_timestamp}.html"
        drift.generate_report(html_file, title_story=f"Drift report on {date.strftime('%d/%m/%Y')}")
        with open(html_file, "r") as f:
            html = f.read()
        os.remove(html_file)
        return Response(content=html, media_type="text/html", status_code=200)

    auc = drift.auc
    return {"auc": auc}
"""

@app.post("/get_data")
def get_data(data: dict):
    start = data['start']
    if 'end' not in data:
        # today date to str format
        end = datetime.now().strftime("%Y-%m-%d")
    else:
        end = data['end']
    # Check if start and end are valid
    if start > end:
        return Response(status_code=400)
    
    mydb, mycursor = connect_db()
    sql = "SELECT * FROM Patient WHERE timestamp BETWEEN %s AND %s"
    mycursor.execute(sql, (start, end))
    myresult = mycursor.fetchall()

    # transform myresult to dict
    myresult = [dict(zip(mycursor.column_names, row)) for row in myresult]
    return {'result' : myresult}