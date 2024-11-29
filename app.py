from src.apis.dex_api import fetch_uniswap_prices
from src.arbitrage.detector import find_arbitrage_opportunities

def main():
    print("Fetching prices from Uniswap...")
    prices = fetch_uniswap_prices()
    print("Prices:", prices)

    print("\nDetecting arbitrage opportunities...")
    opportunities = find_arbitrage_opportunities(prices)
    if opportunities:
        print("Arbitrage Opportunities Found:")
        for opp in opportunities:
            print(f"Buy: {opp['buy']}, Sell: {opp['sell']}, Profit: {opp['profit']:.4f}")
    else:
        print("No arbitrage opportunities found.")

if __name__ == "__main__":
    main()
