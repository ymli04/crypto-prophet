import requests
import pandas as pd
import sqlite3
import schedule
import time

# 连接 SQLite 数据库（如果不存在会自动创建）
conn = sqlite3.connect("crypto.db")
cursor = conn.cursor()

# 创建 BTC OHLC 数据表
cursor.execute("""
CREATE TABLE IF NOT EXISTS btc_ohlc (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp BIGINT,
    open FLOAT,
    high FLOAT,
    low FLOAT,
    close FLOAT,
    volume FLOAT
)
""")
conn.commit()

# 获取 BTC 价格数据
def fetch_btc_ohlc():
    url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m&limit=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()[0]
        ohlc = (int(data[0]), float(data[1]), float(data[2]), float(data[3]), float(data[4]), float(data[5]))

        # 插入数据
        cursor.execute("INSERT INTO btc_ohlc (timestamp, open, high, low, close, volume) VALUES (?, ?, ?, ?, ?, ?)", ohlc)
        conn.commit()
        print(f"📊 插入数据：{ohlc}")

    else:
        print("❌ 获取 BTC OHLC 数据失败")

# 每 0.5 秒执行一次
schedule.every(0.5).seconds.do(fetch_btc_ohlc)

if __name__ == "__main__":
    print("🚀 开始爬取 BTC 数据...")
    while True:
        schedule.run_pending()
        time.sleep(0.1)
