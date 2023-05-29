from brownie import PrimeCrusaders, config, network
from scripts.helpful_scripts import get_account


def checkStatus():
    account = get_account()

    contract = PrimeCrusaders[-1]
    print('Latest address: ' + contract.address)

    upkeep = contract.checkUpkeep.call(b'',{"from": account})
    print('Needs Upkeep? ' + str(upkeep[0]))
    print('')
    
    queueStatus = contract.queue_status.call({"from": account})
    print('----State----')
    status = ['IDLE', 'VERIFYING']
    print(status[queueStatus[0]])

    print('----Tickets----')
    print('number of tickets: ' + str(queueStatus[1]))
    print('current ticket: ' + str(queueStatus[2]))
    print('')
    
    print('----Current Submission----')
    print('ticket owner: ' + str(queueStatus[3]))
    print('ticket being processed: ' + str(queueStatus[4]))
    state = ['QUEUED', 'PENDING', 'APPROVED', 'REJECTED']
    print('ticket state - ' + str(state[queueStatus[5]]))
    print('')

    print('----Functions Results----')
    funcStatus = contract.functions_status.call({"from": account})
    print('Last Request Id: ' + str(funcStatus[0]))
    print('Last Response: ' + str(funcStatus[1]))
    print('Last Error: ' + str(funcStatus[2]))
    print('Last Batch: ' + str(funcStatus[3]))
    print('Gas Estimated: ' + str(funcStatus[4]))
    print('')

def main():
    checkStatus()
