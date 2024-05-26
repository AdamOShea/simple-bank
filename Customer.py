class Customer:
    def __init__(self, uuid, name, dob, email, pin, accounts) -> None:
        self.uuid = uuid
        self.name = name
        self.dob = dob
        self.email = email
        self.pin = pin
        self.accounts = accounts
        
    def __str__(self) -> str:
        return f"Customer: {self.name}\nCustomer ID: {self.uuid}\nDate of Birth: {self.dob}\nEmail: {self.email}"