# Challenge 2: 方法类型大练习

## 目标
熟练使用实例方法、类方法、静态方法

## 功能要求
1. 实例方法 to_fahrenheit(): 摄氏转华氏
2. 类方法 from_fahrenheit(cls, f): 从华氏创建
3. 类方法 from_string(cls, s): 从 "36.5C" 或 "97.7F" 解析
4. 静态方法 is_freezing(c): 判断是否低于0度

## 验收标准
- Temperature(36.5).to_fahrenheit() == 97.7
- Temperature.from_fahrenheit(97.7).celsius == 36.5
- Temperature.from_string('0C').celsius == 0
- Temperature.is_freezing(-5) == True
