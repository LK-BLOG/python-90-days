from dataclasses import dataclass, field
from enum import Enum

class QuestStatus(Enum):
    NOT_STARTED = 'not_started'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'

@dataclass
class Quest:
    name: str
    description: str
    objectives: list = field(default_factory=list)
    rewards: dict = field(default_factory=dict)
    # TODO: start(), update_objective(), check_complete()
