// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import {ERC1155} from "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import {Counters} from "@openzeppelin/contracts/utils/Counters.sol";

    //copied from a blog post: https://coinsbench.com/fully-decentralized-erc-721-and-erc-1155-nfts-6c229adf9c9b
abstract contract ERC1155IPFS is ERC1155 {
    mapping (uint256 => string) private _tokenURIs;
    using Counters for Counters.Counter; 
    Counters.Counter private _tokenIds; 
    
        //fed empty string to constructor because the uri is set later, per mint
    constructor() ERC1155("") {} 
    
        //for now, tokenURI is the full IPFS link to the metadata
            //ex: https://ipfs.io/ipfs/bafybeidcuj7x347s2ekyicsu2udaime4dzwf7v5qob446pfspx3j765n7m/ipfs_script_template.json
        //later, this may be adapted to ipfsURI to reduce size
            //ex: ipfs://bafybeibnsoufr2renqzsh347nrx54wcubt5lgkeivez63xvivplfwhtpym/metadata.json
    function mintToken(string memory tokenURI, uint256 amount) public returns(uint256) { 
        uint256 newItemId = _tokenIds.current(); 
        _mint(msg.sender, newItemId, amount, "");
        _setTokenUri(newItemId, tokenURI); 
        _tokenIds.increment(); 
        return newItemId; 
    } 

        //overwrites OpenZeppelin's uri function
    function uri(uint256 tokenId) override public view returns (string memory) { 
        return(_tokenURIs[tokenId]); 
    } 
    
    function _setTokenUri(uint256 tokenId, string memory tokenURI) private {
         _tokenURIs[tokenId] = tokenURI; 
    } 
}