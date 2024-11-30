def find_arbitrage_opportunities(swap_prices):
    """
    Detect arbitrage opportunities between token prices on PancakeSwap.
    :param swap_prices: Dictionary with token pair prices from PancakeSwap
    :return: List of arbitrage opportunities
    """
    opportunities = []
    pairs = list(swap_prices.keys())
    
    for i in range(len(pairs)):
        for j in range(len(pairs)):
            if i != j:
                pair1 = pairs[i]
                pair2 = pairs[j]
                price1 = swap_prices[pair1]
                price2 = swap_prices[pair2]

                # Check for arbitrage opportunity
                if price1 > price2 * 1.01:  # Example: 1% profit threshold
                    opportunities.append({
                        "buy": pair2,
                        "sell": pair1,
                        "profit": price1 - (price2 * 1.01)
                    })
    return opportunities
