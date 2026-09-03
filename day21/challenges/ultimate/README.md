# Boss: HTTP Request Decorator System

## Goal
Build composable HTTP decorators.

## Decorators
- @rate_limit(calls_per_second=1)
- @cache(ttl=300)
- @retry(max_attempts=3, delay=1)
- @log(level="INFO")
- @authenticate(token=None)

## Difficulty: 4/5