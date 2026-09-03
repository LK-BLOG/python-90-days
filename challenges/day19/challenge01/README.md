# Challenge 01: Range Iterator

## Goal
Create a custom range-like iterator.

## Requirements
- Support start, stop, step parameters
- Must implement iterator protocol
- Should work like built-in range()

## Input
start, stop, step

## Output
Iterator yielding numbers

## Acceptance Criteria
- list(MyRange(5)) == [0, 1, 2, 3, 4]
- list(MyRange(1, 5)) == [1, 2, 3, 4]
- list(MyRange(0, 10, 2)) == [0, 2, 4, 6, 8]

## Difficulty: 1.5/5