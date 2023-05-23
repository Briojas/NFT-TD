// SPDX-License-Identifier: MIT
pragma solidity ^0.8.12;

import "@chainlink/contracts/src/v0.8/ChainlinkClient.sol";
import "@chainlink/contracts/src/v0.8/AutomationCompatible.sol";
import "@chainlink/contracts/src/v0.8/ConfirmedOwner.sol";

    //using the "Iterable Mappings" Solidity example
struct Submission {
    address payable player;
    uint key_index; //storage position in the queue array
    uint ticket; //position in the queue for execution
    bytes[2] script_cid; //script IPFS CID broken into halves
    bool executed; //sent for execution
    uint score; //score after execution finished
}

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

enum States {READY, EXECUTING, EXECUTED, COLLECTING, COLLECTED}

struct Queue { 
    mapping(uint => Submission) data;
    Key_Flag[] keys;
    Tickets tickets;
    States state;
}

struct High_Score {
    uint reset_interval;
    uint score;
    address payable leader;
    //todo: add growing pool of tokens here to award leader after reset interval rolls over
}

type Iterator is uint;

library Queue_Management {
    function initiate(Queue storage self) internal {
        self.tickets.num_tickets = 0; //will increment to 1 after first Submission
        self.tickets.curr_ticket = 0; //first ticket submitted will be ticket 1
        self.tickets.next_submission_key = 0; //first submission is placed at beginning of queue
        self.state = States.READY;
    }

    function insert(Queue storage self, bytes calldata script_cid_1, bytes calldata script_cid_2) internal{
        uint key = self.tickets.next_submission_key;
        uint key_index = self.data[key].key_index;
        self.tickets.num_tickets ++;
        self.data[key].ticket = self.tickets.num_tickets;
        self.data[key].script_cid[0] = script_cid_1;
        self.data[key].script_cid[1] = script_cid_2;
        self.data[key].executed = false;
        if (key_index > 0){ //checks if key already existed, and was overwritten
            self.keys[key_index].deleted = false; //a deleted Submission overwritten should not be marked deleted
        } else { //if key didn't exist, the queue array has grown
            key_index = self.keys.length;
            self.keys.push();
            self.data[key].key_index = key_index + 1;
            self.keys[key_index].key = key;
        }
        set_next_submission_key(self);
    }

    function remove(Queue storage self, uint key) internal returns (bool success) {
        uint key_index = self.data[key].key_index;
        if (key_index == 0)
            return false;
        delete self.data[key];
        self.keys[key_index - 1].deleted = true;
        return true;
    }

    function set_next_submission_key(Queue storage self) internal {
        if(self.keys.length < 0){
            self.tickets.next_submission_key = 0;
        }
        self.tickets.next_submission_key = Iterator.unwrap(iterator_find_next_deleted(self, 0));
    }

    function find_ticket_key(Queue storage self, uint ticket) internal view returns (uint goal_key){
        for(
            Iterator key = iterate_start(self);
            iterate_valid(self, key);
            key = iterate_next(self, key)
        ){
            if(!self.data[Iterator.unwrap(key)].executed && ticket == self.data[Iterator.unwrap(key)].ticket){
                goal_key =  Iterator.unwrap(key);
            }
        }
    }

    function set_curr_ticket_key(Queue storage self) internal {
        self.tickets.curr_ticket_key = find_ticket_key(self, self.tickets.curr_ticket);
    }

    function pull_ticket(Queue storage self) internal view returns (string memory) {
        string memory script_cid_1 = string(self.data[self.tickets.curr_ticket_key].script_cid[0]);
        string memory script_cid_2 = string(self.data[self.tickets.curr_ticket_key].script_cid[1]);

        return string.concat(script_cid_1, script_cid_2);
    }

    function update_state(Queue storage self) internal {
        if(self.state == States.READY){
            self.state = States.EXECUTING;
        }else if(self.state == States.EXECUTING){
            self.state = States.EXECUTED;
        }else if(self.state == States.EXECUTED){
            self.state = States.COLLECTING;
        }else if(self.state == States.COLLECTING){
            self.state = States.COLLECTED;
        }else if(self.state == States.COLLECTED){
            self.state = States.READY;
        }
    }

    function update_execution_status(Queue storage self, bool status) internal {
        self.data[self.tickets.curr_ticket_key].executed = status;
    }

    function update_score(Queue storage self, uint score) internal {
        self.data[self.tickets.curr_ticket].score = score;
    }

    function iterate_start(Queue storage self) internal view returns (Iterator) {
        return iterator_skip_deleted(self, 0);
    }

    function iterate_valid(Queue storage self, Iterator iterator) internal view returns (bool) {
        return Iterator.unwrap(iterator) < self.keys.length;
    }

    function iterate_next(Queue storage self, Iterator iterator) internal view returns (Iterator) {
        return iterator_skip_deleted(self, Iterator.unwrap(iterator) + 1);
    }

    function iterator_skip_deleted(Queue storage self, uint key_index) internal view returns (Iterator) {
        while (key_index < self.keys.length && self.keys[key_index].deleted)
            key_index++;
        return Iterator.wrap(key_index);
    }
    
    function iterator_find_next_deleted(Queue storage self, uint key_index) internal view returns (Iterator) {
        while (key_index < self.keys.length && !self.keys[key_index].deleted)
            key_index++;
        return Iterator.wrap(key_index);
    }
}

contract BeOurPest is ChainlinkClient, AutomationCompatibleInterface, ConfirmedOwner{
        //activity data
    Queue public activity;
    using Queue_Management for Queue;

    High_Score public high_score;
    uint private high_score_time_stamp;

    uint private retry_submitting_interval;
    uint private retry_scoring_interval;
    uint private retry_time_stamp;
    uint16 public retry_attempts;
    uint16 public max_retry_attempts;

    event submission_ticket(
        address user,
        uint ticket,
        uint ticket_key,
        string script_cid
    );
    event executed_ticket(
        address player,
        uint ticket,
        bool executed
    );
    event scored_ticket(
        address player,
        uint ticket,
        uint score
    );
    
        //node data
    using Chainlink for Chainlink.Request;
    address private oracle;
    bytes32 private job_id_pubsub_int;
    bytes32 private job_id_pub_str;
    uint256 private oracle_fee; //LINK
    uint256 private queue_fee; //ETH //currently unused due to goEth being nearly unobtainable
    string private score_topic = "/score";
    
    /**
     * Network: Goerli
     * Link token: 0x326C977E6efc84E512bB9C30f76E30c160eD06FB
     * Oracle: 0x4e79B49ed00c905c732Eaa535D6026237D4AB9f0
     * Job IDs: below
     * Oracle Fee: 0.01 LINK 
     * Queue Fee: 0.001 ETH
     */
    constructor(uint score_reset_interval_sec, uint retry_submitting_interval_sec, uint retry_scoring_interval_sec) ConfirmedOwner(msg.sender) {
        //Chainlink services management
        setChainlinkToken(0x326C977E6efc84E512bB9C30f76E30c160eD06FB);
        oracle = 0x4e79B49ed00c905c732Eaa535D6026237D4AB9f0;
        job_id_pubsub_int =  "d9de30463fdd429aab7c2ed8dde708d8";
        job_id_pub_str =  "01c687c6a43e4b4a80d9f0f62eed6a5c";
        oracle_fee = 0.01 * (10 ** 18);
        queue_fee = 0.001 * (10 ** 18);

        //start the queue
        activity.initiate();

        //retry management
        retry_submitting_interval = retry_submitting_interval_sec; //time to retry running a submitted ticket
        retry_scoring_interval = retry_scoring_interval_sec; //time to retry grabbing a ticket's score
        max_retry_attempts = 5;
        retry_attempts = 0;

        //high score management
        high_score.reset_interval = score_reset_interval_sec; //time to reset the activity's high score
        high_score.score = 0;
        high_score.leader = payable(0);
        high_score_time_stamp = block.timestamp;
    }

    function checkUpkeep(bytes calldata checkData) external override view returns (bool upkeepNeeded, bytes memory performData) {
            //high score may be reset while processing a submission
        upkeepNeeded = (block.timestamp - high_score_time_stamp) > high_score.reset_interval;

        if(activity.state == States.READY){
            upkeepNeeded = activity.tickets.curr_ticket < activity.tickets.num_tickets;
        }else if(activity.state == States.EXECUTING){
            upkeepNeeded = (block.timestamp - retry_time_stamp) > retry_submitting_interval;
        }else if(activity.state== States.EXECUTED){
            upkeepNeeded = true;
        }else if(activity.state== States.COLLECTING){
            upkeepNeeded = (block.timestamp - retry_time_stamp) > retry_scoring_interval;
        }else if(activity.state == States.COLLECTED){
            upkeepNeeded = true;
        }
        performData = checkData; //unused. separated logic executed based on internal states
    }

    function performUpkeep(bytes calldata performData) external override {
        performData; //unused. see above

        if((block.timestamp - high_score_time_stamp) > high_score.reset_interval){
            high_score_time_stamp = block.timestamp;
            award_winner();
            //todo: remove deleted keys from the end of the queue for efficient contract sizing
        }
        if(activity.state == States.READY && activity.tickets.curr_ticket < activity.tickets.num_tickets){
            retry_time_stamp = block.timestamp;
            activity.tickets.curr_ticket ++;
            activity.set_curr_ticket_key();
            execute_submission();
        }else if(activity.state == States.EXECUTING && (block.timestamp - retry_time_stamp) > retry_submitting_interval){
            activity.state = States.READY;
            //todo: track number of retries
        }else if(activity.state == States.EXECUTED){
            retry_time_stamp = block.timestamp;
            retry_attempts = retry_attempts + 1;
            collect_score();
        }else if(activity.state == States.COLLECTING && (block.timestamp - retry_time_stamp) > retry_submitting_interval){
            if(retry_attempts > max_retry_attempts){
                activity.state = States.READY;
            }else{
                activity.state = States.EXECUTED;
            }
        }else if(activity.state == States.COLLECTED){
            check_for_high_score();
        }
    }

        //todo: make join_queue payable for populating award pool?
    function join_queue(bytes calldata script_cid_1, bytes calldata script_cid_2) public returns (uint ticket, uint ticket_key){
        // require(msg.value == queue_fee); //make payable to obtain fees?
        activity.insert(script_cid_1, script_cid_2);
        ticket_key = activity.tickets.next_submission_key - 1;
        ticket = activity.data[ticket_key].ticket; 
        emit submission_ticket(
            address(msg.sender),
            ticket,
            ticket_key,
            activity.pull_ticket()
        );
    }

    function submission_data(uint ticket_key) public view returns (
        address player,
        uint ticket,
        string memory script_cid,
        bool executed,
        uint score
    ){
        player = activity.data[ticket_key].player; 
        ticket = activity.data[ticket_key].ticket;
        string memory script_cid_1 = string(activity.data[ticket_key].script_cid[0]);
        string memory script_cid_2 = string(activity.data[ticket_key].script_cid[1]);
        script_cid = string.concat(script_cid_1, script_cid_2);
        executed = activity.data[ticket_key].executed;
        score = activity.data[ticket_key].score;
    }
    
    /**
     * Chainlink requests to
            - send IPFS scripts to cl-ea-mqtt-relay for executing activitys (execute_sumbission)
            - subscribe on activity score topics to pull score data (grab_score)
        on the MQTT broker(s) utilized by the Node's External Adapter managing the activity's state.
     */
    function execute_submission() private returns (bytes32 requestId){
        string memory action = "ipfs";
        string memory topic = "script";
        string memory payload = activity.pull_ticket();
        activity.update_state(); //States: READY -> EXECUTING

            //TODO: test qos levels 
        return call_pub_str(action, topic, 0, payload, 0); 
            
            //now sending ipfs CID directly to hardware for processing
            //hardware will query ipfs for the json script, and execute locally
            //"call_ipfs()" not needed currently, but may reimplement for future functionality
        //return call_ipfs(topic, payload); //qos and retained flags ignored
    }
    function collect_score() private returns (bytes32 requestId){
        string memory action = "subscribe";
        activity.update_state(); //States: EXECUTED -> COLLECTING
        return call_pubsub_int(action, score_topic, 0, 0, 0); //payload and retained flag ignored
    }
    function call_pubsub_int(
        string memory _action, 
        string memory _topic, 
        int16 _qos, 
        int256 _payload, 
        int16 _retain
        ) private returns (bytes32 requestId){
            Chainlink.Request memory request = buildChainlinkRequest(job_id_pubsub_int, address(this), this.fulfill_score.selector);
            
            // Set the params for the external adapter
            request.add("action", _action); //options: "publish", "subscribe"
            request.add("topic", _topic);
            request.addInt("qos", _qos);
            request.addInt("payload", _payload); //int
            request.addInt("retain", _retain);
            
            // Sends the request
            return sendChainlinkRequestTo(oracle, request, oracle_fee);
    }

    function call_pub_str( 
        string memory _action, 
        string memory _topic, 
        int16 _qos,  
        string memory _payload,
        int16 _retain
        ) private returns (bytes32 requestId){
            Chainlink.Request memory request = buildChainlinkRequest(job_id_pub_str, address(this), this.fulfill_execution_request.selector);
            
            // Set the params for the external adapter
            request.add("action", _action); //options: "publish"
            request.add("topic", _topic); 
            request.addInt("qos", _qos);
            request.add("payload", _payload); //string
            request.addInt("retain", _retain);
            
            // Sends the request
            return sendChainlinkRequestTo(oracle, request, oracle_fee);
    }

    function fulfill_execution_request(bytes32 _requestId, bool status) public recordChainlinkFulfillment(_requestId){
        emit executed_ticket(
            activity.data[activity.tickets.curr_ticket_key].player,
            activity.data[activity.tickets.curr_ticket_key].ticket,
            status);
        if (status){
            activity.update_execution_status(status);
            activity.update_state(); //States: EXECUTING -> EXECUTED
        }else{
            activity.state = States.READY; //resetting states 
        }
        
    }
    function fulfill_score(bytes32 _requestId, uint256 score) public recordChainlinkFulfillment(_requestId){
        activity.update_score(score); 
        emit scored_ticket(
            activity.data[activity.tickets.curr_ticket_key].player,
            activity.data[activity.tickets.curr_ticket_key].ticket,
            score);
        activity.update_state(); //States: COLLECTING -> COLLECTED
    }

    function check_for_high_score() private {
        if(activity.data[activity.tickets.curr_ticket_key].score > high_score.score){
            high_score.score = activity.data[activity.tickets.curr_ticket_key].score;
            high_score.leader = activity.data[activity.tickets.curr_ticket_key].player;
        }
        activity.update_state(); //States: COLLECTED -> READY
    }

    function award_winner() private {
        //todo: award pool to winner before resetting current leader and current high score
        high_score.leader = payable(0);
        high_score.score = 0;
    }

    function withdraw_link() public onlyOwner {
        LinkTokenInterface link = LinkTokenInterface(chainlinkTokenAddress());
        require(link.transfer(msg.sender, link.balanceOf(address(this))), "Unable to transfer");
    }

    function withdraw_eth() public onlyOwner {
        address payable to = payable(msg.sender);
        to.transfer(address(this).balance);
    }
    function debug_reset() public onlyOwner {
        //only using for testing
        //probably need an actual version of this, but need it based on a time interval for resetting
        activity.state = States.READY; //resetting states ; 
    }
}
