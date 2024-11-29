import requests
import json
import os

from dotenv import load_dotenv

url = os.getenv("INFURA_URL")

payload = {
  "jsonrpc": "2.0",
  "method": "eth_blockNumber",
  "params": [],
  "id": 1
}

headers = {'content-type': 'application/json'}

response = requests.post(url, data=json.dumps(payload), headers=headers).json()

print(response)