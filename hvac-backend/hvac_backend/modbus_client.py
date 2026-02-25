import asyncio
import logging
from typing import Optional
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException

from hvac_backend import registers as reg

logger = logging.getLogger(__name__)


class ModbusClient:
    def __init__(self, config: dict):
        self.host = config.get("host", "192.168.110.200")
        self.port = config.get("port", 502)
        self.slave_id = config.get("slave_id", 1)
        self.timeout = config.get("timeout", 5)
        
        self._client: Optional[ModbusTcpClient] = None
        self._connected = False
        
        # 所有寄存器数据缓存
        self.all_registers_data = {}
        # 按分组缓存
        self.grouped_data = {}
    
    @property
    def is_connected(self) -> bool:
        return self._connected and self._client is not None
    
    async def connect(self) -> bool:
        try:
            if self._client is not None:
                self._client.close()
            
            self._client = ModbusTcpClient(
                host=self.host,
                port=self.port,
                timeout=self.timeout
            )
            
            if self._client.connect():
                self._connected = True
                logger.info(f"Connected to Modbus at {self.host}:{self.port}")
                return True
            else:
                self._connected = False
                return False
        except Exception as e:
            logger.error(f"Error connecting to Modbus: {e}")
            self._connected = False
            return False
    
    async def disconnect(self):
        self._connected = False
        if self._client:
            self._client.close()
            self._client = None
    
    async def reconnect(self):
        await self.disconnect()
        await self.connect()
    
    async def auto_reconnect(self):
        while True:
            if not self.is_connected:
                await self.connect()
            await asyncio.sleep(10)
    
    def read_register(self, address: int) -> Optional[int]:
        if not self.is_connected:
            return None
        try:
            result = self._client.read_holding_registers(
                address=address, count=1, device_id=self.slave_id
            )
            if not result.isError():
                return result.registers[0]
            return None
        except ModbusException as e:
            logger.error(f"Error reading register {address}: {e}")
            self._connected = False
            return None
    
    def write_register(self, address: int, value: int) -> bool:
        if not self.is_connected:
            return False
        try:
            result = self._client.write_register(
                address=address, value=value, device_id=self.slave_id
            )
            return not result.isError()
        except ModbusException as e:
            logger.error(f"Error writing register {address}: {e}")
            return False
    
    async def poll_environment_data(self):
        while True:
            if self.is_connected:
                try:
                    # 读取所有寄存器
                    self.all_registers_data = {}
                    self.grouped_data = {}
                    
                    for address, info in reg.REGISTERS.items():
                        raw_value = self.read_register(address)
                        scaled_value = reg.scale_value(raw_value or 0, address)
                        
                        self.all_registers_data[address] = {
                            "name": info["name"],
                            "address": address,
                            "raw": raw_value,
                            "value": scaled_value,
                            "unit": info["unit"],
                            "rw": info["rw"],
                            "desc": info["desc"],
                            "group": info["group"],
                        }
                        
                        # 按分组存储
                        group = info["group"]
                        if group not in self.grouped_data:
                            self.grouped_data[group] = {}
                        self.grouped_data[group][address] = {
                            "name": info["name"],
                            "address": address,
                            "raw": raw_value,
                            "value": scaled_value,
                            "unit": info["unit"],
                            "rw": info["rw"],
                            "desc": info["desc"],
                        }
                        
                except Exception as e:
                    logger.error(f"Error polling data: {e}")
            
            await asyncio.sleep(3)
    
    def get_status(self) -> dict:
        return {"connected": self.is_connected, "host": self.host, "port": self.port}
    
    def get_all_registers(self) -> dict:
        """获取所有寄存器数据"""
        return self.all_registers_data
    
    def get_grouped_data(self) -> dict:
        """获取按分组的数据"""
        return self.grouped_data
    
    def get_environment(self) -> dict:
        """获取环境数据（兼容旧接口）"""
        env_group = self.grouped_data.get("environment", {})
        result = {}
        for addr, data in env_group.items():
            name_map = {
                "室内 PM2.5": "pm25",
                "室内 CO2": "co2",
                "室外温度": "outdoor_temp",
                "室外湿度": "outdoor_humidity",
            }
            key = name_map.get(data["name"])
            if key:
                result[key] = data["value"]
        return result
    
    def get_system(self) -> dict:
        """获取系统数据（返回完整寄存器信息）"""
        sys_group = self.grouped_data.get("system", {})
        result = {}
        for addr, data in sys_group.items():
            name_map = {
                "系统总电源": "power",
                "在家/离家模式": "home_mode",
                "运行模式": "run_mode",
                "新风风速设定": "fan_speed",
            }
            key = name_map.get(data["name"])
            if key:
                result[key] = data
        return result
    
    def get_rooms(self) -> dict:
        """获取房间数据（返回完整寄存器信息）"""
        result = {}
        for room_id, room_info in reg.ROOMS.items():
            group_data = self.grouped_data.get(room_id, {})
            result[room_id] = {
                "temp": group_data.get(room_info["temp"], {}),
                "humidity": group_data.get(room_info["humidity"], {}),
                "dew_point": group_data.get(room_info["dew_point"], {}),
                "setpoint": group_data.get(room_info["setpoint"], {}),
            }
        return result
    
    def set_power(self, on: bool) -> bool:
        """设置系统总电源"""
        return self.write_register(reg.RegisterAddress.SYSTEM_POWER, 1 if on else 0)
    
    def set_home_mode(self, home: bool) -> bool:
        """设置在家/离家模式"""
        return self.write_register(reg.RegisterAddress.HOME_MODE, 1 if home else 0)
    
    def set_run_mode(self, mode: int) -> bool:
        """设置运行模式"""
        return self.write_register(reg.RegisterAddress.RUN_MODE, mode)
    
    def set_fan_speed(self, speed: int) -> bool:
        """设置新风风速"""
        return self.write_register(reg.RegisterAddress.FAN_SPEED, speed)
    
    def set_room_setpoint(self, room_id: str, temp: float) -> bool:
        if room_id not in reg.ROOMS:
            logger.warning(f"Unknown room_id: {room_id}")
            return False
        setpoint_addr = reg.ROOMS[room_id]["setpoint"]
        value = reg.unscale_value(temp, setpoint_addr)
        logger.info(f"Setting {room_id} temperature: {temp}°C -> register {setpoint_addr} = {value}")
        result = self.write_register(setpoint_addr, value)
        logger.info(f"Write result: {result}")
        return result
    
    def write_register_by_address(self, address: int, value: float) -> bool:
        """通过地址写入寄存器"""
        if address not in reg.REGISTERS:
            return False
        if reg.REGISTERS[address]["rw"] != "RW":
            return False
        raw_value = reg.unscale_value(value, address)
        return self.write_register(address, raw_value)
