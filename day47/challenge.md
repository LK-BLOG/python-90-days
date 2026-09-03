# Day 47 挑战任务

## Challenge 1: 手动DI容器
**目标：** 实现一个简易DI容器

**要求：**
1. 实现Container类，支持bind/resolve/singleton
2. 支持Factory注册（每次resolve创建新实例）
3. 支持Singleton注册（全局唯一实例）
4. 写测试验证行为

**验收：** Container能正确管理对象生命周期
**难度：** ⭐⭐

---

## Challenge 2: 使用dependency-injector
**目标：** 用框架实现DI

**要求：**
1. 安装dependency-injector
2. 定义Container（含Database/Cache/Service providers）
3. 使用Configuration读取配置
4. 使用@inject装饰器注入
5. 写测试验证

**验收：** 通过Container能正确获取所有服务实例
**难度：** ⭐⭐⭐

---

## Challenge 3: 工厂模式 + 配置驱动
**目标：** 实现配置驱动的服务工厂

**要求：**
1. 实现ServiceRegistry注册表
2. 支持装饰器注册服务
3. 配置文件决定使用哪个实现
4. 支持运行时替换

**验收：** 修改配置文件即可切换服务实现
**难度：** ⭐⭐

---

## Challenge 4: 综合DI练习
**目标：** 为一个简单的Web应用配置DI

**要求：**
1. 定义UserRepository, UserService, UserController
2. 用DI容器管理所有服务
3. 支持不同环境（dev/prod/test）使用不同实现
4. 写测试验证环境切换

**验收：** 通过配置切换整个应用的行为
**难度：** ⭐⭐⭐
