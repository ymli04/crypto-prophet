import random

class Market:
    def __init__(self):
        self.usdt_pool = 100000000  
        self.btc_pool = 1000000  
        self.total_funds = self.usdt_pool + self.btc_pool  
        self.capital_flow = 0  # 资金流入流出

    def adjust_market_funds(self, value_variable):
        """ 根据价值变量调整 USDT 和 BTC 资金池 """
        net_funds = self.usdt_pool + self.btc_pool
        expected_usdt = net_funds * 0.5  # 目标 USDT 占比
        self.capital_flow = (expected_usdt - self.usdt_pool) * 0.1  # 资金流入流出 10%
        self.usdt_pool += self.capital_flow
        self.btc_pool -= self.capital_flow

    def display_market(self):
        print(f"📊 资金池情况：USDT {self.usdt_pool:.2f} | BTC {self.btc_pool:.2f} | 资金流动: {self.capital_flow:.2f}")

class Player:
    def __init__(self, name, capital):
        self.name = name
        self.capital = capital
        self.position = {
            "USDT": capital * 0.5,  
            "long": capital * 0.25,  
            "short": capital * 0.15,  
            "holding": capital * 0.10  
        }

    def adjust_positions(self, market):
        """ 确保持仓平衡（总持仓 = USDT - 资金流入流出） """
        total_positions = self.position["long"] + self.position["short"] + self.position["holding"]
        expected_positions = self.position["USDT"] + total_positions
        net_funds = market.usdt_pool + market.btc_pool
        expected_usdt = net_funds * 0.5 - market.capital_flow  # 修正 USDT 资金流入流出

        if abs(expected_positions - expected_usdt) > 1e-5:
            adjust_factor = expected_usdt / expected_positions
            self.position["long"] *= adjust_factor
            self.position["short"] *= adjust_factor
            self.position["holding"] *= adjust_factor
            self.position["USDT"] = expected_usdt - (self.position["long"] + self.position["short"] + self.position["holding"])
            print(f"⚖ {self.name} 进行平仓调整（修正后 USDT: {expected_usdt:.2f}）")

# **玩家初始化**
players = [
    Player("🐋 鲸鱼", capital=1000000),
    Player("🏦 富豪", capital=500000),
    Player("💰 富人", capital=100000),
    Player("🏠 平民", capital=5000)
]

# **运行交易模拟**
if __name__ == "__main__":
    market = Market()
    for _ in range(5):
        market.adjust_market_funds(random.uniform(-10, 10))
        market.display_market()

        for player in players:
            player.adjust_positions(market)
