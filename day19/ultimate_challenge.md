# Day 19 Boss: Log Stream Processor

## Project: BigDataLogProcessor

## Goal
Build a streaming log processor that handles GB-scale files with constant memory.

## Requirements
1. Read log files line by line (never load full file into memory)
2. Support filters: by date range, log level, keyword
3. Aggregate: count by level, count by hour, error rate
4. Group: group log lines by module/service
5. All operations must be lazy/iterator-based

## Log Format
```
2024-01-15 10:30:45 [INFO] module=auth User login successful
2024-01-15 10:31:02 [ERROR] module=payment Payment failed: timeout
```

## Input
- Log file path
- Filter criteria (optional)
- Group-by field (optional)

## Output
- Filtered log lines (iterator)
- Aggregation results (dict)
- Grouped results (dict of lists)

## Constraints
- Memory usage must be O(1) regardless of file size
- Must use iterator protocol (no loading full file)
- Must support chaining operations

## Acceptance Criteria
- Can process a 1GB+ log file without running out of memory
- Filter by date range works
- Filter by log level works
- Count by level aggregation works
- Group by module works
- Operations can be chained (filter then group then aggregate)

## Difficulty: 3.5/5