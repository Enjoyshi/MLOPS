from fastapi import FastAPI
import mysql.connector

app = FastAPI()

def connect_db():
    mydb = mysql.connector.connect(
        host="kafka-mysql",
        user="root",
        password="11111111",
    )
    mycursor = mydb.cursor()
    return mydb, mycursor

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/data")
def read_data():
    mydb, mycursor = connect_db()
    mycursor.execute("SELECT * FROM kafka.Patient")
    myresult = mycursor.fetchall()
    return myresult

