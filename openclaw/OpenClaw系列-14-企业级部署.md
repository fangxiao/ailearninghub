# 企业级部署：从开发到生产

阅读时间：35分钟
难度等级：⭐⭐⭐⭐⭐ 原理篇
你将收获：掌握企业级部署的完整流程

<br/>

***

<br/>

## 从架构到生产：最后一步

前三篇你学会了核心循环、记忆系统、架构设计，理解了OpenClaw的"灵魂"和"骨架"。

**但还有最后一个问题：**

• "开发环境跑得好好的，怎么上线？"
• "如何保证生产环境稳定？"
• "高并发怎么处理？"
• "出问题了怎么排查？"

这一篇，带你走完最后一步——从开发到生产。

<br/>

***

<br/>

## 一、企业级需求

### 1.1 功能需求

**生产环境必须满足：**

| 指标 | 要求 | 说明 |
|------|------|------|
| 可用性 | 99.9%+ | 每年停机不超过8.7小时 |
| 并发 | 1000+ QPS | 每秒处理1000+请求 |
| 延迟 | <3s | 95%请求3秒内响应 |
| 扩展性 | 弹性伸缩 | 根据负载自动扩缩 |

<br/>

### 1.2 非功能需求

**生产环境还需要：**

```
安全性：
• 数据加密（传输、存储）
• 访问控制（认证、授权）
• 审计日志（操作记录）
• 合规性（GDPR、等保）

可维护性：
• 配置管理
• 版本控制
• 回滚机制
• 文档完善

可观测性：
• 监控指标
• 日志收集
• 链路追踪
• 告警通知
```

<br/>

***

<br/>

## 二、架构设计

### 2.1 单机架构（开发环境）

```
┌─────────────────────────────────┐
│          单机部署               │
│  ┌─────────────────────────┐   │
│  │     OpenClaw Server     │   │
│  │  ┌─────┐ ┌─────┐ ┌───┐ │   │
│  │  │Agent│ │Skill│ │DB │ │   │
│  │  └─────┘ └─────┘ └───┘ │   │
│  └─────────────────────────┘   │
└─────────────────────────────────┘

特点：
✅ 简单易部署
✅ 开发调试方便
❌ 单点故障
❌ 无法扩展
❌ 性能有限
```

<br/>

### 2.2 分布式架构（生产环境）

```
                    ┌─────────────┐
                    │   用户请求   │
                    └──────┬──────┘
                           ↓
                    ┌─────────────┐
                    │  负载均衡   │
                    │   (Nginx)   │
                    └──────┬──────┘
                           ↓
        ┌──────────────────┼──────────────────┐
        ↓                  ↓                  ↓
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│  API Gateway  │  │  API Gateway  │  │  API Gateway  │
│   (实例1)     │  │   (实例2)     │  │   (实例3)     │
└───────┬───────┘  └───────┬───────┘  └───────┬───────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           ↓
                    ┌─────────────┐
                    │   消息队列   │
                    │   (Redis)   │
                    └──────┬──────┘
                           ↓
        ┌──────────────────┼──────────────────┐
        ↓                  ↓                  ↓
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│ Agent Service │  │ Agent Service │  │ Agent Service │
│   (实例1)     │  │   (实例2)     │  │   (实例3)     │
└───────┬───────┘  └───────┬───────┘  └───────┬───────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           ↓
        ┌──────────────────┼──────────────────┐
        ↓                  ↓                  ↓
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│    PostgreSQL │  │    Redis      │  │  Vector DB    │
│   (主数据库)   │  │   (缓存)      │  │  (向量库)     │
└───────────────┘  └───────────────┘  └───────────────┘
```

<br/>

### 2.3 核心服务拆分

```yaml
services:
  # API网关
  api-gateway:
    image: openclaw/api-gateway:latest
    ports:
      - "80:80"
    depends_on:
      - agent-service
      - skill-service
  
  # Agent服务
  agent-service:
    image: openclaw/agent-service:latest
    replicas: 3
    environment:
      - REDIS_URL=redis://redis:6379
      - DB_URL=postgresql://db:5432/openclaw
  
  # Skill服务
  skill-service:
    image: openclaw/skill-service:latest
    replicas: 2
  
  # 消息队列
  redis:
    image: redis:7-alpine
  
  # 数据库
  postgres:
    image: postgres:15-alpine
  
  # 向量数据库
  milvus:
    image: milvusdb/milvus:latest
```

<br/>

***

<br/>

## 三、容器化部署

### 3.1 Docker镜像

**Dockerfile：**

```dockerfile
# 基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 配置环境变量
ENV OPENCLAW_ENV=production
ENV LOG_LEVEL=INFO

# 暴露端口
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 启动命令
CMD ["python", "-m", "openclaw.server"]
```

<br/>

### 3.2 多阶段构建

```dockerfile
# 构建阶段
FROM python:3.11 AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 运行阶段
FROM python:3.11-slim

WORKDIR /app

# 复制依赖
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# 复制代码
COPY . .

# 非 root 用户
RUN useradd -m openclaw
USER openclaw

EXPOSE 8000
CMD ["python", "-m", "openclaw.server"]
```

<br/>

### 3.3 Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  openclaw:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENCLAW_ENV=production
      - DATABASE_URL=postgresql://user:pass@postgres:5432/openclaw
      - REDIS_URL=redis://redis:6379
      - LLM_API_KEY=${LLM_API_KEY}
    depends_on:
      - postgres
      - redis
    volumes:
      - ./data:/app/data
    restart: unless-stopped
  
  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=openclaw
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped
  
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

<br/>

***

<br/>

## 四、Kubernetes编排

### 4.1 Deployment

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: openclaw-agent
  labels:
    app: openclaw
    component: agent
spec:
  replicas: 3
  selector:
    matchLabels:
      app: openclaw
      component: agent
  template:
    metadata:
      labels:
        app: openclaw
        component: agent
    spec:
      containers:
      - name: agent
        image: openclaw/agent-service:v1.0.0
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: openclaw-secrets
              key: database-url
        - name: LLM_API_KEY
          valueFrom:
            secretKeyRef:
              name: openclaw-secrets
              key: llm-api-key
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

<br/>

### 4.2 Service

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: openclaw-agent
spec:
  selector:
    app: openclaw
    component: agent
  ports:
  - port: 80
    targetPort: 8000
  type: ClusterIP

---
# Ingress
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: openclaw-ingress
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  tls:
  - hosts:
    - api.openclaw.example.com
    secretName: openclaw-tls
  rules:
  - host: api.openclaw.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: openclaw-agent
            port:
              number: 80
```

<br/>

### 4.3 HPA（自动伸缩）

```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: openclaw-agent-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: openclaw-agent
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Pods
        value: 2
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Pods
        value: 4
        periodSeconds: 60
```

<br/>

***

<br/>

## 五、高可用设计

### 5.1 负载均衡

```nginx
# nginx.conf
upstream openclaw_backend {
    least_conn;  # 最少连接
    server 10.0.0.1:8000 weight=3;
    server 10.0.0.2:8000 weight=3;
    server 10.0.0.3:8000 weight=2;
    server 10.0.0.4:8000 backup;  # 备用
    
    keepalive 32;  # 保持连接数
}

server {
    listen 80;
    server_name api.openclaw.example.com;
    
    # HTTPS重定向
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.openclaw.example.com;
    
    ssl_certificate /etc/ssl/openclaw.crt;
    ssl_certificate_key /etc/ssl/openclaw.key;
    
    location / {
        proxy_pass http://openclaw_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        
        # 超时设置
        proxy_connect_timeout 10s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # 健康检查
    location /health {
        access_log off;
        return 200 "OK";
    }
}
```

<br/>

### 5.2 数据库高可用

```yaml
# PostgreSQL 主从复制
primary:
  image: postgres:15
  environment:
    - POSTGRES_REPLICATION_MODE=master
    - POSTGRES_REPLICATION_USER=replicator
  volumes:
    - pg_primary_data:/var/lib/postgresql/data

replica:
  image: postgres:15
  environment:
    - POSTGRES_REPLICATION_MODE=slave
    - POSTGRES_MASTER_HOST=primary
    - POSTGRES_MASTER_PORT=5432
  volumes:
    - pg_replica_data:/var/lib/postgresql/data
  depends_on:
    - primary

# 连接池（PgBouncer）
pgbouncer:
  image: edoburu/pgbouncer
  environment:
    - DATABASE_URL=postgres://user:pass@primary:5432/openclaw
    - POOL_MODE=transaction
    - MAX_DB_CONNECTIONS=100
    - DEFAULT_POOL_SIZE=20
```

<br/>

### 5.3 缓存高可用

```yaml
# Redis Sentinel（哨兵模式）
redis-master:
  image: redis:7-alpine
  command: redis-server

redis-sentinel:
  image: redis:7-alpine
  command: redis-sentinel /etc/redis/sentinel.conf
  depends_on:
    - redis-master

# sentinel.conf
sentinel monitor mymaster redis-master 6379 2
sentinel down-after-milliseconds mymaster 5000
sentinel failover-timeout mymaster 60000
```

<br/>

### 5.4 容错机制

```python
class CircuitBreaker:
    """熔断器"""
    
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.state = "closed"  # closed, open, half-open
        self.last_failure_time = None
    
    async def call(self, func: callable, *args, **kwargs):
        """带熔断的调用"""
        if self.state == "open":
            # 检查是否可以尝试半开
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "half-open"
            else:
                raise CircuitBreakerOpenError("熔断器打开")
        
        try:
            result = await func(*args, **kwargs)
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise
    
    def on_success(self):
        """成功回调"""
        self.failure_count = 0
        self.state = "closed"
    
    def on_failure(self):
        """失败回调"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = "open"


# 使用示例
breaker = CircuitBreaker(failure_threshold=5, timeout=60)

async def call_llm_with_breaker(prompt: str):
    return await breaker.call(llm_client.generate, prompt)
```

<br/>

***

<br/>

## 六、监控与告警

### 6.1 Prometheus监控

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'openclaw'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_label_app]
        regex: openclaw
        action: keep

# 指标示例
# openclaw_agent_requests_total{agent_id="xxx", status="success"} 1234
# openclaw_agent_latency_seconds{agent_id="xxx", quantile="0.95"} 2.5
# openclaw_llm_tokens_total{model="gpt-4"} 50000
```

<br/>

### 6.2 Grafana仪表盘

```
关键指标：

1. 请求量（QPS）
   - 总请求数
   - 成功/失败率
   - 按Agent分组

2. 延迟（Latency）
   - P50/P95/P99
   - 按接口分组
   - 趋势图

3. 资源使用
   - CPU使用率
   - 内存使用率
   - 网络IO

4. LLM指标
   - Token消耗
   - API调用次数
   - 成本统计

5. Agent状态
   - 运行中Agent数
   - 等待队列长度
   - 错误率
```

<br/>

### 6.3 告警规则

```yaml
# alerting_rules.yml
groups:
  - name: openclaw-alerts
    rules:
      # 错误率告警
      - alert: HighErrorRate
        expr: rate(openclaw_agent_requests_total{status="error"}[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "错误率过高"
          description: "Agent错误率超过10%"
      
      # 延迟告警
      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(openclaw_agent_latency_seconds_bucket[5m])) > 5
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "延迟过高"
          description: "P95延迟超过5秒"
      
      # 资源告警
      - alert: HighMemoryUsage
        expr: container_memory_usage_bytes / container_spec_memory_limit_bytes > 0.9
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "内存使用过高"
          description: "内存使用率超过90%"
```

<br/>

### 6.4 告警通知

```yaml
# alertmanager.yml
global:
  resolve_timeout: 5m

route:
  group_by: ['alertname', 'severity']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  receiver: 'team-openclaw'
  
  routes:
    - match:
        severity: critical
      receiver: 'team-openclaw-critical'
    
    - match:
        severity: warning
      receiver: 'team-openclaw-warning'

receivers:
  - name: 'team-openclaw-critical'
    slack_configs:
      - channel: '#openclaw-critical'
        send_resolved: true
    
    pagerduty_configs:
      - service_key: 'xxx'
  
  - name: 'team-openclaw-warning'
    slack_configs:
      - channel: '#openclaw-alerts'
        send_resolved: true
```

<br/>

***

<br/>

## 七、日志管理

### 7.1 日志规范

```python
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    """JSON格式日志"""
    
    def format(self, record):
        log_obj = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # 添加额外字段
        if hasattr(record, 'agent_id'):
            log_obj["agent_id"] = record.agent_id
        if hasattr(record, 'user_id'):
            log_obj["user_id"] = record.user_id
        if hasattr(record, 'trace_id'):
            log_obj["trace_id"] = record.trace_id
        
        # 异常信息
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_obj)

# 配置
logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.StreamHandler()
    ]
)

for handler in logging.root.handlers:
    handler.setFormatter(JSONFormatter())
```

<br/>

### 7.2 ELK日志收集

```yaml
# Filebeat配置
filebeat.inputs:
  - type: log
    paths:
      - /var/log/openclaw/*.log
    json.keys_under_root: true
    json.add_error_key: true

output.elasticsearch:
  hosts: ["elasticsearch:9200"]
  index: "openclaw-%{+yyyy.MM.dd}"

# Kibana索引模板
{
  "index_patterns": ["openclaw-*"],
  "mappings": {
    "properties": {
      "timestamp": {"type": "date"},
      "level": {"type": "keyword"},
      "agent_id": {"type": "keyword"},
      "user_id": {"type": "keyword"},
      "trace_id": {"type": "keyword"},
      "message": {"type": "text"}
    }
  }
}
```

<br/>

### 7.3 链路追踪

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger import JaegerExporter

# 配置Jaeger
trace.set_tracer_provider(TracerProvider())
jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

tracer = trace.get_tracer(__name__)

# 使用示例
async def process_request(request_id: str):
    with tracer.start_as_current_span("process_request") as span:
        span.set_attribute("request_id", request_id)
        
        # 调用LLM
        with tracer.start_as_current_span("llm_call"):
            result = await llm_client.generate(prompt)
        
        # 执行工具
        with tracer.start_as_current_span("tool_execution"):
            output = await tool.execute(params)
        
        return output
```

<br/>

***

<br/>

## 八、安全加固

### 8.1 网络安全

```yaml
# NetworkPolicy
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: openclaw-network-policy
spec:
  podSelector:
    matchLabels:
      app: openclaw
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8000
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: postgres
    ports:
    - protocol: TCP
      port: 5432
  - to:
    - podSelector:
        matchLabels:
          app: redis
    ports:
    - protocol: TCP
      port: 6379
```

<br/>

### 8.2 数据安全

```python
from cryptography.fernet import Fernet
import os

class DataEncryption:
    """数据加密"""
    
    def __init__(self):
        key = os.getenv("ENCRYPTION_KEY")
        self.cipher = Fernet(key)
    
    def encrypt(self, data: str) -> bytes:
        """加密"""
        return self.cipher.encrypt(data.encode())
    
    def decrypt(self, encrypted: bytes) -> str:
        """解密"""
        return self.cipher.decrypt(encrypted).decode()

# 使用示例
encryption = DataEncryption()

# 加密存储
encrypted_api_key = encryption.encrypt(api_key)
db.save("api_key", encrypted_api_key)

# 解密使用
encrypted = db.get("api_key")
api_key = encryption.decrypt(encrypted)
```

<br/>

### 8.3 访问控制

```python
from functools import wraps
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer

security = HTTPBearer()

class RBAC:
    """基于角色的访问控制"""
    
    ROLES = {
        "admin": ["*"],
        "developer": ["agent:create", "agent:read", "skill:*"],
        "viewer": ["agent:read", "skill:read"]
    }
    
    @staticmethod
    def has_permission(role: str, permission: str) -> bool:
        """检查权限"""
        role_permissions = RBAC.ROLES.get(role, [])
        
        # 通配符匹配
        for rp in role_permissions:
            if rp == "*":
                return True
            if rp.endswith(":*"):
                if permission.startswith(rp[:-1]):
                    return True
            if rp == permission:
                return True
        
        return False

def require_permission(permission: str):
    """权限装饰器"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, user=Depends(get_current_user), **kwargs):
            if not RBAC.has_permission(user.role, permission):
                raise HTTPException(403, "权限不足")
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# 使用示例
@app.post("/agents")
@require_permission("agent:create")
async def create_agent(request: CreateAgentRequest):
    # 创建Agent
    pass
```

<br/>

***

<br/>

## 九、成本优化

### 9.1 资源优化

```yaml
# 资源配额
apiVersion: v1
kind: ResourceQuota
metadata:
  name: openclaw-quota
spec:
  hard:
    requests.cpu: "20"
    requests.memory: 40Gi
    limits.cpu: "40"
    limits.memory: 80Gi

# LimitRange（限制单个Pod）
apiVersion: v1
kind: LimitRange
metadata:
  name: openclaw-limits
spec:
  limits:
  - type: Container
    default:
      cpu: "1"
      memory: "1Gi"
    defaultRequest:
      cpu: "500m"
      memory: "512Mi"
    max:
      cpu: "4"
      memory: "4Gi"
```

<br/>

### 9.2 LLM成本优化

```python
class LLMCostOptimizer:
    """LLM成本优化"""
    
    # 模型价格（$/1K tokens）
    PRICES = {
        "gpt-4": {"input": 0.03, "output": 0.06},
        "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
        "claude-3": {"input": 0.015, "output": 0.075},
        "glm-4": {"input": 0.001, "output": 0.001}
    }
    
    def __init__(self):
        self.cache = LRUCache(maxsize=1000)
    
    async def generate(self, prompt: str, model: str = "gpt-3.5-turbo"):
        """带缓存的生成"""
        # 1. 检查缓存
        cache_key = self.hash_prompt(prompt, model)
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # 2. 选择模型（根据复杂度）
        if self.is_simple_task(prompt):
            model = "gpt-3.5-turbo"
        elif self.is_complex_task(prompt):
            model = "gpt-4"
        
        # 3. 调用LLM
        result = await self.llm_client.generate(prompt, model)
        
        # 4. 缓存结果
        self.cache[cache_key] = result
        
        # 5. 记录成本
        tokens = self.count_tokens(prompt, result)
        cost = self.calculate_cost(tokens, model)
        self.log_cost(cost)
        
        return result
    
    def is_simple_task(self, prompt: str) -> bool:
        """判断是否简单任务"""
        # 简单规则：字数少、无复杂逻辑
        return len(prompt) < 500 and "分析" not in prompt
    
    def calculate_cost(self, tokens: dict, model: str) -> float:
        """计算成本"""
        price = self.PRICES[model]
        return (tokens["input"] * price["input"] + 
                tokens["output"] * price["output"]) / 1000
```

<br/>

***

<br/>

## 十、运维自动化

### 10.1 CI/CD流程

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Build Docker Image
      run: |
        docker build -t openclaw/agent-service:${{ github.sha }} .
        docker push openclaw/agent-service:${{ github.sha }}
    
    - name: Run Tests
      run: |
        docker run openclaw/agent-service:${{ github.sha }} pytest
  
  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
    - name: Deploy to Kubernetes
      run: |
        kubectl set image deployment/openclaw-agent \
          agent=openclaw/agent-service:${{ github.sha }}
    
    - name: Wait for Rollout
      run: |
        kubectl rollout status deployment/openclaw-agent --timeout=300s
    
    - name: Run Smoke Tests
      run: |
        ./scripts/smoke-test.sh
```

<br/>

### 10.2 故障排查

```bash
#!/bin/bash
# troubleshooting.sh

echo "=== OpenClaw 故障排查 ==="

# 1. 检查Pod状态
echo "1. Pod状态："
kubectl get pods -l app=openclaw

# 2. 检查日志
echo "2. 最近日志："
kubectl logs -l app=openclaw --tail=100

# 3. 检查事件
echo "3. 最近事件："
kubectl get events --sort-by='.lastTimestamp' | tail -20

# 4. 检查资源使用
echo "4. 资源使用："
kubectl top pods -l app=openclaw

# 5. 检查健康状态
echo "5. 健康检查："
kubectl exec -it deployment/openclaw-agent -- curl -s localhost:8000/health

# 6. 检查数据库连接
echo "6. 数据库连接："
kubectl exec -it deployment/openclaw-agent -- python -c "
import psycopg2
conn = psycopg2.connect('$DATABASE_URL')
print('数据库连接正常')
"

# 7. 检查Redis连接
echo "7. Redis连接："
kubectl exec -it deployment/openclaw-agent -- python -c "
import redis
r = redis.from_url('$REDIS_URL')
print('Redis连接正常')
"
```

<br/>

***

<br/>

## 十一、实战案例

### 11.1 案例一：智能客服系统

```yaml
# 架构
用户 → 负载均衡 → API网关 → Agent服务
                              ↓
                         知识库(RAG)
                              ↓
                         LLM推理

# 部署配置
replicas: 10
autoscaling:
  min: 5
  max: 50
  target_cpu: 60%

# 性能指标
QPS: 2000+
延迟: P95 < 2s
可用性: 99.95%
```

<br/>

### 11.2 案例二：内容生产平台

```yaml
# 架构
任务队列 → Worker Agent → 内容存储 → 发布服务

# 多Agent协作
agents:
  - planner: 2 replicas
  - writer: 10 replicas
  - editor: 5 replicas
  - publisher: 3 replicas

# 成本优化
- 使用GPT-3.5做初稿
- 使用GPT-4做精修
- 缓存常见内容模板
```

<br/>

***

<br/>

## 十二、小结

### 企业级部署要点

> **架构：** 微服务、分布式、高可用
>
> **容器化：** Docker + Kubernetes
>
> **监控：** Prometheus + Grafana
>
> **日志：** ELK Stack
>
> **安全：** 网络、数据、访问控制
>
> **成本：** 资源优化、模型选择

### 部署检查清单

- [ ] 架构设计完成
- [ ] Docker镜像构建
- [ ] Kubernetes配置就绪
- [ ] 监控告警配置
- [ ] 日志收集配置
- [ ] 安全加固完成
- [ ] CI/CD流程配置
- [ ] 灾备方案就绪
- [ ] 文档完善
- [ ] 压力测试通过

<br/>

***

<br/>

## 系列总结

恭喜你完成了《OpenClaw从入门到精通》全部15篇！

### 学习路径回顾

```
新手篇（5篇）：
✅ OpenClaw是什么
✅ 10分钟部署
✅ 10个实用任务
✅ 基础配置指南
✅ 默认Skills与管理

进阶篇（6篇）：
✅ 第一个自定义Skill
✅ Agent工作流
✅ 多Agent协作
✅ 工具与API集成
✅ 进阶篇总结

原理篇（4篇）：
✅ 核心循环
✅ 记忆系统
✅ 架构解析
✅ 企业级部署
```

### 你现在的能力

• ✅ 会使用OpenClaw
• ✅ 会开发Skill
• ✅ 会设计工作流
• ✅ 会组建多Agent团队
• ✅ 会集成外部服务
• ✅ 理解核心原理
• ✅ 能企业级部署

**你已经是一名合格的OpenClaw开发者了！** 🎉

<br/>

***

<br/>

## 下一步

### 持续学习

• 🔗 官方文档：docs.openclaw.ai
• 🔗 社区：discord.gg/clawd
• 🔗 Skills市场：clawhub.com
• 🔗 GitHub：github.com/openclaw

### 实践项目

1. 个人助手系统
2. 智能客服系统
3. 内容生产平台
4. 数据分析平台

### 贡献社区

• 分享你的Skill
• 贡献代码
• 撰写教程
• 帮助新手

<br/>

***

**系列导航**

• 上一篇：OpenClaw架构解析：设计哲学
• 系列完结

<br/>

***

本文是《OpenClaw从入门到精通》系列第14篇（原理篇第4篇·完结篇）
作者：生活助理 | 发布时间：2026-03-26

**感谢你的坚持！期待在社区见到你的作品！** 🚀
