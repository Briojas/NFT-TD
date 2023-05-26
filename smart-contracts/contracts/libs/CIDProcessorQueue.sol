// SPDX-License-Identifier: MIT
pragma solidity ^0.8.12;

    //using the "Iterable Mappings" Solidity example
library CIDProcessorQueue {
    enum State {IDLE, ENCODED, VERIFYING, VERIFIED, size} //size is used to iterate through enum, not as a State id
    enum Result {QUEUED, PENDING, APPROVED, DENIED}

    struct Submission {
        address payable user;
        uint key_index; //storage position in the queue array
        uint ticket; //position in the queue for execution
        string ipfs_url; //ipfs link to the item being processed
        Result result; //result of the submission
    }
    
    //TODO: implement Batch struct to group submissions together for simultaneous processing

    struct Key_Flag { 
        uint key; 
        bool deleted;
    }

    struct Tickets {
        uint num_tickets;
        uint curr_ticket;
        uint curr_ticket_key;
        uint next_submission_key;
    }

    struct Queue { 
        mapping(uint => Submission) data;
        Key_Flag[] keys;
        Tickets tickets;
        State state;
    }
    
    type Iterator is uint;

    function initiate(Queue storage self) internal {
        self.tickets.num_tickets = 0; //will increment to 1 after first Submission
        self.tickets.curr_ticket = 0; //first ticket submitted will be ticket 1
        self.tickets.next_submission_key = 0; //first submission is placed at beginning of queue
        self.state = State.IDLE;
    }

    function join(Queue storage self, string calldata ipfs_url) internal{
        uint key = self.tickets.next_submission_key;
        self.tickets.num_tickets ++;
            //submission details
        self.data[key].ticket = self.tickets.num_tickets;
        self.data[key].ipfs_url = ipfs_url;
        self.data[key].result = Result(0);

        handle_existing_key(self, key);
        set_next_sub_key(self);
    }

    function handle_existing_key(Queue storage self, uint key) internal {
        uint key_index = self.data[key].key_index;
        if (key_index > 0){ //checks if key already existed, and was overwritten
            self.keys[key_index].deleted = false; //a deleted Submission overwritten should not be marked deleted
        } else { //if key didn't exist, the queue array has grown
            key_index = self.keys.length;
            self.keys.push();
            self.data[key].key_index = key_index + 1;
            self.keys[key_index].key = key;
        }
    }

    function remove(Queue storage self, uint key) internal returns (bool success) {
        uint key_index = self.data[key].key_index;
        if (key_index == 0)
            return false;
        delete self.data[key];
        self.keys[key_index - 1].deleted = true;
        return true;
    }

    function set_next_sub_key(Queue storage self) internal {
        self.tickets.next_submission_key = Iterator.unwrap(iterate_deleted(self, 0, false));
    }

    function find_ticket_key(Queue storage self, uint ticket) internal view returns (uint goal_key){
        goal_key = 0;
        for(
            Iterator key = iterate_start(self);
            iterate_valid(self, key);
            key = iterate_next(self, key)
        ){
            if(ticket == self.data[Iterator.unwrap(key)].ticket){
                goal_key =  Iterator.unwrap(key);
            }
        }
    }

    function set_curr_ticket_key(Queue storage self) internal {
        self.tickets.curr_ticket_key = find_ticket_key(self, self.tickets.curr_ticket);
    }

    function update_state(Queue storage self) internal {
        if(State(uint(self.state)) == State(uint(State.size) - 1)){
            self.state = State(0);
        }else{
            self.state = State(uint(self.state) + 1);
        }
    }

    function set_sub_state(Queue storage self, Result result) internal {
        self.data[self.tickets.curr_ticket_key].result = result;
    }

    function iterate_start(Queue storage self) internal view returns (Iterator) {
        return iterate_deleted(self, 0, true);
    }

    function iterate_valid(Queue storage self, Iterator iterator) internal view returns (bool) {
        return Iterator.unwrap(iterator) < self.keys.length;
    }

    function iterate_next(Queue storage self, Iterator iterator) internal view returns (Iterator) {
        return iterate_deleted(self, Iterator.unwrap(iterator) + 1, true);
    }

    function iterate_deleted(Queue storage self, uint key_index, bool skip) internal view returns (Iterator) {
        while (key_index < self.keys.length){
            key_index++;
            if(skip && self.keys[key_index].deleted){
                return Iterator.wrap(key_index); //returns index of next key that is not deleted
            }else if(!skip && !self.keys[key_index].deleted){
                return Iterator.wrap(key_index); //returns index of next key that is deleted
            }
        }
        return Iterator.wrap(key_index); //returns last index; either all were deleted, or none were
    }

    event ticket_assigned(
        address user,
        uint ticket,
        uint ticket_key,
        string cid
    );
}