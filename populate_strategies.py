import sqlite3, config
import alpaca_trade_api as tradeapi

connection = sqlite3.connect(config.DB_FILE)
connection.row_factory = sqlite3.Row

cursor = connection.cursor()

strategies = ['opening_range_breakout', 'opening_range_breakdown', 'bollinger_bands']
for strategy in strategies:
  cursor.execute("""
  INSERT INTO strategy (name)
  VALUES (?)
  """, (strategy, ))
  connection.commit()