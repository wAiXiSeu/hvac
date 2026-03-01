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
├── custom_components/     # Home Assistant 集成
│   └── hvac_modbus/       # HACS 自定义集成
└── start.sh               # 启动脚本
```

## 房间配置

系统支持 4 个房间：
- 客厅 (living_room)
- 主卧 (master_bedroom)
- 次卧 (second_bedroom)
- 书房 (study_room)

## Home Assistant 集成

通过 HACS 安装自定义集成，可在 Home Assistant 中直接通过 Modbus TCP 控制 HVAC 系统（无需独立后端服务）。

### 架构说明

集成直接通过 Modbus TCP 协议与 HVAC 设备通信，无需运行独立的后端服务。

```
Home Assistant --> Modbus TCP --> HVAC 设备 (192.168.110.200:502)
```

### 安装方式

#### 方式一：手动安装

1. 将 `custom_components/hvac_modbus` 目录复制到 Home Assistant 的 `custom_components` 目录下：
   ```bash
   cp -r custom_components/hvac_modbus /path/to/homeassistant/custom_components/
   ```

2. 重启 Home Assistant

#### 方式二：HACS 安装

1. 打开 Home Assistant，进入 **HACS** > **集成**
2. 点击右上角 **⋮** 菜单，选择 **自定义仓库**
3. 添加仓库：
   - 仓库 URL：`https://github.com/wAiXiSeu/hvac`
   - 类别：选择 **Integration**
4. 点击 **添加**，等待仓库加载完成
5. 在 HACS 集成列表中找到 **HVAC Modbus**，点击 **下载**
6. 下载完成后重启 Home Assistant

### 配置集成

1. 进入 **设置** > **设备与服务** > **添加集成**
2. 搜索 "HVAC Modbus"
3. 输入 Modbus 设备连接参数：
   - 主机：Modbus 设备 IP（默认 `192.168.110.200`）
   - 端口：Modbus 端口（默认 `502`）
   - 从机 ID：Modbus 从机 ID（默认 `1`）
   - 扫描间隔：数据刷新间隔（默认 `30` 秒）
4. 点击提交完成配置

### 提供的实体

#### Climate 恒温器（4个）
| 实体 ID | 名称 | 功能 |
|---------|------|------|
| climate.hvac_living_room | 客厅恒温器 | 温度显示与设定 |
| climate.hvac_master_bedroom | 主卧恒温器 | 温度显示与设定 |
| climate.hvac_second_bedroom | 次卧恒温器 | 温度显示与设定 |
| climate.hvac_study_room | 书房恒温器 | 温度显示与设定 |

#### Sensor 传感器（18个）
- **环境监测**：PM2.5、CO2、室外温度、室外湿度
- **房间传感器**：每个房间的温度、湿度、露点温度
- **约克主机**：供水温度、回水温度
- **新风系统**：压缩机频率、供水温、回水温
- **连接状态**：HVAC 连接状态

#### Switch 开关（4个）
- 系统电源
- 在家模式
- 厨卫辐射
- 加湿功能

#### Select 选择器（1个）
- 运行模式（制冷/制热/通风/除湿）

#### Number 数值（3个）
- 新风风速（0-100%）
- 制热供水设定点
- 制冷供水设定点

### 温度单位设置

集成默认使用摄氏度（°C）。如果 Home Assistant 显示华氏度（°F），请修改全局设置：

1. 进入 **设置** > **一般设置**
2. 找到 **单位系统**
3. 选择 **公制** 或将温度单位改为 **摄氏度**

或在 `configuration.yaml` 中添加：
```yaml
homeassistant:
  unit_system: metric
```

### 控制操作说明

#### 恒温器控制

每个房间的恒温器支持：
- **查看当前温度**：显示房间实时温度
- **设定目标温度**：点击 +/- 按钮或拖动滑块调整
- **切换模式**：选择制热、制冷或关闭
- **预设模式**：在家模式 / 离家模式

#### 系统开关

| 开关 | 功能 | 说明 |
|------|------|------|
| 系统电源 | 总开关 | 关闭后整个系统停止运行 |
| 在家模式 | 模式切换 | 离家时关闭可节能 |
| 厨卫辐射 | 厨卫地暖 | 控制厨房卫生间辐射供暖 |
| 加湿功能 | 加湿器 | 控制新风加湿功能 |

#### 运行模式

| 模式 | 说明 |
|------|------|
| 制冷 | 夏季制冷模式 |
| 制热 | 冬季制热模式 |
| 通风 | 仅通风不调温 |
| 除湿 | 除湿模式 |

### Dashboard 配置示例

#### 添加恒温器卡片

```yaml
type: thermostat
entity: climate.hvac_living_room
name: 客厅恒温器
```

#### 添加传感器卡片

```yaml
type: glance
title: 室内环境
entities:
  - entity: sensor.hvac_living_room_temp
    name: 客厅温度
  - entity: sensor.hvac_living_room_humidity
    name: 客厅湿度
  - entity: sensor.hvac_env_indoor_pm25
    name: PM2.5
  - entity: sensor.hvac_env_indoor_co2
    name: CO2
```

#### 添加控制面板

```yaml
type: entities
title: HVAC 控制
entities:
  - entity: switch.hvac_system_power
    name: 系统电源
  - entity: switch.hvac_home_mode
    name: 在家模式
  - entity: select.hvac_run_mode
    name: 运行模式
  - entity: number.hvac_fan_speed
    name: 新风风速
```

### 实体完整列表

#### Climate 恒温器

| 实体 ID | 名称 |
|---------|------|
| climate.hvac_living_room | 客厅恒温器 |
| climate.hvac_master_bedroom | 主卧恒温器 |
| climate.hvac_second_bedroom | 次卧恒温器 |
| climate.hvac_study_room | 书房恒温器 |

#### Sensor 传感器

| 实体 ID | 名称 |
|---------|------|
| sensor.hvac_env_indoor_pm25 | 室内 PM2.5 |
| sensor.hvac_env_indoor_co2 | 室内 CO2 |
| sensor.hvac_env_outdoor_temp | 室外温度 |
| sensor.hvac_env_outdoor_humidity | 室外湿度 |
| sensor.hvac_living_room_temp | 客厅温度 |
| sensor.hvac_living_room_humidity | 客厅湿度 |
| sensor.hvac_living_room_dew_point | 客厅露点 |
| sensor.hvac_master_bedroom_temp | 主卧温度 |
| sensor.hvac_master_bedroom_humidity | 主卧湿度 |
| sensor.hvac_master_bedroom_dew_point | 主卧露点 |
| sensor.hvac_second_bedroom_temp | 次卧温度 |
| sensor.hvac_second_bedroom_humidity | 次卧湿度 |
| sensor.hvac_second_bedroom_dew_point | 次卧露点 |
| sensor.hvac_study_room_temp | 书房温度 |
| sensor.hvac_study_room_humidity | 书房湿度 |
| sensor.hvac_study_room_dew_point | 书房露点 |
| sensor.hvac_york_supply_temp | 约克供水温度 |
| sensor.hvac_york_return_temp | 约克回水温度 |
| sensor.hvac_fresh_air_compressor_freq | 新风压缩机频率 |
| sensor.hvac_fresh_air_supply_temp | 新风供水温度 |
| sensor.hvac_fresh_air_return_temp | 新风回水温度 |
| sensor.hvac_connection_status | HVAC 连接状态 |

#### Switch 开关

| 实体 ID | 名称 |
|---------|------|
| switch.hvac_system_power | 系统电源 |
| switch.hvac_home_mode | 在家模式 |
| switch.hvac_kitchen_radiant | 厨卫辐射 |
| switch.hvac_humidifier | 加湿功能 |

#### Select 选择器

| 实体 ID | 名称 | 选项 |
|---------|------|------|
| select.hvac_run_mode | 运行模式 | 制冷/制热/通风/除湿 |

#### Number 数值

| 实体 ID | 名称 | 范围 |
|---------|------|------|
| number.hvac_fan_speed | 新风风速 | 0-100% |
| number.hvac_heating_setpoint | 制热供水设定点 | 30-60°C |
| number.hvac_cooling_setpoint | 制冷供水设定点 | 5-30°C |

### 本地测试

#### 方式一：Docker 启动 Home Assistant（推荐）

```bash
# 1. 创建配置目录
mkdir -p ~/homeassistant

# 2. 启动 Home Assistant 容器
docker run -d \
  --name homeassistant \
  --privileged \
  --restart=unless-stopped \
  -e TZ=Asia/Shanghai \
  -v ~/homeassistant:/config \
  --network host \
  ghcr.io/home-assistant/home-assistant:stable

# 3. 等待启动完成（约1-2分钟），访问 http://localhost:8123
# 首次访问需要创建管理员账号

# 4. 安装集成（使用符号链接方便开发调试）
mkdir -p ~/homeassistant/custom_components
ln -s $(pwd)/custom_components/hvac_modbus ~/homeassistant/custom_components/hvac_modbus

# 5. 重启容器使集成生效
docker restart homeassistant
```

#### 方式二：使用现有 Home Assistant

```bash
# 复制集成到 HA 配置目录
cp -r custom_components/hvac_modbus /path/to/homeassistant/custom_components/

# 重启 Home Assistant
# HA OS: ha core restart
# Docker: docker restart homeassistant
# venv: sudo systemctl restart home-assistant@homeassistant
```

#### 配置集成

1. 打开 Home Assistant Web 界面（http://localhost:8123）
2. 进入 **设置** > **设备与服务**
3. 点击右下角 **添加集成** 按钮
4. 搜索 "HVAC Modbus"
5. 输入 Modbus 设备地址：
   - 主机：`192.168.110.200`（Modbus 设备 IP）
   - 端口：`502`（Modbus TCP 端口）
   - 从机 ID：`1`
6. 点击提交完成配置

**注意**：使用 `--network host` 模式确保 Docker 容器可以直接访问局域网内的 Modbus 设备。

#### 验证实体

在 HA 中检查：
- **开发者工具** > **状态**：搜索 `hvac` 查看所有实体
- **概览** 页面添加实体卡片验证数据显示

#### 开发调试

查看 Home Assistant 日志：
```bash
# Docker 方式
docker logs homeassistant -f

# HA OS
ha core logs

# venv
journalctl -u home-assistant -f
```

### 使用示例

#### 自动化示例：离家自动关闭

```yaml
automation:
  - alias: "离家关闭HVAC"
    trigger:
      - platform: state
        entity_id: input_boolean.away_mode
        to: "on"
    action:
      - service: switch.turn_off
        target:
          entity_id: switch.hvac_system_power
```

#### 自动化示例：温度过高告警

```yaml
automation:
  - alias: "客厅温度过高告警"
    trigger:
      - platform: numeric_state
        entity_id: sensor.hvac_living_room_temp
        above: 28
    action:
      - service: notify.mobile_app
        data:
          message: "客厅温度过高"
```

### 故障排查

**问题：实体显示 unavailable**
- 检查 Modbus 设备是否在线
- 检查 Home Assistant 能否访问 Modbus 设备 IP
- 查看 Home Assistant 日志中的错误信息

**问题：控制命令无响应**
- 确认 Modbus 设备连接正常
- 检查寄存器地址是否正确
- 查看 Home Assistant 日志中的 Modbus 错误

**问题：Docker 网络无法连接 Modbus 设备**
- 使用 `--network host` 模式运行容器
- 确保容器和 Modbus 设备在同一局域网
- 检查防火墙设置

**问题：集成找不到**
- 确认 custom_components 目录正确
- 确认目录结构为 `custom_components/hvac_modbus/__init__.py`
- 重启 Home Assistant

**问题：配置时连接失败**
- 确认 Modbus 设备 IP 和端口正确
- 检查防火墙是否阻止连接
- 确保从机 ID 设置正确
- 使用 Modbus 测试工具验证连接
