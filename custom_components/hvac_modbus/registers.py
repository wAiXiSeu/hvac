"""
Modbus 寄存器地址定义
从后端迁移，用于 Home Assistant 集成直接读取 Modbus
"""

# 常用寄存器地址常量
class RegisterAddress:
    # 系统控制
    SYSTEM_POWER = 1033          # 系统总电源
    HOME_MODE = 1034             # 在家/离家模式
    RUN_MODE = 1041              # 运行模式
    FAN_SPEED = 1047             # 新风风速设定
    
    # 厨卫功能
    KITCHEN_RADIANT = 1133       # 厨卫辐射开关
    
    # 新风系统
    HUMIDIFIER = 1168            # 面板加湿开关

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
    1035: {"name": "制热送风温度下限", "unit": "°C", "rw": "RO", "scaling": 0.1, "desc": "防结露保护", "group": "system"},
    1036: {"name": "制冷送风温度设定", "unit": "°C", "rw": "RO", "scaling": 0.1, "desc": "制冷模式送风温度", "group": "system"},
    1037: {"name": "加湿停止上限", "unit": "%", "rw": "RO", "scaling": 1, "desc": "湿度达50%强制停加湿", "group": "system"},
    1041: {"name": "运行模式", "unit": "", "rw": "RW", "scaling": 1, "desc": "1:制冷 2:制热 3:通风 4:除湿", "group": "system"},
    1046: {"name": "新风机送风口湿度", "unit": "%", "rw": "RO", "scaling": 0.1, "desc": "监控送风是否过湿", "group": "system"},
    1047: {"name": "新风风速设定", "unit": "%", "rw": "RW", "scaling": 1, "desc": "风速百分比", "group": "system"},
    1048: {"name": "加湿启动湿度起点", "unit": "%", "rw": "RW", "scaling": 1, "desc": "低于此值且加湿开启则启动", "group": "system"},
    
    # ========== 约克主机区 ==========
    1029: {"name": "约克回水温度", "unit": "°C", "rw": "RO", "scaling": 0.1, "desc": "主机回水温度", "group": "york"},
    1030: {"name": "约克供水温度", "unit": "°C", "rw": "RO", "scaling": 0.1, "desc": "主机供水温度", "group": "york"},
    1031: {"name": "约克运行模式反馈", "unit": "", "rw": "RO", "scaling": 1, "desc": "0:冷 1:热 8:循环", "group": "york"},
    1062: {"name": "制热供水设定点", "unit": "°C", "rw": "RW", "scaling": 0.1, "desc": "制热模式供水温度设定", "group": "york"},
    1066: {"name": "制冷供水设定点", "unit": "°C", "rw": "RW", "scaling": 0.1, "desc": "制冷模式供水温度设定", "group": "york"},
    
    # ========== 客厅 ==========
    1085: {"name": "客厅实际温度", "unit": "°C", "rw": "RO", "scaling": 0.1, "desc": "客厅当前温度", "group": "living_room"},
    1086: {"name": "客厅设计基准温", "unit": "°C", "rw": "RO", "scaling": 0.1, "desc": "系统默认舒适点", "group": "living_room"},
    1087: {"name": "客厅实际湿度", "unit": "%", "rw": "RO", "scaling": 0.1, "desc": "客厅当前湿度", "group": "living_room"},
    1088: {"name": "客厅露点温度", "unit": "°C", "rw": "RO", "scaling": 0.1, "desc": "客厅露点温度", "group": "living_room"},
    # 1089: {"name": "客厅辐射开关", "unit": "", "rw": "RW", "scaling": 1, "desc": "1:开 0:关", "group": "living_room"},
    # 1090: {"name": "客厅设定温度", "unit": "°C", "rw": "RW", "scaling": 0.5, "desc": "客厅目标温度", "group": "living_room"},
    1093: {"name": "客厅辐射开关", "unit": "", "rw": "RW", "scaling": 1, "desc": "先于1089变化", "group": "living_room"},
    1094: {"name": "客厅温度设定", "unit": "°C", "rw": "RW", "scaling": 0.5, "desc": "先于1090变化", "group": "living_room"},
    
    # ========== 主卧 ==========
    1095: {"name": "主卧实际温度", "unit": "°C", "rw": "RO", "scaling": 0.1, "desc": "主卧当前温度", "group": "master_bedroom"},
    1096: {"name": "主卧设计基准温", "unit": "°C", "rw": "RO", "scaling": 0.1, "desc": "系统默认舒适点", "group": "master_bedroom"},
    1097: {"name": "主卧实际湿度", "unit": "%", "rw": "RO", "scaling": 0.1, "desc": "主卧当前湿度", "group": "master_bedroom"},
    1098: {"name": "主卧露点温度", "unit": "°C", "rw": "RO", "scaling": 0.1, "desc": "主卧露点温度", "group": "master_bedroom"},
    # 1099: {"name": "主卧辐射开关", "unit": "", "rw": "RW", "scaling": 1, "desc": "1:开 0:关", "group": "master_bedroom"},
    # 1101: {"name": "主卧设定温度", "unit": "°C", "rw": "RW", "scaling": 0.5, "desc": "主卧目标温度", "group": "master_bedroom"},
    1103: {"name": "主卧辐射开关", "unit": "", "rw": "RW", "scaling": 1, "desc": "面板辐射设置", "group": "master_bedroom"},
    1104: {"name": "主卧设定温度", "unit": "°C", "rw": "RW", "scaling": 0.5, "desc": "面板温度设置", "group": "master_bedroom"},
    
    # ========== 次卧 ==========
    1105: {"name": "次卧实际温度", "unit": "°C", "rw": "RO", "scaling": 0.1, "desc": "次卧当前温度", "group": "second_bedroom"},
    1106: {"name": "次卧设计基准温", "unit": "°C", "rw": "RO", "scaling": 0.1, "desc": "系统默认舒适点", "group": "second_bedroom"},
    1107: {"name": "次卧实际湿度", "unit": "%", "rw": "RO", "scaling": 0.1, "desc": "次卧当前湿度", "group": "second_bedroom"},
    1108: {"name": "次卧露点温度", "unit": "°C", "rw": "RO", "scaling": 0.1, "desc": "次卧露点温度", "group": "second_bedroom"},
    # 1109: {"name": "次卧辐射开关", "unit": "", "rw": "RW", "scaling": 1, "desc": "1:开 0:关", "group": "second_bedroom"},
    # 1110: {"name": "次卧设定温度", "unit": "°C", "rw": "RW", "scaling": 0.5, "desc": "次卧目标温度", "group": "second_bedroom"},
    1113: {"name": "次卧温度设定", "unit": "°C", "rw": "RW", "scaling": 0.5, "desc": "面板温度设置", "group": "second_bedroom"},
    1114: {"name": "次卧辐射开关", "unit": "", "rw": "RW", "scaling": 1, "desc": "面板辐射设置", "group": "second_bedroom"},
    
    # ========== 书房 ==========
    1115: {"name": "书房温度设定", "unit": "°C", "rw": "RW", "scaling": 0.5, "desc": "面板温度设置", "group": "study_room"},
    1116: {"name": "书房辐射开关", "unit": "", "rw": "RW", "scaling": 1, "desc": "面板辐射设置", "group": "study_room"},
    1117: {"name": "书房实际温度", "unit": "°C", "rw": "RO", "scaling": 0.1, "desc": "书房当前温度", "group": "study_room"},
    1118: {"name": "书房设计基准温", "unit": "°C", "rw": "RO", "scaling": 0.1, "desc": "系统默认舒适点", "group": "study_room"},
    1119: {"name": "书房实际湿度", "unit": "%", "rw": "RO", "scaling": 0.1, "desc": "书房当前湿度", "group": "study_room"},
    1120: {"name": "书房露点温度", "unit": "°C", "rw": "RO", "scaling": 0.1, "desc": "书房露点温度", "group": "study_room"},
    # 1121: {"name": "书房辐射开关", "unit": "", "rw": "RW", "scaling": 1, "desc": "1:开 0:关", "group": "study_room"},
    # 1123: {"name": "书房设定温度", "unit": "°C", "rw": "RW", "scaling": 0.5, "desc": "书房目标温度", "group": "study_room"},
    
    # ========== 厨卫与功能区 ==========
    1133: {"name": "厨卫辐射开关", "unit": "", "rw": "RW", "scaling": 1, "desc": "厨房卫生间辐射控制", "group": "kitchen"},
    
    # ========== 新风系统 ==========
    1049: {"name": "新风机状态码1", "unit": "", "rw": "RO", "scaling": 1, "desc": "0x8104表示正常运行", "group": "fresh_air"},
    1161: {"name": "新风压缩机频率", "unit": "Hz", "rw": "RO", "scaling": 1, "desc": "新风机压缩机运行频率", "group": "fresh_air"},
    1162: {"name": "新风机整机电流", "unit": "A", "rw": "RO", "scaling": 0.1, "desc": "新风机整机电流", "group": "fresh_air"},
    1163: {"name": "新风机压缩机电流", "unit": "A", "rw": "RO", "scaling": 0.1, "desc": "新风机压缩机电流", "group": "fresh_air"},
    1164: {"name": "新风内部供水温", "unit": "°C", "rw": "RO", "scaling": 0.1, "desc": "新风机内部换热器温1", "group": "fresh_air"},
    1165: {"name": "新风内部回水温", "unit": "°C", "rw": "RO", "scaling": 0.1, "desc": "新风机内部换热器温2", "group": "fresh_air"},
    1168: {"name": "面板加湿开关", "unit": "", "rw": "RW", "scaling": 1, "desc": "1:开 0:关", "group": "fresh_air"},
}

# 房间配置（统一使用面板寄存器作为主控制）
ROOMS = {
    "living_room": {"name": "客厅", "temp": 1085, "humidity": 1087, "dew_point": 1088, "setpoint": 1094, "radiant": 1093, "design_temp": 1086},
    "master_bedroom": {"name": "主卧", "temp": 1095, "humidity": 1097, "dew_point": 1098, "setpoint": 1104, "radiant": 1103, "design_temp": 1096},
    "second_bedroom": {"name": "次卧", "temp": 1105, "humidity": 1107, "dew_point": 1108, "setpoint": 1113, "radiant": 1114, "design_temp": 1106},
    "study_room": {"name": "书房", "temp": 1117, "humidity": 1119, "dew_point": 1120, "setpoint": 1115, "radiant": 1116, "design_temp": 1118},
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

# 批量读取范围定义
REGISTER_RANGES = [
    (1024, 30),   # 环境 + 系统控制: 1024-1053
    (1062, 10),   # 约克主机: 1062-1071
    (1085, 40),   # 房间区: 1085-1124
    (1133, 2),    # 厨卫: 1133-1134
    (1161, 10),   # 新风: 1161-1170
]


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
            # 温度设定：20°C -> 40
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
