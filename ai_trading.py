import random
import numpy as np
from sklearn.linear_model import LinearRegression

class Market:
    def __init__(self):
        self.usdt_pool = 100000000  
        self.btc_pool = 1000000  
        self.btc_supply = 1000000  
        self.price = 1000  
        self.mvrv = 2  
        self.nupl = 0.5  
        self.tiv = 1000  
        self.value_variable = 0  
        self.market_value_variable = 1  
        self.historical_data = []  

        # **初始化 AI 预测模型**
        self.model_mvrv = None
        self.model_nupl = None
        self.model_tiv = None

    def adjust_market_funds(self):
        """ 根据市场价值变量调整 USDT 和 BTC 资金池 """
        expected_usdt = (self.usdt_pool + self.btc_pool) * 0.5  
        capital_flow = (expected_usdt - self.usdt_pool) * 0.1  
        self.usdt_pool += capital_flow
        self.btc_pool -= capital_flow  

    def calculate_btc_price(self, total_spot_position, total_leverage_position):
        """ 计算 BTC 价格（基于市场总价值计算） """
        market_cap = total_spot_position + total_leverage_position + self.usdt_pool  
        self.price = market_cap / self.btc_supply  
        print(f"📈 BTC 最新价格: {self.price:.2f} USDT")

    def display_market(self):
        """ **显示市场状态** """
        print(f"📊 **市场情况：USDT {self.usdt_pool:.2f} | BTC {self.btc_pool:.2f} | BTC 价格: {self.price:.2f} USDT**")

    def record_data(self):
        """ 记录市场数据用于 AI 训练 """
        self.historical_data.append([self.mvrv, self.nupl, self.tiv])

    def train_ai(self):
        """ 训练 AI 预测市场变量 """
        if len(self.historical_data) < 20:
            return  

        data = np.array(self.historical_data)
        X = data[:-1, :]  
        y_mvrv = data[1:, 0]  
        y_nupl = data[1:, 1]  
        y_tiv = data[1:, 2]  

        self.model_mvrv = LinearRegression().fit(X, y_mvrv)
        self.model_nupl = LinearRegression().fit(X, y_nupl)
        self.model_tiv = LinearRegression().fit(X, y_tiv)

        print("✅ AI 训练完成，优化市场预测能力！")

    def predict_future_market(self):
        """ **预测未来市场变量（修正 AI 训练未完成的情况）** """
        if self.model_mvrv is None or self.model_nupl is None or self.model_tiv is None:
            print("⚠️ AI 预测模型未训练，返回当前市场变量")
            return self.mvrv, self.nupl, self.tiv  

        X_latest = np.array([self.historical_data[-1]])
        pred_mvrv = self.model_mvrv.predict(X_latest)[0]
        pred_nupl = self.model_nupl.predict(X_latest)[0]
        pred_tiv = self.model_tiv.predict(X_latest)[0]

        return pred_mvrv, pred_nupl, pred_tiv

    def update_value_variable(self):
        """ **更新市场变量（结合 AI 预测优化）** """
        self.mvrv += random.uniform(-0.1, 0.1)  
        self.nupl += random.uniform(-0.05, 0.05)  
        self.tiv += random.uniform(-2, 2)  

        self.mvrv = max(0.5, min(4.5, self.mvrv))  
        self.nupl = max(-0.3, min(0.8, self.nupl))  
        self.tiv = max(950, min(1050, self.tiv))  

        # 记录数据用于 AI 训练
        self.record_data()

        # AI 预测
        pred_mvrv, pred_nupl, pred_tiv = self.predict_future_market()

        print(f"📊 **预测市场变量：MVRV {pred_mvrv:.2f} | NUPL {pred_nupl:.2f} | TIV {pred_tiv:.2f}**")

# **运行 AI 训练**
if __name__ == "__main__":
    market = Market()
    for _ in range(50):
        market.update_value_variable()
        market_price = random.uniform(950, 1050)

        print(f"\n📊 当前市场价格: {market_price:.2f}")

        market.adjust_market_funds()
        market.display_market()

        if _ % 10 == 0:  
            market.train_ai()
