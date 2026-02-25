"""
Modbus 寄存器地址定义
基于 docs/modbus.jpg 中的寄存器映射表
"""

# ========== 系统环境区 ==========
SYSTEM_PM25 = 41024          # 室内 PM2.5 (RO)
SYSTEM_CO2 = 41026           # 室内 CO2 (RO)
SYSTEM_OUTDOOR_TEMP = 41027  # 室外温度 (RO), scaling: 0.1
SYSTEM_OUTDOOR_HUM = 41028   # 室外湿度 (RO), scaling: 0.1

# ========== 系统控制区 ==========
SYSTEM_POWER = 41033         # 系统总电源 (RW): 1=开, 0=关
SYSTEM_MODE = 41034          # 在家/离家模式 (RW): 1=在家, 0=离家
SYSTEM_RUN_MODE = 41041      # 运行模式 (RW): 1=制热, 2=制冷, 3=除湿, 4=通风
SYSTEM_FAN_SPEED = 41047     # 新风风速设定 (RW): %

# ========== 约克主机区 ==========
YORK_SUPPLY_TEMP = 41029     # 约克供水温度 (RO), scaling: 0.1
YORK_RETURN_TEMP = 41030     # 约克回水温度 (RO), scaling: 0.1
HEAT_SETPOINT = 41062        # 制热供水设定点 (RW), scaling: 0.1
COOL_SETPOINT = 41066        # 制冷供水设定点 (RW), scaling: 0.1

# ========== 房间温度 (实际值, 只读) ==========
LIVING_ROOM_TEMP = 41085     # 客厅实际温度 (RO), scaling: 0.1
LIVING_ROOM_HUM = 41087      # 客厅实际湿度 (RO), scaling: 0.1
MASTER_BEDROOM_TEMP = 41095     # 主卧实际温度 (RO)
MASTER_BEDROOM_HUM = 41097      # 主卧实际湿度 (RO)
SECOND_BEDROOM_TEMP = 41105     # 次卧实际温度 (RO)
SECOND_BEDROOM_HUM = 41107      # 次卧实际湿度 (RO)
STUDY_ROOM_TEMP = 41117     # 书房实际温度 (RO)
STUDY_ROOM_HUM = 41119      # 书房实际湿度 (RO)

# ========== 房间温度设定 (可写) ==========
LIVING_ROOM_SETPOINT = 41090     # 客厅设定温度 (RW), write = temp * 2
MASTER_BEDROOM_SETPOINT = 41101  # 主卧设定温度 (RW)
SECOND_BEDROOM_SETPOINT = 41110 # 次卧设定温度 (RW)
STUDY_ROOM_SETPOINT = 41123      # 书房设定温度 (RW)

# 寄存器缩放因子
SCALING_FACTORS = {
    SYSTEM_OUTDOOR_TEMP: 0.1,
    SYSTEM_OUTDOOR_HUM: 0.1,
    YORK_SUPPLY_TEMP: 0.1,
    YORK_RETURN_TEMP: 0.1,
    HEAT_SETPOINT: 0.1,
    COOL_SETPOINT: 0.1,
    LIVING_ROOM_TEMP: 0.1,
    LIVING_ROOM_HUM: 0.1,
    MASTER_BEDROOM_TEMP: 0.1,
    MASTER_BEDROOM_HUM: 0.1,
    SECOND_BEDROOM_TEMP: 0.1,
    SECOND_BEDROOM_HUM: 0.1,
    STUDY_ROOM_TEMP: 0.1,
    STUDY_ROOM_HUM: 0.1,
    LIVING_ROOM_SETPOINT: 0.5,
    MASTER_BEDROOM_SETPOINT: 0.5,
    SECOND_BEDROOM_SETPOINT: 0.5,
    STUDY_ROOM_SETPOINT: 0.5,
}


def scale_value(value: int, register: int) -> float:
    """根据寄存器地址缩放值"""
    scaling = SCALING_FACTORS.get(register, 1)
    return value * scaling


def unscale_value(value: float, register: int) -> int:
    """将值反缩放后用于写入寄存器"""
    scaling = SCALING_FACTORS.get(register, 1)
    if scaling == 0.5:
        return int(value * 2)
    return int(value / scaling)
