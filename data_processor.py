import sqlite3
import pandas as pd

# 连接 SQLite 数据库
conn = sqlite3.connect("crypto.db")

# **读取 BTC 数据**
query = """
SELECT timestamp, open, high, low, close, volume, market_cap, total_supply, price
FROM btc_data
ORDER BY timestamp DESC
LIMIT 100;
"""
df = pd.read_sql_query(query, conn)

# 关闭数据库连接
conn.close()

# **转换 `timestamp` 为 `datetime`**
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s", errors="coerce")

# **打印数据**
print("✅ 处理后的数据样本：")
print(df.head())

# **存储为 CSV 以便检查**
df.to_csv("merged_data.csv", index=False)
print("✅ 数据整合完成，已保存为 merged_data.csv")
