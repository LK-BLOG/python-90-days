\"\"\"Day 54: WebSocket测试\"\"\"

import pytest


def test_connection_manager():
    from broadcast import ConnectionManager
    manager = ConnectionManager()
    assert len(manager.active_connections) == 0


def test_room():
    from room_manager import Room
    room = Room(\"test\")
    assert room.name == \"test\"
    assert len(room.connections) == 0


def test_chat_server():
    from chat_app import ChatServer, ChatMessage
    chat = ChatServer()
    assert chat.get_online_users() == []
    assert \"general\" in chat.rooms
