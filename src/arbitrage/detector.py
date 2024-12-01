from decimal import Decimal

def find_arbitrage_opportunities(swap_prices):
    opportunities = []
    for pair, dex_prices in swap_prices.items():
        dex_names = list(dex_prices.keys())
        for i in range(len(dex_names)):
            for j in range(i + 1, len(dex_names)):
                dex1, dex2 = dex_names[i], dex_names[j]
                price1, price2 = dex_prices[dex1], dex_prices[dex2]
                if price1 and price2:
                    if price1 > price2 * Decimal("1.01"):
                        opportunities.append({
                            "token_in": pair.split("->")[0],  # token_in (e.g., WBNB)
                            "token_out": pair.split("->")[1],  # token_out (e.g., USDT)
                            "amount_in": 1,  # or your calculated amount_in
                            "amount_out_min": price1 - (price2 * Decimal("1.01")),
                        })
                    elif price2 > price1 * Decimal("1.01"):
                        opportunities.append({
                            "token_in": pair.split("->")[1],  # token_in (e.g., USDT)
                            "token_out": pair.split("->")[0],  # token_out (e.g., WBNB)
                            "amount_in": 1,  # or your calculated amount_in
                            "amount_out_min": price2 - (price1 * Decimal("1.01")),
                        })
    return opportunities
