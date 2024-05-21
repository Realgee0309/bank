import hashlib
import sqlite3
import datetime
import random

class Account:
    def __init__(self, accNo, name, password, acc_type, deposit):
        self.accNo = accNo
        self.name = name
        self.password = password
        self.acc_type = acc_type
        self.deposit = deposit

    def createAccount(self):
        conn = sqlite3.connect('bank.db')
        cursor = conn.cursor()

        # Insert new account details into the database
        cursor.execute("INSERT INTO accounts VALUES (?, ?, ?, ?, ?)",
                       (self.accNo, self.name, self.password, self.acc_type, self.deposit))

        conn.commit()
        conn.close()

    def authenticate(self, password):
        # Compare hashed password with stored password hash
        return self.password == hashlib.sha256(password.encode()).hexdigest()

    def depositAmount(self, amount):
        conn = sqlite3.connect('bank.db')
        cursor = conn.cursor()

        # Update account balance in the database
        self.deposit += amount
        cursor.execute("UPDATE accounts SET deposit = ? WHERE accNo = ?", (self.deposit, self.accNo))

        # Log the deposit transaction
        self.logTransaction(amount, "Deposit")

        conn.commit()
        conn.close()

    def withdrawAmount(self, amount):
        conn = sqlite3.connect('bank.db')
        cursor = conn.cursor()

        # Check if account has sufficient balance
        if self.deposit >= amount:
            # Update account balance in the database
            self.deposit -= amount
            cursor.execute("UPDATE accounts SET deposit = ? WHERE accNo = ?", (self.deposit, self.accNo))

            # Log the withdrawal transaction
            self.logTransaction(amount, "Withdrawal")

            conn.commit()
        else:
            print("\tInsufficient balance")

        conn.close()

    def transferAmount(self, recipient_accNo, amount):
        conn = sqlite3.connect('bank.db')
        cursor = conn.cursor()

        # Check if account has sufficient balance for transfer
        if self.deposit >= amount:
            # Update sender's account balance
            self.deposit -= amount
            cursor.execute("UPDATE accounts SET deposit = ? WHERE accNo = ?", (self.deposit, self.accNo))

            # Update recipient's account balance
            cursor.execute("SELECT deposit FROM accounts WHERE accNo = ?", (recipient_accNo,))
            recipient_balance = cursor.fetchone()[0]
            recipient_balance += amount
            cursor.execute("UPDATE accounts SET deposit = ? WHERE accNo = ?", (recipient_balance, recipient_accNo))

            # Log the transfer transactions
            self.logTransaction(amount, f"Transfer to {recipient_accNo}")
            self.logTransaction(amount, f"Transfer from {self.accNo}")

            conn.commit()
        else:
            print("\tInsufficient balance for transfer")

        conn.close()

    def logTransaction(self, amount, transaction_type):
        conn = sqlite3.connect('bank.db')
        cursor = conn.cursor()

        # Log transaction details into the transactions table
        cursor.execute("INSERT INTO transactions VALUES (?, ?, ?, ?)",
                       (self.accNo, amount, transaction_type, datetime.datetime.now()))

        conn.commit()
        conn.close()

    def getBalance(self):
        return self.deposit

    def getTransactionHistory(self):
        conn = sqlite3.connect('bank.db')
        cursor = conn.cursor()

        # Retrieve transaction history from the transactions table
        cursor.execute("SELECT * FROM transactions WHERE accNo = ?", (self.accNo,))
        transactions = cursor.fetchall()

        conn.close()
        return transactions

    def closeAccount(self):
        conn = sqlite3.connect('bank.db')
        cursor = conn.cursor()

        # Delete account from the accounts table
        cursor.execute("DELETE FROM accounts WHERE accNo = ?", (self.accNo,))

        # Delete associated transactions from the transactions table
        cursor.execute("DELETE FROM transactions WHERE accNo = ?", (self.accNo,))

        conn.commit()
        conn.close()

class Bank:
    def __init__(self):
        self.accounts = {}

    def createAccount(self):
        accNo = random.randint(100000, 999999)
        name = input("\tEnter the account holder name: ")
        password = input("\tEnter the password for the account: ")
        acc_type = input("\tEnter the type of account [C/S]: ")
        deposit = int(input("\tEnter the initial deposit amount: "))

        # Create an Account object and add it to the accounts dictionary
        account = Account(accNo, name, hashlib.sha256(password.encode()).hexdigest(), acc_type, deposit)
        self.accounts[accNo] = account

        # Call createAccount method to store account details in the database
        account.createAccount()

    def login(self, accNo, password):
        if accNo in self.accounts:
            account = self.accounts[accNo]
            if account.authenticate(password):
                print("\n\tLogin successful!")
                return account
            else:
                print("\n\tInvalid account number or password. Please try again.")
                return None
        else:
            print("\n\tAccount does not exist. Please try again.")
            return None

    def deposit(self, account, amount):
        account.depositAmount(amount)

    def withdraw(self, account, amount):
        account.withdrawAmount(amount)

    def transfer(self, sender_accNo, recipient_accNo, amount):
        sender_account = self.accounts.get(sender_accNo)
        if sender_account:
            sender_account.transferAmount(recipient_accNo, amount)
        else:
            print("\tSender account does not exist")

    def getBalance(self, account):
        return account.getBalance()

    def getTransactionHistory(self, account):
        return account.getTransactionHistory()

    def closeAccount(self, account):
        account.closeAccount()
        del self.accounts[account.accNo]

# Database initialization
def initialize_database():
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()

    # Create tables if they don't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS accounts
                      (accNo INTEGER PRIMARY KEY, name TEXT, password TEXT, acc_type TEXT, deposit REAL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions
                      (accNo INTEGER, amount REAL, transaction_type TEXT, date TEXT)''')

    conn.commit()
    conn.close()

def main():
    initialize_database()
    bank = Bank()

    while True:
        print("\n\tMAIN MENU")
        print("\t1. Log in")
        print("\t2. Create a new account")
        print("\t3. Exit")
        choice = input("\tEnter your choice: ")

        if choice == '1':
            accNo = input("\tEnter
