## ADDED Requirements

### Requirement: 房间设计基准温传感器

系统 SHALL 为每个房间提供设计基准温传感器，显示系统默认舒适点温度。

#### Scenario: 查看房间设计基准温

- **WHEN** 用户查看房间设计基准温传感器
- **THEN** 系统显示该房间的设计基准温度值（单位：°C）
- **THEN** 默认值为 23.0°C

### Requirement: 房间面板温度设置传感器

系统 SHALL 为每个房间提供面板温度设置传感器，显示面板上的温度设定值。

#### Scenario: 查看面板温度设置

- **WHEN** 用户查看房间面板温度设置传感器
- **THEN** 系统显示面板当前设定的温度值（单位：°C）

### Requirement: 房间面板辐射设置传感器

系统 SHALL 为客厅、主卧、次卧、书房提供面板辐射设置状态传感器。

#### Scenario: 查看面板辐射设置状态

- **WHEN** 用户查看面板辐射设置传感器
- **THEN** 系统显示面板上的辐射设置状态（开/关）

### Requirement: 面板设置实体标识

系统 SHALL 为所有面板设置传感器创建与房间关联的唯一标识符。

#### Scenario: 传感器 ID 格式

- **WHEN** 系统创建面板设置传感器
- **THEN** 设计基准温传感器 ID 格式为 `sensor.hvac_<room_id>_design_temp`
- **THEN** 面板温度设置传感器 ID 格式为 `sensor.hvac_<room_id>_panel_temp`
- **THEN** 面板辐射设置传感器 ID 格式为 `sensor.hvac_<room_id>_panel_radiant`

#### Scenario: 完整实体 ID 列表

- **WHEN** 系统创建所有面板设置传感器
- **THEN** 客厅设计基准温: `sensor.hvac_living_room_design_temp`
- **THEN** 客厅面板温度: `sensor.hvac_living_room_panel_temp`
- **THEN** 客厅面板辐射: `sensor.hvac_living_room_panel_radiant`
- **THEN** 主卧设计基准温: `sensor.hvac_master_bedroom_design_temp`
- **THEN** 主卧面板温度: `sensor.hvac_master_bedroom_panel_temp`
- **THEN** 主卧面板辐射: `sensor.hvac_master_bedroom_panel_radiant`
- **THEN** 次卧设计基准温: `sensor.hvac_second_bedroom_design_temp`
- **THEN** 次卧面板温度: `sensor.hvac_second_bedroom_panel_temp`
- **THEN** 次卧面板辐射: `sensor.hvac_second_bedroom_panel_radiant`
- **THEN** 书房设计基准温: `sensor.hvac_study_room_design_temp`
- **THEN** 书房面板温度: `sensor.hvac_study_room_panel_temp`
- **THEN** 书房面板辐射: `sensor.hvac_study_room_panel_radiant`
