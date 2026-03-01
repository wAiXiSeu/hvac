"""Data coordinator for HVAC integration."""

import logging
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .modbus import HVACModbusClient, HVACModbusError
from .const import DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class HVACDataCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator to manage HVAC data updates via Modbus."""

    def __init__(
        self,
        hass: HomeAssistant,
        modbus: HVACModbusClient,
        scan_interval: int = DEFAULT_SCAN_INTERVAL,
    ) -> None:
        """Initialize the coordinator."""
        self.modbus = modbus
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=scan_interval),
        )
        self._scan_interval = scan_interval

    @property
    def connected(self) -> bool:
        """Return if the Modbus device is connected."""
        return self.modbus.is_connected

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from Modbus device."""
        try:
            # Read all data from Modbus
            data = await self.modbus.read_all_data()
            
            if not data.get("connected", False):
                _LOGGER.warning("Modbus device not connected, attempting reconnect...")
                
            return data
        except Exception as err:
            _LOGGER.error("Error reading from Modbus device: %s", err)
            raise UpdateFailed(f"Error communicating with Modbus: {err}") from err

    def get_room_data(self, room_id: str) -> dict[str, Any] | None:
        """Get data for a specific room."""
        if not self.data:
            return None
        rooms = self.data.get("rooms", [])
        for room in rooms:
            if room.get("id") == room_id:
                return room
        return None

    def get_system_data(self) -> dict[str, Any]:
        """Get system control data."""
        if not self.data:
            return {}
        return self.data.get("system", {})

    def get_environment_data(self) -> dict[str, Any]:
        """Get environment data."""
        if not self.data:
            return {}
        return self.data.get("environment", {})

    def get_york_data(self) -> dict[str, Any]:
        """Get york data."""
        if not self.data:
            return {}
        return self.data.get("york", {})

    def get_fresh_air_data(self) -> dict[str, Any]:
        """Get fresh air data."""
        if not self.data:
            return {}
        return self.data.get("fresh_air", {})

    def get_kitchen_data(self) -> dict[str, Any]:
        """Get kitchen data."""
        if not self.data:
            return {}
        return self.data.get("kitchen", {})

    def get_registers_by_group(self, group: str) -> dict[str, Any]:
        """Get registers for a specific group."""
        if not self.data:
            return {}
        registers = self.data.get("registers", {})
        return registers.get(group, {})

    def get_register_value(self, group: str, register_name: str) -> Any:
        """Get a specific register value."""
        registers = self.get_registers_by_group(group)
        for addr, data in registers.items():
            if data.get("name") == register_name:
                return data.get("value")
        return None

    def get_register_data(self, address: int) -> dict[str, Any] | None:
        """Get register data by address."""
        if not self.data:
            return None
        for group_data in self.data.get("registers", {}).values():
            if address in group_data:
                return group_data[address]
        return None
