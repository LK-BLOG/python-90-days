"""classmethod 工厂方法"""
class User:
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email

    @classmethod
    def from_dict(cls, data):
        return cls(data['name'], data['age'], data['email'])

    @classmethod
    def from_string(cls, s):
        name, age, email = s.split(',')
        return cls(name, int(age), email)

    @classmethod
    def anonymous(cls, age):
        return cls('Anonymous', age, '')

u1 = User.from_dict({'name': 'Alice', 'age': 25, 'email': 'a@b.com'})
u2 = User.from_string('Bob,30,b@b.com')
print(u1.name, u2.name)
