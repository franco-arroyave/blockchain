import json
import hashlib
from wallet import Wallet
from transaction import Transaction

wallets = {}
transactions = {}
def load_data():
    '''
    Loads data from json files.
    '''
    with open("wallets.json", "r") as fW:
        global wallets 
        wallets = json.load(fW)
    with open("transactions.json", "r") as fT:
        global transactions 
        transactions = json.load(fT)

def save_data():
    '''
    Saves data to json files.
    '''
    with open("wallets.json", "w") as fW:
        json.dump(wallets, fW)
    with open("transactions.json", "w") as fT:
        json.dump(transactions, fT)


def translate(walletFrom, amount, walletTo):
    '''
    Translates money.
    
    Args:
        walletFrom (Wallet): the wallet to withdraw from.
        amount (float): the amount to transfer.
        walletTo (Wallet): the wallet to deposit to.
    '''
    if len(transactions) == 0:
        id = 0
    else:
        id = len(transactions) + 1
    t = walletFrom.withdraw(amount, walletTo.get_address(), id)
    if type(t) is Transaction:
        transactions[t.get_id()] = t.get_transaction()
        wallets[walletFrom.get_address()] = walletFrom.get_wallet()
        walletTo.deposit(t)
        wallets[walletTo.get_address()] = walletTo.get_wallet()
    else:
        print({'Error':'Transaction not created'})
    save_data()

def hasher(data):
    m = hashlib.sha256()
    m.update(bytes(data, 'utf-8'))
    return m
    #return m.hexdigest()

def create_wallet(address):
    if address not in wallets:
        w = Wallet(address)
        wallets[address] = w.get_wallet()
        save_data()
        return {'Message':'Wallet created'}
    else:
        return {'Error':'Wallet already exists'}

def load_wallet(address:str):
    if address in wallets:
        w = Wallet(address)
        w.load(wallets[address])
        return w
    else:
        return {'Error':'Wallet does not exist'}
    
def init():
    '''
    Initializes the files.json.
    '''
    data = {}	
    with open("wallets.json", "w") as archivo:
        json.dump(data, archivo)
    with open("transactions.json", "w") as archivo:
        json.dump(data, archivo)

def main():
    load_data()
    while True:
        print('----Main-----\n')
        print('1. New wallet\n2. Show wallets\n3. Translate\n4. Init')
        print('5. Exit')
        print('\n------------')
        match input('Option: '):
            case '1':
                print(create_wallet(input('Address: ')))
            case '2':
                print(list(wallets.keys()))
            case '3':
                w1 = load_wallet(input('Address Wallet origin: '))
                w2 = load_wallet(input('Address Wallet destination: '))
                amount = float(input('Amount: '))
                translate(w1, amount, w2)
            case '4':
                init()
            case '5':
                break
            case _:
                print('Invalid option')


main()

