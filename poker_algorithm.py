import sqlite3
import pandas as pd
import random

# **连接 SQLite 数据库**
conn = sqlite3.connect("crypto.db")

# **读取市场数据**
query = """
SELECT timestamp, market_cap, price, volume, mvrv, nupl
FROM btc_data
ORDER BY timestamp DESC
LIMIT 100;
"""
df = pd.read_sql_query(query, conn)
conn.close()

# **处理 NaN 数据**
df["mvrv"] = df["mvrv"].fillna(2)  # 默认 MVRV = 2
df["nupl"] = df["nupl"].fillna(0.5)  # 默认 NUPL = 0.5

# **计算 MVRV 变量**
def normalize_mvrv(mvrv):
    if mvrv >= 4:
        return 10
    elif mvrv <= 0.8:
        return -10
    else:
        return (mvrv - 2) / 2 * 10  # 归一化到 -10 ~ 10

df["mvrv_score"] = df["mvrv"].apply(normalize_mvrv)

# **计算 NUPL 变量**
def normalize_nupl(nupl):
    if nupl >= 0.75:
        return 10
    elif nupl <= -0.28:
        return -10
    else:
        return (nupl - 0.5) / 0.25 * 10  # 归一化到 -10 ~ 10

df["nupl_score"] = df["nupl"].apply(normalize_nupl)

# **计算 TIV 变量**
high = df["price"].max()
low = df["price"].min()

def normalize_tiv(price):
    if high == low:
        return 0  # 防止除零错误
    return ((price - low) / (high - low)) * 20 - 10  # 归一化到 -10 ~ 10

df["tiv_score"] = df["price"].apply(normalize_tiv)

# **计算短期波动变量**
def calculate_short_term_trend(prices):
    highest = max(prices)
    lowest = min(prices)
    current = prices[-1]

    # 计算短期涨跌幅
    change = ((current - lowest) / (highest - lowest)) * 20 - 10
    return max(-10, min(10, change))  # 限制范围 -10~10

df["short_term_trend"] = df["price"].rolling(5).apply(lambda x: calculate_short_term_trend(x), raw=True)

# **计算场外变量（随机模拟新闻影响，范围 -10~10）**
def random_news_impact():
    return random.uniform(-10, 10)  # 假设新闻影响随机变化

df["news_impact"] = df["timestamp"].apply(lambda x: random_news_impact())

# **分析变量趋势**
def analyze_trend(x):
    if len(x) < 2:
        return 0  # 不足两条数据，不判断趋势
    prev_value = x[-2]  # 直接用索引，而不是 .iloc
    current_value = x[-1]
    if prev_value < current_value:
        return abs(current_value)  # 趋势向上，保留正数
    elif prev_value > current_value:
        return -abs(current_value)  # 趋势向下，变成负数
    return 0  # 变量无变化

df["mvrv_trend"] = df["mvrv_score"].rolling(2).apply(analyze_trend, raw=True)
df["nupl_trend"] = df["nupl_score"].rolling(2).apply(analyze_trend, raw=True)
df["tiv_trend"] = df["tiv_score"].rolling(2).apply(analyze_trend, raw=True)
df["short_term_trend"] = df["short_term_trend"].rolling(2).apply(analyze_trend, raw=True)
df["news_trend"] = df["news_impact"].rolling(2).apply(analyze_trend, raw=True)

# **计算最终市场变量**
df["final_value"] = df[["mvrv_trend", "nupl_trend", "tiv_trend", "short_term_trend", "news_trend"]].mean(axis=1)

# **打印调试信息**
print("✅ 计算后的市场变量：")
print(df[["timestamp", "mvrv_trend", "nupl_trend", "tiv_trend", "short_term_trend", "news_trend", "final_value"]].head())

# **存储为 CSV**
df.to_csv("market_variables.csv", index=False)
print("✅ 数据整合完成，已保存为 market_variables.csv")
