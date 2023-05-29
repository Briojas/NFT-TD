// SPDX-License-Identifier: MIT
pragma solidity ^0.8.12;

library CIDProcessorQueue {
    enum State {IDLE, VERIFYING, size} //size is used to iterate through enum, not as a State id
    enum Result {QUEUED, PENDING, APPROVED, REJECTED}

    struct Submission {
        address user;
        uint ticket; //position in the queue for execution
        string ipfs_url; //ipfs link to the item being processed
        Result result; //result of the submission
    }

    struct Tickets {
        uint num_tickets;
        uint curr_ticket;
    }

    struct Queue { 
        mapping(uint => Submission) data;
        string[] submissionBatch; //TODO: implement Batch management
        Tickets tickets;
        State state;
    }

    function initiate(Queue storage self) internal {
        self.tickets.num_tickets = 0; //will increment to 1 after first Submission
        self.tickets.curr_ticket = 0; //first ticket submitted will be ticket 1
        self.state = State(0);
    }

    function join(Queue storage self, address user, string calldata ipfs_url) internal{
        self.tickets.num_tickets ++;
        uint key = self.tickets.num_tickets;
            //submission details
        self.data[key].user = user;
        self.data[key].ticket = key;
        self.data[key].ipfs_url = ipfs_url;
        self.data[key].result = Result(0);
        emit ticket_assigned(
            self.data[key].user, 
            self.data[key].ticket, 
            self.data[key].ipfs_url
        );
    }

    function build_batch(Queue storage self) internal {
        self.submissionBatch = new string[](0); //Chainlink Functions Request.args requires String[]
        set_sub_status(self, Result.PENDING);

            //TODO: implement multi-submission batching
        string memory ipfs_url;
        (,ipfs_url,)= current_ticket(self);
        self.submissionBatch.push(ipfs_url);
    }

    function ticket_approved(Queue storage self) internal {
        set_sub_status(self, Result.APPROVED);
    }

    function ticket_rejected(Queue storage self) internal {
        set_sub_status(self, Result.REJECTED);
    }

    function current_ticket(Queue storage self) internal view returns (address, string memory, Result) {
        return (
            self.data[self.tickets.curr_ticket].user,
            self.data[self.tickets.curr_ticket].ipfs_url,
            self.data[self.tickets.curr_ticket].result
        );
    }

    function update_state(Queue storage self) internal {
        if(State(uint(self.state)) == State(uint(State.size) - 1)){
            self.state = State(0);
        }else{
            self.state = State(uint(self.state) + 1);
        }
    }

    function set_sub_status(Queue storage self, Result result) internal {
        self.data[self.tickets.curr_ticket].result = result;
    }

    event ticket_assigned(
        address user,
        uint ticket,
        string ipfs_url
    );
}