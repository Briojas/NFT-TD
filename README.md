# NFT_TD

[Quantifying Semi-Fungible Tokens](https://lucid.app/lucidchart/2e5db8d6-8e89-4b3f-bd9c-c5e5e2881ebd/edit?viewport_loc=1196%2C-222%2C3328%2C1742%2C0_0&invitationId=inv_e4ef847c-63fc-4e43-8b84-f26cfb9ce26d)

## Inspiration

Non-fungible and Semi-fungible tokens represent the future of digital assets. Currently, most implementations of utility-based NFTs or SFTs are restricted to fixed supply sizes and metadata. We wanted to create a way to quantify the tolerances of NFTs and SFTs to allow for more dynamic and flexible tokenomics.

## What it does

We created a smart contract that allows for the minting of SFTs within a specified tolerance. Each SFT has seven sections of its metadata hashed through IPFS. The tolerance for minting, for this project, is defined as 15% (1/7 hashes) being unique.

## How we built it

Chainlink Functions
Space and Time (SxT)
Chainlink Automations
Brownie 
Hardhat

## Challenges we ran into

Configuring SxT to work with Chainlink Functions was especially difficult since I had decided to work with Brownie. So, I had to use the hardhat functions tool chainlink built for the beta to test interactions before attempting to deploy. This was all a headache.

## Accomplishments that we're proud of

Completing a end-to-end demo of a user editing an NFT's metadata, submitting it to be minted, handling that submission though a queue with Chainlink Automations, utilizing Automations to make a Chainlink Functions request to verify that user's NFT submission is within the specified tolerance, adding missing NFT data back into the SxT database, and then minting the NFT to the user if approved.

## What we learned

We learned how to use Chainlink Functions, Chainlink Automations, and Space and Time (SxT) to create a dynamic NFT minting system. It was a blast working with the Functions and SxT closed betas. I hope to provide feedback to support the development of these tools.

## What's next for Verifying NFT Tolerances

We would like to actually implement the game this minting system was designed for. We want to see what affect on the size of the total pool of NFTs will be from a system like this, and how we can tune the parameters to obtain the desired token distribution.
