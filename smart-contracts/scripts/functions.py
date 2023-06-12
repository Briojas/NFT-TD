from brownie import PrimeCrusaders, config, network
from scripts.helpful_scripts import get_account

    #TODO: feed in as an arg
localSubscriptionId = 334

def functions():
    account = get_account()

    contract = PrimeCrusaders[-1]
    print('Working address: ' + contract.address)

    deployedSourceCode = contract.sourceCode.call({"from": account})
    # with open('C:/HomoSimulo/NFT-TD/smart-contracts/contracts/functions-js-scripts/debug.js', 'r') as file:
    with open('C:/HomoSimulo/NFT-TD/smart-contracts/contracts/functions-js-scripts/verify-mint-API.js', 'r') as file:
        localSourceCode = file.read()
    deployedSubscriptionId = contract.subscriptionId.call({"from": account})

    secrets = "0xdb81a7077bf6a6d5c4a75615c9743da50204da8220f7065020ec8e009100963f3430d70a7b4f58c919497c4d894e4d65c60dba7c6d450fe1d2e4495ece4e0d2631ee0eaa8ef1745da07074bdf23fc7161adf025913dc62b991e6e393da8f98aeb6b5101737fae8f45ece1f8d0140ef0b072253c9ba40610a9152d244c130ad2a3324d9597f25ecc44db8eb034818e080fd3bf89bf3b7308518b3a54f57d3c0fc23"
    depoloyedSecrets = contract.secrets.call({"from": account})

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
    if secrets == depoloyedSecrets:
        print('Secrets up to date.')
    else:
        print('Updating secrets...')
        contract.updateSecrets(secrets, {"from": account})
        print('Secrets updated with local script.')

def main():
    functions()
