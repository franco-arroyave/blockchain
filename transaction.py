import time

class Transaction:

    def __init__(self, id, fromW, toW, amount):
        self.id = id
        self.fromW = fromW
        self.toW = toW
        self.amount = amount
        self.timestamp = time.time()
        self.id = id

    def get_id(self):
        return self.id

    def get_amount(self):
        return self.amount

    def get_transaction(self):
        return {'id':self.id, 
                'fromW':self.fromW, 
                'toW':self.toW, 
                'amount':self.amount, 
                'timestamp':self.timestamp
                }