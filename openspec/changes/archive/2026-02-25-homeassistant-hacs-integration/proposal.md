# Home Assistant HACS 集成

## 概述

为 HVAC 暖通空调系统开发一个 Home Assistant 自定义集成，支持通过 HACS (Home Assistant Community Store) 安装。用户可以在 Home Assistant 中查看和控制所有 HVAC 设备。

## 动机

### 问题
- 当前 HVAC 系统只能通过专用的 Web 界面访问
- 无法与智能家居平台集成
- 用户无法在统一的智能家居界面中管理 HVAC 系统

### 解决方案
开发 Home Assistant 集成，通过 HTTP API 连接现有后端服务，实现：
- 温度监控和控制
- 湿度、露点温度监测
- 系统电源、运行模式控制
- 新风系统控制
- 环境数据监测（PM2.5、CO2）

## 范围

### 包含
- Climate 实体（4个房间恒温器）
- Sensor 实体（环境、房间、约克主机、新风系统传感器）
- Switch 实体（系统电源、在家模式、厨卫辐射、加湿功能）
- Select 实体（运行模式选择）
- Number 实体（风速、设定点控制）
- UI 配置流程（Config Flow）
- HACS 发布支持

### 不包含
- 直接 Modbus 连接（通过后端 API 代理）
- Home Assistant 自动化脚本
- Lovelace 面板卡片

## 目标用户

- 已有 Home Assistant 智能家居的用户
- 希望在统一界面管理 HVAC 系统的用户
- 需要智能家居自动化的用户

## 成功标准

1. 用户可通过 HACS 安装集成
2. 配置后自动发现并创建所有实体
3. 实体状态实时更新（30秒轮询）
4. 控制命令响应正确
5. 连接断开后自动重连

## 技术方案

采用 HTTP API 连接现有后端：
- 后端地址：`http://localhost:8000`
- API 端点：`/api/rooms`, `/api/system`, `/api/registers/grouped`
- 认证：可选 API Key

## 风险与缓解

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| 后端服务不可用 | 集成无法使用 | 添加连接状态传感器，断线提示 |
| API 接口变更 | 实体失效 | 版本化 API，向后兼容 |
| 网络延迟 | 控制响应慢 | 异步请求，超时处理 |

## 相关资源

- 现有后端 API 文档：`/hvac-backend/hvac_backend/router.py`
- 寄存器定义：`/hvac-backend/hvac_backend/registers.py`
- Home Assistant 集成开发文档：https://developers.home-assistant.io/
