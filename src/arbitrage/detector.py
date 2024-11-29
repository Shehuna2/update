def find_arbitrage_opportunities(prices):
    """
    Detect arbitrage opportunities from price data.
    :param prices: Dictionary with token pair prices
    :return: List of arbitrage opportunities
    """
    opportunities = []
    for pair1, price1 in prices.items():
        for pair2, price2 in prices.items():
            if pair1 != pair2:
                # Check if an arbitrage opportunity exists
                if price1 > price2 * 1.01:  # Example threshold: 1% profit
                    opportunities.append({
                        "buy": pair2,
                        "sell": pair1,
                        "profit": price1 - (price2 * 1.01)
                    })
    return opportunities
