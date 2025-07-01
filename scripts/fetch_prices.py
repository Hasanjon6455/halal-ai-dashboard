
import yfinance as yf
from datetime import datetime, timedelta

def get_price_data(ticker):
    try:
        end_date = datetime.today()
        start_date = end_date - timedelta(days=7)
        data = yf.download(ticker, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))

        if data.empty or len(data['Close']) < 2:
            return None, None, None

        start_price = data['Close'].iloc[0].item()
        end_price = data['Close'].iloc[-1].item()
        pct_change = round(((end_price - start_price) / start_price) * 100, 2)

        return start_price, end_price, pct_change
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None, None, None
