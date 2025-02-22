import random

# **定义玩家类**
class Player:
    def __init__(self, name, capital, risk_tolerance, weights, trade_frequency):
        self.name = name  # 玩家名称
        self.capital = capital  # 资金量
        self.risk_tolerance = risk_tolerance  # 风险承受能力
        self.weights = weights  # 交易决策权重
        self.trade_frequency = trade_frequency  # 交易频率 (固定值)
        self.position = 0  # 持仓量
        self.trades = []  # 交易记录

    def make_decision(self, market_vars):
        """
        根据市场变量 + 交易频率 计算交易信号。
        market_vars = {
            "value_variable": 2.5,
            "short_term_variable": 1.3,
            "external_variable": 0.0
        }
        """
        total_score = (
            market_vars["value_variable"] * self.weights["value"] +
            market_vars["short_term_variable"] * self.weights["short_term"] +
            market_vars["external_variable"] * self.weights["external"]
        )

        if total_score > self.trade_frequency:  # 交易门槛
            self.buy(total_score)
        elif total_score < -self.trade_frequency:
            self.sell(total_score)
        else:
            print(f"{self.name} 持仓不变 (交易频率: {self.trade_frequency}, 总评分: {total_score:.2f})")

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

# **玩家权重（影响三种市场变量）**
player_weights = {
    "whale": {"value": 0.7, "short_term": 0.2, "external": 0.1},
    "rich": {"value": 0.5, "short_term": 0.3, "external": 0.2},
    "middle_class": {"value": 0.3, "short_term": 0.5, "external": 0.2},
    "retail": {"value": 0.2, "short_term": 0.3, "external": 0.5},
    "leverage": {"value": 0.1, "short_term": 0.8, "external": 0.1}
}

# **交易频率**
player_trade_frequencies = {
    "whale": 6,
    "rich": 5,
    "middle_class": 4,
    "retail": 1,
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

# **模拟玩家决策**
def simulate_poker_algorithm():
    # 假设市场变量（从 `market_variables.csv` 读取数据）
    market_vars = {
        "value_variable": random.uniform(-10, 10),  # 价值变量
        "short_term_variable": random.uniform(-10, 10),  # 短期波动变量
        "external_variable": 0.0  # 场外变量，默认 0，后续接入 ChatGPT
    }

    print(f"\n📊 当前市场变量：{market_vars}")

    for player in players:
        player.make_decision(market_vars)

# **运行模拟**
if __name__ == "__main__":
    simulate_poker_algorithm()
