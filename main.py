
import os
import requests

# Load configuration securely from GitHub Secrets
ACCOUNT_ID = os.environ.get("OANDA_ACCOUNT_ID")
API_KEY = os.environ.get("OANDA_API_KEY")

# Using OANDA's practice/demo environment endpoint
BASE_URL = f"https://api-fxpractice.oanda.com/v3/accounts/{ACCOUNT_ID}"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def get_current_price(instrument="EUR_USD"):
    """Fetches the latest mid-market price for a currency pair."""
    url = f"{BASE_URL}/pricing?instruments={instrument}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        data = response.json()
        try:
            prices = data.get("prices", [])
            if prices:
                bid = float(prices[0]["bids"][0]["price"])
                ask = float(prices[0]["asks"][0]["price"])
                mid_price = (bid + ask) / 2
                print(f"[{instrument}] Current Market Price: {mid_price}")
                return mid_price
        except (KeyError, IndexError) as e:
            print(f"Error parsing price data: {e}")
    else:
        print(f"Failed to fetch price. Status Code: {response.status_code}, Response: {response.text}")
    
    return None

def execute_trade(instrument="EUR_USD", units=1000):
    """Places a market order. Positive units = Buy, Negative units = Sell."""
    url = f"{BASE_URL}/orders"
    payload = {
        "order": {
            "units": str(units),
            "instrument": instrument,
            "timeInForce": "FOK",
            "type": "MARKET",
            "positionFill": "DEFAULT"
        }
    }
    
    response = requests.post(url, json=payload, headers=HEADERS)
    if response.status_code in [200, 201]:
        print("Trade executed successfully!")
        print(response.json())
    else:
        print(f"Order placement failed: {response.status_code}, {response.text}")

def run_bot():
    print("Starting Forex Bot execution loop...")
    
    if not ACCOUNT_ID or not API_KEY:
        print("Error: Missing credentials. Ensure GitHub Secrets are configured.")
        return

    instrument = "EUR_USD"
    current_price = get_current_price(instrument)
    
    if current_price:
        # EXAMPLE LOGIC:
        # Replace this placeholder condition with your actual trading rules or indicator thresholds.
        # For safety in this template, it only logs the price and doesn't fire real market orders 
        # until you modify the condition below.
        
        target_buy_price = 1.0500  # Example trigger threshold
        
        if current_price < target_buy_price:
            print(f"Price is below target ({target_buy_price}). Executing BUY order.")
            execute_trade(instrument, units=1000)
        else:
            print(f"Price ({current_price}) has not met the strategy entry condition. Holding position.")

if __name__ == "__main__":
    run_bot()
