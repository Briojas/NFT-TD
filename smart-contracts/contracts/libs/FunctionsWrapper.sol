// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import {Functions, FunctionsClient} from "../dev/functions/FunctionsClient.sol";
// import "@chainlink/contracts/src/v0.8/dev/functions/FunctionsClient.sol"; // Once published
import {ConfirmedOwner} from "@chainlink/contracts/src/v0.8/ConfirmedOwner.sol";

abstract contract FunctionsWrapper is FunctionsClient, ConfirmedOwner {
    using Functions for Functions.Request;

    bytes public requestCBOR;
    bytes32 public latestRequestId;
    bytes public latestResponse;
    bytes public latestError;
    uint64 public subscriptionId;
    uint32 public fulfillGasLimit;

    event OCRResponse(bytes32 indexed requestId, bytes result, bytes err);

    constructor(
        address oracle,
        uint64 _subscriptionId,
        uint32 _fulfillGasLimit
    ) FunctionsClient(oracle) ConfirmedOwner(msg.sender) {
        subscriptionId = _subscriptionId;
        fulfillGasLimit = _fulfillGasLimit;
    }

    /**
   * @notice Generates a new Functions.Request. This pure function allows the request CBOR to be generated off-chain, saving gas.
   *
   * @param source JavaScript source code
   * @param secrets Encrypted secrets payload
   * @param args List of arguments accessible from within the source code
   */
    function generateRequest(
        string calldata source,
        bytes calldata secrets,
        string[] calldata args
    ) public pure returns (bytes memory) {
        Functions.Request memory req;
        req.initializeRequest(Functions.Location.Inline, Functions.CodeLanguage.JavaScript, source);
        if (secrets.length > 0) req.addRemoteSecrets(secrets);
        if (args.length > 0) req.addArgs(args);
        return req.encodeCBOR();
    }

    /**
    * @notice Sets the bytes representing the CBOR-encoded Functions.Request that is sent when performUpkeep is called

    * @param _subscriptionId The Functions billing subscription ID used to pay for Functions requests
    * @param _fulfillGasLimit Maximum amount of gas used to call the client contract's `handleOracleFulfillment` function
    * @param newRequestCBOR Bytes representing the CBOR-encoded Functions.Request
    */
    function setRequest(
        uint64 _subscriptionId,
        uint32 _fulfillGasLimit,
        bytes calldata newRequestCBOR
    ) external onlyOwner {
        subscriptionId = _subscriptionId;
        fulfillGasLimit = _fulfillGasLimit;
        requestCBOR = newRequestCBOR;
    }

    /**
    * @notice Called by performUpkeep to make the Functions sendRequest call
    */
    function callRequest() private {
        bytes32 requestId = s_oracle.sendRequest(subscriptionId, requestCBOR, fulfillGasLimit);

        s_pendingRequests[requestId] = s_oracle.getRegistry();
        emit RequestSent(requestId);
        latestRequestId = requestId;
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

    /**
    * @notice Allows the Functions oracle address to be updated
    *
    * @param oracle New oracle address
    */
    function updateOracleAddress(address oracle) public onlyOwner {
        setOracle(oracle);  
    }
}