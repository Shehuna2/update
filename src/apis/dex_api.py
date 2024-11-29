import os
import requests

from dotenv import load_dotenv
from web3 import Web3

# Load environment variables
load_dotenv()
INFURA_URL = os.getenv("INFURA_URL")
web3 = Web3(Web3.HTTPProvider(INFURA_URL))



UNISWAP_SUBGRAPH_URL = "https://gateway.thegraph.com/api/09c76de0cf573cbb4f2eb2fdc30df41c/subgraphs/id/5zvR82QoaXYFyDEKLZ9t6v9adgnptxYpKpSbxtgVENFV"



def fetch_uniswap_prices():
    """
    Fetch token pair prices from Uniswap using The Graph.
    """
    query = """
    {
      pairs(first: 5) {
        token0 {
          symbol
        }
        token1 {
          symbol
        }
        reserve0
        reserve1
      }
    }
    """
    response = requests.post(UNISWAP_SUBGRAPH_URL, json={"query": query})
    
    # Check if the response was successful
    if response.status_code == 200:
        try:
            data = response.json()
            # Debugging: Print the raw data returned from the API
            print("Raw data from API:", data)

            # Check if the expected keys exist in the response
            if not data or "data" not in data or not data["data"]:
                raise Exception("Error: Expected data not found in the response.")

            
            prices = {}
            for pair in data["data"]["pairs"]:
                token0 = pair["token0"]["symbol"]
                token1 = pair["token1"]["symbol"]
                reserve0 = float(pair["reserve0"])
                reserve1 = float(pair["reserve1"])
                price = reserve1 / reserve0
                prices[f"{token0}/{token1}"] = price

            return prices
        
        except Exception as e:
            # Add more specific exception handling for data issues
            raise Exception(f"Error processing data: {e}")
    
    else:
        raise Exception(f"Error fetching data: {response.text}")

