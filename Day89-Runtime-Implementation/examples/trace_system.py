#!/usr/bin/env python3
"""Trace System Example"""

import uuid
import time
from contextlib import contextmanager
from typing import Dict, List, Any, Optional, Generator
from dataclasses import dataclass, field


@dataclass
class TraceSpan:
    """Trace span data structure"""
    trace_id: str
    span_id: str
    parent_span_id: Optional[str]
    name: str
    start_time: float
    end_time: Optional[float] = None
    attributes: Dict[str, Any] = field(default_factory=dict)
    status: str = "OK"
    
    @property
    def duration_ms(self) -> float:
        if self.end_time is None:
            return 0
        return (self.end_time - self.start_time) * 1000


class Tracer:
    """Execution tracer"""
    def __init__(self):
        self.spans: List[TraceSpan] = []
        self.current_trace_id: Optional[str] = None
    
    def start_trace(self, name: str) -> str:
        trace_id = str(uuid.uuid4())
        self.current_trace_id = trace_id
        span = TraceSpan(
            trace_id=trace_id,
            span_id=str(uuid.uuid4()),
            parent_span_id=None,
            name=name,
            start_time=time.time()
        )
        self.spans.append(span)
        return trace_id
    
    @contextmanager
    def span(self, name: str, parent_id: str = None) -> Generator[TraceSpan, None, None]:
        span = TraceSpan(
            trace_id=self.current_trace_id or str(uuid.uuid4()),
            span_id=str(uuid.uuid4()),
            parent_span_id=parent_id,
            name=name,
            start_time=time.time()
        )
        self.spans.append(span)
        try:
            yield span
            span.status = "OK"
        except Exception as e:
            span.status = f"ERROR: {str(e)}"
            span.attributes["error"] = str(e)
            raise
        finally:
            span.end_time = time.time()
    
    def get_trace(self, trace_id: str) -> List[TraceSpan]:
        return [s for s in self.spans if s.trace_id == trace_id]
    
    def export(self, trace_id: str) -> Dict:
        spans = self.get_trace(trace_id)
        return {
            "trace_id": trace_id,
            "spans": [{
                "span_id": s.span_id,
                "parent_span_id": s.parent_span_id,
                "name": s.name,
                "duration_ms": round(s.duration_ms, 2),
                "status": s.status,
                "attributes": s.attributes
            } for s in spans]
        }
    
    def print_trace(self, trace_id: str):
        """Pretty print trace"""
        trace = self.export(trace_id)
        print(f"\nTrace: {trace[\"trace_id\"]}")
        print("-" * 60)
        for span in trace["spans"]:
            indent = "  " if span["parent_span_id"] else ""
            status_icon = "[OK]" if span["status"] == "OK" else "[ERR]"
            print(f"{indent}{status_icon} {span[\"name\"]}: {span[\"duration_ms\"]}ms")
        print("-" * 60)


async def main():
    print("=== Trace System Example ===")
    
    tracer = Tracer()
    
    # Start trace
    trace_id = tracer.start_trace("user_request")
    
    # Simulate processing
    with tracer.span("parse_input") as span:
        span.attributes["input_type"] = "text"
        time.sleep(0.05)
    
    with tracer.span("llm_call", parent_id=span.span_id) as llm_span:
        llm_span.attributes["model"] = "gpt-4"
        llm_span.attributes["tokens"] = 150
        time.sleep(0.1)
    
    with tracer.span("tool_execution", parent_id=span.span_id) as tool_span:
        tool_span.attributes["tool_name"] = "calculator"
        time.sleep(0.03)
    
    # Print trace
    tracer.print_trace(trace_id)
    
    # Export trace
    print("\nExported trace data:")
    import json
    print(json.dumps(tracer.export(trace_id), indent=2))


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
