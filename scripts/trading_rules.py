
def trading_decision(pct_change):
    if pct_change is None:
        return "No Data"
    elif pct_change <= -5:
        return "BUY $5"
    elif pct_change >= 10:
        return "SELL $10"
    else:
        return "HOLD"
