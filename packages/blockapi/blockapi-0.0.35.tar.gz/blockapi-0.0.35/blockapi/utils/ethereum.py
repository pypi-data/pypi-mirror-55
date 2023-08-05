from web3 import Web3
import json
import requests
from blockapi.api import EtherscanAPI
from ethereum_input_decoder import AbiMethod


class Ethereum:
    def __init__(self, node_url, contracts=None):
        self.contracts = contracts
        self.node_url = node_url
        self.web3 = Web3(Web3.HTTPProvider(self.node_url))
        self.abi = None

    def load_abi(self, contract):
        contract_addr = self.contracts[contract]
        myapi = EtherscanAPI(contract_addr)
        self.abi = myapi.get_abi(contract_addr)['result']

    def toChecksumAddress(self, address):
        return self.web3.toChecksumAddress(address)

    def get_contract(self, contract):
        self.load_abi(contract)
        return self.web3.eth.contract(address=Web3.toChecksumAddress(
            self.contracts[contract]), abi=self.abi)

    def get_tx_by_hash(self, txhash):
        tx = self.web3.eth.getTransaction(txhash)
        return tx

    def get_function_by_inputdata(self, tx_input):
        tx_input_decoded = AbiMethod.from_input_lookup(
            bytes.fromhex(tx_input[2:]))
        tx_input_values = list(tx_input_decoded.values())
        tx_function = tx_input_values[0]
        return tx_function

