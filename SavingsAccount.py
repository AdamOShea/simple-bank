class SavingsAccount(Account):
    def __init__(self, customer, uuid, balance, withdrawLimit) -> None:
        super().__init__(customer, uuid, balance)
        self.withdrawLimit = withdrawLimit