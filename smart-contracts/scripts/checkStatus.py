from brownie import PrimeCrusaders, config, network
from scripts.helpful_scripts import get_account


def checkStatus():
    account = get_account()

    contract = PrimeCrusaders[-1]
    print('Latest address: ' + contract.address)

    upkeep = contract.checkUpkeep.call(b'',{"from": account})
    print('Needs Upkeep? ' + str(upkeep[0]))
    print('')
    
    queueStatus = contract.status.call({"from": account})
    print('----State----')
    print(queueStatus[0])

    print('----Tickets----')
    print('number of tickets: ' + str(queueStatus[1]))
    print('current ticket: ' + str(queueStatus[2]))
    print('')
    
    print('----Current Submission----')
    print('ticket owner: ' + str(queueStatus[3]))
    print('ticket being processed: ' + str(queueStatus[4]))
    status = ['IDLE', 'VERIFYING']
    print('ticket status - ' + str(status[queueStatus[5]]))
    print('')

    # print('----Next Script----')
    # next_ticket_key = str(queue[0][3])
    # print('next ticket: ' + next_ticket_key)
    # next_script = contract.submission_data.call(ticket_key, {"from": account})
    # print('script owner: ' + next_script[0])
    # print('script to be processed: ' + next_script[2])
    # print('')

    # print('----Queue State----')
    # print(states[queue[1]])

def main():
    checkStatus()
