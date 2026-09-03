#!/usr/bin/env python3
"""Tests for Agent Loop Implementation"""

import asyncio
import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from examples.agent_loop import AgentLoop, AgentState, Message, MockLLM, MockToolExecutor, MockMemory, MockStateManager


@pytest.fixture
def components():
    """Create test components"""
    return {
        "llm": MockLLM(),
        "tools": MockToolExecutor(),
        "memory": MockMemory(),
        "state": MockStateManager()
    }


@pytest.fixture
def agent(components):
    """Create agent instance"""
    return AgentLoop(**components)


def test_agent_state_enum():
    """Test AgentState enum"""
    assert AgentState.IDLE.value == "idle"
    assert AgentState.THINKING.value == "thinking"
    assert AgentState.FINISHED.value == "finished"


def test_message_creation():
    """Test Message dataclass"""
    msg = Message(role="user", content="hello")
    assert msg.role == "user"
    assert msg.content == "hello"
    assert msg.metadata is None
    
    msg_with_meta = Message(role="assistant", content="hi", metadata={"tool": "test"})
    assert msg_with_meta.metadata["tool"] == "test"


def test_agent_initialization(agent):
    """Test agent initialization"""
    assert agent.max_iterations == 10
    assert agent.current_state == AgentState.IDLE


@pytest.mark.asyncio
async def test_agent_run(agent, components):
    """Test agent run"""
    result = await agent.run("hello world")
    assert result is not None
    assert agent.current_state == AgentState.FINISHED
    assert len(components["memory"].messages) > 0


@pytest.mark.asyncio
async def test_agent_state_transitions(agent):
    """Test state transitions during run"""
    initial_state = agent.current_state
    assert initial_state == AgentState.IDLE
    
    await agent.run("test")
    assert agent.current_state == AgentState.FINISHED


@pytest.mark.asyncio
async def test_message_history(components):
    """Test message history tracking"""
    agent = AgentLoop(**components)
    await agent.run("first message")
    await agent.run("second message")
    
    messages = components["memory"].messages
    assert len(messages) >= 4  # 2 user + 2 assistant


def test_mock_llm():
    """Test MockLLM"""
    llm = MockLLM()
    assert llm.call_count == 0
    
    asyncio.run(llm.chat([]))
    assert llm.call_count == 1


def test_mock_memory():
    """Test MockMemory"""
    memory = MockMemory()
    assert len(memory.messages) == 0
    
    memory.add_message(Message(role="user", content="test"))
    assert len(memory.messages) == 1
    
    messages = memory.get_messages()
    assert messages[0].content == "test"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
