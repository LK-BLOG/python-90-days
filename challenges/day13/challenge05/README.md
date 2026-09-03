# Challenge 5: 组合 vs 继承

## 目标
用组合+继承设计灵活的数据库系统

## 功能要求
1. Logger mixin: log(msg) 方法
2. Serializable mixin: to_dict() 方法
3. Database 基类（组合包含 Logger）
4. MySQL 和 PostgreSQL 继承 Database
5. connect(), disconnect(), query(sql) 方法

## 验收标准
- MySQL().connect() 返回连接信息
- db.log('test') 输出带前缀的日志
- db.query('SELECT 1') 返回结果
- db.to_dict() 返回字典
