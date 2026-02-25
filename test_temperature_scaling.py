#!/usr/bin/env python3
"""
测试温度设定的缩放逻辑
"""

# 模拟寄存器定义
REGISTERS = {
    1090: {"name": "客厅设定温度", "unit": "°C", "rw": "RW", "scaling": 0.5, "desc": "客厅目标温度"},
}

def unscale_value(value: float, address: int) -> int:
    """将值反缩放后用于写入寄存器"""
    if address in REGISTERS:
        scaling = REGISTERS[address].get("scaling", 1)
        if scaling == 0.5:
            result = int(value * 2)
            print(f"  温度 {value}°C × 2 = 寄存器值 {result}")
            return result
        result = int(value / scaling)
        return result
    return int(value)

def scale_value(value: int, address: int) -> float:
    """根据寄存器地址缩放值"""
    if address in REGISTERS:
        scaling = REGISTERS[address].get("scaling", 1)
        result = value * scaling
        print(f"  寄存器值 {value} × {scaling} = 温度 {result}°C")
        return result
    return value

print("=" * 50)
print("温度设定测试")
print("=" * 50)

# 测试场景
test_cases = [
    ("设定20°C", 20.0, 1090),
    ("设定22.5°C", 22.5, 1090),
    ("设定25°C", 25.0, 1090),
]

for name, temp, addr in test_cases:
    print(f"\n{name}:")
    print(f"  输入温度: {temp}°C")
    register_value = unscale_value(temp, addr)
    print(f"  写入寄存器: {register_value}")
    
    # 验证读取
    print(f"\n  验证读取:")
    read_temp = scale_value(register_value, addr)
    print(f"  读取温度: {read_temp}°C")
    
    if abs(read_temp - temp) < 0.01:
        print(f"  ✓ 验证成功")
    else:
        print(f"  ✗ 验证失败：期望 {temp}°C，实际 {read_temp}°C")

print("\n" + "=" * 50)
