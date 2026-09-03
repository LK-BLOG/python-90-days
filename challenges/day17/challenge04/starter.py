from dataclasses import dataclass

@dataclass
class Product:
    name: str
    price: float
    stock: int
    # TODO: __post_init__ 验证 price>0, stock>=0
