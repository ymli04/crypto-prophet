import random

# **定义玩家类**
class Player:
    def __init__(self, name, capital, risk_tolerance, weights):
        self.name = name  # 玩家名称
        self.capital = capital  # 资金量
        self.risk_tolerance = risk_tolerance  # 风险承受能力
        self.weights = weights  # 交易决策权重
        self.position = 0  # 持仓量
        self.trades = []  # 交易记录

    def make_decision(self, market_vars):
        """
        根据市场变量 + 权重 计算交易信号。
        market_vars = {
            "mvrv": 2.5,
            "nupl": 0.3,
            "tiv": 1.5
        }
        """
        total_score = (
            market_vars["mvrv"] * self.weights["mvrv"] +
            market_vars["nupl"] * self.weights["nupl"] +
            market_vars["tiv"] * self.weights["tiv"]
        )

        if total_score > 1.5:  # 交易门槛降低
            self.buy(total_score)
        elif total_score < -1.5:
            self.sell(total_score)
        else:
            print(f"{self.name} 持仓不变")

    def buy(self, market_value):
        buy_amount = self.capital * 0.1  # 买入 10% 资金
        self.position += buy_amount
        self.capital -= buy_amount
        self.trades.append(f"BUY {buy_amount} at {market_value}")
        print(f"{self.name} 买入 {buy_amount} BTC at 市场值 {market_value}")

    def sell(self, market_value):
        if self.position > 0:
            sell_amount = self.position * 0.5  # 卖出 50% 持仓
            self.position -= sell_amount
            self.capital += sell_amount
            self.trades.append(f"SELL {sell_amount} at {market_value}")
            print(f"{self.name} 卖出 {sell_amount} BTC at 市场值 {market_value}")

# **玩家权重**
player_weights = {
    "whale": {"mvrv": 0.6, "nupl": 0.3, "tiv": 0.1},
    "rich": {"mvrv": 0.5, "nupl": 0.4, "tiv": 0.1},
    "middle_class": {"mvrv": 0.3, "nupl": 0.4, "tiv": 0.3},
    "retail": {"mvrv": 0.2, "nupl": 0.5, "tiv": 0.3},
    "leverage": {"mvrv": 0.1, "nupl": 0.1, "tiv": 0.8}
}

# **创建五类玩家**
players = [
    Player("🐋 鲸鱼", capital=1000000, risk_tolerance="低", weights=player_weights["whale"]),
    Player("🏦 富豪", capital=500000, risk_tolerance="中", weights=player_weights["rich"]),
    Player("💰 富人", capital=100000, risk_tolerance="中高", weights=player_weights["middle_class"]),
    Player("🏠 平民", capital=5000, risk_tolerance="高", weights=player_weights["retail"]),
    Player("🔥 杠杆", capital=1000, risk_tolerance="极高", weights=player_weights["leverage"]),
]

# **模拟玩家决策**
def simulate_poker_algorithm():
    # 假设市场变量
    market_vars = {
        "mvrv": random.uniform(0.5, 5),
        "nupl": random.uniform(-0.3, 0.8),
        "tiv": random.uniform(-10, 10)
    }

    print(f"\n📊 当前市场变量：{market_vars}")

    for player in players:
        player.make_decision(market_vars)

# **运行模拟**
if __name__ == "__main__":
    simulate_poker_algorithm()
