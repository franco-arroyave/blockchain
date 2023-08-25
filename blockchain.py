import json as jn
import hashlib
from wallet import Wallet
from transaction import Transaction

wallets = jn.loads(open ("wallets.json").read())
transactions = jn.loads(open ("transactions.json").read())

def transfer(wallet, amount, walletTo):
    if len(transactions) == 0:
        id = 0
    else:
        id = max(transactions.keys()) + 1
    t = wallet.withdraw(amount, walletTo.get_address(), id)
    if type(t) is Transaction:
        transactions.append(t.get_id(), t.get_transaction())
        walletTo.deposit(t)



my_wallet.deposit(50)
my_wallet.withdraw(30)

print(f"Final balance: {my_wallet.get_balance()}")

def hasher(data):
    m = hashlib.sha256()
    m.update(bytes(data, 'utf-8'))
    return m
    #return m.hexdigest()
