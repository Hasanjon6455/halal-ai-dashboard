
import pandas as pd
from scripts.fetch_prices import get_price_data
from scripts.trading_rules import trading_decision
from alpaca_config import API_KEY, SECRET_KEY, BASE_URL
import alpaca_trade_api as tradeapi

def simulate_weekly_trades(csv_path):
    df = pd.read_csv(csv_path)
    results = []

    api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL)

    for _, row in df.iterrows():
        ticker = row["Ticker"]
        name = row["Stock Name"]
        avoid = row.get("Avoid", "N")

        memo = ""

        if avoid == "Y":
            action = "SKIP (Boycott)"
            prev = curr = pct = None
            memo = "Flagged for boycott"
        else:
            prev, curr, pct = get_price_data(ticker)
            action = trading_decision(pct)

            try:
                if action == "BUY $5":
                    api.submit_order(symbol=ticker, qty=1, side='buy', type='market', time_in_force='gtc')
                    memo = "Buy order submitted"
                elif action == "SELL $10":
                    api.submit_order(symbol=ticker, qty=1, side='sell', type='market', time_in_force='gtc')
                    memo = "Sell order submitted"
                else:
                    memo = "No action"
            except Exception as e:
                memo = f"Failed to {action.split()[0]}: {str(e)}"


        results.append({
            "Stock Name": name,
            "Ticker": ticker,
            "Market": row["Market"],
            "Previous Price": prev,
            "Current Price": curr,
            "Price Change (%)": pct,
            "Decision": action,
            "Memo": memo  # new line
        })

    return pd.DataFrame(results)
