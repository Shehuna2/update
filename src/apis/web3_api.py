import os
import requests

from dotenv import load_dotenv
from web3 import Web3

# Load environment variables
# load_dotenv()
# INFURA_URL = os.getenv("INFURA_URL")
# web3 = Web3(Web3.HTTPProvider(INFURA_URL))
# BSC_RPC_URL = "https://bsc-dataseed.binance.org/"
# web3 = Web3(Web3.HTTPProvider(BSC_RPC_URL))

# PancakeSwap Subgraph endpoint
# SUBGRAPH_URL = "https://developer.pancakeswap.finance/apis/subgraph"


# Connect to BSC (Binance Smart Chain)
bsc_rpc = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc_rpc))

# PancakeSwap Router contract address and ABI
router_address = Web3.to_checksum_address("0x10ED43C718714eb63d5aA57B78B54704E256024E")
router_abi = [
    {
        "inputs": [
            {"internalType": "uint256", "name": "amountIn", "type": "uint256"},
            {"internalType": "address[]", "name": "path", "type": "address[]"}
        ],
        "name": "getAmountsOut",
        "outputs": [{"internalType": "uint256[]", "name": "", "type": "uint256[]"}],
        "stateMutability": "view",
        "type": "function"
    }
]

# Token addresses
WBNB = Web3.to_checksum_address("0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c")
USDT = Web3.to_checksum_address("0x55d398326f99059fF775485246999027B3197955")

# Initialize contract
router_contract = web3.eth.contract(address=router_address, abi=router_abi)

def get_token_price(amount_in, path):
    try:
        # Query the blockchain for the output amount
        amounts_out = router_contract.functions.getAmountsOut(amount_in, path).call()
        return web3.from_wei(amounts_out[-1], "ether")  # Convert to human-readable format
    except Exception as e:
        print(f"Error fetching token price: {e}")
        return None

# Fetch price: 1 WBNB -> USDT
amount_in_wei = web3.to_wei(1, "ether")  # 1 BNB
price = get_token_price(amount_in_wei, [WBNB, USDT])

print(f"1 WBNB = {price} USDT")
