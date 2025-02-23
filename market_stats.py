import random

class Market:
    def __init__(self):
        self.usdt_pool = 100000000  
        self.btc_pool = 1000000  
        self.total_funds = self.usdt_pool + self.btc_pool  
        self.capital_flow = 0  
        self.btc_supply = 1000000  
        self.price = 1000  
        self.mvrv = 2  
        self.nupl = 0.5  
        self.tiv = 1000  
        self.base_value_variable = 0  
        self.market_value_variable = 1  # **初始为牛市**
        self.last_base_value = 0  

    def adjust_market_funds(self):
        """ 根据市场价值变量调整 USDT 和 BTC 资金池 """
        net_funds = self.usdt_pool + self.btc_pool
        expected_usdt = net_funds * 0.5  
        self.capital_flow = (expected_usdt - self.usdt_pool) * 0.1  
        self.usdt_pool += self.capital_flow
        self.btc_pool -= self.capital_flow  

    def calculate_btc_price(self, total_spot_position, total_leverage_position):
        """ 计算 BTC 价格（基于市场总价值计算） """
        market_cap = total_spot_position + total_leverage_position + self.usdt_pool  
        self.price = market_cap / self.btc_supply  
        print(f"📈 BTC 最新价格: {self.price:.2f} USDT")

    def update_value_variable(self):
        """ **长期价值变量计算（符合牛熊市判断逻辑）** """
        self.mvrv += random.uniform(-0.1, 0.1)  
        self.nupl += random.uniform(-0.05, 0.05)  
        self.tiv += random.uniform(-2, 2)  

        self.mvrv = max(0.5, min(4.5, self.mvrv))  
        self.nupl = max(-0.3, min(0.8, self.nupl))  
        self.tiv = max(950, min(1050, self.tiv))  

        value_mvrv = (self.mvrv - 2) * 5  
        value_nupl = (self.nupl - 0.5) * 40  
        value_tiv = ((self.tiv - 950) / (1050 - 950)) * 20 - 10  

        # **计算基础价值变量**
        self.base_value_variable = (value_mvrv + value_nupl + value_tiv) / 3  

        # **判断市场趋势（牛熊转换）**
        if self.base_value_variable > self.last_base_value:
            self.market_value_variable = max(0.5, self.market_value_variable + 0.1)  # **保持牛市**
        elif self.base_value_variable < self.last_base_value:
            self.market_value_variable = min(-0.5, self.market_value_variable - 0.1)  # **保持熊市**

        self.last_base_value = self.base_value_variable  # **更新趋势**

        print(f"📊 **基础价值变量: {self.base_value_variable:.2f} | 市场价值变量: {self.market_value_variable:.2f}**")

    def display_market(self):
        print(f"📊 市场情况：USDT {self.usdt_pool:.2f} | BTC {self.btc_pool:.2f} | 资金流动: {self.capital_flow:.2f}")

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

    def get_total_position(self):
        """ 计算玩家的现货总持仓 """
        return self.position["long"] + self.position["short"] + self.position["holding"]

class LeverageMarket:
    def __init__(self):
        self.leverage_positions = []
        self.leverage_funds = 50000000  
        self.btc_pool = 500000  

    def check_liquidations(self, market_price):
        """ 检查杠杆市场的爆仓情况 """
        total_leverage_position = 0
        remaining_positions = []
        for position in self.leverage_positions:
            if (position["direction"] == "long" and market_price <= position["liquidation_price"]) or \
               (position["direction"] == "short" and market_price >= position["liquidation_price"]):
                print(f"💥 {position['player']} 在 {market_price:.2f} 爆仓！杠杆: {position['leverage']}x")
            else:
                remaining_positions.append(position)
                total_leverage_position += position["total_amount"]
        
        self.leverage_positions = remaining_positions
        return total_leverage_position

# **玩家初始化**
players = [
    Player("🐋 鲸鱼", capital=1000000),
    Player("🏦 富豪", capital=500000),
    Player("💰 富人", capital=100000),
    Player("🏠 平民", capital=5000)
]

# **杠杆市场初始化**
leverage_market = LeverageMarket()

# **运行市场统计**
if __name__ == "__main__":
    market = Market()
    for _ in range(5):
        market.update_value_variable()
        market_price = random.uniform(950, 1050)
        print(f"\n📊 当前市场价格: {market_price:.2f}")

        market.adjust_market_funds()
        market.display_market()

        total_spot_position = sum(player.get_total_position() for player in players)
        total_leverage_position = leverage_market.check_liquidations(market_price)

        market.calculate_btc_price(total_spot_position, total_leverage_position)
