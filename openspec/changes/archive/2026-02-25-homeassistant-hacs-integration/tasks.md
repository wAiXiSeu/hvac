# Home Assistant HACS 集成任务清单

## 准备工作

- [x] 创建 OpenSpec 提案文件
- [x] 创建设计文档

## 实现任务

### 阶段 1：基础文件（预估 0.5 小时）

- [x] 1.1 创建集成目录 `custom_components/hvac_modbus/`
- [x] 1.2 创建 `manifest.json` - 集成元数据
- [x] 1.3 创建 `const.py` - 常量定义

### 阶段 2：API 层（预估 1 小时）

- [x] 2.1 创建 `api.py` - HVACApiClient 类
  - [x] 2.1.1 实现 `__init__` 和会话管理
  - [x] 2.1.2 实现 `get_rooms()` 方法
  - [x] 2.1.3 实现 `set_room_setpoint()` 方法
  - [x] 2.1.4 实现 `get_system()` 方法
  - [x] 2.1.5 实现 `set_system()` 方法
  - [x] 2.1.6 实现 `get_grouped_registers()` 方法
  - [x] 2.1.7 实现 `get_status()` 方法
  - [x] 2.1.8 添加错误处理和重试逻辑

### 阶段 3：数据协调器（预估 0.5 小时）

- [x] 3.1 创建 `coordinator.py` - HVACDataCoordinator 类
  - [x] 3.1.1 继承 DataUpdateCoordinator
  - [x] 3.1.2 实现 `_async_update_data()` 方法
  - [x] 3.1.3 设置 30 秒轮询间隔
  - [x] 3.1.4 添加连接状态管理

### 阶段 4：配置流程（预估 1 小时）

- [x] 4.1 创建 `config_flow.py`
  - [x] 4.1.1 实现 `ConfigFlow` 类
  - [x] 4.1.2 实现配置表单（Step 1：用户输入）
  - [x] 4.1.3 实现连接测试（`async_validate_input`）
  - [x] 4.1.4 实现配置保存
  - [x] 4.1.5 实现 `OptionsFlowHandler`（可选）

### 阶段 5：入口文件（预估 0.5 小时）

- [x] 5.1 创建 `__init__.py`
  - [x] 5.1.1 实现 `async_setup_entry()`
  - [x] 5.1.2 实现 `async_unload_entry()`
  - [x] 5.1.3 创建 coordinator 和 api 实例
  - [x] 5.1.4 注册平台

### 阶段 6：Climate 平台（预估 1.5 小时）

- [x] 6.1 创建 `climate.py`
  - [x] 6.1.1 实现 `async_setup_platform()`
  - [x] 6.1.2 创建 `HVACRoomClimate` 实体类
  - [x] 6.1.3 实现 `current_temperature` 属性
  - [x] 6.1.4 实现 `target_temperature` 属性
  - [x] 6.1.5 实现 `async_set_temperature()` 方法
  - [x] 6.1.6 实现 `hvac_modes` 属性
  - [x] 6.1.7 实现 `preset_modes` 属性
  - [x] 6.1.8 为 4 个房间创建实体

### 阶段 7：Sensor 平台（预估 2 小时）

- [x] 7.1 创建 `sensor.py`
  - [x] 7.1.1 实现 `async_setup_platform()`
  - [x] 7.1.2 创建基础 `HVACSensor` 实体类
  - [x] 7.1.3 创建环境传感器实体（4个）
  - [x] 7.1.4 创建房间温度传感器实体（4个）
  - [x] 7.1.5 创建房间湿度传感器实体（4个）
  - [x] 7.1.6 创建房间露点传感器实体（4个）
  - [x] 7.1.7 创建约克主机传感器实体（2个）
  - [x] 7.1.8 创建新风系统传感器实体（4个）
  - [x] 7.1.9 创建连接状态传感器实体（1个）

### 阶段 8：Switch 平台（预估 1 小时）

- [x] 8.1 创建 `switch.py`
  - [x] 8.1.1 实现 `async_setup_platform()`
  - [x] 8.1.2 创建 `HVACSwitch` 实体类
  - [x] 8.1.3 实现 `is_on` 属性
  - [x] 8.1.4 实现 `async_turn_on()` 方法
  - [x] 8.1.5 实现 `async_turn_off()` 方法
  - [x] 8.1.6 创建系统电源开关实体
  - [x] 8.1.7 创建在家模式开关实体
  - [x] 8.1.8 创建厨卫辐射开关实体
  - [x] 8.1.9 创建加湿功能开关实体

### 阶段 9：Select 平台（预估 0.5 小时）

- [x] 9.1 创建 `select.py`
  - [x] 9.1.1 实现 `async_setup_platform()`
  - [x] 9.1.2 创建 `RunModeSelect` 实体类
  - [x] 9.1.3 实现 `current_option` 属性
  - [x] 9.1.4 实现 `async_select_option()` 方法
  - [x] 9.1.5 实现 `options` 属性

### 阶段 10：Number 平台（预估 1 小时）

- [x] 10.1 创建 `number.py`
  - [x] 10.1.1 实现 `async_setup_platform()`
  - [x] 10.1.2 创建 `HVACNumber` 实体类
  - [x] 10.1.3 实现 `native_value` 属性
  - [x] 10.1.4 实现 `async_set_native_value()` 方法
  - [x] 10.1.5 创建新风风速实体
  - [x] 10.1.6 创建制热设定点实体
  - [x] 10.1.7 创建制冷设定点实体

### 阶段 11：后端 API 扩展（预估 0.5 小时）

- [ ] 11.1 扩展后端 API（如需要）
  - [ ] 11.1.1 添加 `/api/york` 端点
  - [ ] 11.1.2 添加 `/api/kitchen` 端点
  - [ ] 11.1.3 添加 `/api/fresh-air` 端点

### 阶段 12：测试与验证（预估 2 小时）

- [ ] 12.1 单元测试
  - [ ] 12.1.1 API 客户端测试
  - [ ] 12.1.2 实体状态测试
- [ ] 12.2 集成测试
  - [ ] 12.2.1 配置流程测试
  - [ ] 12.2.2 数据更新测试
  - [ ] 12.2.3 控制命令测试
- [ ] 12.3 手动测试
  - [ ] 12.3.1 安装集成
  - [ ] 12.3.2 验证所有实体
  - [ ] 12.3.3 验证控制功能

### 阶段 13：HACS 发布准备（预估 0.5 小时）

- [ ] 13.1 创建 `hacs.json` 文件
- [ ] 13.2 创建 GitHub Release
- [ ] 13.3 更新主 README 添加安装说明

## 任务统计

- **已完成**: 56/72 任务
- **剩余**: 16 任务（阶段 11-13）
- **核心文件**: 11 个（已全部创建）

## 依赖关系

```
阶段 1 (基础) → 阶段 2 (API) → 阶段 3 (Coordinator) → 阶段 4 (Config Flow) → 阶段 5 (入口) ✓
                                                                                    ↓
                              阶段 6-10 (实体平台) ←─────────────────────────────────── ✓
                                                                                    ↓
                              阶段 11 (后端扩展) → 阶段 12 (测试) → 阶段 13 (HACS)
```
