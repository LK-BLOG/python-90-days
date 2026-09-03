class SimDB:
    def __init__(self):
        self.connected = False
        self.committed = 0
        self.rolled_back = 0

    def connect(self):
        self.connected = True
        return self

    def disconnect(self):
        self.connected = False

    def commit(self):
        self.committed += 1

    def rollback(self):
        self.rolled_back += 1

class DBContext:
    def __init__(self, db):
        self.db = db

    def __enter__(self):
        pass  # TODO: connect

    def __exit__(self, *args):
        pass  # TODO: commit or rollback + disconnect

# Test
if __name__ == "__main__":
    db = SimDB().connect()
    with DBContext(db):
        print("Working...")
    print(f"Connected: {db.connected}")
    print(f"Committed: {db.committed}")