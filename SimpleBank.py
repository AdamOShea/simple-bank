import uuid
import os
import time
from tinydb import TinyDB, Query
import re
from dataclasses import dataclass

@dataclass
class Customer:
    def __init__(self, uuid, name, dob, email, pin, accounts):
        self.uuid = uuid
        self.name = name
        self.dob = dob
        self.email = email
        self.pin = pin
        self.accounts = accounts
        
    def __str__(self) -> str:
        return f"Customer: {self.name}\nCustomer ID: {self.uuid}\nDate of Birth: {self.dob}\nEmail: {self.email}"

class Account:
    def __init__(self, customer, uuid, balance):
        self.customer = customer
        self.uuid = uuid
        self.balance = balance
    
    def __str__(self) -> str:
        return f"Account Holder: {self.customer.name}\nAccount ID: {self.uuid}\nCurrent Balance: {self.balance}"
    
class SavingsAccount(Account):
    def __init__(self, customer, uuid, balance, withdrawLimit):
        super().__init__(customer, uuid, balance)
        self.withdrawLimit = withdrawLimit
        
class CurrentAccount(Account):
    def __init__(self, customer, uuid, balance, creditLimit):
        super().__init__(customer, uuid, balance, creditLimit)
        self.creditLimit = creditLimit
            

def fetchCustomer(email, pin):
    cust = Query()
    customerDb = TinyDB('customers.json')
    
    searchedCust = customerDb.get(cust.email.matches(email, flags=re.IGNORECASE)  & (cust.pin.matches(pin)))
    
    activeCustomer = Customer(**searchedCust)
    
    return activeCustomer
    

def registerCustomer():
    os.system('cls')
    print("************ Register with SimpleBank ************\n\nPlease Enter Your Details\n\n")
    
    name = input("Enter Your Name: ")
    dob = input("Enter Your Date of Birth (DD/MM/YYYY): ")
    email = input("Enter Your Email: ")
    pin = input("Please Enter Your 4 Digit PIN (4 Numbers Only): ")
    accounts = []
    
    newCustomer = Customer(str(uuid.uuid1()), name, dob, email, pin, accounts)
    customerDb = TinyDB('customers.json')
    customerDb.insert({'uuid':newCustomer.uuid,'name':newCustomer.name,'dob':newCustomer.dob,'email':newCustomer.email,'pin':newCustomer.pin,'accounts':newCustomer.accounts})
    
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
        print("Incorrect details, please try again")
        time.sleep(3)
    else:
        print("Welcome back " + str(cust.name) + ", logging you in...")
        time.sleep(3)
        mainMenu(cust)

def mainMenu(cust):
    pass
    
def menu():
    
    while True:
        os.system('cls')
        print("************ Welcome To SimpleBank ************\n\n")
        print("Please select an option from the menu using the corresponding numbers:\n\n1. Login\n2. Register\n\nPress [x] to exit the program.\n")
        
        menuOption = input("Enter: ")
        if menuOption == "1":
            loginCustomer()
        elif menuOption == "2":
            registerCustomer()
        elif menuOption == "x" or "X":
            break

menu()