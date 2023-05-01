# Contract Development

## Setup

- install brownie in virtual env

  ```bash
  pipenv run
  pipenv install -r requirements.txt
  ```

- check brownie version

  ```bash
  pipenv run brownie --version
  ```

- Set `WEB3_INFURA_PROJECT_ID`, and `PRIVATE_KEY` [environment variables](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html) in the `.env` file

  ```
  export WEB3_INFURA_PROJECT_ID=<PROJECT_ID>
  export PRIVATE_KEY=<PRIVATE_KEY>
  ```

- Add the Sepolia network to brownie:

  ```
  pipenv run brownie networks add Ethereum sepolia host=https://sepolia.infura.io/v3/$WEB3_INFURA_PROJECT_ID chainid=11155111 explorer=https://sepolia.etherscan.io/
  ```

  - note: may need to include a ` character before $WEB3_INFURA_PROJECT_ID to recognize the dollar sign as a string

- check sepolia network was added correctly:

  ```bash
  pipenv run brownie networks list true
  ```

- if needed, modify sepolia network details with:
  ```bash
  pipenv run brownie networks modify sepolia host=https://sepolia.infura.io/v3/`$WEB3_INFURA_PROJECT_ID
  ```

## Test Install

```bash
brownie test --network sepolia
```

## Linting

```
pip install black
pip install autoflake
autoflake --in-place --remove-unused-variables --remove-all-unused-imports -r .
black .
```

If you're using [vscode](https://code.visualstudio.com/) and the [solidity extension](https://github.com/juanfranblanco/vscode-solidity), you can create a folder called `.vscode` at the root folder of this project, and create a file called `settings.json`, and add the following content:

```json
{
  "solidity.remappings": [
    "@chainlink/=[YOUR_HOME_DIR]/.brownie/packages/smartcontractkit/chainlink-brownie-contracts@0.2.2",
    "@openzeppelin/=[YOUR_HOME_DIR]/.brownie/packages/OpenZeppelin/openzeppelin-contracts@4.3.2"
  ]
}
```

This will quiet the linting errors it gives you.

## Resources

To get started with Brownie:

- [Chainlink Documentation](https://docs.chain.link/docs)
- Check out the [Chainlink documentation](https://docs.chain.link/docs) to get started from any level of smart contract engineering.
- Check out the other [Brownie mixes](https://github.com/brownie-mix/) that can be used as a starting point for your own contracts. They also provide example code to help you get started.
- ["Getting Started with Brownie"](https://medium.com/@iamdefinitelyahuman/getting-started-with-brownie-part-1-9b2181f4cb99) is a good tutorial to help you familiarize yourself with Brownie.
- For more in-depth information, read the [Brownie documentation](https://eth-brownie.readthedocs.io/en/stable/).

Any questions? Join our [Discord](https://discord.gg/2YHSAey)

## License

This project is licensed under the [MIT license](LICENSE).
