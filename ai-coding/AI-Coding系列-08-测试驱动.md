# 测试驱动：AI 帮你写测试

阅读时间：25分钟
难度等级：⭐⭐⭐ 进阶
你将收获：掌握 AI 辅助测试技术，测试覆盖率从 0 到 90%

<br/>

***

<br/>

## 回顾：你已经掌握了什么？

**新手篇（01-05）你学会了：**
- ✅ AI Coding 的基础使用
- ✅ 5个核心操作
- ✅ 提示词技巧

**进阶篇前2篇：**
- ✅ 第6篇：代码库理解 - 让 AI 认识项目
- ✅ 第7篇：多文件编辑 - 批量重构技巧

**你已经能够：**
- 理解项目结构
- 批量修改多个文件
- 进行复杂重构

**但你还缺少一个关键环节：**

重构后，如何确保代码没有问题？测试！

**问题：** 写测试很花时间，很多人不想写、不会写、写不完。

**这一篇将教你：** 如何让 AI 帮你写测试，快速、全面、专业。

<br/>

***

<br/>

## 开篇：测试的困境

**场景1：不想写测试**

```
你：这个功能写完了
同事：测试呢？
你：没时间...以后补...
（3个月后）
你：由于没有测试，重构引入了3个bug
```

**场景2：不会写测试**

```
你：要测试这个函数
问题：
- 不知道测试什么
- 不知道怎么 mock
- 不知道边界条件
- 写出来的测试很脆弱
```

**场景3：测试写不完**

```
你：项目有50个函数
问题：
- 手写测试要2天
- 测试代码比业务代码还多
- 每次改功能都要改测试
```

**解决方法：** 让 AI 帮你写测试，快速、全面、专业。

<br/>

***

<br/>

## 一、为什么测试这么重要？

### 1.1 测试的价值

**测试 = 代码的安全网**

```
没有测试：
❌ 改代码心惊胆战
❌ 不知道哪里会出错
❌ 重构不敢动
❌ Bug 反复出现

有测试：
✅ 改代码有信心
✅ 立即发现问题
✅ 重构无压力
✅ Bug 一次修复
```

**测试覆盖率与质量的关系：**

| 覆盖率 | 代码质量 | 重构难度 |
|:------:|:--------:|:--------:|
| 0% | ⭐⭐ | 😱 很难 |
| 30% | ⭐⭐⭐ | 😰 较难 |
| 60% | ⭐⭐⭐⭐ | 😊 容易 |
| 90% | ⭐⭐⭐⭐⭐ | 🎉 很容易 |

<br/>

### 1.2 AI 写测试的优势

**对比：**

| 方面 | 手写测试 | AI 写测试 |
|------|----------|-----------|
| 速度 | 1小时/函数 | 1分钟/函数 |
| 覆盖率 | 60-70% | 90%+ |
| 边界情况 | 经常遗漏 | 自动识别 |
| Mock 设置 | 手动配置 | 自动生成 |
| 维护成本 | 高 | 低 |
| 质量一致性 | 因人而异 | 稳定 |

**AI 的特别能力：**

```
✅ 自动识别边界情况
✅ 生成多种测试场景
✅ 自动 mock 依赖
✅ 发现隐藏 bug
✅ 保持测试代码质量
```

<br/>

***

<br/>

## 二、快速上手：生成单元测试

### 2.1 基础示例

**被测试的函数：**

```python
# app/services/user_service.py

def calculate_discount(user_level: str, amount: float) -> float:
    """
    根据用户等级计算折扣
    
    Args:
        user_level: 用户等级（normal, silver, gold, platinum）
        amount: 原始金额
    
    Returns:
        折扣后金额
    
    Raises:
        ValueError: 用户等级无效或金额为负
    """
    if amount < 0:
        raise ValueError("金额不能为负")
    
    discounts = {
        'normal': 1.0,      # 无折扣
        'silver': 0.95,     # 95折
        'gold': 0.9,        # 9折
        'platinum': 0.85    # 85折
    }
    
    if user_level not in discounts:
        raise ValueError(f"无效的用户等级: {user_level}")
    
    return amount * discounts[user_level]
```

**生成测试：**

```python
# tests/test_user_service.py

import pytest
from app.services.user_service import calculate_discount


class TestCalculateDiscount:
    """测试折扣计算函数"""
    
    # ===== 正常情况测试 =====
    
    def test_normal_user(self):
        """测试普通用户（无折扣）"""
        result = calculate_discount('normal', 100.0)
        assert result == 100.0
    
    def test_silver_user(self):
        """测试银牌用户（95折）"""
        result = calculate_discount('silver', 100.0)
        assert result == 95.0
    
    def test_gold_user(self):
        """测试金牌用户（9折）"""
        result = calculate_discount('gold', 100.0)
        assert result == 90.0
    
    def test_platinum_user(self):
        """测试白金用户（85折）"""
        result = calculate_discount('platinum', 100.0)
        assert result == 85.0
    
    # ===== 边界情况测试 =====
    
    def test_zero_amount(self):
        """测试金额为0"""
        result = calculate_discount('normal', 0.0)
        assert result == 0.0
    
    def test_very_small_amount(self):
        """测试极小金额"""
        result = calculate_discount('gold', 0.01)
        assert result == pytest.approx(0.009, rel=1e-2)
    
    def test_very_large_amount(self):
        """测试极大金额"""
        result = calculate_discount('platinum', 1000000.0)
        assert result == 850000.0
    
    def test_float_precision(self):
        """测试浮点数精度"""
        result = calculate_discount('silver', 99.99)
        assert result == pytest.approx(94.9905, rel=1e-4)
    
    # ===== 异常情况测试 =====
    
    def test_invalid_user_level(self):
        """测试无效用户等级"""
        with pytest.raises(ValueError, match="无效的用户等级"):
            calculate_discount('diamond', 100.0)
    
    def test_negative_amount(self):
        """测试负数金额"""
        with pytest.raises(ValueError, match="金额不能为负"):
            calculate_discount('normal', -100.0)
    
    def test_empty_user_level(self):
        """测试空用户等级"""
        with pytest.raises(ValueError):
            calculate_discount('', 100.0)
    
    # ===== 参数类型测试 =====
    
    def test_string_amount(self):
        """测试字符串金额（应该失败）"""
        with pytest.raises(TypeError):
            calculate_discount('normal', '100')
    
    def test_integer_amount(self):
        """测试整数金额（应该自动转换）"""
        result = calculate_discount('gold', 100)
        assert result == 90.0
```

**测试覆盖率：100%**

✅ 覆盖范围：
- 正常情况：4个测试
- 边界情况：4个测试
- 异常情况：3个测试
- 类型测试：2个测试
- **总计：13个测试用例**

<br/>

### 2.2 测试类方法

**被测试的类：**

```python
# app/services/order_service.py

class OrderService:
    """订单服务"""
    
    def __init__(self, db, email_service):
        self.db = db
        self.email_service = email_service
    
    def create_order(self, user_id: int, items: list) -> Order:
        """创建订单"""
        # 验证用户
        user = self.db.get_user(user_id)
        if not user:
            raise ValueError("用户不存在")
        
        # 计算总价
        total = sum(item['price'] * item['quantity'] for item in items)
        
        # 创建订单
        order = Order(
            user_id=user_id,
            items=items,
            total=total,
            status='pending'
        )
        
        # 保存订单
        self.db.save_order(order)
        
        # 发送邮件
        self.email_service.send(
            to=user.email,
            subject="订单创建成功",
            body=f"您的订单总额：{total}"
        )
        
        return order
```

**生成测试（带 Mock）：**

```python
# tests/test_order_service.py

import pytest
from unittest.mock import Mock, MagicMock, patch
from app.services.order_service import OrderService


class TestOrderService:
    """测试订单服务"""
    
    @pytest.fixture
    def mock_db(self):
        """模拟数据库"""
        db = Mock()
        db.get_user = Mock(return_value=Mock(
            id=1,
            email="test@example.com"
        ))
        db.save_order = Mock()
        return db
    
    @pytest.fixture
    def mock_email_service(self):
        """模拟邮件服务"""
        service = Mock()
        service.send = Mock()
        return service
    
    @pytest.fixture
    def order_service(self, mock_db, mock_email_service):
        """创建订单服务实例"""
        return OrderService(mock_db, mock_email_service)
    
    def test_create_order_success(self, order_service, mock_db, mock_email_service):
        """测试成功创建订单"""
        # 准备数据
        items = [
            {'price': 10.0, 'quantity': 2},
            {'price': 5.0, 'quantity': 3}
        ]
        
        # 执行
        order = order_service.create_order(user_id=1, items=items)
        
        # 验证
        assert order.user_id == 1
        assert order.total == 35.0  # 10*2 + 5*3
        assert order.status == 'pending'
        
        # 验证数据库调用
        mock_db.get_user.assert_called_once_with(1)
        mock_db.save_order.assert_called_once()
        
        # 验证邮件发送
        mock_email_service.send.assert_called_once()
    
    def test_create_order_user_not_found(self, order_service, mock_db):
        """测试用户不存在"""
        # 设置 mock 返回 None
        mock_db.get_user.return_value = None
        
        # 执行并验证异常
        with pytest.raises(ValueError, match="用户不存在"):
            order_service.create_order(user_id=999, items=[])
    
    def test_create_order_empty_items(self, order_service):
        """测试空订单"""
        # 执行
        order = order_service.create_order(user_id=1, items=[])
        
        # 验证
        assert order.total == 0.0
    
    def test_create_order_email_sent(self, order_service, mock_db, mock_email_service):
        """测试邮件发送"""
        # 执行
        order_service.create_order(user_id=1, items=[
            {'price': 100.0, 'quantity': 1}
        ])
        
        # 验证邮件参数
        call_args = mock_email_service.send.call_args
        assert call_args[1]['to'] == "test@example.com"
        assert "订单创建成功" in call_args[1]['subject']
        assert "100" in call_args[1]['body']
```

**关键点：**
- ✅ 自动生成 Mock 对象
- ✅ 验证依赖调用
- ✅ 测试异常情况
- ✅ 验证副作用（邮件发送）

<br/>

***

<br/>

## 三、进阶技巧：高级测试场景

### 3.1 测试异步代码

**被测试的异步函数：**

```python
# app/services/async_service.py

import aiohttp

async def fetch_user_data(user_id: int) -> dict:
    """异步获取用户数据"""
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.example.com/users/{user_id}') as response:
            if response.status == 404:
                raise ValueError("用户不存在")
            return await response.json()
```

**生成异步测试：**

你：为 fetch_user_data 生成测试

AI：

```python
# tests/test_async_service.py

import pytest
import aiohttp
from aioresponses import aioresponses
from app.services.async_service import fetch_user_data


class TestFetchUserData:
    """测试异步获取用户数据"""
    
    @pytest.mark.asyncio
    async def test_fetch_success(self):
        """测试成功获取数据"""
        # 模拟 API 响应
        with aioresponses() as m:
            m.get(
                'https://api.example.com/users/1',
                payload={'id': 1, 'name': 'Alice'}
            )
            
            # 执行
            result = await fetch_user_data(1)
            
            # 验证
            assert result == {'id': 1, 'name': 'Alice'}
    
    @pytest.mark.asyncio
    async def test_user_not_found(self):
        """测试用户不存在"""
        with aioresponses() as m:
            m.get(
                'https://api.example.com/users/999',
                status=404
            )
            
            # 执行并验证异常
            with pytest.raises(ValueError, match="用户不存在"):
                await fetch_user_data(999)
    
    @pytest.mark.asyncio
    async def test_network_error(self):
        """测试网络错误"""
        with aioresponses() as m:
            m.get(
                'https://api.example.com/users/1',
                exception=aiohttp.ClientError()
            )
            
            # 执行并验证异常
            with pytest.raises(aiohttp.ClientError):
                await fetch_user_data(1)
```

**关键点：**
- ✅ 使用 `@pytest.mark.asyncio`
- ✅ Mock 异步 HTTP 请求
- ✅ 测试网络错误

<br/>

### 3.2 测试数据库操作

**被测试的数据库操作：**

```python
# app/models/user.py

from sqlalchemy import Column, Integer, String
from app.db.base import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String)
    
    @classmethod
    def find_by_email(cls, session, email: str):
        """根据邮箱查找用户"""
        return session.query(cls).filter(cls.email == email).first()
```

**生成数据库测试：**

你：为 User.find_by_email 生成测试

AI：

```python
# tests/test_user_model.py

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.user import User
from app.db.base import Base


@pytest.fixture
def db_session():
    """创建测试数据库会话"""
    # 使用内存数据库
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session
    
    session.close()


class TestUserModel:
    """测试用户模型"""
    
    def test_find_by_email_success(self, db_session):
        """测试成功查找用户"""
        # 准备数据
        user = User(email='test@example.com', name='Test User')
        db_session.add(user)
        db_session.commit()
        
        # 执行
        found = User.find_by_email(db_session, 'test@example.com')
        
        # 验证
        assert found is not None
        assert found.email == 'test@example.com'
        assert found.name == 'Test User'
    
    def test_find_by_email_not_found(self, db_session):
        """测试用户不存在"""
        # 执行
        found = User.find_by_email(db_session, 'notexist@example.com')
        
        # 验证
        assert found is None
    
    def test_find_by_email_case_sensitive(self, db_session):
        """测试邮箱大小写敏感"""
        # 准备数据
        user = User(email='Test@Example.com', name='Test')
        db_session.add(user)
        db_session.commit()
        
        # 执行
        found_lower = User.find_by_email(db_session, 'test@example.com')
        found_upper = User.find_by_email(db_session, 'Test@Example.com')
        
        # 验证
        assert found_lower is None  # 小写查不到
        assert found_upper is not None  # 原样可以查到
```

**关键点：**
- ✅ 使用内存数据库
- ✅ 测试 fixture 隔离
- ✅ 测试边界情况

<br/>

### 3.3 参数化测试

**场景：** 测试多个输入组合

你：为折扣函数生成参数化测试

AI：

```python
# tests/test_discount.py

import pytest
from app.services.user_service import calculate_discount


@pytest.mark.parametrize("level,amount,expected", [
    # 正常情况
    ('normal', 100.0, 100.0),
    ('silver', 100.0, 95.0),
    ('gold', 100.0, 90.0),
    ('platinum', 100.0, 85.0),
    
    # 边界情况
    ('normal', 0.0, 0.0),
    ('gold', 0.01, 0.009),
    ('platinum', 1000000.0, 850000.0),
    
    # 特殊值
    ('silver', 99.99, 94.9905),
    ('gold', 3.333, 2.9997),
])
def test_calculate_discount_normal(level, amount, expected):
    """参数化测试：正常情况"""
    result = calculate_discount(level, amount)
    assert result == pytest.approx(expected, rel=1e-4)


@pytest.mark.parametrize("level,amount,error_match", [
    ('diamond', 100.0, "无效的用户等级"),
    ('', 100.0, "无效的用户等级"),
    ('normal', -100.0, "金额不能为负"),
])
def test_calculate_discount_error(level, amount, error_match):
    """参数化测试：异常情况"""
    with pytest.raises(ValueError, match=error_match):
        calculate_discount(level, amount)
```

**优点：**
- ✅ 一个测试函数，多个测试用例
- ✅ 代码简洁，易维护
- ✅ 覆盖全面

<br/>

***

<br/>

## 四、测试驱动开发（TDD）

### 4.1 TDD 流程

**传统开发：**
```
1. 写代码
2. 写测试
3. 测试失败
4. 修改代码
5. 测试通过
```

**TDD 开发：**
```
1. 写测试（先失败）
2. 写代码（让测试通过）
3. 重构（优化代码）
4. 重复
```

**TDD with AI：**
```
1. 告诉 AI 需求 → AI 生成测试（10秒）
2. AI 生成代码（20秒）
3. 运行测试（5秒）
4. 重构优化（可选）
```

<br/>

### 4.2 TDD 实战示例

**场景：** 开发一个密码验证函数

**步骤1：告诉 AI 需求**

你：我要写一个密码验证函数，要求：
- 至少8个字符
- 包含大小写字母
- 包含数字
- 包含特殊字符
- 返回布尔值

AI：我将先生成测试：

```python
# tests/test_password_validator.py

import pytest
from app.utils.password import validate_password


class TestPasswordValidator:
    """测试密码验证"""
    
    def test_valid_password(self):
        """测试有效密码"""
        assert validate_password("Passw0rd!") == True
        assert validate_password("MyP@ss123") == True
    
    def test_too_short(self):
        """测试太短的密码"""
        assert validate_password("Pass0!") == False
    
    def test_no_uppercase(self):
        """测试没有大写字母"""
        assert validate_password("passw0rd!") == False
    
    def test_no_lowercase(self):
        """测试没有小写字母"""
        assert validate_password("PASSW0RD!") == False
    
    def test_no_digit(self):
        """测试没有数字"""
        assert validate_password("Password!") == False
    
    def test_no_special_char(self):
        """测试没有特殊字符"""
        assert validate_password("Passw0rd") == False
    
    def test_empty_password(self):
        """测试空密码"""
        assert validate_password("") == False
```

现在运行测试（应该失败，因为函数不存在）
```

**步骤2：AI 生成代码**

```
AI：现在生成实现代码：

```python
# app/utils/password.py

import re

def validate_password(password: str) -> bool:
    """
    验证密码强度
    
    要求：
    - 至少8个字符
    - 包含大小写字母
    - 包含数字
    - 包含特殊字符
    
    Args:
        password: 待验证的密码
    
    Returns:
        bool: 是否通过验证
    """
    if len(password) < 8:
        return False
    
    if not re.search(r'[a-z]', password):  # 小写字母
        return False
    
    if not re.search(r'[A-Z]', password):  # 大写字母
        return False
    
    if not re.search(r'\d', password):     # 数字
        return False
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):  # 特殊字符
        return False
    
    return True
```

现在运行测试（应该通过）

**步骤3：运行测试**

AI：✅ 所有测试通过（8/8）

你：优化一下代码

AI：

```python
# 优化版本

import re

def validate_password(password: str) -> bool:
    """验证密码强度"""
    if len(password) < 8:
        return False
    
    patterns = [
        r'[a-z]',        # 小写字母
        r'[A-Z]',        # 大写字母
        r'\d',           # 数字
        r'[!@#$%^&*(),.?":{}|<>]'  # 特殊字符
    ]
    
    return all(re.search(pattern, password) for pattern in patterns)
```

更简洁，易读

你：好的，再运行一次测试

AI：✅ 所有测试通过（8/8）
✅ 重构后功能不变

**时间对比：**
- 手动 TDD：30-60分钟
- AI TDD：5-10分钟
- 提升：6-10倍

<br/>

***

<br/>

## 五、测试覆盖率

### 5.1 什么是覆盖率？

**定义：** 测试覆盖的代码行数 / 总代码行数

```
示例：

def add(a, b):      # 第1行
    return a + b    # 第2行

def multiply(a, b): # 第3行
    return a * b    # 第4行

测试：
def test_add():
    assert add(1, 2) == 3

覆盖率：
- 测试了第1、2行
- 没有测试第3、4行
- 覆盖率 = 2/4 = 50%
```

<br/>

### 5.2 覆盖率目标

| 项目类型 | 推荐覆盖率 |
|----------|:----------:|
| 个人项目 | 60-70% |
| 团队项目 | 70-80% |
| 企业项目 | 80-90% |
| 金融/医疗 | 90%+ |

**关键：**
- ✅ 核心逻辑要 90%+
- ✅ 工具函数可以低一些
- ⚠️ 不要为了覆盖率而测试

<br/>

### 5.3 使用 AI 提高覆盖率

**场景：** 当前覆盖率 60%，提升到 90%

你：分析覆盖率报告，帮我提升到 90%

AI：分析覆盖率报告：

未覆盖的代码：
1. app/services/user_service.py:25-30（异常处理）
2. app/utils/validators.py:15-20（边界检查）
3. app/models/order.py:40-50（状态转换）

生成测试补充这些部分？

你：生成

AI：已生成 15 个新测试用例：

- tests/test_user_service_exception.py（5个）
- tests/test_validators_edge.py（5个）
- tests/test_order_state.py（5个）

运行测试？

你：运行

AI：✅ 所有测试通过（新+旧：58/58）
✅ 覆盖率提升：60% → 92%

<br/>

***

<br/>

## 六、最佳实践

### 6.1 测试命名

**好的命名：**

```python
def test_create_order_with_empty_items_should_return_zero_total():
    """测试：创建空订单应该返回0总价"""
    pass

def test_login_with_invalid_password_should_raise_error():
    """测试：无效密码登录应该抛出异常"""
    pass
```

**不好的命名：**

```python
def test_order():  # 太模糊
    pass

def test_1():      # 无意义
    pass
```

<br/>

### 6.2 测试结构

**AAA 模式：**

```python
def test_create_order():
    # Arrange（准备）
    user_id = 1
    items = [{'price': 10.0, 'quantity': 2}]
    
    # Act（执行）
    order = create_order(user_id, items)
    
    # Assert（验证）
    assert order.total == 20.0
```

<br/>

### 6.3 测试独立性

**好的测试：**

```python
def test_create_user(db_session):
    """每个测试独立"""
    user = User(email='test@example.com')
    db_session.add(user)
    assert db_session.query(User).count() == 1

def test_delete_user(db_session):
    """不依赖上一个测试"""
    user = User(email='test2@example.com')
    db_session.add(user)
    # ...
```

**不好的测试：**

```python
user = None

def test_create_user():
    global user
    user = User(email='test@example.com')  # 依赖全局变量
    # ...

def test_delete_user():
    delete_user(user)  # 依赖上一个测试
    # ...
```

<br/>

***

<br/>

## 七、常见问题

### Q1：测试太慢怎么办？

**答：** 优化策略

```
1. 使用内存数据库
2. Mock 外部依赖
3. 并行运行测试
4. 只运行相关测试
```

<br/>

### Q2：测试太脆弱怎么办？

**答：** 提高测试质量

```
1. 不要测试实现细节
2. 只测试公开接口
3. 使用稳定的测试数据
4. Mock 外部依赖
```

<br/>

### Q3：旧代码没有测试怎么办？

**答：** 渐进式补充

```
1. 先测试核心功能
2. 修改时补充测试
3. 重构时补充测试
4. 不要一次性补全
```

<br/>

***

<br/>

## 八、总结

### 核心要点

**1. 测试的价值**
```
- 代码的安全网
- 重构的信心来源
- 文档的作用
```

**2. AI 写测试的优势**
```
- 快速（1分钟/函数）
- 全面（90%+ 覆盖率）
- 专业（自动识别边界）
```

**3. 测试类型**
```
- 单元测试
- 集成测试
- 端到端测试
```

**4. TDD with AI**
```
- 先写测试（AI 生成）
- 再写代码（AI 生成）
- 重构优化
```

<br/>

### 效率对比

| 任务 | 手动 | AI 辅助 | 提升 |
|------|------|---------|------|
| 写测试 | 1小时 | 5分钟 | 12倍 |
| 提高覆盖率 | 1天 | 2小时 | 4倍 |
| TDD 一个功能 | 30分钟 | 5分钟 | 6倍 |

<br/>

***

<br/>

**系列导航**

• 上一篇：多文件编辑：复杂重构不求人
• 下一篇：调试高手：快速定位和修复 Bug

<br/>

***

本文是《AI Coding 从入门到精通》系列第8篇  
作者：生活助理 | 发布时间：2026-04-03

**让 AI 帮你写测试，从噩梦变享受，测试覆盖率从 0 到 90%！** 🚀
