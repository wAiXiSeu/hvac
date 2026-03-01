# Home Assistant HACS 集成设计文档

## 架构概览

```
┌─────────────────────────────────────────────────────────────┐
│                    Home Assistant                            │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              custom_components/hvac_modbus          │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐          │    │
│  │  │ Climate  │  │ Sensor   │  │ Switch   │          │    │
│  │  │  (4个)   │  │  (18个)  │  │  (4个)   │          │    │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘          │    │
│  │       │             │             │                 │    │
│  │  ┌────┴─────────────┴─────────────┴────┐           │    │
│  │  │           Coordinator                │           │    │
│  │  │         (30秒轮询更新)               │           │    │
│  │  └────────────────┬────────────────────┘           │    │
│  │                   │                                 │    │
│  │  ┌────────────────┴────────────────────┐           │    │
│  │  │           HVACApiClient             │           │    │
│  │  │         (aiohttp 异步请求)          │           │    │
│  │  └────────────────┬────────────────────┘           │    │
│  └───────────────────┼───────────────────────────────┘    │
└──────────────────────┼────────────────────────────────────┘
                       │ HTTP API
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              HVAC Backend (FastAPI)                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ /api/rooms   │  │ /api/system  │  │ /api/status  │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└──────────────────────┬──────────────────────────────────────┘
                       │ Modbus TCP
                       ▼
              ┌─────────────────┐
              │   HVAC 设备     │
              └─────────────────┘
```

## 目录结构

```
custom_components/hvac_modbus/
├── __init__.py          # 集成入口，setup_entry/unload_entry
├── manifest.json        # 集成元数据（HACS 必需）
├── config_flow.py       # UI 配置流程
├── const.py             # 常量定义
├── api.py               # API 客户端（异步 HTTP 请求）
├── coordinator.py       # 数据协调器（统一轮询）
├── climate.py           # Climate 平台（恒温器实体）
├── sensor.py            # Sensor 平台（传感器实体）
├── switch.py            # Switch 平台（开关实体）
├── select.py            # Select 平台（选择器实体）
└── number.py            # Number 平台（数值实体）
```

## 核心组件设计

### 1. manifest.json

```json
{
  "domain": "hvac_modbus",
  "name": "HVAC Modbus",
  "version": "1.0.0",
  "documentation": "https://github.com/user/hvac",
  "dependencies": [],
  "codeowners": ["@user"],
  "requirements": ["aiohttp>=3.8.0"],
  "iot_class": "local_polling",
  "config_flow": true
}
```

### 2. API 客户端 (api.py)

负责与后端 HTTP API 通信：

```python
class HVACApiClient:
    async def get_rooms() -> list[dict]      # GET /api/rooms
    async def set_room_setpoint(room_id, temp)  # PUT /api/rooms/{id}
    async def get_system() -> dict           # GET /api/system
    async def set_system(power, home_mode, run_mode, fan_speed)  # PUT /api/system
    async def get_grouped_registers() -> dict  # GET /api/registers/grouped
    async def get_status() -> dict           # GET /api/status
```

### 3. 数据协调器 (coordinator.py)

使用 `DataUpdateCoordinator` 统一管理数据轮询：

```python
class HVACDataCoordinator(DataUpdateCoordinator):
    scan_interval = 30  # 30秒轮询
    
    async def _async_update_data():
        # 并行获取所有数据
        rooms = await api.get_rooms()
        system = await api.get_system()
        registers = await api.get_grouped_registers()
        return {
            "rooms": rooms,
            "system": system,
            "registers": registers
        }
```

### 4. 配置流程 (config_flow.py)

UI 配置界面，用户输入：
- 后端 URL（默认 `http://localhost:8000`）
- 可选 API Key
- 轮询间隔（默认 30 秒）

## 实体详细设计

### Climate 实体（4个）

| 实体 ID | 名称 | 当前温度 | 目标温度 | 支持操作 |
|---------|------|----------|----------|----------|
| climate.living_room | 客厅 | room.temp | room.setpoint | 设定温度 |
| climate.master_bedroom | 主卧 | room.temp | room.setpoint | 设定温度 |
| climate.second_bedroom | 次卧 | room.temp | room.setpoint | 设定温度 |
| climate.study_room | 书房 | room.temp | room.setpoint | 设定温度 |

**Climate 实体属性：**
- `current_temperature`: 当前温度
- `target_temperature`: 目标温度
- `target_temperature_step`: 0.5
- `min_temp`: 16
- `max_temp`: 30
- `hvac_modes`: ["off", "heat", "cool"]（仅显示，实际由系统控制）
- `preset_modes`: ["home", "away"]

### Sensor 实体（18个）

**环境监测（4个）**
| 实体 ID | 名称 | 单位 | 设备类 |
|---------|------|------|--------|
| sensor.indoor_pm25 | 室内 PM2.5 | μg/m³ | pm25 |
| sensor.indoor_co2 | 室内 CO2 | ppm | carbon_dioxide |
| sensor.outdoor_temperature | 室外温度 | °C | temperature |
| sensor.outdoor_humidity | 室外湿度 | % | humidity |

**房间传感器（12个）**
每个房间 3 个传感器：
- `sensor.{room}_temperature` - 当前温度
- `sensor.{room}_humidity` - 当前湿度
- `sensor.{room}_dew_point` - 露点温度

**约克主机（2个）**
| 实体 ID | 名称 | 单位 |
|---------|------|------|
| sensor.york_supply_temp | 约克供水温度 | °C |
| sensor.york_return_temp | 约克回水温度 | °C |

**新风系统（4个）**
| 实体 ID | 名称 | 单位 |
|---------|------|------|
| sensor.fresh_air_compressor_freq | 压缩机频率 | Hz |
| sensor.fresh_air_supply_temp | 供水温度 | °C |
| sensor.fresh_air_return_temp | 回水温度 | °C |
| sensor.fresh_air_status | 状态码 | - |

### Switch 实体（4个）

| 实体 ID | 名称 | API 映射 |
|---------|------|----------|
| switch.hvac_power | 系统电源 | system.power |
| switch.home_mode | 在家模式 | system.home_mode |
| switch.kitchen_radiant | 厨卫辐射 | registers[1133] |
| switch.humidifier | 加湿功能 | registers[1168] |

### Select 实体（1个）

| 实体 ID | 名称 | 选项 |
|---------|------|------|
| select.run_mode | 运行模式 | 制冷, 制热, 通风, 除湿 |

**选项映射：**
- 制冷 → 1
- 制热 → 2
- 通风 → 3
- 除湿 → 4

### Number 实体（3个）

| 实体 ID | 名称 | 范围 | 步进 | API 映射 |
|---------|------|------|------|----------|
| number.fan_speed | 新风风速 | 0-100 | 5 | system.fan_speed |
| number.heating_setpoint | 制热设定点 | 30-60 | 0.5 | registers[1062] |
| number.cooling_setpoint | 制冷设定点 | 5-30 | 0.5 | registers[1066] |

## 配置流程设计

1. 用户在 HA 中添加集成
2. 显示配置表单：
   - 后端 URL（必填，默认 `http://localhost:8000`）
   - API Key（可选）
   - 轮询间隔（可选，默认 30 秒）
3. 测试连接
4. 连接成功后创建条目
5. 自动创建所有实体

## 数据流

```
1. HA 启动
   └→ setup_entry()
      └→ 创建 HVACApiClient
      └→ 创建 HVACDataCoordinator
      └→ 首次获取数据
      └→ 注册平台（climate, sensor, switch, select, number）

2. 轮询更新（每30秒）
   └→ coordinator.async_refresh()
      └→ api.get_rooms()
      └→ api.get_system()
      └→ api.get_grouped_registers()
      └→ 更新 coordinator.data
      └→ 触发实体状态更新

3. 用户控制
   └→ 实体方法调用（如 set_temperature）
      └→ api.set_room_setpoint()
      └→ 等待下次轮询更新状态
      └→ 或立即本地更新（乐观更新）
```

## 错误处理

1. **连接失败**：设置连接状态传感器为 `disconnected`，实体状态为 `unavailable`
2. **API 错误**：记录日志，返回默认值，不阻塞其他功能
3. **超时处理**：设置 10 秒超时，超时后重试 3 次

## HACS 发布配置

仓库根目录需要 `hacs.json`：

```json
{
  "name": "HVAC Modbus Integration",
  "content_in_root": false,
  "zip_release": true,
  "filename": "hvac_modbus.zip"
}
```

## 依赖项

- Python >= 3.10
- Home Assistant >= 2023.1
- aiohttp >= 3.8.0
