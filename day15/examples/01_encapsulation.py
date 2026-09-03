"""封装：公有/保护/私有"""
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner      # 公有
        self._bank = '招商银行'  # 保护
        self.__balance = balance  # 私有

    @property
    def balance(self):
        return self.__balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError('存款必须大于0')
        self.__balance += amount

    def withdraw(self, amount):
        if amount > self.__balance:
            raise ValueError('余额不足')
        self.__balance -= amount

acc = BankAccount('Alice', 10000)
acc.deposit(5000)
print(acc.balance)  # 15000
