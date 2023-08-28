import os
import json
import hashlib
from wallet import Wallet
from transaction import Transaction
from block import Block


wallets = {}
transactions = {}
queueTrans = []
blocks = {'blocks':[]}

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
    with open("blocks.json", "r") as fB:
        global blocks
        blocks = json.load(fB)

def save_data():
    '''
    Saves data to json files.
    '''
    with open("wallets.json", "w") as fW:
        json.dump(wallets, fW)
    with open("transactions.json", "w") as fT:
        json.dump(transactions, fT)
    with open("blocks.json", "w") as fB:
        json.dump(blocks, fB)

def translate(walletFrom:Wallet, amount:float, walletTo:Wallet):
    '''
    Translates money.
    
    Args:
        walletFrom (Wallet): the wallet to withdraw from.
        amount (float): the amount to transfer.
        walletTo (Wallet): the wallet to deposit to.
    '''
    id = len(transactions)
    t = walletFrom.withdraw(amount, walletTo.get_address(), id)
    if type(t) is Transaction:
        transactions[t.get_id()] = t.get_transaction()
        wallets[walletFrom.get_address()] = walletFrom.get_wallet()
        walletTo.deposit(t)
        wallets[walletTo.get_address()] = walletTo.get_wallet()
    else:
        print({'Error':'Transaction not created'})
    save_data()

def addTran(walletFrom:Wallet, amount:float, walletTo:Wallet):
    '''
    enqueue transaction for the block.
    
    Args:
        walletFrom (Wallet): the wallet to withdraw from.
        amount (float): the amount to transfer.
        walletTo (Wallet): the wallet to deposit to.
    '''
    if len(transactions) == 0:
        id = 0
    else:
        id = len(transactions)
    t = walletFrom.withdraw(amount, walletTo.get_address(), id)
    if type(t) is Transaction:
        queueTrans.append(t.get_transaction())
        transactions[t.get_id()] = t.get_transaction()
        wallets[walletFrom.get_address()] = walletFrom.get_wallet()
    else:
        print({'Error':'Transaction not created'})
    save_data()

def add_block(wNode:Wallet):
    '''
    Adds a block to the blockchain.

    Args:
        wNode (Wallet): the wallet (node) that mine the block.
    '''
    global queueTrans
    if len(blocks['blocks']) == 0:
        id = 0
        cb = coinbase(wNode)
        phash = hasher(str('0'))
        block = Block(id, [cb.get_transaction()], phash)
    elif len(queueTrans)>0:
        id = len(blocks['blocks'])
        cb = coinbase(wNode)
        phash = blocks['blocks'][len(blocks['blocks'])-1]['hash']
        t = [cb.get_transaction()]+queueTrans
        block = Block(id, t, phash)
    else:
        print({'Error':'No transaction to add'})
        return None
    
    blockDict = block.find_nonce()
    blocks['blocks'].append(blockDict)
    for tran in blockDict['block']['body']['transactions']:
        tranObj = Transaction(tran['id'], tran['fromW'], tran['toW'], tran['amount'], tran['timestamp'])
        toWallet = load_wallet(tran['toW'])
        toWallet.deposit(tranObj)
        wallets[toWallet.get_address()] = toWallet.get_wallet()
    queueTrans = []
    save_data()
    
def coinbase(wNode:Wallet):
    '''
    Generate a coinbase transaction.
    
    Args:
        wNode (Wallet): the wallet to deposit to.
    '''
    t = Transaction(len(transactions), 'coinbase', wNode.get_address(), 1.0)
    transactions[t.get_id()] = t.get_transaction()
    save_data()
    return t

def hasher(data:str):
    '''
    Hashes data.

    Args:
        data (str): the data to hash.

    Returns:   
        str: the hashed data
    '''

    m = hashlib.sha256()
    m.update(bytes(data, 'utf-8'))
    #return m
    return m.hexdigest()

def create_wallet(address:str):
    '''
    Creates a wallet.

    Args:
        address (str): the address of the wallet.
    Returns:
        dict: the wallet.
    '''

    if address not in wallets:
        w = Wallet(address)
        wallets[address] = w.get_wallet()
        save_data()
        return {'Message':'Wallet created'}
    else:
        return {'Error':'Wallet already exists'}

def load_wallet(address:str):
    '''
    Loads a wallet to dict wallets .
    
    Args:
        address (str): the address of the wallet.
        
    Returns:
        dict: the wallet
    '''
    if address in wallets:
        w = Wallet(address)
        w.load(wallets[address])
        return w
    else:
        raise Exception('Error', 'Wallet does not exist')
    
def init():
    '''
    Initializes the files.json.
    '''	
    with open("wallets.json", "w") as archivo:
        json.dump(wallets, archivo)
    with open("transactions.json", "w") as archivo:
        json.dump(transactions, archivo)
    with open("blocks.json", "w") as archivo:
        json.dump(blocks, archivo)

def main():
    '''
    Main function, just create transfers.
    '''
    if os.path.exists('wallets.json') and os.path.exists('transactions.json') and os.path.exists('blocks.json'):
        load_data()
    else:
        init()
    while True:
        print('----Menu-----\n')
        print('1. New wallet\n2. Show wallets\n3. Translate\n4. Init')
        print('0. Exit')
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
            case '0':
                save_data()
                break
            case _:
                print('Invalid option')

def main2():
    '''
    Main function, Creates the transfers and queues them to be processed in one block.
    '''
    if os.path.exists('wallets.json') and os.path.exists('transactions.json') and os.path.exists('blocks.json'):
        load_data()
    else:
        init()
    while True:
        print('----Menu-----\n')
        print('1. New wallet\n2. Show wallets\n3. Translate\n4. Add block')
        print('0. Exit')
        print('\n------------')
        match input('Option: '):
            case '1':
                print(create_wallet(input('Address: ')))
            case '2':
                print(list(wallets.keys()))
            case '3':
                try:
                    w1 = load_wallet(input('Address Wallet origin: '))
                    w2 = load_wallet(input('Address Wallet destination: '))
                    amount = float(input('Amount: '))
                    addTran(w1, amount, w2)
                except Exception as e:
                    print(e)
            case '4':
                add_block(load_wallet(input('Address Wallet mine: ')))
            case '0':
                break
            case _:
                print('Invalid option')

main2()

