import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Simulating stock price movements
np.random.seed(42)  # Ensures we get the same random values every time we run the code
days = 100  # Number of trading days
price = 100  # Starting stock price
price_changes = np.random.normal(loc=0, scale=1, size=days)  # Simulate daily price changes
stock_prices = price + np.cumsum(price_changes)  # Cumulative sum to get stock prices over time

# Setting trading rules
buy_threshold = 0  # Buy when price increases from previous day
sell_threshold = -0.5  # Sell when price drops by 0.5 from the previous day
stop_loss = 0.95  # 5% loss
take_profit = 1.10  # 10% profit

# Simulating the trading bot
position = False  # Track if we currently own the stock
buy_price = 0  # Store the price at which we buy
balance = 1000  # Starting money
stock_owned = 0  # Number of stocks owned
trade_log = []  # Store trade history

for i in range(1, days):
    price_today = stock_prices[i]
    price_yesterday = stock_prices[i - 1]
    
    # Buy Condition
    if not position and price_today > price_yesterday + buy_threshold:
        buy_price = price_today
        stock_owned = balance // buy_price  # Buy as many as we can afford
        balance -= stock_owned * buy_price  # Deduct cost from balance
        position = True
        trade_log.append((i, "BUY", buy_price, stock_owned))
    
    # Sell Condition (Stop-Loss or Take-Profit)
    elif position:
        if price_today <= buy_price * stop_loss or price_today >= buy_price * take_profit:
            balance += stock_owned * price_today  # Sell everything
            position = False
            trade_log.append((i, "SELL", price_today, stock_owned))
            stock_owned = 0  # Reset stock count

# Convert trade log to DataFrame
trades_df = pd.DataFrame(trade_log, columns=["Day", "Action", "Price", "Shares"])
print(trades_df)

# Plot stock price and trading actions
plt.figure(figsize=(10,5))
plt.plot(stock_prices, label="Stock Price", color="blue")
buy_days = trades_df[trades_df["Action"] == "BUY"]["Day"]
buy_prices = trades_df[trades_df["Action"] == "BUY"]["Price"]
sell_days = trades_df[trades_df["Action"] == "SELL"]["Day"]
sell_prices = trades_df[trades_df["Action"] == "SELL"]["Price"]
plt.scatter(buy_days, buy_prices, color="green", marker="^", label="Buy Signal", s=100)
plt.scatter(sell_days, sell_prices, color="red", marker="v", label="Sell Signal", s=100)
plt.legend()
plt.title("Trading Bot Simulation")
plt.xlabel("Days")
plt.ylabel("Stock Price")
plt.show()
