"""任务系统"""
from dataclasses import dataclass, field
from enum import Enum

class QuestStatus(Enum):
    NOT_STARTED = 'not_started'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'

@dataclass
class QuestObjective:
    description: str
    target: str
    required: int = 1
    current: int = 0

    def update(self, target, count=1):
        if target == self.target:
            self.current = min(self.required, self.current + count)
        return self.is_complete

    @property
    def is_complete(self):
        return self.current >= self.required

@dataclass
class Quest:
    name: str
    description: str
    objectives: list = field(default_factory=list)
    rewards: dict = field(default_factory=dict)
    status: QuestStatus = QuestStatus.NOT_STARTED

    def start(self):
        self.status = QuestStatus.IN_PROGRESS

    def check_complete(self):
        if all(obj.is_complete for obj in self.objectives):
            self.status = QuestStatus.COMPLETED
            return True
        return False
