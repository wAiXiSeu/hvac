## 1. 数据层更新

- [x] 1.1 更新 modbus.py `_parse_data()` 方法，新增系统阈值数据字段
- [x] 1.2 更新 modbus.py `_parse_data()` 方法，新增房间辐射开关数据字段
- [x] 1.3 更新 modbus.py `_parse_data()` 方法，新增房间面板设置数据字段
- [x] 1.4 在 modbus.py 新增 `set_room_radiant()` 方法

## 2. 传感器实体扩展

- [x] 2.1 新增约克运行模式反馈传感器 (sensor.hvac_york_run_mode_feedback)
- [x] 2.2 新增制热送风温度下限传感器 (sensor.hvac_heating_supply_temp_limit)
- [x] 2.3 新增制冷送风温度设定传感器 (sensor.hvac_cooling_supply_temp_set)
- [x] 2.4 新增加湿停止上限传感器 (sensor.hvac_humidity_stop_limit)
- [x] 2.5 新增新风机送风口湿度传感器 (sensor.hvac_fresh_air_outlet_humidity)
- [x] 2.6 新增新风机整机电流传感器 (sensor.hvac_fresh_air_total_current)
- [x] 2.7 新增新风机压缩机电流传感器 (sensor.hvac_fresh_air_compressor_current)
- [x] 2.8 新增各房间设计基准温传感器 (4个)
- [x] 2.9 新增各房间面板温度设置传感器 (4个)
- [x] 2.10 新增各房间面板辐射设置传感器 (3个，书房面板辐射为 RO)

## 3. 开关实体扩展

- [x] 3.1 新增客厅辐射开关实体 (switch.hvac_living_room_radiant)
- [x] 3.2 新增主卧辐射开关实体 (switch.hvac_master_bedroom_radiant)
- [x] 3.3 新增次卧辐射开关实体 (switch.hvac_second_bedroom_radiant)
- [x] 3.4 新增书房辐射开关实体 (switch.hvac_study_room_radiant)

## 4. 数值实体扩展

- [x] 4.1 新增加湿启动湿度起点数值实体 (number.hvac_humidity_start_point)
- [x] 4.2 在 modbus.py 新增 `set_humidity_start_point()` 方法

## 5. 测试与验证

- [x] 5.1 验证所有新增实体在 Home Assistant 中正确显示
- [x] 5.2 验证房间辐射开关可正常控制
- [x] 5.3 验证加湿启动湿度起点可正常设定
- [x] 5.4 验证现有实体功能不受影响
