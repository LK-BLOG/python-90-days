# Boss: ETL Data Pipeline

def csv_reader(filepath):
    pass  # TODO: yield dicts from CSV

def json_reader(filepath):
    pass  # TODO: yield dicts from JSON (one per line)

def filter_records(reader, condition):
    pass  # TODO: yield records matching condition

def transform(reader, func):
    pass  # TODO: yield func(record) for each record

def group_by(reader, field):
    pass  # TODO: return dict of grouped records

def csv_writer(records, filepath):
    pass  # TODO: write records to CSV

# Test
if __name__ == "__main__":
    # Generate test data
    import csv
    with open("test.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["name", "age", "salary", "dept"])
        w.writerow(["Alice", "30", "50000", "Engineering"])
        w.writerow(["Bob", "25", "45000", "Marketing"])
        w.writerow(["Charlie", "35", "60000", "Engineering"])

    reader = csv_reader("test.csv")
    filtered = filter_records(reader, lambda r: int(r["age"]) > 28)
    grouped = group_by(filtered, "dept")
    print(grouped)