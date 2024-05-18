import random
import pickle
import pathlib
from pymongo import MongoClient

# Define the Account class to represent bank accounts
class Account:
    def __init__(self):
        self.accNo = 0
        self.name = ''
        self.password = ''
        self.deposit = 0
        self.type = ''

    # Method to create a new account
    def createAccount(self):
        self.accNo = random.randint(100000, 999999)
        self.name = input("\tEnter the account holder name: ")
        self.password = input("\tEnter the password for your account: ")
        self.type = input("\tEnter the type of account [C/S]: ")
        self.deposit = int(input("\tEnter the Initial amount (>=500 for Saving and >=1000 for current): "))
        print("\n\n\n\tAccount Created Successfully")
        print("\tYour Account Number is:", self.accNo)

    # Method to display account details
    def showAccount(self):
        print("\tAccount Number : ", self.accNo)
        print("\tAccount Holder Name : ", self.name)
        print("\tType of Account : ", self.type)
        print("\tBalance : ", self.deposit)

    # Method to modify account details
    def modifyAccount(self):
        print("\tAccount Number : ", self.accNo)
        self.name = input("\tModify Account Holder Name : ")
        self.type = input("\tModify type of Account : ")
        self.deposit = int(input("\tModify Balance : "))

    # Method to deposit money into the account
    def depositAmount(self, amount):
        self.deposit += amount

    # Method to withdraw money from the account
    def withdrawAmount(self, amount):
        if self.deposit >= amount:
            self.deposit -= amount
        else:
            print("\tInsufficient balance")

    # Method to print account details
    def report(self):
        print(self.accNo, " ", self.name, " ", self.type, " ", self.deposit)

    # Getter methods for account attributes
    def getAccountNo(self):
        return self.accNo

    def getAccountHolderName(self):
        return self.name

    def getAccountType(self):
        return self.type

    def getDeposit(self):
        return self.deposit

# Function to display introduction message
def intro():
    print("\n\n")
    print("\t========================")
    print("\t BANK SYSTEM")
    print("\t========================")

    input()

# Function for user login
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

# Function to validate login credentials
def validateLogin(accNo, password):
    result = collection.find_one({"accNo": accNo, "password": password})
    return result is not None

# Function to create a new account
def writeAccount():
    account = Account()
    account.createAccount()
    writeAccountsFile(account)

# Function to display details of all accounts
def displayAll():
    for account in collection.find():
        print("\tAccount Number : ", account["accNo"])
        print("\tAccount Holder Name : ", account["name"])
        print("\tType of Account : ", account["type"])
        print("\tBalance : ", account["deposit"])

# Function to display details of a specific account
def displaySp(num):
    account = collection.find_one({"accNo": num})
    if account:
        print("\tAccount Number : ", account["accNo"])
        print("\tAccount Holder Name : ", account["name"])
        print("\tType of Account : ", account["type"])
        print("\tBalance : ", account["deposit"])
    else:
        print("\tNo existing record with this number")

# Function to deposit or withdraw money from an account
def depositAndWithdraw(num1, num2):
    account = collection.find_one({"accNo": num1})
    if account:
        if num2 == 1:
            amount = int(input("\tEnter the amount to deposit : "))
            account["deposit"] += amount
            collection.update_one({"accNo": num1}, {"$set": {"deposit": account["deposit"]}})
            print("\tYour account is updated")
        elif num2 == 2:
            amount = int(input("\tEnter the amount to withdraw : "))
            if account["deposit"] >= amount:
                account["deposit"] -= amount
                collection.update_one({"accNo": num1}, {"$set": {"deposit": account["deposit"]}})
            else:
                print("\tInsufficient balance")
    else:
        print("\tNo records to Search")

# Function to delete an account
def deleteAccount(num):
    result = collection.delete_one({"accNo": num})
    if result.deleted_count == 1:
        print("\tAccount deleted successfully")
    else:
        print("\tNo existing record with this number")

# Function to modify details of an account
def modifyAccount(num):
    account = collection.find_one({"accNo": num})
    if account:
        print("\tAccount Number : ", account["accNo"])
        name = input("\tModify Account Holder Name : ")
        acc_type = input("\tModify type of Account : ")
        deposit = int
                print("\tModify Balance : ")
        new_values = {"$set": {"name": name, "type": acc_type, "deposit": deposit}}
        collection.update_one({"accNo": num}, new_values)
        print("\tAccount details modified successfully")
    else:
        print("\tNo existing record with this number")

# Function to write account details to MongoDB
def writeAccountsFile(account):
    account_data = {
        "accNo": account.accNo,
        "name": account.name,
        "password": account.password,
        "type": account.type,
        "deposit": account.deposit
    }
    collection.insert_one(account_data)

# MongoDB URI and client initialization
uri = "mongodb+srv://saltrickpajon:<password>@cluster0.gytjppx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client["bank_system"]
collection = db["accounts"]

# Main function
def main():
    intro()
    accNo = login()
    while True:
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

if __name__ == "__main__":
    main()
