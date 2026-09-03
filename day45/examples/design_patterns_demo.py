# Day 45 设计模式示例

# === Observer 模式 ===
class EventEmitter:
    def __init__(self):
        self._listeners = {}
    
    def on(self, event, callback):
        self._listeners.setdefault(event, []).append(callback)
    
    def emit(self, event, *args, **kwargs):
        for cb in self._listeners.get(event, []):
            cb(*args, **kwargs)

emitter = EventEmitter()
emitter.on('order_created', lambda o: print(f'Email: order {o} confirmed'))
emitter.on('order_created', lambda o: print(f'Inventory: reserved for {o}'))
emitter.emit('order_created', 'ORD-001')

# === Strategy 模式 ===
from abc import ABC, abstractmethod

class Compressor(ABC):
    @abstractmethod
    def compress(self, data: bytes) -> bytes: ...

class ZipCompressor(Compressor):
    def compress(self, data):
        import zipfile, io
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, 'w') as zf:
            zf.writestr('data', data)
        return buf.getvalue()

class GzipCompressor(Compressor):
    def compress(self, data):
        import gzip
        return gzip.compress(data)

class FileProcessor:
    def __init__(self, compressor: Compressor):
        self._compressor = compressor
    def process(self, data):
        return self._compressor.compress(data)

# === Factory 模式 ===
class Logger:
    def __init__(self, name, level='INFO'):
        self.name = name
        self.level = level
    def log(self, msg):
        print(f'[{self.level}] {self.name}: {msg}')

class LoggerFactory:
    @staticmethod
    def create(log_type='console'):
        if log_type == 'console':
            return Logger('Console', 'INFO')
        elif log_type == 'file':
            return Logger('File', 'DEBUG')
        elif log_type == 'error':
            return Logger('Error', 'ERROR')
        raise ValueError(f'Unknown type: {log_type}')

# === Builder 模式 ===
class QueryBuilder:
    def __init__(self):
        self._table = ''
        self._wheres = []
        self._order = ''
        self._limit_val = None
    
    def table(self, name):
        self._table = name
        return self
    
    def where(self, cond):
        self._wheres.append(cond)
        return self
    
    def order_by(self, field, desc=False):
        self._order = f'ORDER BY {field} {\"DESC\" if desc else \"\"}'.strip()
        return self
    
    def limit(self, n):
        self._limit_val = n
        return self
    
    def build(self):
        q = f'SELECT * FROM {self._table}'
        if self._wheres:
            q += ' WHERE ' + ' AND '.join(self._wheres)
        if self._order:
            q += ' ' + self._order
        if self._limit_val:
            q += f' LIMIT {self._limit_val}'
        return q

if __name__ == '__main__':
    q = QueryBuilder().table('users').where('age > 18').order_by('name').limit(10).build()
    print(q)
