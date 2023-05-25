// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import {ERC1155} from "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import {Counters} from "@openzeppelin/contracts/utils/Counters.sol";

    //copied from a blog post: https://coinsbench.com/fully-decentralized-erc-721-and-erc-1155-nfts-6c229adf9c9b
abstract contract ERC1155IPFS is ERC1155 {
    mapping (uint256 => string) private _tokenURIs;
    using Counters for Counters.Counter; 
    Counters.Counter private _tokenIds; 
    
    constructor() ERC1155("") {} 
    
        //were tokenURI is the full IPFS link to the metadata, ex: 
    function mintToken(string memory tokenURI, uint256 amount) public returns(uint256) { 
        uint256 newItemId = _tokenIds.current(); 
        _mint(msg.sender, newItemId, amount, "");
        _setTokenUri(newItemId, tokenURI); 
        _tokenIds.increment(); 
        return newItemId; 
    } 

    function uri(uint256 tokenId) override public view returns (string memory) { 
        return(_tokenURIs[tokenId]); 
    } 
    
    function _setTokenUri(uint256 tokenId, string memory tokenURI) private {
         _tokenURIs[tokenId] = tokenURI; 
    } 
}