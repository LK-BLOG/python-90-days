# Challenge 4: 单例 + slots

## 目标
结合单例模式和 __slots__

## 功能要求
1. __slots__ 限制属性
2. __new__ 实现单例
3. update(**kwargs) 更新配置
4. reset() 重置

## 验收标准
- Config() is Config() == True
- 属性只能是 db_host, db_port, db_name, debug
- update(db_host='new') 后属性更新
- reset() 后所有属性为 None
