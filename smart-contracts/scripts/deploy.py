from scripts.helpful_scripts import get_account, is_verifiable_contract
from brownie import PrimeCrusaders, config, network
import sys

def deploy():
    oracle_address = "0x649a2C205BE7A3d5e99206CEEFF30c794f0E31EC"
    fulfillGasLimit = 1000000
    subscriptionId = 0
        #unused until batch minting implemented
    mintInterval = 0 
    mintBatchSize = 0 
        #get the source code from the JavaScript file
    with open('C:/HomoSimulo/NFT-TD/smart-contracts/contracts/functions-js-scripts/verify-mint-API.js', 'r') as file:
        javascript_code = file.read()

    account = get_account()
    contract = PrimeCrusaders.deploy(
        oracle_address,
        javascript_code,
        subscriptionId,
        fulfillGasLimit,
        mintInterval,
        mintBatchSize,
        {"from": account}
    )

    contract.tx.wait(2) # wait for 2 blocks
    print(f"Contract deployed to {contract.address}")

    return contract

def main():
    deploy()
