from fastapi import FastAPI, Response
import mysql.connector
import joblib
import pandas as pd
import numpy as np
from eurybia import SmartDrift
from datetime import datetime
import os

app = FastAPI()

def connect_db():
    mydb = mysql.connector.connect(
        host="kafka-mysql",
        user="root",
        password="11111111",
        database="kafka"
    )
    mycursor = mydb.cursor()
    return mydb, mycursor

def load_model(path):
    model = joblib.load(path)
    return model


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


@app.get("/data_drift")
def data_drift():
    mydb, mycursor = connect_db()
    sql_current = "SELECT * FROM Patient"
    sql_base = "SELECT * FROM Ref"

    df_base = pd.read_sql(sql_base, mydb)
    df_current = pd.read_sql(sql_current, mydb)
    df_current.drop(["id", "prediction"], axis=1, inplace=True)
    df_base.drop("id", axis=1, inplace=True)
    # model = load_model("../svm_model.joblib")

    drift = SmartDrift(df_current= df_current, df_baseline= df_base)
    

    date = datetime.now().timestamp()
    date = str(date).split('.')[0]

    drift.compile(full_validation=True, date_compile_auc='01/01/2022', datadrift_file=f"../datadrift_auc_{date}.csv")
    html_file = f"../drift_report_{date}.html"

    drift.generate_report(html_file, title_story=f"Drift report on {date}")
    with open(html_file, "r") as f:
        html = f.read()
    
    return Response(content=html, media_type="text/html")