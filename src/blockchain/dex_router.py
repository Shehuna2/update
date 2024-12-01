import time


class DexRouter:
    def __init__(self, web3, router_address):
        self.web3 = web3
        self.router_address = self.web3.to_checksum_address(router_address)
        self.router_contract = self.web3.eth.contract(
            address=self.router_address,
            abi=[{
                "constant": False,
                "inputs": [
                    {"name": "_spender", "type": "address"},
                    {"name": "_value", "type": "uint256"}
                ],
                "name": "approve",
                "outputs": [{"name": "", "type": "bool"}],
                "type": "function"
            }]
        )

    def approve_token(self, token_address, spender_address, amount, account):
        contract = self.web3.eth.contract(address=token_address, abi=self.router_contract.abi)
        approve_txn = contract.functions.approve(spender_address, amount).buildTransaction({
            'chainId': 56,  # Example for Binance Smart Chain
            'gas': 50000,
            'gasPrice': self.web3.toWei('5', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(account.address),
        })
        return account.sign_and_send_transaction(approve_txn)

def execute_swap(self, token_in, token_out, amount_in, amount_out_min, recipient, account):
    swap_txn = self.router_contract.functions.swapExactTokensForTokens(
        amount_in,
        amount_out_min,
        [token_in, token_out],
        recipient,
        int(time.time()) + 60  # 1-minute deadline
    ).buildTransaction({
        'chainId': 56,  # Example for Binance Smart Chain
        'gas': 200000,
        'gasPrice': self.web3.toWei('5', 'gwei'),
        'nonce': self.web3.eth.getTransactionCount(account.address),
    })
    return account.sign_and_send_transaction(swap_txn)
