# Exercise: Implement TransactionManager

class TransactionManager:
    def __init__(self, connection):
        pass  # TODO

    def __enter__(self):
        pass  # TODO: begin transaction

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass  # TODO: commit if no error, rollback if error

# Test
if __name__ == "__main__":
    conn = {"connected": True}
    with TransactionManager(conn) as tx:
        print("Doing work...")
        # If an exception occurs, transaction should rollback
    print("Transaction completed")