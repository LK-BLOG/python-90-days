# Day 20 Boss: ETL Data Pipeline

## Project: GeneratorETLPipeline

## Goal
Build a complete ETL pipeline using generator chains.

## Stages
1. **Extract**: Read CSV/JSON files lazily (generator-based)
2. **Transform**: Clean data (strip, type convert, validate)
3. **Transform**: Add computed fields
4. **Aggregate**: Group by field, compute stats
5. **Load**: Output to CSV/JSON/console

## Requirements
- Each stage is a generator function
- Stages can be chained together
- Memory efficient (process one record at a time)
- Support multiple input formats
- Support multiple output formats

## Data Format
```csv
name,age,salary,department
Alice,30,50000,Engineering
Bob,25,45000,Marketing
Charlie,35,60000,Engineering
```

## Acceptance Criteria
- Can read CSV files lazily
- Can read JSON files lazily
- Can filter records by condition
- Can compute derived fields (e.g., salary * 1.1)
- Can group by field and aggregate
- Can output to CSV and JSON
- Pipeline is composable (pipe output of one to input of next)
- Memory usage is O(1) per record

## Difficulty: 4/5