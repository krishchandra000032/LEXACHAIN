# contract_manager.py
import os
import json
from web3 import Web3
from solc import compile_standard, install_solc

def deploy_and_execute(solidity_code: str):
    # 1. Connect to BlockDAG network
    w3 = Web3(Web3.HTTPProvider(os.getenv("RPC_URL")))
    if not w3.is_connected():
        raise ConnectionError("Failed to connect to the blockchain.")

    chain_id = w3.eth.chain_id
    deployer_address = w3.eth.account.from_key(os.getenv("PRIVATE_KEY")).address
    
    # 2. Compile the Solidity code
    compiled_sol = compile_standard({
        "language": "Solidity",
        "sources": {"SmartContract.sol": {"content": solidity_code}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    })

    # Get contract data
    contract_interface = compiled_sol['contracts']['SmartContract.sol']['YourContractName'] # Replace with dynamic name-finding logic
    bytecode = contract_interface['evm']['bytecode']['object']
    abi = contract_interface['abi']
    
    # 3. Deploy the contract
    Contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    nonce = w3.eth.get_transaction_count(deployer_address)
    
    transaction = Contract.constructor().build_transaction({
        "chainId": chain_id,
        "from": deployer_address,
        "nonce": nonce,
        "gasPrice": w3.eth.gas_price
    })

    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=os.getenv("PRIVATE_KEY"))
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    return {
        "status": "deployed",
        "contract_address": tx_receipt.contractAddress,
        "transaction_hash": w3.to_hex(tx_hash)
    }
