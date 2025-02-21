import requests
import pandas as pd
import sqlite3
import schedule
import time

# 连接 SQLite 数据库
conn = sqlite3.connect("crypto.db")
cursor = conn.cursor()

# **创建数据表**
cursor.execute("""
CREATE TABLE IF NOT EXISTS btc_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp BIGINT,
    open FLOAT,
    high FLOAT,
    low FLOAT,
    close FLOAT,
    volume FLOAT,
    market_cap FLOAT,
    total_supply FLOAT,
    price FLOAT
)
""")
conn.commit()

# **从 CoinGecko 获取 BTC 数据**
def fetch_data():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        
        market_data = data["market_data"]
        timestamp = int(time.time())  # 获取当前时间戳（秒）
        open_price = market_data["current_price"]["usd"]
        high_price = market_data["high_24h"]["usd"]
        low_price = market_data["low_24h"]["usd"]
        close_price = market_data["current_price"]["usd"]
        volume = market_data["total_volume"]["usd"]
        market_cap = market_data["market_cap"]["usd"]
        total_supply = market_data["total_supply"]
        price = market_data["current_price"]["usd"]

        latest = (timestamp, open_price, high_price, low_price, close_price, volume, market_cap, total_supply, price)
        
        # **存入数据库**
        cursor.execute("""
        INSERT INTO btc_data (timestamp, open, high, low, close, volume, market_cap, total_supply, price)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, latest)
        conn.commit()
        
        print(f"📊 插入数据：{latest}")

    else:
        print("❌ 获取 BTC 数据失败")

# **定时爬取，每 5 秒运行一次**
schedule.every(5).seconds.do(fetch_data)

if __name__ == "__main__":
    print("🚀 开始爬取 BTC 数据...")
    while True:
        schedule.run_pending()
        time.sleep(1)
