\"\"\"接口隔离原则示例\"\"\"

from abc import ABC, abstractmethod


# ===== 违反ISP =====
class WorkerBad(ABC):
    \"\"\"胖接口：不是所有工人都需要吃饭睡觉\"\"\"

    @abstractmethod
    def work(self) -> None: ...

    @abstractmethod
    def eat(self) -> None: ...

    @abstractmethod
    def sleep(self) -> None: ...


class RobotBad(WorkerBad):
    def work(self) -> None:
        print(\"Robot working\")

    def eat(self) -> None:
        raise NotImplementedError(\"Robots don't eat!\")

    def sleep(self) -> None:
        raise NotImplementedError(\"Robots don't sleep!\")


# ===== 遵循ISP =====
class Workable(ABC):
    @abstractmethod
    def work(self) -> None: ...


class Feedable(ABC):
    @abstractmethod
    def eat(self) -> None: ...


class Sleepable(ABC):
    @abstractmethod
    def sleep(self) -> None: ...


class HumanWorker(Workable, Feedable, Sleepable):
    \"\"\"人类工人：工作、吃饭、睡觉\"\"\"

    def work(self) -> None:
        print(\"Human working\")

    def eat(self) -> None:
        print(\"Human eating\")

    def sleep(self) -> None:
        print(\"Human sleeping\")


class Robot(Workable):
    \"\"\"机器人：只工作\"\"\"

    def work(self) -> None:
        print(\"Robot working\")


class HumanoidRobot(Workable, Feedable):
    \"\"\"仿生机器人：工作、充电（模拟吃饭）\"\"\"

    def work(self) -> None:
        print(\"HumanoidRobot working\")

    def eat(self) -> None:
        print(\"HumanoidRobot charging\")


def run_shift(workers: list[Workable]) -> None:
    \"\"\"只需要Workable接口\"\"\"
    for w in workers:
        w.work()


def feed_staff(workers: list[Feedable]) -> None:
    \"\"\"只需要Feedable接口\"\"\"
    for w in workers:
        w.eat()


if __name__ == \"__main__\":
    staff = [HumanWorker(), Robot(), HumanoidRobot()]

    print(\"--- Working ---\")
    run_shift(staff)

    print(\"\\n--- Feeding ---\")
    feed_staff([w for w in staff if isinstance(w, Feedable)])
