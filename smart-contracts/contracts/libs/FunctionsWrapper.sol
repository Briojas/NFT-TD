// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import {Functions, FunctionsClient} from "../dev/functions/FunctionsClient.sol";
// import "@chainlink/contracts/src/v0.8/dev/functions/FunctionsClient.sol"; // Once published
import {ConfirmedOwner} from "@chainlink/contracts/src/v0.8/ConfirmedOwner.sol";

abstract contract FunctionsWrapper is FunctionsClient, ConfirmedOwner {
    using Functions for Functions.Request;

    string public sourceCode;
    bytes32 public latestRequestId;
    bytes public latestResponse;
    bytes public latestError;
    uint8 public responseHeaderSize = 4;
    uint64 public subscriptionId;
    uint32 public fulfillGasLimit;

    event OCRResponse(bytes32 indexed requestId, bytes result, bytes err);

    constructor(
        address oracle,
        string memory _sourceCode,
        uint64 _subscriptionId,
        uint32 _fulfillGasLimit
    ) FunctionsClient(oracle) ConfirmedOwner(msg.sender) {
        sourceCode = _sourceCode;
        subscriptionId = _subscriptionId;
        fulfillGasLimit = _fulfillGasLimit;
        resetFunctionResponse();
    }

    /**
   * @notice Generates a new Functions.Request.
   *
   * @param secrets Encrypted secrets payload
   * @param args List of arguments accessible from within the source code
   */
    function executeRequest(
        bytes memory secrets,
        string[] memory args
    ) internal {
        Functions.Request memory req;
        req.initializeRequest(Functions.Location.Inline, Functions.CodeLanguage.JavaScript, sourceCode);
        if (secrets.length > 0) req.addRemoteSecrets(secrets);
        if (args.length > 0) req.addArgs(args);
        
        bytes32 assignedReqID = sendRequest(req, subscriptionId, fulfillGasLimit);
        latestRequestId = assignedReqID;
    }

    /**
    * @notice Callback that is invoked once the DON has resolved the request or hit an error
    *
    * @param requestId The request ID, returned by sendRequest()
    * @param response Aggregated response from the user code
    * @param err Aggregated error from the user code or from the execution pipeline
    * Either response or error parameter will be set, but never both
    */
    function fulfillRequest(bytes32 requestId, bytes memory response, bytes memory err) internal override {
        latestResponse = response;
        latestError = err;
        emit OCRResponse(requestId, response, err);
    }

    function gotFunctionResponse() internal view returns (bool) {
        return latestResponse.length != latestError.length;
    }

    function validFunctionResponse(uint submissionSize) internal view returns (bool) {
        require(latestResponse.length >= responseHeaderSize, "Invalid response length");
        return (latestResponse.length - responseHeaderSize) == submissionSize;
    }

    function resetFunctionResponse() internal {
        latestResponse = ""; 
        latestError = "";
    }
        
    function updateSourceCode(string memory _sourceCode) public onlyOwner {
        sourceCode = _sourceCode;
    }

    function updateOracleAddress(address oracle) public onlyOwner {
        setOracle(oracle);  
    }

    function updateSubscriptionId(uint64 _subscriptionId) public onlyOwner {
        subscriptionId = _subscriptionId;
    }
}