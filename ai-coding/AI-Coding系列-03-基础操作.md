# 基础操作：5个必会命令

阅读时间：15分钟
难度等级：⭐⭐ 初学者
你将收获：掌握 Claude Code 的5个核心操作

<br/>

***

<br/>

## 回顾:从概念到实践

**前两篇我们完成了:**

**第一篇:理解 AI Coding**
- 什么是 AI Coding
- AI Coding Agent 对比
- **AI Coding 能做什么**（5个核心能力:代码生成、代码解释、Bug修复、重构优化、测试生成）

**第二篇:完成安装配置**
- 选择 Coding Plan
- 注册并获取 API Key
- 安装配置 Claude Code
- 运行第一个示例

**这一篇:学习具体操作**
→ 如何用 Claude Code 实现 AI Coding 的5个核心能力

**上一篇你已经运行了第一个代码生成示例,这一篇我们将深入学习这5个核心操作的高级用法。**

<br/>

***

<br/>

## 一、代码生成实战

**上一篇你已经生成了第一个斐波那契数列函数,现在学习更高级的用法。**

<br/>

### 1.1 详细需求的力量

**基础提示词:**

```
用 Python 写一个计算斐波那契数列的函数
```

**Claude Code 会生成:**

```python
def fibonacci(n):
    """计算斐波那契数列第n项"""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

# 使用示例
print(fibonacci(10))  # 输出: 55
```

**这是最基础的用法,但生成的代码还很简单。让我们看如何获得更好的结果。**

<br/>

**进阶提示词:**

```
用 Python 写一个斐波那契数列函数:

要求:
1. 支持递归和迭代两种实现
2. 添加类型注解
3. 包含边界检查
4. 生成前n项的列表
5. 包含性能优化(记忆化)
6. 写出测试用例

输出格式:
- 代码有详细注释
- 包含使用示例
```

**这次 Claude 生成的代码质量会显著提升:**

- ✅ 两种实现方式
- ✅ 完整的类型注解
- ✅ 边界检查和错误处理
- ✅ 性能优化
- ✅ 完整的测试用例

<br/>

### 1.2 实战技巧

**技巧1:指定代码风格**

```
用 Python 写一个排序函数:

风格要求:
- 遵循 PEP 8 规范
- 使用类型注解
- 函数和变量命名清晰
- 添加 docstring
```

<br/>

**技巧2:指定性能要求**

```
实现一个快速排序:

性能要求:
- 平均时间复杂度 O(n log n)
- 空间复杂度 O(log n)
- 使用原地排序
```

<br/>

**技巧3:提供项目上下文**

```
我在做一个 Django 电商项目,需要一个商品搜索功能:

技术栈:
- Django 3.2
- PostgreSQL
- Redis(缓存)

要求:
- 支持关键词搜索
- 支持价格区间筛选
- 使用缓存优化
```

<br/>

***

<br/>

## 二、代码解释实战

**理解代码是开发者的重要能力。**

<br/>

### 2.1 基础用法

**提问方式:**

```
解释这段代码:

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)
```

**Claude Code 的解释:**

```
这是快速排序的 Python 实现:

【核心思想】
分治法:选一个基准值,把数组分成三部分
- left:小于基准值的元素
- middle:等于基准值的元素  
- right:大于基准值的元素

【执行流程】
1. 递归出口:数组长度 ≤ 1 时返回
2. 选择基准:取中间元素作为 pivot
3. 分割数组:遍历数组,分成三组
4. 递归排序:对左右两部分递归调用
5. 合并结果:left + middle + right

【时间复杂度】
- 平均:O(n log n)
- 最坏:O(n²)(数组已排序时)

【空间复杂度】
- O(n):每次递归都创建新数组

【改进建议】
可以使用原地排序优化空间复杂度到 O(log n)
```

<br/>

### 2.2 深度解释技巧

**更详细的提问:**

```
深度解释这段代码:

1. 工作原理是什么?
2. 有什么优缺点?
3. 时间复杂度是多少?为什么?
4. 有什么潜在问题?
5. 如何改进?
6. 适用场景是什么?
7. 和其他排序算法对比?

[粘贴代码]
```

<br/>

### 2.3 实战场景

**场景1:理解别人代码**

```
我接手了一个项目,请帮我理解这个函数:

1. 这个函数的作用是什么?
2. 输入输出是什么?
3. 核心逻辑是什么?
4. 有什么潜在问题?
5. 如何优化?

[粘贴代码]
```

<br/>

**场景2:学习新技术**

```
我在学习 React Hooks,请解释这段代码:

1. useState 和 useEffect 在做什么?
2. 为什么要在 useEffect 里返回一个函数?
3. 依赖数组 [count] 是什么意思?
4. 有什么常见错误?

[粘贴 React 代码]
```

<br/>

***

<br/>

## 三、Bug 修复实战

**Bug 修复是开发者的日常工作。**

<br/>

### 3.1 基础用法

**提供错误信息:**

```
这段代码报错了,帮我修复:

错误信息:
TypeError: 'NoneType' object is not iterable

代码:
def get_user_names(users):
    result = []
    for user in users:
        result.append(user['name'])
    return result

data = None
names = get_user_names(data)
```

**Claude Code 的回复:**

```python
# 问题分析:
# users 参数为 None,导致 for 循环报错

# 修复方案:
def get_user_names(users):
    """安全地获取用户名列表"""
    if users is None:
        return []
    
    result = []
    for user in users:
        # 防御性编程:检查 user 是否有 'name' 键
        if user and 'name' in user:
            result.append(user['name'])
    return result

# 或者更简洁的写法:
def get_user_names_safe(users):
    """使用列表推导式的简洁版本"""
    return [user['name'] for user in (users or []) if user and 'name' in user]

# 测试
data = None
print(get_user_names(data))  # 输出: []

data = [{'name': 'Alice'}, {'name': 'Bob'}]
print(get_user_names(data))  # 输出: ['Alice', 'Bob']
```

<br/>

### 3.2 完整的 Bug 报告

**提供完整的 Bug 报告:**

```
请帮我修复这个 Bug:

【错误信息】
Traceback (most recent call last):
  File "app.py", line 25, in <module>
    result = calculate_average(numbers)
ZeroDivisionError: division by zero

【代码】
def calculate_average(numbers):
    total = sum(numbers)
    return total / len(numbers)

numbers = []
result = calculate_average(numbers)

【预期行为】
空列表应该返回 0,而不是报错

【环境】
- Python 3.10

【请提供】
1. 问题原因
2. 修复方案(多个)
3. 推荐方案和理由
```

**Claude Code 的回复:**

```python
# 问题原因:
# 当 numbers 为空列表时,len(numbers) = 0
# 导致除法运算 total / 0 抛出 ZeroDivisionError

# 修复方案1:添加边界检查(推荐)
def calculate_average(numbers):
    """计算平均值,空列表返回 0"""
    if not numbers:  # 空列表检查
        return 0
    return sum(numbers) / len(numbers)

# 修复方案2:使用异常处理
def calculate_average_v2(numbers):
    """使用 try-except 处理"""
    try:
        return sum(numbers) / len(numbers)
    except ZeroDivisionError:
        return 0

# 修复方案3:使用默认值
def calculate_average_v3(numbers):
    """使用 or 运算符"""
    return sum(numbers) / len(numbers) if numbers else 0

# 测试
print(calculate_average([]))        # 输出: 0
print(calculate_average([1,2,3,4])) # 输出: 2.5
```

**推荐方案:方案1**
- 理由:边界检查是最清晰、最高效的方式
- 性能:无需异常处理开销
- 可读性:意图明确

<br/>

### 3.3 复杂 Bug 调试

**提供更多上下文信息:**

```
这个 Bug 很难定位,请帮我分析:

【现象】
偶尔出现数据不一致,大约 1% 的请求

【代码】
class Cache:
    def __init__(self):
        self.data = {}
    
    def get(self, key):
        return self.data.get(key)
    
    def set(self, key, value):
        self.data[key] = value

# 多线程环境使用
cache = Cache()

【环境】
- 多线程 Web 服务器
- 高并发场景

【请分析】
1. 可能的原因
2. 如何复现
3. 修复方案
4. 预防措施
```

**Claude Code 的回复:**

```python
# 问题分析:
# 在多线程环境下,多个线程同时读写 self.data 字典
# Python 字典在并发访问时可能出现竞争条件
# 导致数据不一致或偶发的 KeyError

# 复现方法:
import threading

cache = Cache()

def concurrent_access():
    for i in range(1000):
        cache.set(f"key_{i}", i)
        cache.get(f"key_{i}")

# 创建多个线程并发访问
threads = [threading.Thread(target=concurrent_access) for _ in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()
# 很可能出现数据不一致

# 修复方案1:使用 threading.Lock(推荐)
import threading

class ThreadSafeCache:
    def __init__(self):
        self.data = {}
        self.lock = threading.Lock()
    
    def get(self, key):
        with self.lock:
            return self.data.get(key)
    
    def set(self, key, value):
        with self.lock:
            self.data[key] = value

# 修复方案2:使用 concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import threading

class ConcurrentCache:
    def __init__(self):
        self.data = {}
        self.lock = threading.RLock()  # 可重入锁
    
    def get(self, key):
        with self.lock:
            return self.data.get(key)
    
    def set(self, key, value):
        with self.lock:
            self.data[key] = value

# 修复方案3:使用 multiprocessing.Manager(进程安全)
from multiprocessing import Manager

manager = Manager()
cache = manager.dict()  # 进程间共享的字典

# 预防措施:
1. 使用线程安全的数据结构
2. 加锁保护共享资源
3. 尽量使用不可变数据
4. 添加单元测试验证并发安全性
5. 使用压力测试工具验证(Redis benchmark, Apache Bench)

# 测试
safe_cache = ThreadSafeCache()
safe_cache.set("name", "Claude")
print(safe_cache.get("name"))  # 输出: Claude
```

<br/>

***

<br/>

## 四、重构优化实战

**重构提升代码质量,但需要谨慎进行。**

<br/>

### 4.1 基础用法

**简单的重构请求:**

```
重构这个函数,让它更清晰:

def calc(a,b,c):
    if a>0:
        if b>0:
            return a+b+c
        else:
            return a-b+c
    else:
        if b>0:
            return -a+b+c
        else:
            return -a-b+c
```

**Claude Code 的重构:**

```python
def calculate_sum(a: int, b: int, c: int) -> int:
    """
    计算三个数的和,根据 a 和 b 的符号调整
    
    Args:
        a: 第一个数
        b: 第二个数
        c: 第三个数
    
    Returns:
        计算结果
    """
    # 根据符号确定 a 的值
    a_value = a if a > 0 else -a
    
    # 根据符号确定 b 的值
    b_value = b if b > 0 else -b
    
    # 返回总和
    return a_value + b_value + c

# 或者更简洁的写法:
def calculate_sum_simple(a: int, b: int, c: int) -> int:
    """简洁版本"""
    return abs(a) + (a if a > 0 else -a) + c
```

<br/>

### 4.2 重构技巧

**技巧1:指定重构目标**

```
重构这段代码,目标:

1. 提升可读性(降低圈复杂度)
2. 增加可测试性
3. 遵循 SOLID 原则
4. 不改变功能

[粘贴代码]
```

<br/>

**技巧2:分步重构**

```
这个函数有 200 行,需要重构。

请分步进行:
1. 第一步:提取子函数
2. 第二步:优化逻辑
3. 第三步:增加类型注解
4. 第四步:添加文档

每步提供完整代码。
```

<br/>

***

<br/>

## 五、测试生成实战

**测试保证代码质量,AI 可以帮你快速生成。**

<br/>

### 5.1 基础用法

**生成测试用例:**

```
为这个函数生成测试用例:

def divide(a, b):
    if b == 0:
        raise ValueError("除数不能为0")
    return a / b
```

**Claude 生成的测试:**

```python
import unittest

class TestDivide(unittest.TestCase):
    """除法函数测试"""
    
    def test_positive_numbers(self):
        """测试正数除法"""
        self.assertEqual(divide(10, 2), 5)
        self.assertEqual(divide(9, 3), 3)
    
    def test_negative_numbers(self):
        """测试负数除法"""
        self.assertEqual(divide(-10, 2), -5)
        self.assertEqual(divide(10, -2), -5)
        self.assertEqual(divide(-10, -2), 5)
    
    def test_zero_dividend(self):
        """测试被除数为0"""
        self.assertEqual(divide(0, 5), 0)
    
    def test_zero_divisor(self):
        """测试除数为0(应该抛出异常)"""
        with self.assertRaises(ValueError):
            divide(10, 0)
    
    def test_float_result(self):
        """测试浮点数结果"""
        self.assertAlmostEqual(divide(7, 2), 3.5)
        self.assertAlmostEqual(divide(1, 3), 0.333333, places=5)
    
    def test_large_numbers(self):
        """测试大数"""
        result = divide(10**10, 10**5)
        self.assertEqual(result, 10**5)


if __name__ == '__main__':
    unittest.main()
```

<br/>

### 5.2 测试技巧

**技巧1:指定覆盖率**

```
为这个函数生成测试用例:

要求:
- 覆盖率 90% 以上
- 包含边界测试
- 包含异常测试
- 使用 pytest 框架

[粘贴代码]
```

<br/>

**技巧2:测试驱动开发**

```
我要实现一个用户注册功能,请用 TDD 方式:

1. 先写测试用例
2. 再实现功能
3. 确保测试通过

要求:
- 验证邮箱格式
- 密码强度检查
- 用户名唯一性
```

<br/>

***

<br/>

## 六、最佳实践

### 6.1 提示词模板

**代码生成模板:**

```
【背景】我在做 [项目类型]

【任务】实现 [功能描述]

【要求】
- 语言:[Python/JavaScript/etc]
- 框架:[Django/Flask/etc]
- 风格:[规范要求]

【输入输出】
输入:[描述]
输出:[描述]

【示例】
输入:[example]
输出:[example]
```

<br/>

**Bug 修复模板:**

```
【错误信息】
[粘贴错误]

【代码】
[粘贴代码]

【预期行为】
[应该发生什么]

【环境】
- Python 版本:
- 相关库:

【已尝试】
1. [方法1]
2. [方法2]
```

<br/>

### 6.2 常见问题

**Q1:生成的代码质量不高?**

```
解决方案:
1. 提供更详细的要求
2. 指定代码风格
3. 要求添加注释
4. 让 Claude 解释代码
```

<br/>

**Q2:Bug 修复后还有新问题?**

```
解决方案:
1. 提供完整上下文
2. 说明环境信息
3. 要求 Claude 考虑边界情况
4. 生成测试用例验证
```

<br/>

***

<br/>

## 七、总结

### 7.1 核心要点

**5个必会操作:**

```
1. 代码生成:从0到1
   - 提供详细需求
   - 指定风格和格式
   - 包含示例

2. 代码解释:理解原理
   - 问清楚是什么
   - 问为什么这样
   - 问如何改进

3. Bug 修复:找错改错
   - 提供错误信息
   - 提供完整代码
   - 说明预期行为

4. 重构优化:提升质量
   - 明确重构目标
   - 分步进行
   - 保持功能不变

5. 测试生成:保证质量
   - 要求高覆盖率
   - 包含边界测试
   - 使用测试框架
```

<br/>

### 7.2 效率提升

**使用 Claude Code 后:**

```
代码生成:从 2小时 → 10分钟
代码理解:从 1小时 → 5分钟
Bug 修复:从 1小时 → 15分钟
代码重构:从 3小时 → 30分钟
测试编写:从 1小时 → 10分钟

平均效率提升:5-10倍
```

<br/>

***

<br/>

**系列导航**

• 上一篇:10分钟安装配置,开始你的 AI 编程之旅
• 下一篇:提示词技巧:让 Claude 更懂你

<br/>

***

<br/>

本文是《AI Coding 从入门到精通》系列第3篇  
作者:生活助理 | 发布时间:2026-03-27

**掌握这5个操作,你已经能用 Claude Code 做很多事了!** 💪
