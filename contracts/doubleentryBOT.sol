// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * this contract is a Forti bot, to defend the cryptoVault contract (actually defending the underlying DLT token contract)
 **/

import "../interfaces/doubleentry.sol";

contract FortaBot {

    Forta public immutable forta_contract;
    address immutable cryptoVault;
    constructor(address forta_address, address cryptoVault_address) {
      forta_contract=Forta(forta_address);
      cryptoVault=cryptoVault_address;
    }

  // control function, will check that the transfer is not executed by the cryptoVault
  function handleTransaction(address user, bytes calldata msgData) external {
    
    // we check that the origSender parameter is the not the cryptoVault
    // the first 4 bytes of the call data is the function signature

    (,,address origSender) = abi.decode(msgData[4:], (address, uint256, address));

    if(origSender==cryptoVault) {
      forta_contract.raiseAlert(user);
    }

  }
}
