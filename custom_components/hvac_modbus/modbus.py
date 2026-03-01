"""Async Modbus TCP Client for HVAC integration."""

import asyncio
import logging
from typing import Any

from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ModbusException

from .registers import REGISTERS, ROOMS, REGISTER_RANGES, scale_value, unscale_value

_LOGGER = logging.getLogger(__name__)


class HVACModbusError(Exception):
    """Exception for HVAC Modbus errors."""
    pass


class HVACModbusClient:
    """Async Modbus TCP client for HVAC system."""

    def __init__(
        self,
        host: str,
        port: int = 502,
        slave_id: int = 1,
        timeout: float = 5.0,
    ):
        """Initialize the Modbus client."""
        self._host = host
        self._port = port
        self._slave_id = slave_id
        self._timeout = timeout
        self._client: AsyncModbusTcpClient | None = None
        self._lock = asyncio.Lock()
        self._connected = False

    @property
    def host(self) -> str:
        """Return the host."""
        return self._host

    @property
    def port(self) -> int:
        """Return the port."""
        return self._port

    @property
    def is_connected(self) -> bool:
        """Return connection status."""
        return self._connected and self._client is not None and self._client.connected

    async def connect(self) -> bool:
        """Connect to the Modbus device."""
        try:
            self._client = AsyncModbusTcpClient(
                host=self._host,
                port=self._port,
                timeout=self._timeout,
            )
            self._connected = await self._client.connect()
            if self._connected:
                _LOGGER.info("Connected to Modbus device at %s:%s", self._host, self._port)
            else:
                _LOGGER.error("Failed to connect to Modbus device at %s:%s", self._host, self._port)
            return self._connected
        except Exception as err:
            _LOGGER.error("Error connecting to Modbus device: %s", err)
            self._connected = False
            return False

    async def disconnect(self) -> None:
        """Disconnect from the Modbus device."""
        if self._client:
            self._client.close()
            self._connected = False
            _LOGGER.info("Disconnected from Modbus device")

    async def _reconnect(self) -> bool:
        """Attempt to reconnect."""
        _LOGGER.info("Attempting to reconnect to Modbus device...")
        await self.disconnect()
        await asyncio.sleep(1)
        return await self.connect()

    async def read_registers(self, address: int, count: int) -> list[int] | None:
        """Read holding registers from the device."""
        if not self.is_connected:
            if not await self._reconnect():
                return None

        async with self._lock:
            try:
                result = await self._client.read_holding_registers(
                    address=address,
                    count=count,
                    device_id=self._slave_id,
                )
                if result.isError():
                    _LOGGER.error("Modbus read error at address %s: %s", address, result)
                    return None
                return list(result.registers)
            except ModbusException as err:
                _LOGGER.error("Modbus exception reading address %s: %s", address, err)
                self._connected = False
                return None
            except Exception as err:
                _LOGGER.error("Unexpected error reading address %s: %s", address, err)
                self._connected = False
                return None

    async def write_register(self, address: int, value: int) -> bool:
        """Write a single holding register."""
        if not self.is_connected:
            if not await self._reconnect():
                return False

        async with self._lock:
            try:
                result = await self._client.write_register(
                    address=address,
                    value=value,
                    device_id=self._slave_id,
                )
                if result.isError():
                    _LOGGER.error("Modbus write error at address %s: %s", address, result)
                    return False
                _LOGGER.debug("Successfully wrote value %s to address %s", value, address)
                return True
            except ModbusException as err:
                _LOGGER.error("Modbus exception writing address %s: %s", address, err)
                self._connected = False
                return False
            except Exception as err:
                _LOGGER.error("Unexpected error writing address %s: %s", address, err)
                self._connected = False
                return False

    async def read_all_data(self) -> dict[str, Any]:
        """Read all register data and return structured data."""
        raw_data: dict[int, int] = {}
        
        # Read all register ranges
        for start_address, count in REGISTER_RANGES:
            registers = await self.read_registers(start_address, count)
            if registers:
                for i, value in enumerate(registers):
                    raw_data[start_address + i] = value

        # Parse raw data into structured format
        return self._parse_data(raw_data)

    def _parse_data(self, raw_data: dict[int, int]) -> dict[str, Any]:
        """Parse raw register data into structured format."""
        result = {
            "connected": self.is_connected,
            "rooms": [],
            "system": {},
            "environment": {},
            "york": {},
            "fresh_air": {},
            "registers": {},
        }

        # Parse room data
        for room_id, room_config in ROOMS.items():
            room_data = {
                "id": room_id,
                "name": room_config["name"],
                "temp": self._get_scaled_value(raw_data, room_config["temp"]),
                "humidity": self._get_scaled_value(raw_data, room_config["humidity"]),
                "dew_point": self._get_scaled_value(raw_data, room_config["dew_point"]),
                "setpoint": self._get_scaled_value(raw_data, room_config["setpoint"]),
            }
            result["rooms"].append(room_data)

        # Parse system data
        result["system"] = {
            "power": raw_data.get(1033, 0) == 1,
            "home_mode": raw_data.get(1034, 0) == 1,
            "run_mode": raw_data.get(1041, 1),
            "fan_speed": raw_data.get(1047, 0),
        }

        # Parse environment data
        result["environment"] = {
            "indoor_pm25": self._get_scaled_value(raw_data, 1024),
            "indoor_co2": self._get_scaled_value(raw_data, 1026),
            "outdoor_temp": self._get_scaled_value(raw_data, 1027),
            "outdoor_humidity": self._get_scaled_value(raw_data, 1028),
        }

        # Parse york data
        result["york"] = {
            "supply_temp": self._get_scaled_value(raw_data, 1029),
            "return_temp": self._get_scaled_value(raw_data, 1030),
            "heating_setpoint": self._get_scaled_value(raw_data, 1062),
            "cooling_setpoint": self._get_scaled_value(raw_data, 1066),
        }

        # Parse fresh air data
        result["fresh_air"] = {
            "compressor_freq": self._get_scaled_value(raw_data, 1161),
            "supply_temp": self._get_scaled_value(raw_data, 1164),
            "return_temp": self._get_scaled_value(raw_data, 1165),
            "humidifier": raw_data.get(1168, 0) == 1,
        }

        # Parse kitchen data
        result["kitchen"] = {
            "radiant": raw_data.get(1133, 0) == 1,
        }

        # Build grouped registers for compatibility
        for address, value in raw_data.items():
            if address in REGISTERS:
                reg_info = REGISTERS[address]
                group = reg_info.get("group", "unknown")
                if group not in result["registers"]:
                    result["registers"][group] = {}
                result["registers"][group][address] = {
                    "address": address,
                    "name": reg_info["name"],
                    "value": scale_value(value, address),
                    "raw": value,
                    "unit": reg_info.get("unit", ""),
                    "desc": reg_info.get("desc", ""),
                }

        return result

    def _get_scaled_value(self, raw_data: dict[int, int], address: int) -> float | None:
        """Get scaled value from raw data."""
        if address in raw_data:
            return scale_value(raw_data[address], address)
        return None

    async def set_room_setpoint(self, room_id: str, temperature: float) -> bool:
        """Set room temperature setpoint."""
        if room_id not in ROOMS:
            _LOGGER.error("Invalid room_id: %s", room_id)
            return False
        
        address = ROOMS[room_id]["setpoint"]
        raw_value = unscale_value(temperature, address)
        return await self.write_register(address, raw_value)

    async def set_system_power(self, power: bool) -> bool:
        """Set system power."""
        return await self.write_register(1033, 1 if power else 0)

    async def set_home_mode(self, home_mode: bool) -> bool:
        """Set home mode."""
        return await self.write_register(1034, 1 if home_mode else 0)

    async def set_run_mode(self, mode: int) -> bool:
        """Set run mode (1=cooling, 2=heating, 3=ventilation, 4=dehumidification)."""
        if mode not in [1, 2, 3, 4]:
            _LOGGER.error("Invalid run mode: %s", mode)
            return False
        return await self.write_register(1041, mode)

    async def set_fan_speed(self, speed: int) -> bool:
        """Set fan speed (0-100%)."""
        if not 0 <= speed <= 100:
            _LOGGER.error("Invalid fan speed: %s", speed)
            return False
        return await self.write_register(1047, speed)

    async def set_kitchen_radiant(self, on: bool) -> bool:
        """Set kitchen radiant."""
        return await self.write_register(1133, 1 if on else 0)

    async def set_humidifier(self, on: bool) -> bool:
        """Set humidifier."""
        return await self.write_register(1168, 1 if on else 0)

    async def set_heating_setpoint(self, temperature: float) -> bool:
        """Set heating supply water setpoint."""
        raw_value = unscale_value(temperature, 1062)
        return await self.write_register(1062, raw_value)

    async def set_cooling_setpoint(self, temperature: float) -> bool:
        """Set cooling supply water setpoint."""
        raw_value = unscale_value(temperature, 1066)
        return await self.write_register(1066, raw_value)

    async def test_connection(self) -> bool:
        """Test connection to the Modbus device."""
        if not await self.connect():
            return False
        # Try reading a register to verify communication
        registers = await self.read_registers(1024, 1)
        return registers is not None
