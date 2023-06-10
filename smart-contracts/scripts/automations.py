from brownie import PrimeCrusaders, config, network
from scripts.helpful_scripts import get_account


def automations():
    account = get_account()

    contract = PrimeCrusaders[-1]
    print('Working address: ' + contract.address)

    upkeep = contract.checkUpkeep.call(b'',{"from": account})
    print('Needs Upkeep? ' + str(upkeep[0]))
    if upkeep[0] == True:
        print('Performing Upkeep...')
        # print('Gas estimated: ' + contract.performUpkeep.estimate_gas(b'', {"from": account}))
        contract.performUpkeep.call(b'', {"from": account})
        print('Upkeep performed.')

def main():
    automations()
