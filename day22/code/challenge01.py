class TransactionManager:
    def __init__(self, conn):
        self.conn = conn

    def __enter__(self):
        pass  # TODO

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass  # TODO

# Test
if __name__ == "__main__":
    conn = {"status": "connected", "tx": None}
    with TransactionManager(conn) as tx:
        conn["tx"] = "active"
        print("Transaction active")
    print(f"Connection status: {conn['tx']}")