from transaction import Transaction

class Wallet:
    def __init__(self, address, initial_balance):
        self.address = address
        self.balance = initial_balance
        self.transactions = []

    def __init__(self, w):
        self.address = w['address']
        self.balance = w['balance']
        self.transactions = w['transactions']
    
    def get_balance(self):
        return self.balance
    
    def deposit(self, tran):
        
        self.balance += tran.get_amount()
        self.wallet['transactions'].append(tran.get_id())
        print(f"Deposited {tran['amount']} units. New balance: {self.wallet['balance']}")
    
    def withdraw(self, amount, toW, id):
        if amount <= self.balance:
            self.balance -= amount
            self.transactions.append(id)
            print(f"Withdrew {amount} units. New balance: {self.wallet['balance']}")
            return Transaction(fromW=self.address, toW=toW, amount=amount, id=id)
        else:
            print("Insufficient funds to withdraw {amount} units.")
            return None

    def get_address(self):
        return self.address

    def get_wallet(self):
        return {'address':self.address, 
                'balance':self.balance, 
                'transactions':self.transactions
                }
