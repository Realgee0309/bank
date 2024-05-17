import pickle
import os
import random
import pathlib

class Account:
    def __init__(self):
        self.accNo = 0
        self.name = ''
        self.password = ''
        self.deposit = 0
        self.type = ''

    def createAccount(self):
        self.accNo = random.randint(100000, 999999)
        self.name = input("\tEnter the account holder name: ")
        self.password = input("\tEnter the password for your account: ")
        self.type = input("\tEnter the type of account [C/S]: ")
        self.deposit = int(input("\tEnter the Initial amount (>=500 for Saving and >=1000 for current): "))
        print("\n\n\n\tAccount Created Successfully")
        print("\tYour Account Number is:", self.accNo)

    def showAccount(self):
        print("\tAccount Number : ", self.accNo)
        print("\tAccount Holder Name : ", self.name)
        print("\tType of Account : ", self.type)
        print("\tBalance : ", self.deposit)

    def modifyAccount(self):
        print("\tAccount Number : ", self.accNo)
        self.name = input("\tModify Account Holder Name : ")
        self.type = input("\tModify type of Account : ")
        self.deposit = int(input("\tModify Balance : "))

    def depositAmount(self, amount):
        self.deposit += amount

    def withdrawAmount(self, amount):
        if self.deposit >= amount:
            self.deposit -= amount
        else:
            print("\tInsufficient balance")

    def report(self):
        print(self.accNo, " ", self.name, " ", self.type, " ", self.deposit)

    def getAccountNo(self):
        return self.accNo

    def getAccountHolderName(self):
        return self.name

    def getAccountType(self):
        return self.type

    def getDeposit(self):
        return self.deposit

def intro():
    print("\n\n")
    print("\t========================")
    print("\t BANK SYSTEM")
    print("\t========================")

    input()

def login():
    while True:
        print("\n\tLOGIN MENU")
        print("\t1. Log in with existing account")
        print("\t2. Create a new account")
        print("\t3. Exit")
        choice = input("\tEnter your choice: ")

        if choice == '1':
            accNo = int(input("\tEnter your account number: "))
            password = input("\tEnter your password: ")

            # Authenticate user
            if validateLogin(accNo, password):
                print("\n\tLogin successful!")
                return accNo
            else:
                print("\n\tInvalid account number or password. Please try again.")

        elif choice == '2':
            writeAccount()  # Create a new account
            print("\n\tNew account created. Please log in again.")
            continue

        elif choice == '3':
            print("\tExiting...")
            exit()

        else:
            print("\tInvalid choice. Please enter a valid option.")

def validateLogin(accNo, password):
    # Connect to database and execute SQL query to validate login
    # Example: SELECT EXISTS(SELECT 1 FROM BankAccounts WHERE accNo = :accNo AND password = :password)
    return True  # Placeholder for demonstration

def writeAccount():
    account = Account()
    account.createAccount()
    # Convert account information to SQL parameters and execute SQL stored procedure to insert into database
    # Example: EXEC CreateAccount @p_accNo = account.accNo, @p_name = account.name, ...
    # Placeholder for demonstration

def displayAll():
    # Connect to database and execute SQL stored procedure to display all accounts
    # Example: EXEC DisplayAllAccounts
    # Placeholder for demonstration
    pass

def displaySp(num):
    # Connect to database and execute SQL stored procedure to display specific account
    # Example: EXEC DisplayAccount @p_accNo = num
    # Placeholder for demonstration
    pass

def depositAndWithdraw(num1, num2):
    # Connect to database and execute SQL stored procedure to deposit or withdraw from account
    # Example: EXEC DepositAmount @p_accNo = num1, @p_amount = amount
    # Placeholder for demonstration
    pass

def deleteAccount(num):
    # Connect to database and execute SQL stored procedure to delete account
    # Example: EXEC DeleteAccount @p_accNo = num
    # Placeholder for demonstration
    pass

def modifyAccount(num):
    # Connect to database and execute SQL stored procedure to modify account
    # Example: EXEC ModifyAccount @p_accNo = num, @p_name = name, ...
    # Placeholder for demonstration
    pass

ch = ''
num = 0
intro()

accNo = login()

while ch != '7':
    print("\n")
    print("\tMAIN MENU")
    print("\t1. DEPOSIT")
    print("\t2. WITHDRAW")
    print("\t3. BALANCE")
    print("\t4. DISPLAY ACCOUNT LIST")
    print("\t5. CLOSE ACCOUNT")
    print("\t6. MODIFY ACCOUNT")
    print("\t7. EXIT")
    print("\tSelect Your Option (1-7) ")
    ch = input("\tEnter your choice : ")

    if ch == '1':
        num = int(input("\tEnter The account No. : "))
        depositAndWithdraw(num, 1)
    elif ch == '2':
        num = int(input("\tEnter The account No. : "))
        depositAndWithdraw(num, 2)
    elif ch == '3':
        num = int(input("\tEnter The account No. : "))
        displaySp(num)
    elif ch == '4':
        displayAll()
    elif ch == '5':
        num = int(input("\tEnter The account No. : "))
        deleteAccount(num)
    elif ch == '6':
        num = int(input("\tEnter The account No. : "))
        modifyAccount(num)
    elif ch == '7':
        print("\tExiting...")
        exit()
    else:
        print("\tInvalid choice. Please enter a valid option.")
