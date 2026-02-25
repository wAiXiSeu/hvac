"""
Modbus 寄存器地址定义
基于 docs/modbus.jpg 中的寄存器映射表
"""

# 寄存器完整定义：地址 -> {名称, 单位, 读写, 缩放因子, 描述, 分组}
REGISTERS = {
    # ========== 系统环境区 ==========
    1024: {"name": "室内 PM2.5", "unit": "μg/m³", "rw": "RO", "scaling": 1, "desc": "室内空气质量", "group": "environment"},
    1026: {"name": "室内 CO2", "unit": "PPM", "rw": "RO", "scaling": 1, "desc": "室内二氧化碳浓度", "group": "environment"},
    1027: {"name": "室外温度", "unit": "°C", "rw": "RO", "scaling": 0.1, "desc": "室外环境温度", "group": "environment"},
    1028: {"name": "室外湿度", "unit": "%", "rw": "RO", "scaling": 0.1, "desc": "室外环境湿度", "group": "environment"},
    
    # ========== 系统控制区 ==========
    1033: {"name": "系统总电源", "unit": "", "rw": "RW", "scaling": 1, "desc": "1:开 0:关", "group": "system"},
    1034: {"name": "在家/离家模式", "unit": "", "rw": "RW", "scaling": 1, "desc": "1:在家 0:离家", "group": "system"},
    101: {"name": "运行模式", "unit": "", "rw": "RW", "scaling": 1, "desc": "1:制热 2:制冷 3:除湿 4:通风", "group": "system"},
    1047: {"name": "新风风速设定", "unit": "%", "rw": "RW", "scaling": 1, "desc": "风速百分比", "group": "system"},
    
    # ========== 约克主机区 ==========
    1029: {"name": "约克供水温度", "unit": "°C", "rw": "RO", "scaling": 0.1, "desc": "主机供水温度", "group": "york"},
    1030: {"name": "约克回水温度", "unit": "°C", "rw": "RO", "scaling": 0.1, "desc": "主机回水温度", "group": "york"},
    1062: {"name": "制热供水设定点", "unit": "°C", "rw": "RW", "scaling": 0.1, "desc": "制热模式供水温度设定", "group": "york"},
    1066: {"name": "制冷供水设定点", "unit": "°C", "rw": "RW", "scaling": 0.1, "desc": "制冷模式供水温度设定", "group": "york"},
    
    # ========== 客厅 ==========
    1085: {"name": "客厅实际温度", "unit": "°C", "rw": "RO", "scaling": 0.1, "desc": "客厅当前温度", "group": "living_room"},
    1087: {"name": "客厅实际湿度", "unit": "%", "rw": "RO", "scaling": 0.1, "desc": "客厅当前湿度", "group": "living_room"},
    1088: {"name": "客厅露点温度", "unit": "°C", "rw": "RO", "scaling": 0.1, "desc": "客厅露点温度", "group": "living_room"},
    1090: {"name": "客厅设定温度", "unit": "°C", "rw": "RW", "scaling": 0.5, "desc": "客厅目标温度", "group": "living_room"},
    
    # ========== 主卧 ==========
    1095: {"name": "主卧实际温度", "unit": "°C", "rw": "RO", "scaling": 0.1, "desc": "主卧当前温度", "group": "master_bedroom"},
    1097: {"name": "主卧实际湿度", "unit": "%", "rw": "RO", "scaling": 0.1, "desc": "主卧当前湿度", "group": "master_bedroom"},
    1098: {"name": "主卧露点温度", "unit": "°C", "rw": "RO", "scaling": 0.1, "desc": "主卧露点温度", "group": "master_bedroom"},
    1101: {"name": "主卧设定温度", "unit": "°C", "rw": "RW", "scaling": 0.5, "desc": "主卧目标温度", "group": "master_bedroom"},
    
    # ========== 次卧 ==========
    1105: {"name": "次卧实际温度", "unit": "°C", "rw": "RO", "scaling": 0.1, "desc": "次卧当前温度", "group": "second_bedroom"},
    1107: {"name": "次卧实际湿度", "unit": "%", "rw": "RO", "scaling": 0.1, "desc": "次卧当前湿度", "group": "second_bedroom"},
    1108: {"name": "次卧露点温度", "unit": "°C", "rw": "RO", "scaling": 0.1, "desc": "次卧露点温度", "group": "second_bedroom"},
    1110: {"name": "次卧设定温度", "unit": "°C", "rw": "RW", "scaling": 0.5, "desc": "次卧目标温度", "group": "second_bedroom"},
    
    # ========== 书房 ==========
    1117: {"name": "书房实际温度", "unit": "°C", "rw": "RO", "scaling": 0.1, "desc": "书房当前温度", "group": "study_room"},
    1119: {"name": "书房实际湿度", "unit": "%", "rw": "RO", "scaling": 0.1, "desc": "书房当前湿度", "group": "study_room"},
    1120: {"name": "书房露点温度", "unit": "°C", "rw": "RO", "scaling": 0.1, "desc": "书房露点温度", "group": "study_room"},
    1123: {"name": "书房设定温度", "unit": "°C", "rw": "RW", "scaling": 0.5, "desc": "书房目标温度", "group": "study_room"},
    
    # ========== 厨卫与功能区 ==========
    1133: {"name": "厨卫辐射开关", "unit": "", "rw": "RW", "scaling": 1, "desc": "厨房卫生间辐射控制", "group": "kitchen"},
    1161: {"name": "新风压缩机频率", "unit": "Hz", "rw": "RO", "scaling": 1, "desc": "新风机压缩机运行频率", "group": "fresh_air"},
    1164: {"name": "新风内部供水温", "unit": "°C", "rw": "RO", "scaling": 0.1, "desc": "新风内部换热器供水温度", "group": "fresh_air"},
    1165: {"name": "新风内部回水温", "unit": "°C", "rw": "RO", "scaling": 0.1, "desc": "新风内部换热器回水温度", "group": "fresh_air"},
    1168: {"name": "面板加湿开关", "unit": "", "rw": "RW", "scaling": 1, "desc": "1:开 0:关", "group": "fresh_air"},
    1049: {"name": "新风机状态码1", "unit": "", "rw": "RO", "scaling": 1, "desc": "0x8104表示正常运行", "group": "fresh_air"},
}

# 房间配置
ROOMS = {
    "living_room": {"name": "客厅", "temp": 1085, "humidity": 1087, "setpoint": 1090},
    "master_bedroom": {"name": "主卧", "temp": 1095, "humidity": 1097, "setpoint": 1101},
    "second_bedroom": {"name": "次卧", "temp": 1105, "humidity": 1107, "setpoint": 1110},
    "study_room": {"name": "书房", "temp": 1117, "humidity": 1119, "setpoint": 1123},
}

# 分组名称
GROUP_NAMES = {
    "environment": "环境监测",
    "system": "系统控制",
    "york": "约克主机",
    "living_room": "客厅",
    "master_bedroom": "主卧",
    "second_bedroom": "次卧",
    "study_room": "书房",
    "kitchen": "厨卫功能",
    "fresh_air": "新风系统",
}


def scale_value(value: int, address: int) -> float:
    """根据寄存器地址缩放值"""
    if address in REGISTERS:
        scaling = REGISTERS[address].get("scaling", 1)
        return value * scaling
    return value


def unscale_value(value: float, address: int) -> int:
    """将值反缩放后用于写入寄存器"""
    if address in REGISTERS:
        scaling = REGISTERS[address].get("scaling", 1)
        if scaling == 0.5:
            return int(value * 2)
        return int(value / scaling)
    return int(value)


def get_registers_by_group(group: str) -> dict:
    """获取指定分组的所有寄存器"""
    return {addr: info for addr, info in REGISTERS.items() if info.get("group") == group}


def get_all_groups() -> list:
    """获取所有分组"""
    groups = set()
    for info in REGISTERS.values():
        groups.add(info.get("group"))
    return list(groups)
