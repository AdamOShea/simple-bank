import uuid
import os
import time
from tinydb import TinyDB, Query
import re
from dataclasses import dataclass


@dataclass
class Customer:
    '''
    Holds information about logged in user
    Main use is to hold uuid's for accounts so they can be accessed in database
    '''
        

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
    '''
    Base account class
    Connects customer with account and holds basic account info
    Deposit and withdraw methods add and subtract to balance but does not make changes to database
    '''
    def __init__(self, accountType, customer, uuid, balance):
        self.accountType = accountType
        self.customer = customer
        self.uuid = uuid
        self.balance = balance
    
    def __str__(self) -> str:
        return f"Account Holder: {self.customer}\nAccount ID: {self.uuid}\nCurrent Balance: {self.balance}"
    
    def deposit(self, amount):
        self.balance = (self.balance + float(amount))
        
    def withdraw(self, amount):
        self.balance = (self.balance - float(amount))
        
class SavingsAccount(Account):
    '''
    Account with withdraw limit included
    Withdraw limit states how many withdrawals per month this account can make
    '''
    def __init__(self, accountType, customer, uuid, balance, withdrawLimit):
        super().__init__(accountType, customer, uuid, balance)
        self.withdrawLimit = withdrawLimit
    
    def __str__(self):
        return f"Account Holder: {self.customer}\nAccount ID: {self.uuid}\n\nCurrent Balance: {self.balance}\nWithdrawl Limit: {self.withdrawLimit}"    
    
class CurrentAccount(Account):
    '''
    Account that includes credit limit
    Credit limit states how far below 0 an account's balance can go
    '''
    def __init__(self, accountType, customer, uuid, balance, creditLimit):
        super().__init__(accountType, customer, uuid, balance)
        self.creditLimit = creditLimit
    def __str__(self):
        super().__str__()
        return f"Account Holder: {self.customer}\nAccount ID: {self.uuid}\n\nCurrent Balance: {self.balance}\nCredit Limit: {self.creditLimit}"      

def fetchCustomer(email, pin):
    '''
    Function for retrieving a customer from the customer database
    Returns a customer object
    '''
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
    '''
    Function for retrieving a current account from the accounts database
    Returns a current account object
    '''
    account = Query()
    accountsDb = TinyDB('accounts.json')
    searchedAccount = accountsDb.get(account.uuid.matches(uuid))
    
    if searchedAccount != None:
        activeAccount = CurrentAccount(**searchedAccount)
        return activeAccount
    else:
        return None

def fetchSavingsAccount(uuid):
    '''
    Function for retrieving a current account from the accounts database
    Returns a savings account object
    '''
    account = Query()
    accountsDb = TinyDB('accounts.json')
    searchedAccount = accountsDb.get(account.uuid.matches(uuid))
    
    if searchedAccount != None:
        activeAccount = SavingsAccount(**searchedAccount)
        return activeAccount
    else:
        return None
    
def registerCustomer():
    '''
    Method for registering a customer
    Takes input from user for customer details
    Inserts new customer into customer database
    Prints info back to the user
    '''
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
    '''
    Method for logging in user
    Takes input for login details
    Searches database with input using fetchCustomer
    If customer not found, asks for input again
    If customer found, proceed to main menu with customer object passed as parameter
    '''
    os.system('cls')
    print("************ Login to SimpleBank ************\n\n")
    email = input("Enter Your Email: ")
    pin = input("Enter Your 4 Digit PIN: ")
    #email = "no.com"
    #pin = "1234"
    
    cust = fetchCustomer(email, pin)
    
    if cust == False:
        print("Your details were entered incorrectly, please try again...")
        time.sleep(2)
        loginCustomer()
    else:
        print("\nWelcome back " + str(cust.name) + ", logging you in...")
        #time.sleep(2)
        mainMenu(cust)
        
def addAccountToCustomer(accountType, cust):
    '''
    Method for creating and inserting an account to the accounts database 
    Also updates customer database to assign new account to the customer
    Checks which type of account customer wants to create
    Creates the account and prints details back to user
    '''
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
    '''
    Method for checking if user already has current account
    '''
    if not cust.currentAccount:
        return True
    else:
        return False
    
def checkSavingsAccountEligibility(cust):
    '''
    Method for checking if user already has savings account
    '''
    if not cust.savingsAccount:
        return True
    else:
        return False
    
def transactionMenu(selectedAccount, accountType, cust):
    '''
    Method for displaying menu for transactions that can be made on user's accounts
    User can deposit, withdraw, transfer between their accounts and transfer to other user's accounts
    User can only transfer between their accounts if they have more than 1 account
    User can only transfer to other users if they selected their current account
    '''
    if accountType == 1:
        account = fetchCurrentAccount(selectedAccount)
    elif accountType == 2:
        account = fetchSavingsAccount(selectedAccount)
    while True:
        os.system('cls')
        print("************ Transaction Menu ************\n")

        if accountType == 1:
            print("Current Account")
        else:
            print("Savings Account")
        print("Current Balance: " + str("%.2f" % account.balance))
        print("\nPlease select the type of transaction you want to make, or exit: ")
        print("\n[1] Deposit")
        print("[2] Withdrawal")
        if cust.currentAccount and cust.savingsAccount:
            print("[3] Transfer between your accounts")
        if accountType == 1:
            print("[4] Transfer to another person's account")
        print("\n[x] Exit")
        
        menuOption = input("Enter: ")
        
        if menuOption == '1':
            depositMenu(selectedAccount, accountType, cust)
            break
        elif menuOption == '2':
            withdrawMenu(selectedAccount, accountType)
            break
        elif menuOption == '3' and cust.currentAccount and cust.savingsAccount:
            #dont allow when only 1 account
            transferBetweenAccounts(selectedAccount, accountType, cust)
            break
        elif menuOption == '4' and accountType != 2:
            transferToOtherPerson(selectedAccount, accountType, cust)
            break
        elif menuOption.lower() == 'x':
            break 
        else:
            print("Invalid input, please try again...")
            time.sleep(2)

def depositMenu(selectedAccount, accountType, cust):
    '''
    Method for allowing user to deposit into their account
    Asks for amount from user then updates database
    '''
    if accountType == 1:
        account = fetchCurrentAccount(selectedAccount)
    elif accountType == 2:
        account = fetchSavingsAccount(selectedAccount)
    while True:
        os.system('cls')
        print("Make a Deposit")
        print("\nCurrent Balance: €" + str("%.2f" % account.balance))
        print("\nPlease enter the amount you would like to deposit, or press [x] to exit")
        
        amount = input("Enter: ")
        
        if amount.lower() == 'x':
            break
        elif amount.replace(".", "").isnumeric():
            
            accountsDb = TinyDB('accounts.json')
            acc = Query()
            accountsDb.update({'balance':(account.balance + float(amount))}, acc.uuid == account.uuid)
            account.deposit(amount)
            
            print("You have deposited €" + amount + " into your account")
            print("Your new balance is €" + str(("%.2f" % account.balance)))
            time.sleep(2)
            transactionMenu(selectedAccount, accountType, cust)
            break
        else:
            print("Invalid input, please try again")
            time.sleep(1)

def withdrawMenu(selectedAccount, accountType, cust):
    '''
    Method for allowing user to withdraw from their account
    Asks for amount for withdrawal from user, then checks if its a valid amount
    If valid, updates database
    '''
    if accountType == 1:
        account = fetchCurrentAccount(selectedAccount)
    elif accountType == 2:
        account = fetchSavingsAccount(selectedAccount)
    while True:
        os.system('cls')
        print("Make a Withdrawal")
        print("\nCurrent Balance: €" + str("%.2f" % account.balance))
        print("\nPlease enter the amount you would like to withdraw, or press [x] to exit")
        
        amount = input("Enter: ")
        
        if amount.lower() == 'x':
            break
        elif amount.replace(".", "").isnumeric():
            if accountType == 1:
                if float(amount) > float(account.balance + 500):
                    print("You do not have the required funds to make this withdrawal. This amount also exceeds your credit limit. Please enter a different amount")
                    time.sleep(2)
                else:
                    accountsDb = TinyDB('accounts.json')
                    acc = Query()
                    accountsDb.update({'balance':(account.balance - float(amount))}, acc.uuid == account.uuid)
                    account.withdraw(amount)
                    
                    print("You have withdrawn €" + amount + " from your account")
                    print("Your new balance is €" + str(("%.2f" % account.balance)))
                    time.sleep(2)
                    transactionMenu(selectedAccount, accountType, cust)
                    break
            if accountType == 2:
                if float(amount) > account.balance:
                    print("You do not have the required funds to make this withdrawal, please enter a different amount")
                    time.sleep(2)
                else:
                    accountsDb = TinyDB('accounts.json')
                    acc = Query()
                    accountsDb.update({'balance':(account.balance - float(amount))}, acc.uuid == account.uuid)
                    account.withdraw(amount)
                    
                    print("You have withdrawn €" + amount + " from your account")
                    print("Your new balance is €" + str(("%.2f" % account.balance)))
                    time.sleep(2)
                    transactionMenu(selectedAccount, accountType, cust)
                    break
        else:
            print("Invalid input, please try again")
            time.sleep(1)
            
def transferBetweenAccounts(selectedAccount, accountType, cust):
    '''
    Method for allowing user to transfer between their accounts
    Displays account balances and asks for amount to transfer from user
    If valid amount, updates both accounts in the database with new balances
    '''
    # display selected account balance and other account balance like in viewAccounts
    # ask for amount, make sure theres enough in account
    # use deposit and withdraw methods on accounts + update in DB
    # future: record transaction
    if accountType == 1:
        account = fetchCurrentAccount(selectedAccount)
        otherAccount = fetchSavingsAccount(cust.savingsAccount)
    elif accountType == 2:
        account = fetchSavingsAccount(selectedAccount)
        otherAccount = fetchCurrentAccount(cust.currentAccount)
        
    while True:
        os.system('cls')
        print("Transfer Between Your Accounts")
        if accountType == 1:
            print("\nCurrent Account Balance: €" + str("%.2f" % account.balance))
            print("\nSavings Account Balance: €" + str("%.2f" % otherAccount.balance))
        elif accountType == 2:
            print("\nSavings Account Balance: €" + str("%.2f" % account.balance))
            print("\nCurrent Account Balance: €" + str("%.2f" % otherAccount.balance))
        
        print("\nPlease enter the amount you would like to transfer, or press [x] to exit")
        
        amount = input("Enter: ")
        
        if amount.lower() == 'x':
            break
        elif amount.replace(".", "").isnumeric():
            if accountType == 1:
                if float(amount) > float(account.balance + 500):
                    print("You do not have the required funds to make this transfer. This amount also exceeds your credit limit. Please enter a different amount")
                    time.sleep(2)
                else:
                    accountsDb = TinyDB('accounts.json')
                    acc = Query()
                    accountsDb.update({'balance':(account.balance - float(amount))}, acc.uuid == account.uuid)
                    account.withdraw(amount)
                    
                    accountsDb.update({'balance':(otherAccount.balance + float(amount))}, acc.uuid == otherAccount.uuid)
                    otherAccount.deposit(amount)
                    
                    print("You have transferred €" + amount + " from your Current Account to your Savings Account")
                    print("Your new Current Account balance is €" + str("%.2f" % account.balance))
                    print("Your new Savings Account balance is €" + str("%.2f" % otherAccount.balance))
                    time.sleep(3)
                    transactionMenu(selectedAccount, accountType, cust)
                    break
            if accountType == 2:
                if float(amount) > account.balance:
                    print("You do not have the required funds to make this transfer, please enter a different amount")
                    time.sleep(2)
                else:
                    accountsDb = TinyDB('accounts.json')
                    acc = Query()
                    accountsDb.update({'balance':(account.balance - float(amount))}, acc.uuid == account.uuid)
                    account.withdraw(amount)
                    
                    accountsDb.update({'balance':(otherAccount.balance + float(amount))}, acc.uuid == otherAccount.uuid)
                    otherAccount.deposit(amount)
                    
                    print("You have transferred €" + amount + " from your Savings Account to your Current Account")
                    print("Your new Savings Account balance is €" + str("%.2f" % account.balance))
                    print("Your new Current Account balance is €" + str("%.2f" % otherAccount.balance))
                    time.sleep(3)
                    transactionMenu(selectedAccount, accountType, cust)
                    break
        else:
            print("Invalid input, please try again")
            time.sleep(1)

def transferToOtherPerson(selectedAccount, accountType, cust):
    
    '''
    Method for allowing user to transfer from their current account to another user's account
    Asks user for UUID of account to transfer to (similar to IBAN)
    Checks if the account exists in DB and is not one of the current users accounts
    Asks for amount from user and if valid, updates both accounts in DB
    '''
    
    account = fetchCurrentAccount(selectedAccount)
    
    while True:
        os.system('cls')
        print("Make a Transfer to Another Person's Account")
        print("\nPlease note that you can only transfer money to other Current Accounts")
        print("\nCurrent Balance: €" + str("%.2f" % account.balance))
        print("\nPlease enter the UUID of the account you would like to transfer to, or press [x] to exit")
        
        uuid = input("Enter: ")
        
        accountsDb = TinyDB('accounts.json')
        acc = Query()
        
        if uuid.lower() == 'x':
            break
        elif accountsDb.search(acc.uuid == uuid) and uuid != cust.currentAccount and uuid != cust.savingsAccount:
            otherAccount = fetchCurrentAccount(uuid)
            print("\nPlease enter the amount you would like to transfer, or press [x] to exit")
        
            amount = input("Enter: ")
            
            if amount.replace(".", "").isnumeric():
                if float(amount) > float(account.balance + 500):
                    print("You do not have the required funds to make this transfer. This amount also exceeds your credit limit. Please enter a different amount")
                    time.sleep(2)
                else:
                    accountsDb = TinyDB('accounts.json')
                    acc = Query()
                    accountsDb.update({'balance':(account.balance - float(amount))}, acc.uuid == account.uuid)
                    account.withdraw(amount)
                    
                    accountsDb.update({'balance':(otherAccount.balance + float(amount))}, acc.uuid == otherAccount.uuid)
                    otherAccount.deposit(amount)
                    
                    print("You have transferred €" + amount + " from your Current Account to the account with UUID: " + uuid)
                    print("Your new Current Account balance is €" + str("%.2f" % account.balance))
                    time.sleep(3)
                    transactionMenu(selectedAccount, accountType, cust)
                    break
            else:
                print("Invalid input, please try again")
                time.sleep(1)
        else:
            print("Invalid UUID entered, please try again")
            time.sleep(1)

def viewAccounts(cust):
    '''
    Method for displaying the current user's accounts
    If user has x account, it will fetch x account from the DB and display its details
    '''
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
            
        print("\n[x] Exit")
        
        menuOption = input("Enter: ")
        
        if cust.currentAccount and menuOption == '1':
            transactionMenu(cust.currentAccount, 1, cust)
            break
        elif not cust.currentAccount and menuOption == '1':
            print("You do not have a current account!")
            time.sleep(2)
        elif cust.savingsAccount and menuOption == '2':
            transactionMenu(cust.savingsAccount, 2, cust)
            break
        elif not cust.savingsAccount and menuOption == '2':
            print("You do not have a current account!")
            time.sleep(2)
        elif menuOption == 'x' or 'X':
            break
        else:
            print("Invalid input, please try again...")
            time.sleep(2)

def createAccount(cust):
    while True:
        '''
        Method that allows user to create an account
        Just asks user to select which type they want and creates entry in DB
        '''
        
        os.system('cls')
        print("************ Create a new Account ************\n")
        print("A Current Account can be used at any time and has a €500 credit limit")
        print("A Savings Account can only make transfers or withdrawals once per month\n")
        print("(Please note that you can only hold 1 of each type of account)\n")
        print("Please select the type of account you want to create, or exit\n[1] Current Account\n[2] Savings Account\n\n[x] Exit")
        
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
    
    '''
    Method that allows user to remove an account
    Asks user which one they want to remove and updates the DBs
    '''
    
    while True:
        os.system('cls')
        print("************ Delete an Account ************")
        print("Please select the account you would like to delete, or exit\n")
        
        if cust.currentAccount:
            print("[1] Current Account")
            
        if cust.savingsAccount:
            print("[2] Savings Account\n")
            
        print("\n[x] Exit")
        
        customerDb = TinyDB('customers.json')
        accountsDb = TinyDB('accounts.json')
        account = Query()
        menuOption = input("Enter: ")
        
        if cust.currentAccount and menuOption == '1':
            while True:
                print("\nAre you sure you want to delete your current account?")
                print("Enter Y to confirm or N to cancel")
                confirm = input("Enter: ")
                if confirm.lower() == 'y':
                    accountsDb.remove(account.uuid == cust.currentAccount)
                    customerDb.update({'currentAccount':None}, account.currentAccount == cust.currentAccount)
                    cust.currentAccount = None
                    print("Account deleted!")
                    time.sleep(2)
                    break
                elif confirm.lower() == 'n':
                    print("Deletion cancelled...")
                    time.sleep(2)
                    break
                else:
                    print("Invalid input, please try again")
                    time.sleep(1)
                
        elif not cust.currentAccount and menuOption == '1':
            print("You do not have a current account!")
            time.sleep(2)
                
        elif cust.savingsAccount and menuOption == '2':
            while True:
                print("\nAre you sure you want to delete your savings account?")
                print("Enter Y to confirm or N to cancel")
                confirm = input("Enter: ")
                print(confirm)
                time.sleep(2)
                if confirm.lower() == 'y':
                    accountsDb.remove(account.uuid == cust.savingsAccount)
                    customerDb.update({'savingsAccount':None}, account.savingsAccount == cust.savingsAccount)
                    cust.savingsAccount = None
                    print("Account deleted!")
                    time.sleep(2)
                    break
                elif confirm.lower() == 'n':
                    print("Deletion cancelled...")
                    time.sleep(2)
                    break
                else:
                    print("Invalid input, please try again")
                    time.sleep(1)
                
        elif not cust.savingsAccount and menuOption == '2':
            print("You do not have a savings account!")
            time.sleep(2)
                
        elif menuOption.lower() == 'x':
            break
        
        else:
            print("Invalid input, please try again")
            time.sleep(1)           

def mainMenu(cust):
    '''
    Main menu method
    '''
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
    '''
    Login menu that is seen when program starts
    '''
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

