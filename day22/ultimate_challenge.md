# Day 22 Boss: Resource Management Middleware

## Project: ResourceMiddleware

## Goal
Build a complete resource management system using context managers and decorators.

## Components
1. **ConnectionPool** - Manage database connections
   - acquire/release connections
   - context manager for automatic release
   - max connections limit

2. **LogContext** - Structured logging context
   - Add request_id, user_id to all logs
   - Context manager for scope management

3. **TimerMiddleware** - Measure execution time
   - Context manager for blocks
   - Decorator for functions

4. **RetryMiddleware** - Retry failed operations
   - Decorator with configurable attempts
   - Exponential backoff

5. **TransactionManager** - Database transactions
   - Auto-commit on success
   - Auto-rollback on exception
   - Nested savepoints

## Acceptance Criteria
- ConnectionPool limits max connections
- LogContext adds context to all log messages
- TimerMiddleware measures block/function time
- RetryMiddleware retries with backoff
- TransactionManager commits/rollbacks correctly
- All components can be composed together
- Clean resource cleanup on exceptions

## Difficulty: 4.5/5