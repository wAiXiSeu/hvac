## Why

三恒系统（恒温、恒湿、恒氧）是提升居住舒适度的核心系统，但目前缺乏本地化的管理控制界面。现有方案通常依赖云端平台，存在网络依赖、数据隐私和响应延迟等问题。开发一个本地 Web 控制界面，可以实现对三恒系统的直接控制，提升用户体验，同时为后续高级功能（如智能控制、能耗优化）奠定基础。

## What Changes

- 新增三恒系统本地控制系统（基础版）
- 实现 Modbus TCP 协议通信，支持连接配置
- 提供本地 Web 界面（React + FastAPI）
- 支持系统开关、模式切换、风速调节等核心控制功能
- 支持多房间温度设定与监控

## Capabilities

### New Capabilities

- `hvac-connection-management`: Modbus TCP 连接配置与状态监控
- `hvac-environment-monitoring`: 室内环境数据采集与显示（PM2.5、CO2、温湿度）
- `hvac-system-control`: 主机控制功能（开关机、运行模式、风速设定）
- `hvac-room-control`: 分房间温度控制与状态监控
- `hvac-data-panel`: 实时数据面板展示

### Modified Capabilities

（无 - 全新功能）

## Impact

- 新增前端项目：`hvac-web`（React）
- 新增后端项目：`hvac-backend`（Python + FastAPI）
- 依赖库：pymodbus、FastAPI、React 等
- 目标部署环境：本地局域网（树莓派/服务器）
