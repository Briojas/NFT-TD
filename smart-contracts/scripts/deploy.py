#!/usr/bin/python3
from scripts.helpful_scripts import get_account, is_verifiable_contract
from brownie import PrimeCrusaders, config, network


def deploy_automation_counter():
    oracle_address = "0x649a2C205BE7A3d5e99206CEEFF30c794f0E31EC"
    
        # Open the JavaScript file in read mode
    with open('C:/HomoSimulo/NFT-TD/smart-contracts/contracts/functions-js-scripts/verify-mint-API.js', 'r') as file:
        # Read the contents of the file
        javascript_code = file.read()

    # Print the JavaScript code
    print(javascript_code)

    account = get_account()
    # contract = AutomatedFunctionsConsumer.deploy(
    #     oracle_address,
    #     {"from": account}
    # )

    # contract.tx.wait(2) # wait for 2 blocks
    # print(f"Contract deployed to {contract.address}")

    # return contract

def main():
    deploy_automation_counter()
