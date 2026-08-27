# 实战07：前端界面

阅读时间：40分钟
难度等级：⭐⭐⭐⭐ 进阶
你将收获：Vue 3 + Element Plus + ECharts 实现完整前端

<br/>

***

<br/>

## 从 API 到界面

**上篇回顾：**

```
✅ 实战06：后端服务 + Skills
   - 用户认证（JWT）
   - 权限管理（RBAC）
   - 团队管理
   - WebSocket 实时通知
```

**本篇目标：**

```
实现完整的前端界面

内容：
✅ Vue 3 项目搭建
✅ Element Plus 集成
✅ API 接口对接
✅ 数据可视化（ECharts）
✅ WebSocket 实时更新
```

**学习要点：**

- ✅ Vue 3 组合式 API
- ✅ Element Plus 组件使用
- ✅ Axios 请求封装
- ✅ ECharts 图表集成
- ✅ WebSocket 客户端

<br/>

***

<br/>

## 一、项目搭建

### 1.1 创建 Vue 3 项目

```bash
# 使用 Vite 创建项目
npm create vite@latest codestats-frontend -- --template vue-ts
cd codestats-frontend

# 安装依赖
npm install element-plus axios echarts pinia vue-router@4

# 安装开发依赖
npm install -D @types/node sass
```

<br/>

### 1.2 项目结构

```
codestats-frontend/
├── src/
│   ├── main.ts                 # 入口文件
│   ├── App.vue                 # 根组件
│   ├── router/                 # 路由
│   ├── store/                  # 状态管理
│   ├── views/                  # 页面
│   ├── components/             # 组件
│   ├── api/                    # API 接口
│   ├── composables/            # 组合式函数
│   ├── utils/                  # 工具函数
│   └── styles/                 # 样式
├── public/
├── .env
├── vite.config.ts
└── package.json
```

<br/>

### 1.3 配置 Vite

```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src')
    }
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
```

<br/>

***

<br/>

## 二、核心功能实现

### 2.1 Axios 封装

```typescript
// src/api/request.ts
import axios from 'axios'
import { ElMessage } from 'element-plus'

const request = axios.create({
  baseURL: '/api',
  timeout: 10000
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => Promise.reject(error)
)

// 响应拦截器
request.interceptors.response.use(
  response => response.data,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    } else {
      ElMessage.error(error.response?.data?.message || '请求失败')
    }
    return Promise.reject(error)
  }
)

export default request
```

<br/>

### 2.2 项目列表页面

```vue
<!-- src/views/projects/ProjectList.vue -->
<template>
  <div class="project-list">
    <el-row :gutter="20">
      <el-col :span="6" v-for="project in projects" :key="project.id">
        <el-card class="project-card" @click="viewProject(project.id)">
          <template #header>
            <div class="card-header">
              <span>{{ project.name }}</span>
              <el-tag v-if="project.github_url" size="small">GitHub</el-tag>
            </div>
          </template>
          
          <el-statistic title="代码行数" :value="project.code_lines" />
          
          <div class="stats-row">
            <span>文件: {{ project.total_files }}</span>
            <span>语言: {{ project.github_language || 'Unknown' }}</span>
          </div>
          
          <div class="tags">
            <el-tag v-for="tag in project.tags" :key="tag.id" size="small">
              {{ tag.name }}
            </el-tag>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-empty v-if="projects.length === 0" description="暂无项目">
      <el-button type="primary" @click="createProject">创建项目</el-button>
    </el-empty>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getProjects } from '@/api/project'

const router = useRouter()
const projects = ref([])

onMounted(async () => {
  projects.value = await getProjects()
})

const viewProject = (id: number) => {
  router.push(`/projects/${id}`)
}

const createProject = () => {
  router.push('/projects/create')
}
</script>

<style scoped>
.project-card {
  cursor: pointer;
  transition: transform 0.2s;
}

.project-card:hover {
  transform: translateY(-5px);
}

.stats-row {
  margin-top: 10px;
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  color: #666;
}

.tags {
  margin-top: 10px;
}
</style>
```

<br/>

***

<br/>

## 三、数据可视化

### 3.1 语言分布饼图

```vue
<!-- src/components/stats/LanguagePie.vue -->
<template>
  <div ref="chartRef" style="width: 100%; height: 400px"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import * as echarts from 'echarts'

const props = defineProps<{
  languageStats: Record<string, number>
}>()

const chartRef = ref<HTMLElement>()
let chart: echarts.ECharts

onMounted(() => {
  chart = echarts.init(chartRef.value!)
  updateChart()
})

watch(() => props.languageStats, updateChart)

function updateChart() {
  const data = Object.entries(props.languageStats).map(([name, value]) => ({
    name,
    value
  }))
  
  chart.setOption({
    title: {
      text: '语言分布',
      left: 'center'
    },
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [{
      type: 'pie',
      radius: '50%',
      data,
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }]
  })
}
</script>
```

<br/>

### 3.2 趋势折线图

```vue
<!-- src/components/stats/TrendLine.vue -->
<template>
  <div ref="chartRef" style="width: 100%; height: 300px"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import * as echarts from 'echarts'

const props = defineProps<{
  history: Array<{ analyzed_at: string; code_lines: number }>
}>()

const chartRef = ref<HTMLElement>()
let chart: echarts.ECharts

onMounted(() => {
  chart = echarts.init(chartRef.value!)
  updateChart()
})

watch(() => props.history, updateChart)

function updateChart() {
  const dates = props.history.map(h => h.analyzed_at.slice(0, 10))
  const values = props.history.map(h => h.code_lines)
  
  chart.setOption({
    title: {
      text: '代码行数趋势'
    },
    xAxis: {
      type: 'category',
      data: dates.reverse()
    },
    yAxis: {
      type: 'value'
    },
    series: [{
      data: values.reverse(),
      type: 'line',
      smooth: true,
      areaStyle: {
        color: 'rgba(64, 158, 255, 0.2)'
      }
    }]
  })
}
</script>
```

<br/>

***

<br/>

## 四、WebSocket 实时更新

### 4.1 WebSocket 服务

```typescript
// src/composables/useWebSocket.ts
import { ref, onUnmounted } from 'vue'

export function useWebSocket(userId: number) {
  const ws = ref<WebSocket>()
  const isConnected = ref(false)
  const messages = ref<any[]>([])
  
  function connect() {
    ws.value = new WebSocket(`ws://localhost:8000/ws/${userId}`)
    
    ws.value.onopen = () => {
      isConnected.value = true
      console.log('WebSocket 连接成功')
    }
    
    ws.value.onmessage = (event) => {
      const message = JSON.parse(event.data)
      messages.value.push(message)
      
      // 处理不同类型的消息
      if (message.type === 'analysis_complete') {
        // 更新项目统计
        // 显示通知
      }
    }
    
    ws.value.onerror = (error) => {
      console.error('WebSocket 错误:', error)
    }
    
    ws.value.onclose = () => {
      isConnected.value = false
      console.log('WebSocket 断开')
      
      // 自动重连
      setTimeout(connect, 5000)
    }
  }
  
  function disconnect() {
    ws.value?.close()
  }
  
  onUnmounted(disconnect)
  
  return {
    connect,
    disconnect,
    isConnected,
    messages
  }
}
```

<br/>

### 4.2 实时分析进度

```vue
<!-- src/views/projects/ProjectDetail.vue -->
<template>
  <div>
    <el-progress 
      v-if="analyzing"
      :percentage="progress"
      :status="progressStatus"
    />
    
    <el-button 
      @click="analyzeProject"
      :loading="analyzing"
      :disabled="analyzing"
    >
      {{ analyzing ? '分析中...' : '开始分析' }}
    </el-button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useWebSocket } from '@/composables/useWebSocket'
import { useUserStore } from '@/store/user'

const userStore = useUserStore()
const { connect, messages } = useWebSocket(userStore.userId)

const analyzing = ref(false)
const progress = ref(0)
const progressStatus = ref('')

onMounted(() => {
  connect()
  
  // 监听分析进度
  messages.value = []
})

// 监听消息变化
watch(messages, (msgs) => {
  const latest = msgs[msgs.length - 1]
  
  if (latest?.type === 'analysis_progress') {
    progress.value = latest.progress
    progressStatus.value = ''
  }
  
  if (latest?.type === 'analysis_complete') {
    progress.value = 100
    progressStatus.value = 'success'
    analyzing.value = false
    
    // 更新统计数据
    project.value = latest.stats
  }
})

async function analyzeProject() {
  analyzing.value = true
  progress.value = 0
  
  await api.analyzeProject(projectId)
}
</script>
```

<br/>

***

<br/>

## 五、总结

### 5.1 完成的功能

**页面实现：**

```
✅ 登录/注册页
✅ 仪表盘
✅ 项目列表
✅ 项目详情
✅ 团队管理
✅ 个人设置
```

**数据可视化：**

```
✅ 语言分布饼图
✅ 代码行数趋势图
✅ 项目对比柱状图
✅ 实时进度条
```

**实时更新：**

```
✅ WebSocket 连接
✅ 分析进度推送
✅ 自动重连
✅ 消息处理
```

<br/>

### 5.2 技术栈总结

```
前端框架：Vue 3 + TypeScript
UI 库：Element Plus
图表：ECharts
状态管理：Pinia
路由：Vue Router 4
HTTP：Axios
实时通信：WebSocket
构建工具：Vite
```

<br/>

### 5.3 下一步

**实战08：数据分析 + AI 特性**

```
📋 代码质量评分（ML 模型）
📋 智能建议（LLM）
📋 数据导出（PDF/Excel）
📋 报告生成
```

<br/>

***

<br/>

**系列导航**

• 上一篇：实战06：后端服务 + Skills
• 下一篇：实战08：数据分析 + AI 特性

<br/>

***

本文是《AI Coding 从入门到精通》系列第22篇  
作者：生活助理 | 发布时间：2026-04-06

**从 API 到界面，完整的用户体验！** 🎨
