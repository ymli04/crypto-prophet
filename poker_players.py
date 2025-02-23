import random

class Market:
    def __init__(self):
        self.usdt_pool = 100000000  # 初始 USDT 池
        self.btc_pool = 1000000  # 初始 BTC 池
        self.total_funds = self.usdt_pool + self.btc_pool  # 总资金量
        self.player_ratios = {
            "whale": 0.12,  
            "rich": 0.17,  
            "middle_class": 0.16,  
            "retail": 0.26,  
            "leverage": 0.29  
        }

    def adjust_market_funds(self, value_variable):
        """ 根据价值变量调整 USDT 和 BTC 资金池，并重新计算玩家比例 """
        if value_variable > 0:  
            inflow = self.usdt_pool * (value_variable / 10) * 0.05  
            self.usdt_pool -= inflow
            self.btc_pool += inflow
        else:  
            outflow = self.btc_pool * (abs(value_variable) / 10) * 0.05  
            self.btc_pool -= outflow
            self.usdt_pool += outflow

        self.total_funds = self.usdt_pool + self.btc_pool  

        btc_ratio = self.btc_pool / self.total_funds
        self.player_ratios["whale"] = btc_ratio * 0.12  
        self.player_ratios["rich"] = btc_ratio * 0.17
        self.player_ratios["middle_class"] = btc_ratio * 0.16
        self.player_ratios["retail"] = btc_ratio * 0.26
        self.player_ratios["leverage"] = btc_ratio * 0.29

    def display_market(self):
        print(f"📊 资金池情况：USDT {self.usdt_pool:.2f} | BTC {self.btc_pool:.2f}")
        print(f"📊 玩家比例（按资金量动态调整）：{self.player_ratios}")

class Player:
    def __init__(self, name, capital, trade_frequency, risk_tolerance):
        self.name = name
        self.capital = capital
        self.trade_frequency = trade_frequency  
        self.risk_tolerance = risk_tolerance
        self.position = {
            "USDT": capital,
            "long": 0,  
            "short": 0,  
            "holding": 0  
        }

    def make_decision(self, value_variable, short_term_variable, external_variable):
        """ 玩家基于市场变量决策交易 """
        total_score = (
            value_variable * 0.5 +
            short_term_variable * 0.3 +
            external_variable * 0.2
        )

        print(f"DEBUG: {self.name} | 交易频率: {self.trade_frequency} | 总评分: {total_score:.2f}")

        if abs(total_score) >= self.trade_frequency:
            if total_score > 0:
                self.buy(total_score)
            else:
                self.sell(total_score)
        else:
            print(f"{self.name} 持仓不变 (交易频率: {self.trade_frequency}, 总评分: {total_score:.2f})")

    def buy(self, market_value):
        """ 买入逻辑 """
        buy_amount = self.position["USDT"] * 0.1
        self.position["long"] += buy_amount * 0.7  
        self.position["holding"] += buy_amount * 0.3  
        self.position["USDT"] -= buy_amount
        print(f"{self.name} 买入 {buy_amount} BTC at 市场值 {market_value}")

    def sell(self, market_value):
        """ 卖出逻辑 """
        if self.position["long"] > 0:
            sell_amount = self.position["long"] * 0.5  
            self.position["long"] -= sell_amount
            self.position["USDT"] += sell_amount
            print(f"{self.name} 卖出 {sell_amount} BTC at 市场值 {market_value}")
        elif self.position["holding"] > 0:
            sell_amount = self.position["holding"] * 0.5  
            self.position["holding"] -= sell_amount
            self.position["USDT"] += sell_amount
            print(f"{self.name} 卖出 {sell_amount} BTC from 长期持有 at 市场值 {market_value}")
        else:
            print(f"{self.name} 无法卖出，持仓为 0")

# **玩家初始化**
players = [
    Player("🐋 鲸鱼", capital=1000000, trade_frequency=6, risk_tolerance="低"),
    Player("🏦 富豪", capital=500000, trade_frequency=5, risk_tolerance="中"),
    Player("💰 富人", capital=100000, trade_frequency=4, risk_tolerance="中高"),
    Player("🏠 平民", capital=5000, trade_frequency=1, risk_tolerance="高"),
    Player("🔥 杠杆", capital=1000, trade_frequency=0, risk_tolerance="极高")
]

# **市场变量计算**
def simulate_market():
    market_vars = {
        "value_variable": random.uniform(-10, 10),
        "short_term_variable": random.uniform(-10, 10),
        "external_variable": random.uniform(-5, 5)
    }
    return market_vars

# **运行交易模拟**
if __name__ == "__main__":
    market = Market()
    for _ in range(5):
        market_vars = simulate_market()
        print(f"\n📊 当前市场变量：{market_vars}")
        
        market.adjust_market_funds(market_vars["value_variable"])
        market.display_market()
        
        for player in players:
            player.make_decision(market_vars["value_variable"], market_vars["short_term_variable"], market_vars["external_variable"])
