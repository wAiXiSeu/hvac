# HVAC 前端组件说明文档

本文档描述了 HVAC 系统前端的组件架构和使用方式。

## 架构概览

前端采用分层组件架构，分为三个主要层次：

```
src/components/
├── ui/              # 通用 UI 组件层（可复用的基础组件）
├── layout/          # 布局组件层（业务逻辑组件）
└── (legacy)/        # 旧组件（待清理）
```

## 通用 UI 组件 (`src/components/ui/`)

这些是无状态或低状态的可复用基础组件，不包含业务逻辑。

### DataDisplay
**用途**: 只读数据展示组件  
**文件**: `DataDisplay.jsx`, `DataDisplay.css`  
**Props**:
- `label`: 数据标签（例如："当前温度"）
- `value`: 数据值
- `unit`: 单位（例如："°C"）

**样式**: 灰色背景，表示只读状态

**使用示例**:
```jsx
<DataDisplay label="当前温度" value="21.2" unit="°C" />
```

---

### ControlInput
**用途**: 可编辑的输入控件（点击进入编辑模式）  
**文件**: `ControlInput.jsx`, `ControlInput.css`  
**Props**:
- `label`: 标签
- `value`: 当前值
- `unit`: 单位
- `min`: 最小值
- `max`: 最大值
- `step`: 步进值（默认 0.5）
- `onSave`: 保存回调函数
- `disabled`: 是否禁用

**交互流程**:
1. 显示当前值，点击进入编辑模式
2. 输入新值，显示 ✓ 和 ✗ 按钮
3. 验证输入范围，显示错误提示
4. 保存成功后退出编辑模式

**使用示例**:
```jsx
<ControlInput 
  label="设定温度"
  value={21}
  unit="°C"
  min={16}
  max={30}
  step={0.5}
  onSave={handleSave}
/>
```

---

### ToggleSwitch
**用途**: 开关控制组件  
**文件**: `ToggleSwitch.jsx`, `ToggleSwitch.css`  
**Props**:
- `label`: 标签
- `checked`: 当前状态（布尔值）
- `onChange`: 状态改变回调函数
- `disabled`: 是否禁用

**使用示例**:
```jsx
<ToggleSwitch 
  label="系统电源"
  checked={power === 1}
  onChange={handlePowerChange}
/>
```

---

### Slider
**用途**: 滑动条控制组件  
**文件**: `Slider.jsx`, `Slider.css`  
**Props**:
- `label`: 标签
- `value`: 当前值
- `min`: 最小值（默认 0）
- `max`: 最大值（默认 100）
- `step`: 步进值（默认 1）
- `unit`: 单位（默认 ""）
- `onChange`: 值改变回调函数
- `disabled`: 是否禁用

**使用示例**:
```jsx
<Slider 
  label="新风风速"
  value={85}
  min={0}
  max={100}
  step={5}
  unit="%"
  onChange={handleSpeedChange}
/>
```

---

### LoadingIndicator
**用途**: 加载状态指示器  
**文件**: `LoadingIndicator.jsx`, `LoadingIndicator.css`  
**Props**:
- `size`: 大小（'small', 'medium', 'large'，默认 'medium'）

**使用示例**:
```jsx
<LoadingIndicator size="small" />
```

---

### FeedbackMessage
**用途**: 成功/错误反馈提示组件  
**文件**: `FeedbackMessage.jsx`, `FeedbackMessage.css`  
**Props**:
- `type`: 类型（'success' 或 'error'）
- `message`: 提示消息
- `onClose`: 关闭回调函数

**自动行为**: 成功消息 2 秒后自动消失，错误消息 5 秒后自动消失

**使用示例**:
```jsx
<FeedbackMessage 
  type="success"
  message="温度设定已更新"
  onClose={() => setFeedback(null)}
/>
```

---

## 布局组件 (`src/components/layout/`)

这些组件包含业务逻辑，负责数据获取、状态管理和 API 调用。

### SystemOverview
**用途**: 系统概览区域容器组件  
**文件**: `SystemOverview.jsx`, `SystemOverview.css`  
**子组件**: EnvironmentMonitoring, SystemControl, YorkHost

**布局**: 三列卡片布局（响应式）

---

### EnvironmentMonitoring
**用途**: 环境监测组件（只读）  
**文件**: `EnvironmentMonitoring.jsx`, `EnvironmentMonitoring.css`  
**数据来源**: HvacDataContext (`environment`)

**显示内容**:
- 室内 PM2.5
- 室内 CO2
- 室外温度
- 室外湿度

**样式**: 只读卡片（灰色背景，📊 图标）

---

### SystemControl
**用途**: 系统控制组件（可操作）  
**文件**: `SystemControl.jsx`, `SystemControl.css`  
**数据来源**: HvacDataContext (`system`, `freshAir`)

**控制功能**:
- 系统电源（开/关）
- 在家/离家模式
- 运行模式（制热/制冷/除湿/通风）
- 新风风速（0-100%）
- 加湿功能（开/关）

**API 调用**:
- `updateSystem()`: 更新系统状态
- `updateFreshAirSpeed()`: 更新新风风速
- `updateHumidifier()`: 更新加湿功能

**样式**: 可编辑卡片（白色背景，⚙️ 图标）

---

### YorkHost
**用途**: 约克主机状态显示（只读）  
**文件**: `YorkHost.jsx`, `YorkHost.css`  
**数据来源**: HvacDataContext (`york`)

**显示内容**:
- 供水温度
- 回水温度
- 制热设定点
- 制冷设定点

**样式**: 只读卡片

---

### RoomSection
**用途**: 房间信息区域容器组件  
**文件**: `RoomSection.jsx`, `RoomSection.css`  
**子组件**: RoomControlPanel, KitchenControl

**布局**: 弹性布局，自动换行，每个卡片宽度 250-320px

---

### RoomControlPanel
**用途**: 单个房间控制面板  
**文件**: `RoomControlPanel.jsx`, `RoomControlPanel.css`  
**数据来源**: Props (`room`)

**显示内容**:
- 房间名称
- 当前温度（只读）
- 当前湿度（只读）
- 设定温度（可编辑，16-30°C）

**API 调用**:
- `updateRoomSetpoint(roomId, temp)`: 更新房间温度设定

**样式**: 可编辑卡片，顶部蓝色下划线

---

### KitchenControl
**用途**: 厨卫辐射控制组件  
**文件**: `KitchenControl.jsx`, `KitchenControl.css`  
**数据来源**: 内部状态

**控制功能**:
- 辐射状态显示（开启/关闭）
- 辐射开关控制

**API 调用**:
- `updateKitchenRadiant(enabled)`: 更新厨卫辐射状态（寄存器 1133）

**样式**: 与房间卡片一致，可编辑卡片

---

### FreshAirSection
**用途**: 新风系统区域容器组件  
**文件**: `FreshAirSection.jsx`, `FreshAirSection.css`  
**数据来源**: HvacDataContext (`freshAir`)

**显示内容**:
- 压缩机频率（只读）
- 供水温度（只读）
- 回水温度（只读）
- 运行状态（只读，带状态码解析）

**状态解析**:
- `0x8104` / `33028`: 正常运行（绿色）
- 其他: 显示状态码（黄色警告）

**样式**: 只读卡片

**注意**: 控制功能已迁移到 SystemControl 组件

---

## 全局状态管理

### HvacDataContext
**文件**: `src/contexts/HvacDataContext.jsx`

**提供的数据**:
```javascript
{
  connection: { status: 'connected'|'disconnected', lastUpdate: Date },
  environment: { pm25, co2, outdoorTemp, outdoorHumidity },
  system: { power, homeMode, runMode, fanSpeed },
  york: { supplyTemp, returnTemp, heatSetpoint, coolSetpoint },
  rooms: [{ id, name, temp, humidity, setpoint }],
  freshAir: { compressorFreq, supplyTemp, returnTemp, statusCode, fanSpeed, humidifier },
  isPolling: boolean,
  refreshData: function
}
```

**轮询机制**:
- 每 5 秒自动刷新数据
- 窗口失焦时暂停轮询（节省资源）
- 窗口恢复焦点时继续轮询

**使用方式**:
```javascript
import { useHvacData } from '../../contexts/HvacDataContext';

function MyComponent() {
  const { system, refreshData } = useHvacData();
  // ...
}
```

---

## 样式系统

### CSS 变量 (`src/theme.css`)

**颜色变量**:
```css
--bg-readonly: #f5f5f5;        /* 只读卡片背景 */
--bg-editable: #ffffff;        /* 可编辑卡片背景 */
--border-color: #ddd;          /* 边框颜色 */
--color-primary: #1890ff;      /* 主题色 */
--color-success: #52c41a;      /* 成功状态 */
--color-error: #ff4d4f;        /* 错误状态 */
```

**间距变量**:
```css
--spacing-xs: 4px;
--spacing-sm: 8px;
--spacing-md: 16px;
--spacing-lg: 24px;
--spacing-xl: 32px;
```

### BEM 命名规范

组件样式类使用 BEM（Block Element Modifier）命名规范：

```css
.block {}                      /* 块 */
.block__element {}            /* 元素 */
.block--modifier {}           /* 修饰符 */
.block__element--modifier {}  /* 元素修饰符 */
```

**示例**:
```css
.room-control-panel {}                    /* 房间控制面板块 */
.room-control-panel__name {}             /* 房间名称元素 */
.room-control-panel__data {}             /* 数据区域元素 */
.data-card--readonly {}                  /* 只读卡片修饰符 */
.data-card--editable {}                  /* 可编辑卡片修饰符 */
```

---

## 视觉区分策略

### 只读 vs 可编辑

**只读组件特征**:
- 背景色: `var(--bg-readonly)` (#f5f5f5)
- 图标: 📊
- 鼠标样式: `cursor: default`
- 无 hover 效果

**可编辑组件特征**:
- 背景色: `var(--bg-editable)` (#ffffff)
- 图标: ⚙️
- 鼠标样式: `cursor: pointer`
- Hover 效果: 阴影提升

---

## 响应式设计

### 断点
- **桌面端**: > 1200px（三列/四列布局）
- **平板端**: 768px - 1200px（两列布局）
- **移动端**: < 768px（单列布局）

### 适配策略
- 使用 Flexbox 弹性布局
- `flex-wrap: wrap` 自动换行
- 设置 `min-width` 和 `max-width` 限制卡片宽度
- 移动端切换为 `flex-direction: column`

---

## API 服务 (`src/services/api.js`)

### 数据获取
- `getStatus()`: 获取连接状态
- `getGroupedRegisters()`: 获取分组寄存器数据
- `getSystem()`: 获取系统状态
- `getRooms()`: 获取房间数据

### 数据写入
- `updateSystem(control)`: 更新系统控制
- `updateRoomSetpoint(roomId, temp)`: 更新房间温度
- `updateFreshAirSpeed(speed)`: 更新新风风速
- `updateHumidifier(enabled)`: 更新加湿功能
- `updateKitchenRadiant(enabled)`: 更新厨卫辐射
- `writeRegister(address, value)`: 通用寄存器写入

### 输入验证
- `validateTemperature(temp, min, max)`: 验证温度输入

---

## 开发指南

### 添加新的只读数据展示
1. 使用 `DataDisplay` 组件
2. 从 `HvacDataContext` 获取数据
3. 使用 `.data-card--readonly` 样式类

### 添加新的控制功能
1. 使用对应的 UI 组件（`ToggleSwitch`, `Slider`, `ControlInput`）
2. 在 `api.js` 中添加 API 方法
3. 实现错误处理和反馈提示
4. 使用 `.data-card--editable` 样式类

### 创建新的布局组件
1. 在 `src/components/layout/` 创建组件文件
2. 使用 `useHvacData()` 获取全局数据
3. 遵循 BEM 命名规范
4. 添加响应式样式

---

## 待清理的旧组件

以下组件已被新架构替代，建议在确认功能正常后删除：

- `ConfigModal.jsx`: 配置弹窗（功能保留）
- `ConnectionStatus.jsx`: 连接状态（功能保留）
- `EnvironmentCard.jsx`: 旧环境卡片（已被 EnvironmentMonitoring 替代）
- `RegistersPanel.jsx`: 旧寄存器面板（已被新架构替代）
- `RoomCards.jsx`: 旧房间卡片（已被 RoomControlPanel 替代）
- `SystemControl.jsx` (根目录): 旧系统控制（已被 layout/SystemControl.jsx 替代）

---

## 性能优化建议

1. **数据轮询优化**: 已实现窗口失焦暂停轮询
2. **避免不必要的重渲染**: 使用 `useCallback` 和 `useMemo`
3. **懒加载**: 考虑对大型组件使用 `React.lazy()`
4. **防抖和节流**: 对频繁触发的操作（如滑动条）添加防抖

---

## 常见问题

### Q: 为什么温度设定没有生效？
A: 检查温度缩放因子。设定温度寄存器使用 `scaling: 0.5`，即设定值 = 温度 × 2。后端已处理缩放逻辑。

### Q: 如何调试数据轮询？
A: 在浏览器控制台查看 `HvacDataContext` 的日志，或使用 React DevTools 查看 Context 数据。

### Q: 如何修改轮询间隔？
A: 在 `HvacDataContext.jsx` 中修改 `POLLING_INTERVAL` 常量（默认 5000ms）。

### Q: 组件样式不生效？
A: 确保已导入对应的 CSS 文件，并检查 CSS 类名是否正确（注意 BEM 命名）。

---

## 版本历史

- **v1.0** (2026-02-25): 初始版本，完成 UI 布局增强和控制逻辑整合
  - 创建通用 UI 组件库
  - 实现三大功能区域布局
  - 实现全局状态管理和数据轮询
  - 实现只读/可编辑视觉区分
  - 实现响应式设计
