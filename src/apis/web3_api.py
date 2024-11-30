import os
import requests

from web3 import Web3
from config import TOKENS, ROUTER_ADDRESS, ROUTER_ABI
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

