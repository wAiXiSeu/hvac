# HVAC 三恒系统本地控制

基于 Modbus RTU 协议的暖通空调控制系统，提供 Web 界面进行房间温度、环境监测和控制。

## 功能特性

- **连接管理** - Modbus TCP 连接配置与状态监控
- **环境监测** - 实时温湿度、CO2 浓度数据采集
- **房间控制** - 各房间温度设定、运行模式切换、风速调节
- **系统控制** - 系统启停、定时控制、故障告警

## 技术栈

- 后端：FastAPI + pymodbus + uvicorn
- 前端：React + Vite + Axios

## 快速开始

### 1. 安装依赖

```bash
# 后端依赖
cd hvac-backend
pip install -r requirements.txt

# 前端依赖
cd hvac-web
npm install
```

### 2. 启动服务

```bash
# 方式一：使用启动脚本（推荐）
./start.sh

# 方式二：手动启动
# 终端1 - 启动后端
cd hvac-backend
uvicorn hvac_backend.main:app --host 0.0.0.0 --port 8000 --reload

# 终端2 - 启动前端
cd hvac-web
npm run dev
```

### 3. 访问系统

- 前端：http://localhost:5173
- 后端 API：http://localhost:8000
- API 文档：http://localhost:8000/docs

## 配置

修改 `hvac-backend/config.yaml` 配置 Modbus 连接参数：

```yaml
modbus:
  host: "192.168.110.200"  # Modbus 设备 IP
  port: 502                 # Modbus 端口
  slave_id: 1               # 从机 ID
  timeout: 5                # 超时时间(秒)
```

## 项目结构

```
hvac/
├── hvac-backend/          # 后端服务
│   ├── hvac_backend/      # Python 包
│   │   ├── main.py        # FastAPI 应用
│   │   ├── modbus_client.py   # Modbus 客户端
│   │   ├── router.py      # API 路由
│   │   └── state.py       # 应用状态
│   └── config.yaml        # 配置文件
├── hvac-web/              # 前端服务
│   └── src/
│       ├── components/    # React 组件
│       ├── hooks/         # 自定义 Hooks
│       └── services/      # API 服务
└── start.sh               # 启动脚本
```

## 房间配置

系统支持 4 个房间：
- 客厅 (living_room)
- 主卧 (master_bedroom)
- 次卧 (second_bedroom)
- 书房 (study_room)
