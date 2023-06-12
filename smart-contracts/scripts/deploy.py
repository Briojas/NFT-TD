from scripts.helpful_scripts import get_account, is_verifiable_contract
from brownie import PrimeCrusaders, config, network
import sys

def deploy():
    oracle_address = "0x649a2C205BE7A3d5e99206CEEFF30c794f0E31EC"
    fulfillGasLimit = 300000
    subscriptionId = 334
        #unused until batch minting implemented
    mintInterval = 0 
    mintBatchSize = 0 
        #get the source code from the JavaScript file
    with open('C:/HomoSimulo/NFT-TD/smart-contracts/contracts/functions-js-scripts/verify-mint-API.js', 'r') as file:
        javascript_code = file.read()

    secrets = "0x049f962f29e768d3d487f3a6d1b11fef029a55a18772e28165bdd155bcd4c2d8bc916e48b79346b35ecd2c7317cb695f005f7e3fd34351a24897976d950c7ab102bc1389cd657dd33b112b41ec01812afcf89beae1cba8b46e6e3317b9f27bc3e52d7c52c084849f90a3e20c5e9e8e9a156be54764a60e44aa65022349c78b3389895468985fe05c6c7126d3cae9c97d17c47fdb1e5f2211374c2083ac47b5fdf3"

    account = get_account()
    contract = PrimeCrusaders.deploy(
        oracle_address,
        javascript_code,
        secrets,
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
