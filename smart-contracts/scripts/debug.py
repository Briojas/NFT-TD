from brownie import PrimeCrusaders, Contract
from scripts.helpful_scripts import get_account

data = [
    'https://ipfs.io/ipfs/bafybeidcuj7x347s2ekyicsu2udaime4dzwf7v5qob446pfspx3j765n7m/ipfs_script_template.json'
]

def debug():
    account = get_account()

    contract = PrimeCrusaders[-1]
    print('Working address: ' + contract.address)

    # print('Building Batch...')
    # # print('Gas estimated: ' + contract.performUpkeep.estimate_gas(b'', {"from": account}))
    # contract.debug_build.call({"from": account})
    # debug = contract.debug.call({"from": account})
    # print('returnLength: ' + str(debug[0]))
    # print('verified: ' + str(debug[1]))

    tokenId = 0
    tokenURI = contract.uri.call(tokenId, {"from": account})
    print('tokenId: ' + str(tokenId))
    print('tokenURI: ' + tokenURI)

def main():
    debug()
