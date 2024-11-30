from web3 import Web3

TELEGRAM_BOT_TOKEN = "7574272150:AAEx0Vv8fog11nOheF8LIqqQVw0kLDaZMBE"
TELEGRAM_CHAT_ID = "7843740783"
MY_PRIVATE_KEY = "0xb25f68c49d0156d31d20a6036825017079e60d1642df422f109054be6b6d531e"

# Binance Smart Chain RPC and Router Details (same as before)
BSC_RPC = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(BSC_RPC))
ROUTER_ADDRESS = Web3.to_checksum_address("0x10ED43C718714eb63d5aA57B78B54704E256024E")
ROUTER_ABI = [
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


# Add SushiSwap Router Details
SUSHISWAP_ROUTER_ADDRESS = Web3.to_checksum_address("0x1b02da8cb0d097eb8d57a175b88c7d8b47997506")
SUSHISWAP_ROUTER_ABI = ROUTER_ABI  # Same ABI as PancakeSwap

# Define DEX details
DEXES = {
    "PancakeSwap": {
        "router_address": ROUTER_ADDRESS,
        "abi": ROUTER_ABI,
    },
    "SushiSwap": {
        "router_address": SUSHISWAP_ROUTER_ADDRESS,
        "abi": SUSHISWAP_ROUTER_ABI,
    },
}


# Define tokens of interest
TOKENS = {
    "WBNB": Web3.to_checksum_address("0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"),
    "USDT": Web3.to_checksum_address("0x55d398326f99059fF775485246999027B3197955"),
    "BUSD": Web3.to_checksum_address("0xe9e7cea3dedca5984780bafc599bd69add087d56"),
    "ETH": Web3.to_checksum_address("0x2170ed0880ac9a755fd29b2688956bd959f933f8"),
}

# Define trading pairs
TRADING_PAIRS = [
    ("WBNB", "USDT"),
    ("WBNB", "BUSD"),
    ("ETH", "WBNB"),
    ("ETH", "USDT"),
]
