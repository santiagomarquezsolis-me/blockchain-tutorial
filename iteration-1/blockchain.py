import hashlib
import time

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.transactions}{self.timestamp}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block mined: {self.hash}")

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4
        self.pending_transactions = []

    def create_genesis_block(self):
        return Block(0, "Genesis Block", time.time(), "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def create_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self):
        if len(self.pending_transactions) == 0:
            print("No transactions to mine")
            return

        # Se extraen las transacciones pendientes de la pila
        transactions_to_mine = []
        while len(self.pending_transactions) > 0:
            transactions_to_mine.append(self.pending_transactions.pop())

        new_block = Block(len(self.chain), transactions_to_mine, time.time(), self.get_latest_block().hash)
        self.add_block(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def __repr__(self):
        return f"Transaction from {self.sender} to {self.receiver} for {self.amount} BTC"

class Node:
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def create_transaction(self, sender, receiver, amount):
        transaction = Transaction(sender, receiver, amount)
        self.blockchain.create_transaction(transaction)
        print(f"Transaction created: {transaction}")

# Creación de la blockchain y adición de bloques
def main():
    blockchain = Blockchain()
    node = Node(blockchain)

    node.create_transaction("Alice", "Bob", 50)
    node.create_transaction("Bob", "Charlie", 25)
    node.create_transaction("Charlie", "Dave", 10)

    print("Mining pending transactions...")
    blockchain.mine_pending_transactions()

    print("\nBlockchain valid?", blockchain.is_chain_valid())

    for block in blockchain.chain:
        print(f"\nIndex: {block.index}")
        print(f"Transactions: {block.transactions}")
        print(f"Timestamp: {block.timestamp}")
        print(f"Previous Hash: {block.previous_hash}")
        print(f"Hash: {block.hash}")
        print(f"Nonce: {block.nonce}")

if __name__ == "__main__":
    main()
