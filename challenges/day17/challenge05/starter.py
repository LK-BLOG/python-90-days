from dataclasses import dataclass, asdict
import json

@dataclass
class Config:
    host: str
    port: int
    debug: bool = False
    # TODO: to_json(), from_json() 类方法
