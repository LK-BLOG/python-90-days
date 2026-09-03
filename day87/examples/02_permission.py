# Day 87 示例 2: 权限控制
from enum import Enum

class Permission(Enum):
    READ = 'read'; WRITE = 'write'; EXECUTE = 'execute'; NETWORK = 'network'

class PermissionManager:
    def __init__(self, agent_id):
        self.agent_id = agent_id; self.perms = set()
    def grant(self, p): self.perms.add(p)
    def check(self, p): return p in self.perms
    def list_perms(self): return [p.value for p in self.perms]

class SandboxedExecutor:
    def __init__(self, pm): self.pm = pm
    def execute(self, action, data=''):
        if action == 'read' and not self.pm.check(Permission.READ): return '无读权限'
        if action == 'write' and not self.pm.check(Permission.WRITE): return '无写权限'
        return f'执行: {action} {data}'

if __name__ == '__main__':
    pm = PermissionManager('agent1')
    pm.grant(Permission.READ)
    ex = SandboxedExecutor(pm)
    print(ex.execute('read', '/tmp/file'))
    print(ex.execute('write', '/tmp/file'))
