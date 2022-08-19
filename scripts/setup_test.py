from brownie import *
import os

# envt setup
current_network=network.show_active()
acct_pwd=os.getenv("ACCT_PWD")

test_acct=accounts.load('ethernaut_rinkeby',acct_pwd)

def main():
    print("hello!!!")
    print("curent network is",current_network)
    print("test_acct:", test_acct)

