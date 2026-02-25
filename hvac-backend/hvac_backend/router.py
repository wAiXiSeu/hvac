from fastapi import APIRouter, Request
from pydantic import BaseModel
from hvac_backend import registers as reg

router = APIRouter()


class ModbusConfig(BaseModel):
    host: str
    port: int
    slave_id: int = 1
    timeout: int = 5


class SystemControl(BaseModel):
    power: bool | None = None
    home_mode: bool | None = None
    run_mode: int | None = None
    fan_speed: int | None = None


class RoomSetpoint(BaseModel):
    temp: float


class RegisterWrite(BaseModel):
    address: int
    value: float


@router.get("/config")
async def get_config(request: Request):
    config = request.app.state.config["modbus"]
    return {
        "host": config.get("host"),
        "port": config.get("port"),
        "slave_id": config.get("slave_id"),
        "timeout": config.get("timeout"),
    }


@router.put("/config")
async def update_config(config: ModbusConfig, request: Request):
    request.app.state.config["modbus"]["host"] = config.host
    request.app.state.config["modbus"]["port"] = config.port
    request.app.state.config["modbus"]["slave_id"] = config.slave_id
    request.app.state.config["modbus"]["timeout"] = config.timeout
    
    request.app.state.modbus_client.host = config.host
    request.app.state.modbus_client.port = config.port
    request.app.state.modbus_client.slave_id = config.slave_id
    request.app.state.modbus_client.timeout = config.timeout
    
    await request.app.state.modbus_client.reconnect()
    
    return {"message": "Configuration updated"}


@router.get("/status")
async def get_status(request: Request):
    return request.app.state.modbus_client.get_status()


@router.get("/registers")
async def get_all_registers(request: Request):
    """获取所有寄存器数据"""
    return request.app.state.modbus_client.get_all_registers()


@router.get("/registers/grouped")
async def get_grouped_registers(request: Request):
    """获取按分组的寄存器数据"""
    grouped_data = request.app.state.modbus_client.get_grouped_data()
    # 添加分组名称
    result = {}
    for group, data in grouped_data.items():
        result[group] = {
            "name": reg.GROUP_NAMES.get(group, group),
            "registers": data
        }
    return result


@router.get("/registers/groups")
async def get_register_groups():
    """获取所有分组信息"""
    return reg.GROUP_NAMES


@router.post("/registers/write")
async def write_register(write_data: RegisterWrite, request: Request):
    """通过地址写入寄存器"""
    success = request.app.state.modbus_client.write_register_by_address(
        write_data.address, write_data.value
    )
    if success:
        return {"message": "Register updated", "address": write_data.address, "value": write_data.value}
    else:
        return {"error": "Failed to write register"}, 400


@router.get("/environment")
async def get_environment(request: Request):
    return request.app.state.modbus_client.get_environment()


@router.get("/system")
async def get_system(request: Request):
    return request.app.state.modbus_client.get_system()


@router.put("/system")
async def update_system(control: SystemControl, request: Request):
    modbus = request.app.state.modbus_client
    
    if control.power is not None:
        modbus.set_power(control.power)
    if control.home_mode is not None:
        modbus.set_home_mode(control.home_mode)
    if control.run_mode is not None:
        modbus.set_run_mode(control.run_mode)
    if control.fan_speed is not None:
        modbus.set_fan_speed(control.fan_speed)
    
    return {"message": "System control updated"}


@router.get("/rooms")
async def get_rooms(request: Request):
    """获取房间数据"""
    room_data = request.app.state.modbus_client.get_rooms()
    
    result = []
    for room_id, room_info in reg.ROOMS.items():
        data = room_data.get(room_id, {})
        result.append({
            "id": room_id,
            "name": room_info["name"],
            "temp": data.get("temp"),
            "humidity": data.get("humidity"),
            "dew_point": data.get("dew_point"),
            "setpoint": data.get("setpoint"),
        })
    
    return result


@router.put("/rooms/{room_id}")
async def update_room(room_id: str, setpoint: RoomSetpoint, request: Request):
    success = request.app.state.modbus_client.set_room_setpoint(room_id, setpoint.temp)
    
    if success:
        return {"message": "Room setpoint updated"}
    else:
        return {"error": "Failed to update room setpoint"}, 400
