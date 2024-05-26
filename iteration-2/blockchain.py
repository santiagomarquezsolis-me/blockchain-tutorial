import hashlib
import time
import random
import string

# Clase que representa un monedero para los usuarios
class Wallet:
    def __init__(self, username):
        self.username = username
        self.address = self.generate_address()
        self.private_key = self.derive_private_key()
        self.balance = 0

    # Genera una dirección única para el monedero
    def generate_address(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

    # Deriva una clave privada basada en la dirección del monedero
    def derive_private_key(self):
        return hashlib.sha256(self.address.encode()).hexdigest()

    def __repr__(self):
        return f"Wallet(username={self.username}, address={self.address}, balance={self.balance})"

# Clase que representa un bloque en la blockchain
class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    # Calcula el hash del bloque basado en sus atributos
    def calculate_hash(self):
        block_string = f"{self.index}{self.transactions}{self.timestamp}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    # Realiza el proceso de minado ajustando el nonce hasta que el hash cumple con la dificultad
    def mine_block(self, difficulty):
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block mined: {self.hash}")

# Clase que representa la blockchain
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4
        self.pending_transactions = []
        self.wallets = {}

    # Crea el bloque génesis
    def create_genesis_block(self):
        return Block(0, "Genesis Block", time.time(), "0")

    # Obtiene el último bloque de la cadena
    def get_latest_block(self):
        return self.chain[-1]

    # Añade un nuevo bloque a la cadena
    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        # Actualiza los saldos de los usuarios
        self.update_balances(new_block.transactions)

    # Crea una nueva transacción y la añade a la lista de transacciones pendientes si es válida
    def create_transaction(self, transaction):
        if self.is_transaction_valid(transaction):
            self.pending_transactions.append(transaction)
            print(f"Transaction created: {transaction}")
        else:
            print("Invalid transaction: Insufficient funds")

    # Verifica si una transacción es válida (si el remitente tiene suficientes fondos)
    def is_transaction_valid(self, transaction):
        sender_wallet = self.wallets.get(transaction.sender)
        if sender_wallet:
            return sender_wallet.balance >= transaction.amount
        return False

    # Mina todas las transacciones pendientes creando un nuevo bloque
    def mine_pending_transactions(self):
        if len(self.pending_transactions) == 0:
            print("No transactions to mine")
            return

        # Crear un nuevo bloque con las transacciones pendientes
        new_block = Block(len(self.chain), self.pending_transactions, time.time(), self.get_latest_block().hash)
        new_block.mine_block(self.difficulty)

        # Añadir el nuevo bloque a la cadena
        self.chain.append(new_block)
        
        # Actualizar los saldos de los usuarios
        self.update_balances(self.pending_transactions)
        
        # Resetear la lista de transacciones pendientes
        self.pending_transactions = []

    # Actualiza los saldos de los monederos después de minar un bloque
    def update_balances(self, transactions):
        for transaction in transactions:
            if isinstance(transaction, Transaction):  # Verificar si es una instancia de Transaction
                sender_wallet = self.wallets.get(transaction.sender)
                receiver_wallet = self.wallets.get(transaction.receiver)
                if sender_wallet and receiver_wallet:
                    sender_wallet.balance -= transaction.amount
                    receiver_wallet.balance += transaction.amount

    # Verifica la validez de toda la cadena de bloques
    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

# Clase que representa una transacción en la blockchain
class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def __repr__(self):
        return f"Transaction from {self.sender} to {self.receiver} for {self.amount} BTC"

# Clase que representa un nodo en la red, responsable de gestionar las transacciones y los monederos
class Node:
    def __init__(self, blockchain):
        self.blockchain = blockchain

    # Crea una nueva transacción
    def create_transaction(self, sender, receiver, amount):
        transaction = Transaction(sender, receiver, amount)
        self.blockchain.create_transaction(transaction)

    # Añade un monedero a la blockchain
    def add_wallet(self, wallet):
        self.blockchain.wallets[wallet.address] = wallet
        print(f"Wallet added: {wallet}")

# Función principal que crea la blockchain, los monederos y las transacciones
def main():
    blockchain = Blockchain()
    node = Node(blockchain)

    # Crear monederos
    alice_wallet = Wallet("Alice")
    bob_wallet = Wallet("Bob")
    charlie_wallet = Wallet("Charlie")
    dave_wallet = Wallet("Dave")

    # Añadir monederos al nodo
    node.add_wallet(alice_wallet)
    node.add_wallet(bob_wallet)
    node.add_wallet(charlie_wallet)
    node.add_wallet(dave_wallet)

    # Asignar saldos iniciales
    alice_wallet.balance = 100
    bob_wallet.balance = 50
    charlie_wallet.balance = 30
    dave_wallet.balance = 20

    # Crear y validar transacciones
    node.create_transaction(alice_wallet.address, bob_wallet.address, 50)   # Transacción válida
    node.create_transaction(bob_wallet.address, charlie_wallet.address, 25) # Transacción válida
    node.create_transaction(charlie_wallet.address, dave_wallet.address, 10) # Transacción válida
    node.create_transaction(dave_wallet.address, alice_wallet.address, 15)  # Transacción válida
    node.create_transaction(charlie_wallet.address, alice_wallet.address, 50) # Transacción inválida (Charlie no tiene suficientes fondos)

    print("Mining pending transactions...")
    blockchain.mine_pending_transactions()

    # Verificar la validez de la cadena
    print("\nBlockchain valid?", blockchain.is_chain_valid())

    # Imprimir los detalles de cada bloque en la cadena
    for block in blockchain.chain:
        print(f"\nIndex: {block.index}")
        print(f"Transactions: {block.transactions}")
        print(f"Timestamp: {block.timestamp}")
        print(f"Previous Hash: {block.previous_hash}")
        print(f"Hash: {block.hash}")
        print(f"Nonce: {block.nonce}")

    # Imprimir los saldos de los monederos
    print("\nBalances:")
    for address, wallet in blockchain.wallets.items():
        print(f"{wallet.username} ({address}): {wallet.balance} BTC")

if __name__ == "__main__":
    main()
