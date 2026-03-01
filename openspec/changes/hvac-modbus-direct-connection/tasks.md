# HVAC Modbus 直连重构任务清单

## 准备工作

- [x] 创建 OpenSpec 提案文件
- [x] 创建设计文档

## 实现任务

### 阶段 1：基础设施更新（预估 0.5 小时）

- [x] 1.1 更新 `manifest.json`
  - [x] 1.1.1 将 requirements 从 `aiohttp>=3.8.0` 改为 `pymodbus>=3.5.0`
  - [x] 1.1.2 更新版本号为 2.0.0
- [x] 1.2 更新 `const.py`
  - [x] 1.2.1 添加 `CONF_SLAVE_ID` 常量
  - [x] 1.2.2 添加 `DEFAULT_MODBUS_PORT = 502`
  - [x] 1.2.3 移除 HTTP API 相关常量
- [x] 1.3 创建 `registers.py`
  - [x] 1.3.1 从后端迁移 REGISTERS 字典
  - [x] 1.3.2 从后端迁移 ROOMS 配置
  - [x] 1.3.3 从后端迁移 scale_value/unscale_value 函数

### 阶段 2：Modbus 客户端（预估 1.5 小时）

- [x] 2.1 创建 `modbus.py`
  - [x] 2.1.1 实现 `HVACModbusClient` 类初始化
  - [x] 2.1.2 实现 `connect()` 方法 - 使用 AsyncModbusTcpClient
  - [x] 2.1.3 实现 `disconnect()` 方法
  - [x] 2.1.4 实现 `is_connected` 属性
  - [x] 2.1.5 实现 `read_registers()` 方法
  - [x] 2.1.6 实现 `write_register()` 方法
  - [x] 2.1.7 实现 `read_all_data()` 方法 - 批量读取所有寄存器
  - [x] 2.1.8 添加自动重连逻辑
  - [x] 2.1.9 添加错误处理和日志

### 阶段 3：配置流程更新（预估 0.5 小时）

- [x] 3.1 修改 `config_flow.py`
  - [x] 3.1.1 更新配置表单：host, port, slave_id, scan_interval
  - [x] 3.1.2 实现 `_test_modbus_connection()` 方法
  - [x] 3.1.3 移除 HTTP API 测试逻辑
  - [x] 3.1.4 更新默认值（port: 502）

### 阶段 4：数据协调器重写（预估 1 小时）

- [x] 4.1 重写 `coordinator.py`
  - [x] 4.1.1 修改构造函数，接收 `HVACModbusClient`
  - [x] 4.1.2 重写 `_async_update_data()` - 直接读取 Modbus
  - [x] 4.1.3 实现 `_parse_rooms_data()` - 解析房间数据
  - [x] 4.1.4 实现 `_parse_system_data()` - 解析系统数据
  - [x] 4.1.5 实现 `_parse_environment_data()` - 解析环境数据
  - [x] 4.1.6 保持现有数据访问接口（get_room_data, get_system_data 等）

### 阶段 5：入口文件更新（预估 0.5 小时）

- [x] 5.1 修改 `__init__.py`
  - [x] 5.1.1 创建 `HVACModbusClient` 实例
  - [x] 5.1.2 建立 Modbus 连接
  - [x] 5.1.3 在 `async_unload_entry` 中断开连接
  - [x] 5.1.4 移除 API 客户端相关代码

### 阶段 6：实体平台更新（预估 1.5 小时）

- [x] 6.1 修改 `climate.py`
  - [x] 6.1.1 更新 `async_set_temperature()` - 使用 Modbus 写入
  - [x] 6.1.2 更新数据读取方式
- [x] 6.2 修改 `sensor.py`
  - [x] 6.2.1 更新数据读取方式
  - [x] 6.2.2 简化传感器值获取逻辑
- [x] 6.3 修改 `switch.py`
  - [x] 6.3.1 更新 `async_turn_on()` - 使用 Modbus 写入
  - [x] 6.3.2 更新 `async_turn_off()` - 使用 Modbus 写入
- [x] 6.4 修改 `select.py`
  - [x] 6.4.1 更新 `async_select_option()` - 使用 Modbus 写入
- [x] 6.5 修改 `number.py`
  - [x] 6.5.1 更新 `async_set_native_value()` - 使用 Modbus 写入

### 阶段 7：清理和文档（预估 0.5 小时）

- [x] 7.1 删除 `api.py`
- [x] 7.2 更新 README.md
  - [x] 7.2.1 更新安装说明
  - [x] 7.2.2 更新配置说明（Modbus 参数）
  - [x] 7.2.3 移除后端相关说明

### 阶段 8：本地测试（预估 1 小时）

- [x] 8.1 部署到本地 Docker HA
  - [x] 8.1.1 复制集成到 custom_components
  - [x] 8.1.2 重启 HA 容器
- [x] 8.2 功能验证
  - [x] 8.2.1 测试集成加载正常
  - [x] 8.2.2 测试配置迁移正常
  - [x] 8.2.3 测试 Modbus 连接逻辑正常
  - [ ] 8.2.4 验证所有传感器数据（需连接真实设备）
  - [ ] 8.2.5 验证恒温器控制（需连接真实设备）
  - [ ] 8.2.6 验证开关控制（需连接真实设备）
  - [ ] 8.2.7 验证模式选择（需连接真实设备）
  - [ ] 8.2.8 验证数值设定（需连接真实设备）

## 任务统计

- **总任务数**: 45
- **预估总时长**: 7 小时

## 依赖关系

```
阶段 1 (基础设施) 
    ↓
阶段 2 (Modbus 客户端) 
    ↓
阶段 3 (配置流程) → 阶段 4 (协调器) → 阶段 5 (入口)
                                          ↓
                                    阶段 6 (实体平台)
                                          ↓
                                    阶段 7 (清理) → 阶段 8 (测试)
```

## 验收标准

1. 集成可在无后端情况下独立运行
2. 所有 30 个实体正常工作
3. 读取和写入功能正常
4. 配置流程友好，支持 Modbus 参数
5. 错误处理完善，支持自动重连
