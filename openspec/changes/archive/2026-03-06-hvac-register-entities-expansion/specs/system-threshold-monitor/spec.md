## ADDED Requirements

### Requirement: 约克运行模式反馈传感器

系统 SHALL 提供约克主机运行模式反馈传感器，显示主机当前实际运行模式。

#### Scenario: 查看运行模式反馈

- **WHEN** 用户查看约克运行模式反馈传感器
- **THEN** 系统显示当前运行模式（0: 冷、1: 热、8: 循环）

### Requirement: 送风温度限值传感器

系统 SHALL 提供制热送风温度下限和制冷送风温度设定传感器。

#### Scenario: 查看制热送风温度下限

- **WHEN** 用户查看制热送风温度下限传感器
- **THEN** 系统显示当前制热送风温度下限值（单位：°C）

#### Scenario: 查看制冷送风温度设定

- **WHEN** 用户查看制冷送风温度设定传感器
- **THEN** 系统显示当前制冷送风温度设定值（单位：°C）

### Requirement: 加湿阈值传感器

系统 SHALL 提供加湿停止上限传感器和加湿启动湿度起点数值实体。

#### Scenario: 查看加湿停止上限

- **WHEN** 用户查看加湿停止上限传感器
- **THEN** 系统显示湿度停止上限值（单位：%）

#### Scenario: 设置加湿启动湿度起点

- **WHEN** 用户设置加湿启动湿度起点
- **THEN** 系统写入寄存器地址 1048
- **THEN** 数值实体状态更新为新设定值

### Requirement: 新风机送风口湿度传感器

系统 SHALL 提供新风机送风口湿度传感器，用于监控送风是否过湿。

#### Scenario: 查看送风口湿度

- **WHEN** 用户查看新风机送风口湿度传感器
- **THEN** 系统显示当前送风口湿度值（单位：%）

### Requirement: 新风机电流传感器

系统 SHALL 提供新风机整机电流和压缩机电流传感器。

#### Scenario: 查看整机电流

- **WHEN** 用户查看新风机整机电流传感器
- **THEN** 系统显示当前整机电流值（单位：A）

#### Scenario: 查看压缩机电流

- **WHEN** 用户查看新风机压缩机电流传感器
- **THEN** 系统显示当前压缩机电流值（单位：A）

### Requirement: 系统阈值实体标识

系统 SHALL 为所有系统阈值传感器创建具有统一前缀的唯一标识符。

#### Scenario: 传感器 ID 格式

- **WHEN** 系统创建系统阈值传感器
- **THEN** 约克运行模式反馈传感器 ID 为 `sensor.hvac_york_run_mode_feedback`
- **THEN** 制热送风温度下限传感器 ID 为 `sensor.hvac_heating_supply_temp_limit`
- **THEN** 制冷送风温度设定传感器 ID 为 `sensor.hvac_cooling_supply_temp_set`
- **THEN** 加湿停止上限传感器 ID 为 `sensor.hvac_humidity_stop_limit`
- **THEN** 新风机送风口湿度传感器 ID 为 `sensor.hvac_fresh_air_outlet_humidity`
- **THEN** 新风机整机电流传感器 ID 为 `sensor.hvac_fresh_air_total_current`
- **THEN** 新风机压缩机电流传感器 ID 为 `sensor.hvac_fresh_air_compressor_current`
- **THEN** 加湿启动湿度起点数值实体 ID 为 `number.hvac_humidity_start_point`
