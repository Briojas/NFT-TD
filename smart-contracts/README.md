# PrimeCrusaders Contract

- address: 0x9f6105FB3b13F99F074cDC0CDDbc8222a9cc5129

## Description

Solidity contract implements the following functionality:

- Chainlink Automations
  - registry address: 0xE16Df59B887e3Caa439E0b29B42bA2e7976FD8b2
- Chainlink Functions:
  - subid: 334
- ERC1155 Token Standard
- custom IPFS CID processing queue library
  - powered by Automations

## Setup

1. install pipenv
2. install dependencies

```bash
pipenv install
```

3. add environment variables

- WEB3_INFURA_PROJECT_ID - infura rpc
- PRIVATE_KEY - private key of the deployer account
- ETHERSCAN_TOKEN - etherscan api token

4. deploy contract

```bash
pipenv run brownie run scripts/deploy.py --network sepolia
```

5. Use the [Chainlink Functions Hardhat](https://github.com/smartcontractkit/functions-hardhat-starter-kit/tree/main) tool to generate subscription and add contract to subid

- see repo for details

6. Add contract to [Chainlink Automations](https://automation.chain.link/) registry

7. Prime contract with data from IPFS

```bash
pipenv run brownie run scripts/submit.py --network sepolia
```

8. Monitor status of contract

```bash
pipenv run brownie run scripts/checkstatus.py --network sepolia
```
