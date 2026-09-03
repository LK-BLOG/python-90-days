# Boss: ETL Data Pipeline

## Goal
Build a generator-based ETL pipeline for CSV/JSON data.

## Requirements
1. csv_reader(filepath) - lazy CSV reader generator
2. json_reader(filepath) - lazy JSON reader generator
3. filter_records(reader, condition) - filter generator
4. transform(reader, func) - transform generator
5. group_by(reader, field) - group aggregator
6. csv_writer(records, filepath) - write output
7. json_writer(records, filepath) - write output

## Difficulty: 4/5