from dataclasses import dataclass

@dataclass(frozen=True)
class Vector3D:
    x: float
    y: float
    z: float
    # TODO: 实现 __add__, __abs__, magnitude 属性
