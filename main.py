import sqlite3
import config
from datetime import date, timedelta
from fastapi import templating
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

current_date = (date.today() - timedelta(days=4)).isoformat()


@app.get("/")
def index(request: Request):
    stock_filter = request.query_params.get('filter', False)
    connection = sqlite3.connect(config.DB_FILE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    if stock_filter == "new_closing_highs":
        cursor.execute("""
        SELECT * FROM (
          SELECT symbol, name, stock_id, max(close), date
          FROM stock_price
          JOIN stock
          ON stock.id = stock_price.stock_id
          GROUP BY stock_id
          ORDER BY symbol
        ) WHERE date = ?
      """, (current_date, ))
        rows = cursor.fetchall()

    elif stock_filter == "new_intraday_highs":
        cursor.execute("""
        SELECT id, symbol, name FROM stock ORDER BY symbol
      """)
        rows = cursor.fetchall()
    elif stock_filter == "new_closing_lows":
        cursor.execute("""
        SELECT id, symbol, name FROM stock ORDER BY symbol
      """)
        rows = cursor.fetchall()
    elif stock_filter == "new_intraday_lows":
        cursor.execute("""
        SELECT id, symbol, name FROM stock ORDER BY symbol
      """)
        rows = cursor.fetchall()
    else:
        cursor.execute("""
        SELECT id, symbol, name FROM stock ORDER BY symbol
      """)
        rows = cursor.fetchall()

    return templates.TemplateResponse("index.html", {"request": request, "stocks": rows})


@app.get("/stock/{symbol}")
def stock_detail(request: Request, symbol):
    connection = sqlite3.connect(config.DB_FILE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(""" 
      SELECT id, symbol, name, exchange FROM stock WHERE symbol = ?
  """, (symbol,))

    row = cursor.fetchone()

    cursor.execute(""" 
      SELECT * FROM stock_price WHERE stock_id = ? ORDER BY date DESC
  """, (row['id'],))

    prices = cursor.fetchall()

    return templates.TemplateResponse("stock.html", {"request": request, "stock": row, "bars": prices})
