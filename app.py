import time
from src.apis.web3_api import fetch_prices_from_dexes
from src.utils.notifications import send_telegram_message
from src.blockchain.blockchain import BlockchainConnector
from src.blockchain.dex_router import DexRouter
from src.arbitrage.detector import find_arbitrage_opportunities
from config import (
    TRADING_PAIRS, DEXES, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, 
    MY_PRIVATE_KEY, BSC_RPC, ROUTER_ADDRESS
    )



# Initialize Blockchain Connection
blockchain = BlockchainConnector(BSC_RPC, MY_PRIVATE_KEY)
router = DexRouter(blockchain.web3, ROUTER_ADDRESS)

ARBITRAGE_THRESHOLD = 0.01  # Minimum profit in ETH to execute trade

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

# Main Execution
def main():
    print("Fetching prices from multiple DEXes...")
    swap_prices = fetch_prices_from_dexes(TRADING_PAIRS, DEXES)

    if not swap_prices:
        print("Failed to fetch DEX prices. Exiting.")
        return

    print("Calculating arbitrage opportunities...")
    opportunities = find_arbitrage_opportunities(swap_prices)

     # Check wallet status before executing the arbitrage
    wallet_status = blockchain.check_wallet_status()  # Check for gas and token balance
    if wallet_status["gas_balance"] < 0.1:  # Assuming 0.1 BNB/ETH is required for gas
        print("Insufficient gas balance. Please add more gas.")
        return
    
    if wallet_status["token_balance"] < 1:  # Assuming at least 1 token is required for trade
        print("Insufficient token balance. Please add more tokens.")
        return

    if opportunities:
        print("Profitable arbitrage opportunities found!")
        for opportunity in opportunities:
            try:
                token_in = opportunity['token_in']
                token_out = opportunity['token_out']
                amount_in = opportunity['amount_in']
                amount_out_min = opportunity['amount_out_min']
                recipient = blockchain.address

                # Approve Token
                print(f"Approving {token_in} for trading...")
                approve_txn = router.approve_token(
                    token_address=token_in,
                    spender_address=ROUTER_ADDRESS,
                    amount=amount_in,
                    account=blockchain
                )
                print(f"Approval TXN Hash: {approve_txn}")

                # Execute Swap
                print(f"Executing swap: {token_in} -> {token_out}")
                swap_txn = router.execute_swap(
                    token_in=token_in,
                    token_out=token_out,
                    amount_in=amount_in,
                    amount_out_min=amount_out_min,
                    recipient=recipient,
                    account=blockchain
                )
                print(f"Swap TXN Hash: {swap_txn}")
                send_telegram_message(f"Swap Successful: {swap_txn}")

            except Exception as e:
                error_message = f"Failed to execute arbitrage: {str(e)}"
                print(error_message)
                send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, error_message)


    else:
        print("No profitable arbitrage opportunities found.")
    print("Finished.")


if __name__ == "__main__":
    main()
