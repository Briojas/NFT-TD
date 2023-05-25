// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import {ConfirmedOwner} from "@chainlink/contracts/src/v0.8/ConfirmedOwner.sol";
import {AutomationCompatibleInterface} from "@chainlink/contracts/src/v0.8/AutomationCompatible.sol";
import {CIDProcessorQueue} from "./libs/CIDProcessorQueue.sol";
import {ERC1155IPFS} from "./libs/ERC1155IPFS.sol";
import {FunctionsWrapper} from "./libs/FunctionsWrapper.sol";

contract PrimeCrusaders is ERC1155IPFS, FunctionsWrapper, AutomationCompatibleInterface {
  uint256 public updateInterval;
  uint256 public lastUpkeepTimeStamp;
  uint256 public upkeepCounter;
  uint256 public responseCounter;

  /**
   * @notice Executes once when a contract is created to initialize state variables
   *
   * @param oracle The FunctionsOracle contract
   * @param subscriptionId The Functions billing subscription ID used to pay for Functions requests
   * @param fulfillGasLimit Maximum amount of gas used to call the client contract's `handleOracleFulfillment` function
   * @param _updateInterval Time interval at which Chainlink Automation should call performUpkeep
   */
  constructor(
    address oracle,
    uint64 subscriptionId,
    uint32 fulfillGasLimit,
    uint256 _updateInterval
  ) ERC1155IPFS() FunctionsWrapper(oracle, subscriptionId, fulfillGasLimit) {
    updateInterval = _updateInterval;
    lastUpkeepTimeStamp = block.timestamp;
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
    upkeepNeeded = (block.timestamp - lastUpkeepTimeStamp) > updateInterval;
  }

  /**
   * @notice Called by Automation to trigger a Functions request
   *
   * The function's argument is unused in this example, but there is an option to have Automation pass custom data
   * returned by checkUpkeep (See Chainlink Automation documentation)
   */
  function performUpkeep(bytes calldata) external override {
    (bool upkeepNeeded, ) = checkUpkeep("");
    require(upkeepNeeded, "Time interval not met");
    lastUpkeepTimeStamp = block.timestamp;
    upkeepCounter = upkeepCounter + 1;

    
  }
}
