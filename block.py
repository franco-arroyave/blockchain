import hashlib
import time

class Block:

    def __init__(self, id:int, transactions:list, previous_hash:str):
        '''
        Initializes a block.
        
        Args:
            id (int): the id of the block.
            transactions (list): the transactions in the block.
            previous_hash (str): the hash of the previous block.
        '''
        
        self.block = {
            'header':{
                'id': id,
                'timestamp': time.time(),
                'previous_hash': previous_hash,
                'hashTree': self.merkel_tree(transactions),
                'nonce': 0
            },
            'body':{
                'transactions': transactions
            }
        }
        self.hash = ''
        
    def merkel_tree(self, trans:list):
        if len(trans) == 0:
            return None

        if len(trans) == 1:
            return hashlib.sha256(bytes(str(trans[0]), 'utf-8')).hexdigest()
        
        else:
            left = self.merkel_tree(trans[:len(trans)//2])
            right = self.merkel_tree(trans[len(trans)//2:])
            return hashlib.sha256(bytes(left+right, 'utf-8')).hexdigest()
        
    def find_nonce(self):
        while hashlib.sha256(bytes(str(self.block), 'utf-8')).hexdigest()[0:4] != '0000':
            self.block['header']['nonce'] += 1
        self.hash = hashlib.sha256(bytes(str(self.block), 'utf-8')).hexdigest()
        return {'hash':self.hash, 'block':self.block}
    
            