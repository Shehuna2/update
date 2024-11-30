from src.apis.web3_api import get_token_price, WBNB, USDT
from web3 import Web3

def main():
    print("Fetching token price for WBNB -> USDT...")
    
    # Set input amount (e.g., 1 WBNB in wei)
    amount_in_wei = Web3.to_wei(1, "ether")
    
    # Define the swap path
    path = [WBNB, USDT]
    
    # Fetch and display the price
    price = get_token_price(amount_in_wei, path)
    if price:
        print(f"1 WBNB = {price} USDT")
    else:
        print("Failed to fetch token price.")

if __name__ == "__main__":
    main()
