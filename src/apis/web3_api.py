import os
import time
import requests

from web3 import Web3
from config import TOKENS, ROUTER_ADDRESS, ROUTER_ABI, MY_PRIVATE_KEY
# from dotenv import load_dotenv


# Load environment variables
# load_dotenv()
# INFURA_URL = os.getenv("INFURA_URL")
# web3 = Web3(Web3.HTTPProvider(INFURA_URL))
BSC_RPC_URL = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(BSC_RPC_URL))

# PancakeSwap Subgraph endpoint
# SUBGRAPH_URL = "https://developer.pancakeswap.finance/apis/subgraph"
router_contract = web3.eth.contract(address=ROUTER_ADDRESS, abi=ROUTER_ABI)

def get_token_price(amount_in, path):
    """Fetch token price via PancakeSwap Router."""
    try:
        amounts_out = router_contract.functions.getAmountsOut(amount_in, path).call()
        return web3.from_wei(amounts_out[-1], "ether")
    except Exception as e:
        print(f"Error fetching token price for path {path}: {e}")
        return None

def get_price_from_dex(amount_in, path, dex):
    """
    Fetch token price from a specific DEX router.
    :param amount_in: Input amount in Wei.
    :param path: List of token addresses for the trading path.
    :param dex: Dictionary containing DEX router details.
    :return: Output price or None if error.
    """
    try:
        router_contract = web3.eth.contract(
            address=dex["router_address"], abi=dex["abi"]
        )
        amounts_out = router_contract.functions.getAmountsOut(amount_in, path).call()
        return web3.from_wei(amounts_out[-1], "ether")
    except Exception as e:
        print(f"Error fetching price from {dex['router_address']}: {e}")
        return None

def fetch_prices_from_dexes(pairs, dexes, amount_in_ether=1):
    """
    Fetch prices for trading pairs across multiple DEXes.
    :param pairs: List of token pairs.
    :param dexes: Dictionary of DEX configurations.
    :param amount_in_ether: Input amount in Ether.
    :return: Nested dictionary with prices from each DEX.
    """
    amount_in_wei = Web3.to_wei(amount_in_ether, "ether")
    prices = {}

    for pair in pairs:
        token1, token2 = pair
        path = [TOKENS[token1], TOKENS[token2]]
        prices[f"{token1}->{token2}"] = {}
        
        for dex_name, dex_details in dexes.items():
            price = get_price_from_dex(amount_in_wei, path, dex_details)
            prices[f"{token1}->{token2}"][dex_name] = price
    
    return prices

def execute_trade(amount_in, path, dex):
    """
    Execute a token swap on the specified DEX.
    :param amount_in: Input amount in Wei.
    :param path: List of token addresses for the trading path.
    :param dex: Dictionary containing DEX router details.
    :return: Transaction receipt or None if error.
    """
    try:
        router_contract = web3.eth.contract(
            address=dex["router_address"], abi=dex["abi"]
        )
        account = web3.eth.default_account  # Set this in web3 configuration
        nonce = web3.eth.get_transaction_count(account)

        tx = router_contract.functions.swapExactTokensForTokens(
            amount_in,
            0,  # Min amount out, adjust for slippage
            path,
            account,
            int(time.time()) + 300  # 5-minute deadline
        ).build_transaction({
            "from": account,
            "gas": 200000,
            "gasPrice": web3.to_wei("5", "gwei"),
            "nonce": nonce,
        })

        signed_tx = web3.eth.account.sign_transaction(tx, private_key=MY_PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"Trade executed. TX Hash: {tx_hash.hex()}")
        return web3.eth.wait_for_transaction_receipt(tx_hash)
    except Exception as e:
        print(f"Trade execution failed: {e}")
        return None

