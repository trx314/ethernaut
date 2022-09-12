// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// import "../interfaces/reentrance.sol";
// import "../interfaces/elevator.sol";

/**
 * contract to simulate it is a Building and trick the elevator
 * with a function isLastFlloor() with same arguments and make it return what it wants
 */
contract gatekeeperAttack {

    // address payable public target;
    // Elevator public immutable target;
    uint64 public test_uint;
    constructor() {
        test_uint=uint64(0);
    }


// attack function to call the target contract
  function test() external {
    test_uint=uint64(0) - 1;
  }
}
