class CurrentAccount(Account):
    def __init__(self, customer, uuid, balance, creditLimit):
        super().__init__(customer, uuid, balance, creditLimit)
        self.creditLimit = creditLimit