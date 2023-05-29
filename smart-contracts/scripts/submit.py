from brownie import PrimeCrusaders, Contract
from scripts.helpful_scripts import get_account

data = [
    'https://ipfs.io/ipfs/bafybeidcuj7x347s2ekyicsu2udaime4dzwf7v5qob446pfspx3j765n7m/ipfs_script_template.json'
]

def submit():
    account = get_account()

    contract = PrimeCrusaders[-1]
    print('Working address: ' + contract.address)

    print('')
    print('Joining queue...')
    for submission in data:
        print ('Submission: ' + submission)
        print('address: ' + account.address)
        # gas_cost = contract.joinQueue.estimate_gas(account.address, submission, {"from": account})
        # print('gas cost: ' + str(gas_cost))
        contract.joinQueue(submission, {"from": account})
        submission_event = Contract(contract.address).events.ticket_assigned.get()[-1]
        print(submission_event.name)
        print(submission_event.data)

def main():
    submit()
