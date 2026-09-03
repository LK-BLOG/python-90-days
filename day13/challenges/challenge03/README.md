# Challenge 3: 描述符验证

## 目标
用描述符实现属性验证系统

## 功能要求
1. ValidatedField 描述符: min_value, max_value, required, type_check
2. __set_name__ 自动获取属性名
3. Product 类使用三个 ValidatedField

## 验收标准
- Product('iPhone', 999.99, 100) 正常创建
- Product('', 999.99, 100) 抛 ValueError (required)
- Product('iPhone', -1, 100) 抛 ValueError (min_value)
- Product(123, 999.99, 100) 抛 ValueError (type_check)
