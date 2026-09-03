import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "starter"))

def test_import():
    from transaction import TransactionManager
    print("TransactionManager imported successfully")

if __name__ == "__main__":
    test_import()
    print("All tests passed!")