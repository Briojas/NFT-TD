// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import {AutomationCompatibleInterface} from "@chainlink/contracts/src/v0.8/AutomationCompatible.sol";
import {CIDProcessorQueue} from "./libs/CIDProcessorQueue.sol";
import {ERC1155IPFS} from "./libs/ERC1155IPFS.sol";
import {FunctionsWrapper} from "./libs/FunctionsWrapper.sol";

contract PrimeCrusaders is ERC1155IPFS, FunctionsWrapper, AutomationCompatibleInterface {
  using CIDProcessorQueue for CIDProcessorQueue.Queue;
  using CIDProcessorQueue for CIDProcessorQueue.State;
  using CIDProcessorQueue for CIDProcessorQueue.Result;
  
  uint256 public mintInterval; //HIGHLY considering updating to 'minterval'
  uint256 public mintBatchSize; 
  uint256 public lastUpkeepTimeStamp;

  CIDProcessorQueue.Queue private mintingQueue;

  /**
   * @notice Executes once when a contract is created to initialize state variables
   *
   * @param oracle The FunctionsOracle contract
   * @param subscriptionId The Functions billing subscription ID used to pay for Functions requests
   * @param fulfillGasLimit Maximum amount of gas used to call the client contract's `handleOracleFulfillment` function
   * @param _mintInterval Time interval at which Chainlink Automation should call performUpkeep
   */
  constructor(
    address oracle, //Sepolia Functions Oracle address: "0x649a2C205BE7A3d5e99206CEEFF30c794f0E31EC"
    string memory sourceCode,
    uint64 subscriptionId,
    uint32 fulfillGasLimit,
    uint256 _mintInterval,
    uint256 _mintBatchSize
  ) ERC1155IPFS() FunctionsWrapper(oracle, sourceCode, subscriptionId, fulfillGasLimit) {
    mintInterval = _mintInterval;
    mintBatchSize = _mintBatchSize;
    // lastUpkeepTimeStamp = block.timestamp; //uneeded until batch processing implemented  

    mintingQueue.initiate();
  }

  /**
   * @notice Used by Automation to check if performUpkeep should be called.
   *
   * The function's argument is unused in this example, but there is an option to have Automation pass custom data
   * that can be used by the checkUpkeep function.
   *
   * Returns a tuple where the first element is a boolean which determines if upkeep is needed and the
   * second element contains custom bytes data which is passed to performUpkeep when it is called by Automation.
   */
  function checkUpkeep(bytes memory) public view override returns (bool upkeepNeeded, bytes memory) {
    upkeepNeeded = false;
    if (mintingQueue.state == CIDProcessorQueue.State.IDLE) {
      upkeepNeeded = mintingQueue.tickets.curr_ticket < mintingQueue.tickets.num_tickets;
    } else if (gotFunctionResponse()) {
      upkeepNeeded = true;
    } 
    return (upkeepNeeded, ""); //not needed for returning, but we might use the bytes data retun later
  }

  /**
   * @notice Called by Automation to trigger a Functions request
   *
   * The function's argument is unused in this example, but there is an option to have Automation pass custom data
   * returned by checkUpkeep (See Chainlink Automation documentation)
   */
  function performUpkeep(bytes calldata) external override {
    (bool upkeepNeeded, ) = checkUpkeep("");
    require(upkeepNeeded, "upkeep not needed");
    // lastUpkeepTimeStamp = block.timestamp; //uneeded until batch processing implemented

    if (mintingQueue.state == CIDProcessorQueue.State.IDLE){
      submit();
    }else {
      issue();
    }
    mintingQueue.update_state();
  }

    //sends mint request off to Chainlink Functions to be verified 
  function submit() internal {
    mintingQueue.build_batch();
    executeRequest("", mintingQueue.submissionBatch); //secrets unused for now
  }

    //mints valid NFTs
  function issue() internal {
    require (latestResponse.length == mintingQueue.submissionBatch.length);
    for (uint256 i; i < mintingQueue.submissionBatch.length; i++){
        //TODO: update for batch processing
      if(latestResponse[i] == "1"){
        mintToken(mintingQueue.pull_ticket_owner(), mintingQueue.pull_ticket_data(), 1);
        mintingQueue.ticket_approved();
      } else {
        mintingQueue.ticket_rejected();
      }
    }
  }
}
