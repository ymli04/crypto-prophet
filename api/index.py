from fastapi import FastAPI
import pandas as pd
import sqlite3
import subprocess

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Crypto Prophet API is running!"}

@app.get("/fetch")
def fetch_and_update():
    result = subprocess.run(["python", "fetch_data.py"], capture_output=True, text=True)
    return {"status": "success", "log": result.stdout}

@app.get("/data")
def get_data():
    try:
        conn = sqlite3.connect("crypto.db")
        query = "SELECT * FROM btc_data ORDER BY timestamp DESC LIMIT 100;"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}
