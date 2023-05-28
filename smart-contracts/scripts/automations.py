from brownie import PrimeCrusaders, config, network
from scripts.helpful_scripts import get_account


def automations():
    account = get_account()

    contract = PrimeCrusaders[-1]
    print('Latest address: ' + contract.address)

    upkeep = contract.checkUpkeep.call(b'',{"from": account})
    print('Needs Upkeep? ' + str(upkeep[0]))
    if upkeep[0] == True:
        print('Performing Upkeep...')
        contract.performUpkeep.call(b'', {"from": account})
        print('Upkeep performed.')

def main():
    automations()
