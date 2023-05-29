from brownie import PrimeCrusaders, config, network
from scripts.helpful_scripts import get_account

    #TODO: feed in as an arg
localSubscriptionId = 334

def functions():
    account = get_account()

    contract = PrimeCrusaders[-1]
    print('Working address: ' + contract.address)

    deployedSourceCode = contract.sourceCode.call({"from": account})
    with open('C:/HomoSimulo/NFT-TD/smart-contracts/contracts/functions-js-scripts/verify-mint-API.js', 'r') as file:
        localSourceCode = file.read()
    deployedSubscriptionId = contract.subscriptionId.call({"from": account})
    
    print('----CL Functions Info----')
    if localSourceCode == deployedSourceCode:
        print('Source code up to date.')
    else:
        print('Updating source code...')
        contract.updateSourceCode(localSourceCode, {"from": account})
        print('Source code updated with local script.')
    if localSubscriptionId == deployedSubscriptionId:
        print('subscriptionId: ' + str(deployedSubscriptionId))
    else:
        print('Updating subscriptionId...')
        contract.updateSubscriptionId(localSubscriptionId, {"from": account})
        print('SubscriptionId updated to: ' + str(localSubscriptionId))

def main():
    functions()
