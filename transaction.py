import time

class Transaction:
    '''
    Represents a transaction.
    '''

    def __init__(self, id, fromW, toW, amount, timestamp=time.time()):
        '''
        Initializes a transaction.
        
        Args:
            id (int): the id of the transaction.
            fromW (str): the address of the sender.
            toW (str): the address of the receiver.
            amount (float): the amount of the transaction.
        '''
        
        self.id = id
        self.fromW = fromW
        self.toW = toW
        self.amount = amount
        self.timestamp = timestamp

    def get_id(self):
        '''
        Returns the id of the transaction.

        Returns:
            int: the id
        '''
        return self.id

    def get_amount(self):
        '''
        Returns the amount of the transaction.
        
        Returns:
            float: the amount.
        '''
        return self.amount

    def get_transaction(self):
        '''
        Returns the transaction.
        
        Returns:
            dict: the transaction.
        '''
        return {'id':self.id, 
                'fromW':self.fromW, 
                'toW':self.toW, 
                'amount':self.amount, 
                'timestamp':self.timestamp
                }