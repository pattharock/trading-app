# import config
# import alpaca_trade_api as tradeapi
# api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.API_URL)
    
# barsets = api.get_barset(['AAPL', 'MSFT'], 'day')

# for symbol in barsets:
#   print(f'Processing Symbol : {symbol}')
#   for bar in barsets[symbol]:
#     print(bar.t, bar.o, bar.h, bar.l, bar.c, bar.v)

# hourly_bars = api.polygon.historic_agg_v2('Z', 1, 'hour', _from='2020-10-02', to='2020-10-22')
# five_minute_bars = api.polygon.historic_agg_v2('Z', 5, 'minute', _from='2020-10-02', to='2020-10-22')
# minute_bars = api.polygon.historic_agg_v2('Z', 1, 'minute', _from='2020-10-02', to='2020-10-22')
# for bar in hourly_bars:
#     print(bar.timestamp, bar.open, bar.high, bar.low, bar.close, bar.volume)
# for bar in five_minute_bars:
#     print(bar.timestamp, bar.open, bar.high, bar.low, bar.close, bar.volume)
# for bar in minute_bars:
#     print(bar.timestamp, bar.open, bar.high, bar.low, bar.close, bar.volume)
import sqlite3, config
import alpaca_trade_api as tradeapi

connection = sqlite3.connect('app.db')
connection.row_factory = sqlite3.Row

cursor = connection.cursor()

cursor.execute("""
    SELECT id, symbol, name FROM stock
""")

rows = cursor.fetchall()

# symbols = [row['symbol'] for row in rows]
symbols = []
stock_dict = {}

for row in rows:
    symbol = row['symbol']
    symbols.append(symbol)
    stock_dict[symbol] = row['id']

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.API_URL)
chunk_size = 200

for i in range(0, len(symbols), chunk_size):
    symbol_chunk = symbols[i:i+chunk_size]
    barsets = api.get_barset(symbol_chunk, 'day')
    for symbol in barsets:
        print(f"processing symbol {symbol}")
        for bar in barsets[symbol]:
            stock_id = stock_dict[symbol]
            cursor.execute("""
                INSERT INTO stock_price (stock_id, date, open, high, low, close, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (stock_id, bar.t.date(), bar.o, bar.h, bar.l, bar.c, bar.v))
connection.commit()