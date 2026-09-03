# -*- coding: utf-8 -*-
# TODO: 定义 InsufficientFundsError 异常
# 包含 balance 和 amount 属性

class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance
    
    def withdraw(self, amount):
        # TODO: 如果余额不足，抛出 InsufficientFundsError
        pass
