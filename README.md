# Lottery Smart Contract

## Introduction
This project encompasses a smart contract designed for conducting a lottery on the Ethereum blockchain. The lottery contract includes various functions to manage the lottery process, including accepting entrance fees, determining the duration of the lottery, and announcing the winner. Notably, the selection of the random winner is facilitated by a crucial function that leverages the Verifiable Random Function (VRF) Coordinator external contract maintained by Chainlink Labs.

## Contract Address
Rinkeby Etherscan Link: [Lottery Contract](https://rinkeby.etherscan.io/address/0x6AEfe817629bEDFb9E0b33dA20fB0D58A76A1F42)

## Solidity Code
The solidity code for the lottery smart contract can be found below:


## Functions
1. **enterLottery:** Allows participants to enter the lottery by paying the entrance fee.
2. **setDuration:** Sets the duration of the lottery, determining when the winner will be announced.
3. **announceWinner:** Announces the winner of the lottery.
4. **getWinner:** Retrieves the address of the winner.

## VRF Coordinator
The lottery smart contract relies on the Verifiable Random Function (VRF) Coordinator external contract provided by Chainlink Labs to ensure the selection of a random winner in a secure and tamper-proof manner.

## Usage
To participate in the lottery, users can call the `enterLottery` function and submit the required entrance fee. The `setDuration` function can be used to specify the duration of the lottery, after which the `announceWinner` function will determine and reveal the winner.

## Conclusion
The lottery smart contract represents a decentralized and transparent approach to conducting lotteries on the Ethereum blockchain. By integrating with the VRF Coordinator provided by Chainlink Labs, the contract ensures fairness and randomness in selecting the winner, fostering trust among participants.
