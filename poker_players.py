import random
import time

class Player:
    def __init__(self, name, capital, risk_tolerance, weights, trade_frequency):
        self.name = name  
        self.capital = capital  
        self.risk_tolerance = risk_tolerance  
        self.weights = weights  
        self.trade_frequency = trade_frequency  
        self.position = {
            "long": capital * 0.2,  # 初始持有 20% 资金的 BTC，确保能卖出
            "short": 0, 
            "holding": 0, 
            "USDT": capital * 0.8  # 剩下 80% 为 USDT
        }  
        self.trades = []  

    def make_decision(self, market_vars):
        """ 计算市场变量影响，并调整仓位 """
        total_score = (
            market_vars["value_variable"] * self.weights["value"] +
            market_vars["short_term_variable"] * self.weights["short_term"] +
            market_vars["external_variable"] * self.weights["external"]
        )

        print(f"DEBUG: {self.name} | 交易频率: {self.trade_frequency} | 总评分: {total_score:.2f}")

        if abs(total_score) > self.trade_frequency:  
            if total_score > 0:
                self.buy(total_score)
            else:
                self.sell(total_score)
        else:
            print(f"{self.name} 持仓不变 (交易频率: {self.trade_frequency}, 总评分: {total_score:.2f})")

    def buy(self, market_value):
        """ 买入逻辑：调整 USDT -> 多单 / 长期持有 """
        buy_amount = self.position["USDT"] * 0.1  
        self.position["long"] += buy_amount * 0.7  
        self.position["holding"] += buy_amount * 0.3  
        self.position["USDT"] -= buy_amount
        self.trades.append(f"BUY {buy_amount} at {market_value}")
        print(f"{self.name} 买入 {buy_amount} BTC at 市场值 {market_value}")

    def sell(self, market_value):
        """ 卖出逻辑：减少持仓，转为 USDT """
        if self.position["long"] > 0:
            sell_amount = self.position["long"] * 0.5  
            self.position["long"] -= sell_amount
            self.position["USDT"] += sell_amount
            self.trades.append(f"SELL {sell_amount} at {market_value}")
            print(f"{self.name} 卖出 {sell_amount} BTC at 市场值 {market_value}")
        else:
            print(f"{self.name} 无法卖出，持仓为 0")

# **玩家权重**
player_weights = {
    "whale": {"value": 0.7, "short_term": 0.2, "external": 0.1},
    "rich": {"value": 0.5, "short_term": 0.3, "external": 0.2},
    "middle_class": {"value": 0.3, "short_term": 0.5, "external": 0.2},
    "retail": {"value": 0.2, "short_term": 0.3, "external": 0.5},
    "leverage": {"value": 0.1, "short_term": 0.8, "external": 0.1}
}

# **交易频率**
player_trade_frequencies = {
    "whale": 3,   
    "rich": 2.5,  
    "middle_class": 2,  
    "retail": 0.5,  
    "leverage": 0
}

# **创建五类玩家**
players = [
    Player("🐋 鲸鱼", capital=1000000, risk_tolerance="低", weights=player_weights["whale"], trade_frequency=player_trade_frequencies["whale"]),
    Player("🏦 富豪", capital=500000, risk_tolerance="中", weights=player_weights["rich"], trade_frequency=player_trade_frequencies["rich"]),
    Player("💰 富人", capital=100000, risk_tolerance="中高", weights=player_weights["middle_class"], trade_frequency=player_trade_frequencies["middle_class"]),
    Player("🏠 平民", capital=5000, risk_tolerance="高", weights=player_weights["retail"], trade_frequency=player_trade_frequencies["retail"]),
    Player("🔥 杠杆", capital=1000, risk_tolerance="极高", weights=player_weights["leverage"], trade_frequency=player_trade_frequencies["leverage"]),
]

# **测试函数**
def test_poker_algorithm():
    market_vars = {
        "value_variable": random.uniform(-10, 10),  
        "short_term_variable": random.uniform(-10, 10),  
        "external_variable": random.uniform(-5, 5)  
    }

    print(f"\n📊 当前市场变量：{market_vars}")

    for player in players:
        player.make_decision(market_vars)

# **运行测试**
if __name__ == "__main__":
    test_poker_algorithm()
