# PrimeCrusaders Contract

- address: 0x15F8a5b8400E203f7C4159c5EaF82A98B7671698

## Description

Solidity contract implements the following functionality:

- Chainlink Automations
  - registry address: 0xE16Df59B887e3Caa439E0b29B42bA2e7976FD8b2
- Chainlink Functions:
  - subid: 334
- ERC1155 Token Standard
- custom IPFS CID processing queue library
  - powered by Automations

## Brownie Setup

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

## Chainlink Functions Configuration

testing using a fork of the official hardhat tool [here](https://github.com/Briojas/functions-hardhat-starter-kit)

## SxT Setup

...Work in progress

for generating new access tokens:

```bash
pipenv run python sxt/register-authenticate.py username
```

for creating schemas and tables with ddl statements:

```bash
pipenv run python sxt/create.py
```

for inserting data into tables with dml statements:

```bash
pipenv run python sxt/modify.py
```

for querying data from tables with dql statements:

```bash
pipenv run python sxt/query.py
```