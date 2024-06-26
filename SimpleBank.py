import uuid
import os
import time
from tinydb import TinyDB, Query
import re
from dataclasses import dataclass

@dataclass
class Customer:
    def __init__(self, uuid, name, dob, email, pin, currentAccount, savingsAccount):
        self.uuid = uuid
        self.name = name
        self.dob = dob
        self.email = email
        self.pin = pin
        self.currentAccount = currentAccount
        self.savingsAccount = savingsAccount
        
    def __str__(self) -> str:
        return f"Customer: {self.name}\nCustomer ID: {self.uuid}\nDate of Birth: {self.dob}\nEmail: {self.email}"

class Account:
    def __init__(self, accountType, customer, uuid, balance):
        self.accountType = accountType
        self.customer = customer
        self.uuid = uuid
        self.balance = balance
    
    def __str__(self) -> str:
        return f"Account Holder: {self.customer}\nAccount ID: {self.uuid}\nCurrent Balance: {self.balance}"
    
class SavingsAccount(Account):
    def __init__(self, accountType, customer, uuid, balance, withdrawLimit):
        super().__init__(accountType, customer, uuid, balance)
        self.withdrawLimit = withdrawLimit
    
    def __str__(self):
        return f"Account Holder: {self.customer}\nAccount ID: {self.uuid}\nCurrent Balance: {self.balance}\nWithdrawl Limit: {self.withdrawLimit}"
    
class CurrentAccount(Account):
    def __init__(self, accountType, customer, uuid, balance, creditLimit):
        super().__init__(accountType, customer, uuid, balance)
        self.creditLimit = creditLimit
    def __str__(self):
        super().__str__()
        return f"Account Holder: {self.customer}\nAccount ID: {self.uuid}\nCurrent Balance: {self.balance}\nCredit Limit: {self.creditLimit}"      

def fetchCustomer(email, pin):
    cust = Query()
    customerDb = TinyDB('customers.json')
    
    
    searchedCust = customerDb.get(cust.email.matches(email, flags=re.IGNORECASE)  & (cust.pin.matches(pin)))
    
    try:
        activeCustomer = Customer(**searchedCust)
    except:
        return False
    else:
        return activeCustomer
    
def fetchCurrentAccount(uuid):
    account = Query()
    accountsDb = TinyDB('accounts.json')
    searchedAccount = accountsDb.get(account.uuid.matches(uuid))
    activeAccount = CurrentAccount(**searchedAccount)
    return activeAccount

def fetchSavingsAccount(uuid):
    account = Query()
    accountsDb = TinyDB('accounts.json')
    searchedAccount = accountsDb.get(account.uuid.matches(uuid))
    activeAccount = SavingsAccount(**searchedAccount)
    return activeAccount
    
def registerCustomer():
    os.system('cls')
    print("************ Register with SimpleBank ************\n\nPlease Enter Your Details\n\n")
    
    name = input("Enter Your Name: ")
    dob = input("Enter Your Date of Birth (DD/MM/YYYY): ")
    email = input("Enter Your Email: ")
    pin = input("Please Enter Your 4 Digit PIN (4 Numbers Only): ")
    
    
    newCustomer = Customer(str(uuid.uuid1()), name, dob, email, pin, None, None)
    customerDb = TinyDB('customers.json')
    customerDb.insert({'uuid':newCustomer.uuid,'name':newCustomer.name,'dob':newCustomer.dob,'email':newCustomer.email,'pin':newCustomer.pin,'currentAccount':newCustomer.currentAccount,'savingsAccount':newCustomer.savingsAccount})
    
    print("Registering Customer....")
    time.sleep(2)
    os.system('cls')
    
    print("You are now registered!\n")
    print(newCustomer)
    time.sleep(3)
    
def loginCustomer():
    os.system('cls')
    print("************ Login to SimpleBank ************\n\n")
    email = input("Enter Your Email: ")
    pin = input("Enter Your 4 Digit PIN: ")
    
    cust = fetchCustomer(email, pin)
    
    if cust == False:
        print("Your details were entered incorrectly, please try again...")
        time.sleep(2)
        loginCustomer()
    else:
        print("\nWelcome back " + str(cust.name) + ", logging you in...")
        time.sleep(2)
        mainMenu(cust)
        
def addAccountToCustomer(accountType, cust):
    
    accountsDb = TinyDB('accounts.json')
    customerDb = TinyDB('customers.json')
    entry = Query()
    
    if accountType == 1:
        newAccount = CurrentAccount("Current", cust.uuid, str(uuid.uuid1()), 0, 500)
        accountsDb.insert({'accountType':"Current",'uuid':newAccount.uuid,'customer':newAccount.customer,'balance':newAccount.balance,'creditLimit':newAccount.creditLimit})
        customerDb.update({'currentAccount':newAccount.uuid}, entry.uuid == cust.uuid)
        cust.currentAccount = newAccount.uuid
        
        os.system('cls')
        print("New Current Account Created!\n")
        print(newAccount)
        time.sleep(3)
        
    elif accountType == 2:
        newAccount = SavingsAccount("Savings", cust.uuid, str(uuid.uuid1()), 0, 1)
        accountsDb.insert({'accountType':"Savings",'uuid':newAccount.uuid,'customer':newAccount.customer,'balance':newAccount.balance,'withdrawLimit':newAccount.withdrawLimit})
        customerDb.update({'savingsAccount':newAccount.uuid}, entry.uuid == cust.uuid)
        cust.savingsAccount = newAccount.uuid
        
        os.system('cls')
        print("New Savings Account Created!\n")
        print(newAccount)
        time.sleep(3)
               
def checkCurrentAccountEligibility(cust):
    if not cust.currentAccount:
        return True
    else:
        return False
    
def checkSavingsAccountEligibility(cust):
    if not cust.savingsAccount:
        return True
    else:
        return False
    
def transactionMenu(account):
    pass

def viewAccounts(cust):
    while True:
        os.system('cls')
        print("************ View Accounts ************\n")
        
        if not cust.currentAccount and not cust.savingsAccount:
            print("You don't have any accounts! Create one on the previous menu.")
            time.sleep(3)
            break
        
        if cust.currentAccount:
            currentAccount = fetchCurrentAccount(cust.currentAccount)
            
            print("Your current account:\n")
            print(currentAccount)
            print("\n")
            
        if cust.savingsAccount:
            savingsAccount = fetchSavingsAccount(cust.savingsAccount)
            
            print("Your savings account:\n")
            print(savingsAccount)
            
        print("\n\nPlease select an account to make a transaction on, or exit: ")
        
        if cust.currentAccount:
            print("[1] Current Account")
            
        if cust.savingsAccount:
            print("[2] Savings Account")
            
        print("[x] Exit\n")
        
        menuOption = input("Enter: ")
        
        if menuOption == 1:
            transactionMenu(cust.currentAccount)
        elif menuOption == 2:
            transactionMenu(cust.savingsAccount)
        elif menuOption == 'x' or 'X':
            break
        else:
            print("Invalid input, please try again...")
            time.sleep(2)

def createAccount(cust):
    while True:
        os.system('cls')
        print("************ Create a new Account ************\n")
        print("A Current Account can be used at any time and has a €500 credit limit")
        print("A Savings Account can only make transfers or withdrawals once per month\n")
        print("(Please note that you can only hold 1 of each type of account)\n")
        print("Please select the type of account you want to create\n[1] Current Account\n[2] Savings Account\n\n[x] Cancel")
        
        
        menuOption = input("Enter: ")
        
        if menuOption == '1':
            if checkCurrentAccountEligibility(cust):
                addAccountToCustomer(1, cust)
            else:
                print("You already have a current account!")
                time.sleep(2)
        elif menuOption == '2':
            if checkSavingsAccountEligibility(cust):
                addAccountToCustomer(2, cust)
            else:
                print("You already have a savings account!")
                time.sleep(2)
        elif menuOption == 'x' or 'X':
            break
        
def deleteAccount(cust):
    while True:
        os.system('cls')
        print("************ Delete an Account ************")
        print("Please select the account you would like to delete, or exit\n")
        
        if cust.currentAccount:
            print("[1] Current Account")
            
        if cust.savingsAccount:
            print("[2] Savings Account\n")
            
        print("[x] Exit\n")
        
        customerDb = TinyDB('customer.json')
        accountsDb = TinyDB('accounts.json')
        account = Query()
        menuOption = input("Enter: ")
        
        if cust.currentAccount and menuOption == 1:
            while True:
                print("Are you sure you want to delete your current account?")
                print("Enter Y to confirm or X to cancel")
                confirm = input("Enter: ")
                if confirm == 'y' or 'Y':
                    accountsDb.remove(account.uuid == cust.currentAccount)
                    customerDb.update({'currentAccount':None}, account.currentAccount == cust.currentAccount)
                    cust.currentAccount = None
                    print("Account deleted!")
                    time.sleep(2)
                elif confirm == 'x' or 'X':
                    print("Deletion cancelled...")
                    time.sleep(2)
                
        elif cust.savingsAccount and menuOption == 2:
            while True:
                print("Are you sure you want to delete your savings account?")
                print("Enter Y to confirm or X to cancel")
                confirm = input("Enter: ")
                if confirm == 'y' or 'Y':
                    accountsDb.remove(account.uuid == cust.savingsAccount)
                    customerDb.update({'savingsAccount':None}, account.savingsAccount == cust.savingsAccount)
                    cust.savingsAccount = None
                    print("Account deleted!")
                    time.sleep(2)
                elif confirm == 'x' or 'X':
                    print("Deletion cancelled...")
                    time.sleep(2)
                
        elif menuOption == 'x' or 'X':
            break
            

def mainMenu(cust):
    while True:
        os.system('cls')
        print("************ Main Menu ************\n\n")
        print("Please select an option from the menu using the corresponding numbers:\n\n[1] View Accounts\n[2] Create a New Account\n[3] Delete an Account\n\nEnter [x] to log out.\n")
        menuOption = input("Enter: ")
        if menuOption == '1':
            viewAccounts(cust)
        elif menuOption == '2':
            createAccount(cust)
        elif menuOption == '3':
            deleteAccount(cust)
        elif menuOption == 'x' or 'X':
            os.system('cls')
            print("Logging Out...")
            cust = None
            time.sleep(2)
            break

def menu():
    
    while True:
        os.system('cls')
        print("************ Welcome To SimpleBank ************\n\n")
        print("Please select an option from the menu using the corresponding numbers:\n\n[1] Login\n[2] Register\n\nPress [x] to exit the program.\n")
        
        menuOption = input("Enter: ")
        if menuOption == "1":
            loginCustomer()
        elif menuOption == "2":
            registerCustomer()
        elif menuOption == "x" or "X":
            break

menu()