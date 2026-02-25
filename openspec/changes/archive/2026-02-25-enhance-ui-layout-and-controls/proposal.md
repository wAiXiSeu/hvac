## Why

当前 HVAC 系统的 Web UI 页面布局简陋，所有信息混杂在一起，只读数据和可控制操作未分离，用户体验差。需要重构页面布局，按功能区域划分，明确区分监测和控制功能，提升操作效率和界面美观度。

## What Changes

- 重构主页面布局为三大功能区域：系统概览、房间信息、新风系统
- 系统概览区域包含：环境监测（只读）、系统控制（可操作）、约克主机状态（只读）
- 房间信息区域包含：各房间控制面板、厨卫控制面板（可操作）
- 新风系统区域：新风控制面板（可操作）
- 视觉上区分只读数据展示和可控制操作区域（使用不同样式、图标、交互提示）
- 优化卡片式布局，增加响应式设计
- 增强控制操作的交互反馈（加载状态、成功/失败提示）

## Capabilities

### New Capabilities
- `ui-system-overview-panel`: 系统概览区域组件，包含环境监测、系统控制、约克主机三个子面板
- `ui-room-control-enhanced`: 增强的房间控制面板，支持温度、模式、风速等参数控制
- `ui-fresh-air-control`: 新风系统控制面板
- `ui-read-write-separation`: UI 组件层面的只读/可写状态管理和视觉区分

### Modified Capabilities
- `hvac-room-control`: 扩展房间控制功能，增加运行模式和风速控制
- `hvac-environment-monitoring`: 调整环境监测数据展示方式，适配新的布局

## Impact

- 影响前端所有组件：需要重构 `App.jsx`、拆分现有组件
- 新增组件：`SystemOverview.jsx`、`EnvironmentMonitoring.jsx`、`SystemControl.jsx`、`YorkHost.jsx`、`FreshAirControl.jsx`、`RoomControlPanel.jsx`
- 修改现有组件：`RoomCards.jsx` 需要重构为 `RoomControlPanel.jsx`
- 调整 CSS 样式：新增布局样式、控制操作样式、只读展示样式
- 后端 API 可能需要扩展：新风控制、运行模式、风速等接口
