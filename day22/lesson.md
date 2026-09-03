# Day 22: Context Managers

## 1. with Statement Protocol
Any class with `__enter__()` and `__exit__()` is a context manager.

```python
class FileManager:
    def __init__(self, filepath, mode):
        self.filepath = filepath
        self.mode = mode

    def __enter__(self):
        self.file = open(self.filepath, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
        if exc_type is not None:
            print(f"Error occurred: {exc_val}")
        return False  # Don't suppress exceptions

with FileManager("test.txt", "w") as f:
    f.write("Hello World")
```

### __exit__ Parameters
- exc_type: Exception class (None if no exception)
- exc_val: Exception instance
- exc_tb: Traceback object
- Return True to suppress exception, False to propagate

## 2. contextlib.contextmanager
Use a generator to create context managers easily.

```python
from contextlib import contextmanager

@contextmanager
def managed_resource(name):
    print(f"Acquiring {name}")
    resource = {"name": name, "active": True}
    try:
        yield resource
    except Exception as e:
        print(f"Error: {e}")
        resource["active"] = False
    finally:
        print(f"Releasing {name}")

with managed_resource("database") as res:
    print(f"Using {res['name']}")
```

## 3. Nested Context Managers
```python
# Multiple managers
with open("in.txt") as fin, open("out.txt", "w") as fout:
    fout.write(fin.read())

# Or using ExitStack
from contextlib import ExitStack

with ExitStack() as stack:
    files = [stack.enter_context(open(f)) for f in ["a.txt", "b.txt"]]
```

## 4. Exception Suppression
```python
from contextlib import suppress

# Suppress specific exceptions
with suppress(FileNotFoundError):
    os.remove("nonexistent.txt")  # No error

# vs try/except
try:
    os.remove("nonexistent.txt")
except FileNotFoundError:
    pass
```

## 5. ExitStack
Dynamically manage any number of context managers.

```python
from contextlib import ExitStack

class ResourcePool:
    def __init__(self):
        self.resources = []

    def acquire(self, name):
        self.resources.append(name)
        return name

    def __enter__(self):
        return self

    def __exit__(self, *args):
        for r in self.resources:
            print(f"Releasing {r}")

with ResourcePool() as pool:
    pool.acquire("db1")
    pool.acquire("db2")
```

## 6. Database Connection Context
```python
class DatabaseConnection:
    def __init__(self, db_url):
        self.db_url = db_url
        self.conn = None

    def __enter__(self):
        self.conn = self._connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.conn.close()
        return False

    def _connect(self):
        print(f"Connecting to {self.db_url}")
        return {"connected": True}

    def execute(self, sql):
        print(f"Executing: {sql}")
```

## 7. Combining with Decorators
```python
import functools, time
from contextlib import contextmanager

def timer_context(label="block"):
    @contextmanager
    def _timer():
        start = time.time()
        yield
        elapsed = time.time() - start
        print(f"{label}: {elapsed:.4f}s")
    return _timer()

def retry_decorator(max_attempts=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if i == max_attempts - 1:
                        raise
                    time.sleep(0.1)
        return wrapper
    return decorator

with timer_context("my task"):
    time.sleep(0.1)
```

## Exercises
1. Implement TransactionManager (commit on success, rollback on error)
2. Implement TimerContext using contextmanager decorator
3. Implement ResourcePool with ExitStack