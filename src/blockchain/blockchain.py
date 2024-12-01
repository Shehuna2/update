from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware  

class BlockchainConnector:
    def __init__(self, rpc_url, private_key):
        self.web3 = Web3(Web3.HTTPProvider(rpc_url))
        
        # Apply PoA middleware to fix the extraData issue for BSC (if needed)
        self.web3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

        if not self.web3.is_connected():
            raise ConnectionError("Unable to connect to the blockchain network.")
        
        self.account = self.web3.eth.account.from_key(private_key)
        self.address = self.account.address

    def get_balance(self, token_contract_address=None):
        """
        Get the balance of tokens or native currency (BNB/ETH) in the wallet.
        :param token_contract_address: Address of the token contract (optional)
        :return: Balance in Ether or token
        """
        if token_contract_address:
            # For ERC-20 / BEP-20 tokens, check token balance
            contract = self.web3.eth.contract(
                address=self.web3.to_checksum_address(token_contract_address),
                abi=[{
                    "constant": True,
                    "inputs": [],
                    "name": "balanceOf",
                    "outputs": [{"name": "", "type": "uint256"}],
                    "type": "function"
                }]
            )
            return contract.functions.balanceOf(self.address).call()
        else:
            # For native coin (BNB for BSC, ETH for Ethereum)
            return self.web3.eth.get_balance(self.address)

    def check_wallet_status(self, token_contract_address=None):
        """
        Check if the wallet has sufficient funds for gas fees and trading.
        :param token_contract_address: Address of the token contract (optional)
        :return: Dictionary with token and gas balance
        """
        gas_balance = self.get_balance()  # Get the native coin (BNB/ETH) balance for gas fees
        token_balance = self.get_balance(token_contract_address)  # Get token balance
        
        print(f"Gas Balance (BNB/ETH): {self.web3.from_wei(gas_balance, 'ether')}")
        print(f"Token Balance: {self.web3.from_wei(token_balance, 'ether') if token_contract_address else token_balance}")
        
        # Check if there are sufficient funds for gas and trading
        return {
            "gas_balance": self.web3.from_wei(gas_balance, 'ether'),
            "token_balance": self.web3.from_wei(token_balance, 'ether') if token_contract_address else token_balance,
        }


    def sign_and_send_transaction(self, transaction):
        signed_txn = self.web3.eth.account.sign_transaction(transaction, private_key=self.account.key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return tx_hash.hex()
