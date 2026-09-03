# Day 21 Boss: HTTP Request Decorator System

## Project: HTTPDecoratorStack

## Goal
Build a set of composable decorators for HTTP requests.

## Decorators to Implement
1. @rate_limit(calls_per_second=1) - throttle requests
2. @cache(ttl=300) - cache responses with TTL
3. @retry(max_attempts=3, delay=1) - retry on failure
4. @log(level="INFO") - log all requests
5. @authenticate(token=None) - add auth header

## Requirements
- All decorators use functools.wraps
- Decorators must be stackable in any order
- Each decorator is independent and testable
- Must work with simulated HTTP calls

## Acceptance Criteria
- @rate_limit prevents more than N calls per second
- @cache returns cached result within TTL
- @retry attempts up to N times before giving up
- @log prints request details
- @authenticate adds authorization header
- All decorators can be combined
- Stacking order is preserved

## Difficulty: 4/5