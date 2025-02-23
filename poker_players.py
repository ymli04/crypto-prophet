import random

class Market:
    def __init__(self):
        self.usdt_pool = 100000000  
        self.btc_pool = 1000000  
        self.total_funds = self.usdt_pool + self.btc_pool  
        self.capital_flow = 0  

    def adjust_market_funds(self, value_variable):
        """ 根据价值变量调整 USDT 和 BTC 资金池 """
        net_funds = self.usdt_pool + self.btc_pool
        expected_usdt = net_funds * 0.5  
        self.capital_flow = (expected_usdt - self.usdt_pool) * 0.1  
        self.usdt_pool += self.capital_flow
        self.btc_pool -= self.capital_flow

    def display_market(self):
        print(f"📊 资金池情况：USDT {self.usdt_pool:.2f} | BTC {self.btc_pool:.2f} | 资金流动: {self.capital_flow:.2f}")

class Player:
    def __init__(self, name, capital, reversal_threshold):
        self.name = name
        self.capital = capital
        self.reversal_threshold = reversal_threshold  
        self.position = {
            "USDT": capital * 0.5,  
            "long": capital * 0.25,  
            "short": capital * 0.15,  
            "holding": capital * 0.10  
        }

    def make_decision(self, value_variable):
        """ 玩家基于价值变量决策交易 """
        abs_value = abs(value_variable)

        # **反转预警触发**
        if abs_value >= self.reversal_threshold:
            print(f"⚠ {self.name} 触发反转预警（阈值: {self.reversal_threshold}）")
            if value_variable > 0:
                self.sell(value_variable)
            else:
                self.buy(value_variable)
        else:
            print(f"{self.name} 继续正常交易（当前价值变量: {value_variable:.2f}）")

    def buy(self, market_value):
        """ 反向交易（买入） """
        buy_amount = self.position["USDT"] * 0.05  
        self.position["long"] += buy_amount * 0.7  
        self.position["holding"] += buy_amount * 0.3  
        self.position["USDT"] -= buy_amount
        print(f"{self.name} 反向买入 {buy_amount} BTC at 市场值 {market_value}")

    def sell(self, market_value):
        """ 反向交易（卖出） """
        sell_amount = self.position["long"] * 0.5  
        self.position["long"] -= sell_amount
        self.position["USDT"] += sell_amount
        print(f"{self.name} 反向卖出 {sell_amount} BTC at 市场值 {market_value}")

    def adjust_positions(self, market):
        """ 确保持仓平衡 """
        total_positions = self.position["long"] + self.position["short"] + self.position["holding"]
        expected_positions = self.position["USDT"] + total_positions
        net_funds = market.usdt_pool + market.btc_pool
        expected_usdt = net_funds * 0.5 - market.capital_flow  

        if abs(expected_positions - expected_usdt) > 1e-5:
            adjust_factor = expected_usdt / expected_positions
            self.position["long"] *= adjust_factor
            self.position["short"] *= adjust_factor
            self.position["holding"] *= adjust_factor
            self.position["USDT"] = expected_usdt - (self.position["long"] + self.position["short"] + self.position["holding"])
            print(f"⚖ {self.name} 进行平仓调整（修正后 USDT: {expected_usdt:.2f}）")

# **玩家初始化**
players = [
    Player("🐋 鲸鱼", capital=1000000, reversal_threshold=8),
    Player("🏦 富豪", capital=500000, reversal_threshold=7),
    Player("💰 富人", capital=100000, reversal_threshold=6),
    Player("🏠 平民", capital=5000, reversal_threshold=5)
]

# **运行交易模拟**
if __name__ == "__main__":
    market = Market()
    for _ in range(5):
        value_variable = random.uniform(-10, 10)
        print(f"\n📊 当前价值变量：{value_variable:.2f}")

        market.adjust_market_funds(value_variable)
        market.display_market()

        for player in players:
            player.make_decision(value_variable)
        
        for player in players:
            player.adjust_positions(market)
