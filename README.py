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
        print("\tType of Account", self.type)
        print("\tBalance : ", self.deposit)

    def modifyAccount(self):
        print("\tAccount Number : ", self.accNo)
        self.name = input("\tModify Account Holder Name :")
        self.type = input("\tModify type of Account :")
        self.deposit = int(input("\tModify Balance :"))

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
        accNo = int(input("\tEnter your account number: "))
        password = input("\tEnter your password: ")

        # Authenticate user
        if validateLogin(accNo, password):
            print("\n\tLogin successful!")
            return accNo
        else:
            print("\n\tInvalid account number or password. Please try again.")


def validateLogin(accNo, password):
    file = pathlib.Path("accounts.data")
    if file.exists():
        with open('accounts.data', 'rb') as infile:
            mylist = pickle.load(infile)
            for item in mylist:
                if item.accNo == accNo and item.password == password:
                    return True
    return False


def writeAccount():
    account = Account()
    account.createAccount()
    writeAccountsFile(account)


def displayAll():
    file = pathlib.Path("accounts.data")
    if file.exists():
        with open('accounts.data', 'rb') as infile:
            mylist = pickle.load(infile)
            for item in mylist:
                print("\t", item.accNo, " ", item.name, " ", item.type, " ", item.deposit)
    else:
        print("\tNo records to display")


def displaySp(num):
    file = pathlib.Path("accounts.data")
    if file.exists():
        with open('accounts.data', 'rb') as infile:
            mylist = pickle.load(infile)
            found = False
            for item in mylist:
                if item.accNo == num:
                    print("\tYour account Balance is = ", item.deposit)
                    found = True
    else:
        print("\tNo records to Search")
    if not found:
        print("\tNo existing record with this number")


def depositAndWithdraw(num1, num2):
    file = pathlib.Path("accounts.data")
    if file.exists():
        with open('accounts.data', 'rb') as infile:
            mylist = pickle.load(infile)
            for item in mylist:
                if item.accNo == num1:
                    if num2 == 1:
                        amount = int(input("\tEnter the amount to deposit : "))
                        item.deposit += amount
                        print("\tYour account is updated")
                    elif num2 == 2:
                        amount = int(input("\tEnter the amount to withdraw : "))
                        item.withdrawAmount(amount)
    else:
        print("\tNo records to Search")

    with open('accounts.data', 'wb') as outfile:
        pickle.dump(mylist, outfile)


def deleteAccount(num):
    file = pathlib.Path("accounts.data")
    if file.exists():
        with open('accounts.data', 'rb') as infile:
            oldlist = pickle.load(infile)
            newlist = [item for item in oldlist if item.accNo != num]

    with open('accounts.data', 'wb') as outfile:
        pickle.dump(newlist, outfile)


def modifyAccount(num):
    file = pathlib.Path("accounts.data")
    if file.exists():
        with open('accounts.data', 'rb') as infile:
            oldlist = pickle.load(infile)
            for item in oldlist:
                if item.accNo == num:
                    item.name = input("\tEnter the account holder name : ")
                    item.type = input("\tEnter the account Type : ")
                    item.deposit = int(input("\tEnter the Amount : "))

        with open('accounts.data', 'wb') as outfile:
            pickle.dump(oldlist, outfile)


def writeAccountsFile(account):
    file = pathlib.Path("accounts.data")
    if file.exists():
        with open('accounts.data', 'rb') as infile:
            oldlist = pickle.load(infile)
            oldlist.append(account)
    else:
        oldlist = [account]

    with open('accounts.data', 'wb') as outfile:
        pickle.dump(oldlist, outfile)


ch = ''
num = 0
intro()

accNo = login()

while ch != '8':
    print("\n")
    print("\tMAIN MENU")
    print("\t1. NEW ACCOUNT")
    print("\t2. DEPOSIT")
    print("\t3. WITHDRAW")
    print("\t4. BALANCE")
    print("\t5. DISPLAY ACCOUNT LIST")
    print("\t6. CLOSE ACCOUNT")
    print("\t7. MODIFY ACCOUNT")
    print("\t8. EXIT")
    print("\tSelect Your Option (1-8) ")
    ch = input("\tEnter your choice : ")

    if ch == '1':
        writeAccount()
    elif ch == '2':
        num = int(input("\tEnter The account No. : "))
        depositAndWithdraw(num, 1)
    elif ch == '3':
        num = int(input("\tEnter The account No. : "))
        depositAndWithdraw(num, 2)
    elif ch == '4':
        num = int(input("\tEnter The account No. : "))
        displaySp(num)
    elif ch == '5':
        displayAll()
    elif ch == '6':
        num = int(input("\tEnter The account No. : "))
        deleteAccount(num)
    elif ch == '7':
        num = int(input("\tEnter The account No. : "))
        modifyAccount
