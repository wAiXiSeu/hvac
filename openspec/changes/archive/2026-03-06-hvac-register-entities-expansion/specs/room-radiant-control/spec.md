## ADDED Requirements

### Requirement: 房间辐射开关控制

系统 SHALL 为每个房间（客厅、主卧、次卧、书房）提供独立的辐射开关实体，允许用户控制各房间的辐射采暖/制冷功能。

#### Scenario: 查看房间辐射开关状态

- **WHEN** 用户查看房间辐射开关实体
- **THEN** 系统显示当前辐射开关状态（开/关）

#### Scenario: 开启房间辐射

- **WHEN** 用户打开房间辐射开关
- **THEN** 系统写入对应寄存器地址（1089/1099/1109/1121）值为 1
- **THEN** 开关状态更新为"开"

#### Scenario: 关闭房间辐射

- **WHEN** 用户关闭房间辐射开关
- **THEN** 系统写入对应寄存器地址值为 0
- **THEN** 开关状态更新为"关"

### Requirement: 房间辐射开关实体标识

系统 SHALL 为每个房间创建具有唯一标识符的辐射开关实体。

#### Scenario: 实体 ID 格式

- **WHEN** 系统创建房间辐射开关实体
- **THEN** 客厅辐射开关实体 ID 为 `switch.hvac_living_room_radiant`
- **THEN** 主卧辐射开关实体 ID 为 `switch.hvac_master_bedroom_radiant`
- **THEN** 次卧辐射开关实体 ID 为 `switch.hvac_second_bedroom_radiant`
- **THEN** 书房辐射开关实体 ID 为 `switch.hvac_study_room_radiant`

### Requirement: 房间辐射开关可用性

系统 SHALL 仅在 Modbus 连接正常且数据刷新成功时显示房间辐射开关为可用状态。

#### Scenario: 连接正常时可用

- **WHEN** Modbus 连接正常
- **THEN** 所有房间辐射开关实体显示为可用

#### Scenario: 连接断开时不可用

- **WHEN** Modbus 连接断开
- **THEN** 所有房间辐射开关实体显示为不可用
