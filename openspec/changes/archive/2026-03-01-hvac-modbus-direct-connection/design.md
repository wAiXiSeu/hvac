# HVAC Modbus 直连重构设计

## 架构变更

### 当前架构

```
┌─────────────────┐     HTTP      ┌─────────────────┐    Modbus    ┌─────────────┐
│ Home Assistant  │ ───────────→ │  FastAPI 后端   │ ──────────→ │ Modbus 设备 │
│ HACS 集成       │   :8000       │  pymodbus       │    :502      │ 192.168.x.x │
└─────────────────┘               └─────────────────┘              └─────────────┘
```

### 目标架构

```
┌─────────────────────────────────────────┐    Modbus    ┌─────────────┐
│ Home Assistant                          │ ──────────→ │ Modbus 设备 │
│ └── HACS 集成 (内置 pymodbus 客户端)    │    :502      │ 192.168.x.x │
└─────────────────────────────────────────┘              └─────────────┘
```

## 组件设计

### 1. Modbus 客户端 (modbus.py)

```python
class HVACModbusClient:
    """异步 Modbus TCP 客户端"""
    
    def __init__(self, host: str, port: int, slave_id: int):
        self._host = host
        self._port = port
        self._slave_id = slave_id
        self._client: AsyncModbusTcpClient | None = None
    
    async def connect(self) -> bool:
        """建立 Modbus 连接"""
        
    async def disconnect(self) -> None:
        """断开连接"""
        
    async def read_registers(self, address: int, count: int) -> list[int]:
        """读取保持寄存器"""
        
    async def write_register(self, address: int, value: int) -> bool:
        """写入单个寄存器"""
        
    async def read_all_data(self) -> dict:
        """读取所有寄存器数据，返回结构化数据"""
```

### 2. 数据协调器 (coordinator.py)

```python
class HVACDataCoordinator(DataUpdateCoordinator):
    """直接使用 Modbus 客户端获取数据"""
    
    def __init__(self, hass, modbus_client: HVACModbusClient):
        self.modbus = modbus_client
        
    async def _async_update_data(self) -> dict:
        # 直接通过 Modbus 读取寄存器
        raw_data = await self.modbus.read_all_data()
        # 解析为房间/系统/环境数据
        return self._parse_data(raw_data)
```

### 3. 配置流程 (config_flow.py)

```python
CONFIG_SCHEMA = vol.Schema({
    vol.Required(CONF_HOST, default="192.168.110.200"): str,
    vol.Required(CONF_PORT, default=502): int,
    vol.Required(CONF_SLAVE_ID, default=1): int,
    vol.Optional(CONF_SCAN_INTERVAL, default=30): int,
})
```

## 文件变更

| 文件 | 操作 | 说明 |
|------|------|------|
| `manifest.json` | 修改 | requirements: aiohttp → pymodbus |
| `const.py` | 修改 | 添加 Modbus 配置常量 |
| `registers.py` | 新增 | 从后端迁移寄存器定义 |
| `modbus.py` | 新增 | 异步 Modbus 客户端 |
| `coordinator.py` | 重写 | 使用 Modbus 直接读取 |
| `config_flow.py` | 修改 | Modbus 参数配置 |
| `__init__.py` | 修改 | 初始化 Modbus 客户端 |
| `climate.py` | 修改 | 写入方法改用 Modbus |
| `sensor.py` | 修改 | 数据源切换 |
| `switch.py` | 修改 | 写入方法改用 Modbus |
| `select.py` | 修改 | 写入方法改用 Modbus |
| `number.py` | 修改 | 写入方法改用 Modbus |
| `api.py` | 删除 | 不再需要 HTTP 客户端 |

## 寄存器读取策略

### 批量读取

为提高效率，按地址范围批量读取：

```python
REGISTER_RANGES = [
    (1024, 10),   # 环境区: 1024-1033
    (1033, 20),   # 系统控制区: 1033-1052
    (1062, 10),   # 约克主机区: 1062-1071
    (1085, 40),   # 房间区: 1085-1124
    (1133, 2),    # 厨卫区: 1133-1134
    (1161, 10),   # 新风区: 1161-1170
]
```

### 数据解析

```python
def parse_register_value(address: int, raw_value: int) -> float:
    """根据寄存器定义解析原始值"""
    reg_info = REGISTERS.get(address)
    if reg_info:
        return raw_value * reg_info.get("scaling", 1)
    return raw_value
```

## 数据流

```
┌────────────────────────────────────────────────────────────────┐
│ HVACDataCoordinator._async_update_data()                       │
│   │                                                            │
│   ├─→ modbus.read_registers(1024, 10)  # 环境数据              │
│   ├─→ modbus.read_registers(1033, 20)  # 系统控制              │
│   ├─→ modbus.read_registers(1085, 40)  # 房间数据              │
│   │                                                            │
│   └─→ _parse_data(raw_data) → {                                │
│         "rooms": [...],                                        │
│         "system": {...},                                       │
│         "environment": {...},                                  │
│         "connected": True                                      │
│       }                                                        │
└────────────────────────────────────────────────────────────────┘
                           ↓
┌────────────────────────────────────────────────────────────────┐
│ Entities (Climate, Sensor, Switch, etc.)                       │
│   │                                                            │
│   ├─→ coordinator.data["rooms"][0]["temp"]     # 读取数据      │
│   │                                                            │
│   └─→ coordinator.modbus.write_register(1090, 42)  # 写入控制  │
│       coordinator.async_request_refresh()                      │
└────────────────────────────────────────────────────────────────┘
```

## 错误处理

```python
class HVACModbusClient:
    async def read_registers(self, address, count):
        try:
            result = await self._client.read_holding_registers(
                address, count, slave=self._slave_id
            )
            if result.isError():
                _LOGGER.error("Modbus read error: %s", result)
                return None
            return list(result.registers)
        except ModbusException as err:
            _LOGGER.error("Modbus exception: %s", err)
            await self._reconnect()
            return None
```

## 测试计划

1. **连接测试**: 验证 Modbus 连接建立
2. **读取测试**: 验证所有寄存器可读
3. **写入测试**: 验证温度设定、开关控制
4. **重连测试**: 模拟断线后自动重连
5. **实体测试**: 验证所有 30 个实体正常工作
