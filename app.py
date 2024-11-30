from src.apis.web3_api import fetch_prices_from_dexes
from config import TRADING_PAIRS, DEXES

def calculate_arbitrage(prices):
    """
    Calculate arbitrage opportunities between DEXes.
    :param prices: Nested dictionary of prices from multiple DEXes.
    :return: List of profitable opportunities.
    """
    opportunities = []
    
    for pair, dex_prices in prices.items():
        dex_names = list(dex_prices.keys())
        
        for i in range(len(dex_names)):
            for j in range(i + 1, len(dex_names)):
                dex1, dex2 = dex_names[i], dex_names[j]
                price1, price2 = dex_prices[dex1], dex_prices[dex2]

                if price1 and price2:
                    # Check for profitable spread
                    if price1 > price2:
                        profit = price1 - price2
                        opportunities.append((pair, dex1, dex2, profit))
                    elif price2 > price1:
                        profit = price2 - price1
                        opportunities.append((pair, dex2, dex1, profit))
    
    return opportunities

def main():
    print("Fetching prices from multiple DEXes...")
    
    # Fetch prices from all DEXes
    prices = fetch_prices_from_dexes(TRADING_PAIRS, DEXES)
    
    print("Calculating arbitrage opportunities...")
    opportunities = calculate_arbitrage(prices)
    
    # Display opportunities
    if opportunities:
        print("Profitable arbitrage opportunities found:")
        for pair, buy_dex, sell_dex, profit in opportunities:
            print(f"Buy on {buy_dex}, sell on {sell_dex}, Pair: {pair}, Profit: {profit:.6f}")
    else:
        print("No profitable arbitrage opportunities at the moment.")
    
    print("Finished.")

if __name__ == "__main__":
    main()
