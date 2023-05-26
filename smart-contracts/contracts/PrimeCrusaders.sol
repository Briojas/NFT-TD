// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import {AutomationCompatibleInterface} from "@chainlink/contracts/src/v0.8/AutomationCompatible.sol";
import {CIDProcessorQueue} from "./libs/CIDProcessorQueue.sol";
import {ERC1155IPFS} from "./libs/ERC1155IPFS.sol";
import {FunctionsWrapper} from "./libs/FunctionsWrapper.sol";

contract PrimeCrusaders is ERC1155IPFS, FunctionsWrapper, AutomationCompatibleInterface {
  using CIDProcessorQueue for CIDProcessorQueue.State;
  using CIDProcessorQueue for CIDProcessorQueue.Queue;
  
  uint256 public mintInterval; //HIGHLY considering updating to 'minterval'
  uint256 public mintBatchSize; 
  uint256 public lastUpkeepTimeStamp;

  mapping(CIDProcessorQueue.State => function(CIDProcessorQueue.Queue storage) internal) stateActions;
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
    address oracle,
    uint64 subscriptionId,
    uint32 fulfillGasLimit,
    uint256 _mintInterval,
    uint256 _mintBatchSize
  ) ERC1155IPFS() FunctionsWrapper(oracle, subscriptionId, fulfillGasLimit) {
    mintInterval = _mintInterval;
    mintBatchSize = _mintBatchSize;
    // lastUpkeepTimeStamp = block.timestamp; //uneeded until batch processing implemented  

    mintingQueue.initiate();

    stateActions[CIDProcessorQueue.State.IDLE] = build;
    stateActions[CIDProcessorQueue.State.ENCODED] = send;
    //once sent, we await the callback from Chainlink Functions, which will update the state to VERIFIED
      //callback is the fullfillRequest function in FunctionsWrapper.sol
      //callback will call update_state(): VERIFYING -> VERIFIED
    stateActions[CIDProcessorQueue.State.VERIFIED] = issue;
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
    } else if(mintingQueue.state == CIDProcessorQueue.State.VERIFIED) {
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

    stateActions[mintingQueue.state](mintingQueue);
    mintingQueue.update_state();
  }

    //build the Chainlink Functions request
  function build(CIDProcessorQueue.Queue storage self) internal {
    //TODO: Implement
  }
  
    //sends mint request off to Chainlink Functions to be verified 
  function send(CIDProcessorQueue.Queue storage self) internal {
    //TODO: Implement
  }

    //mints valid NFTs
  function issue(CIDProcessorQueue.Queue storage self) internal {
    //TODO: Implement
  }
}
