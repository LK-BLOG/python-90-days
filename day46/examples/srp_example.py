\"\"\"单一职责原则示例\"\"\"

from abc import ABC, abstractmethod


# ===== 违反SRP =====
class EmployeeBad:
    \"\"\"反模式：一个类干了所有事\"\"\"

    def __init__(self, name: str, salary: float):
        self.name = name
        self.salary = salary

    def calculate_pay(self) -> float:
        return self.salary * 0.8

    def save_to_db(self) -> None:
        print(f\"Saving {self.name} to database\")

    def generate_report(self) -> str:
        return f\"Report: {self.name}, Pay: {self.calculate_pay()}\"


# ===== 遵循SRP =====
class Employee:
    \"\"\"只管员工数据\"\"\"

    def __init__(self, name: str, salary: float, tax_rate: float = 0.2):
        self.name = name
        self.salary = salary
        self.tax_rate = tax_rate

    def gross_pay(self) -> float:
        return self.salary

    def net_pay(self) -> float:
        return self.salary * (1 - self.tax_rate)


class PayCalculator:
    \"\"\"只管算工资\"\"\"

    def __init__(self, tax_rate: float = 0.2):
        self.tax_rate = tax_rate

    def calculate(self, employee: Employee) -> float:
        return employee.net_pay()


class EmployeeRepository:
    \"\"\"只管持久化\"\"\"

    def __init__(self):
        self._store: list[Employee] = []

    def save(self, employee: Employee) -> None:
        self._store.append(employee)
        print(f\"Saved {employee.name}\")

    def find_all(self) -> list[Employee]:
        return list(self._store)


class ReportGenerator:
    \"\"\"只管生成报告\"\"\"

    def generate(self, employee: Employee, calculator: PayCalculator) -> str:
        pay = calculator.calculate(employee)
        return f\"Report: {employee.name}, Net Pay: {pay:.2f}\"


# 使用示例
if __name__ == \"__main__\":
    emp = Employee(\"Alice\", 10000)
    calc = PayCalculator()
    repo = EmployeeRepository()
    reporter = ReportGenerator()

    repo.save(emp)
    print(reporter.generate(emp, calc))
