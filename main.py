
import os
from datetime import datetime
from scripts.simulate_trades import simulate_weekly_trades

# Create Reports folder if it doesn't exist
os.makedirs("Reports", exist_ok=True)

# Load stock list and run
csv_file = "data/shariah_stocks_filtered_by_bds.csv"
df = simulate_weekly_trades(csv_file)

# Save file with timestamp
today = datetime.today().strftime("%m-%d-%Y")
filename = f"Reports/{today} Weekly Trade Decisions.csv"
df.to_csv(filename, index=False)
print(f"Saved to {filename}")
