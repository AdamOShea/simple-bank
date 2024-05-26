class Account:
    def __init__(self, customer, uuid, balance) -> None:
        self.customer = customer
        self.uuid = uuid
        self.balance = balance
    
    def __str__(self) -> str:
        return f"Account Holder: {self.customer.name}\nAccount ID: {self.uuid}\nCurrent Balance: {self.balance}"