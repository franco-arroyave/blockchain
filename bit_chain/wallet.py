from transaction import Transaction

class Wallet:
    '''
    Represents a wallet.
    '''

    def __init__(self, address:str, initial_balance:float=0.0):
        '''
        Initializes a new wallet.
        
        Args:
            address (str): the address of the wallet.
            initial_balance (float): the initial balance of the wallet.
        '''
        self.address = address
        self.balance = initial_balance
        self.transactions = []

    def load(self, w:dict):
        '''
            Initializes a wallet.

            Args:
                w (dict): the wallet
        '''
        self.address = w['address']
        self.balance = w['balance']
        self.transactions = w['transactions']
    
    def get_balance(self):
        '''
        Returns the balance of the wallet.
        
        Returns:
            float: the balance.
        '''
        return self.balance
    
    def deposit(self, tran:Transaction):
        '''
        Deposits money into the wallet.
        
        Args:
            tran (Transaction): the transaction
        '''
        self.balance += tran.get_amount()
        self.transactions.append(tran.get_id())
        print(f"Deposited {tran.get_amount()} units. New balance: {self.balance}")
    
    def withdraw(self, amount:float, toW:str, id:int):
        '''
        Withdraws money from the wallet.
        
        Args:
            amount (float): the amount to withdraw.
            toW (str): the address of the recipient.
            id (int): the id of the transaction.
            
        Returns:
            Transaction: the transaction.

        Raises:
            ValueError: if the amount is greater than the balance.
        '''
        if amount <= self.balance:
            self.balance -= amount
            self.transactions.append(id)
            print(f"Withdrew {amount} units. New balance: {self.balance}")
            return Transaction(fromW=self.address, toW=toW, amount=amount, id=id)
        else:
            print(f"Insufficient funds to withdraw {amount} units.")
            return None

    def get_address(self):
        '''
        Returns the address of the wallet.

        Returns:
            str: the address
        '''
        return self.address

    def get_wallet(self):
        '''
        Returns the wallet.

        Returns:
            dict: the wallet
        '''
        return {'address':self.address, 
                'balance':self.balance, 
                'transactions':self.transactions
                }
