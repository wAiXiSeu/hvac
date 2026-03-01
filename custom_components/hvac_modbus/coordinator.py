"""Data coordinator for HVAC integration."""

import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import HVACApiClient, HVACApiError
from .const import DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class HVACDataCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator to manage HVAC data updates."""

    def __init__(
        self,
        hass: HomeAssistant,
        api: HVACApiClient,
        scan_interval: int = DEFAULT_SCAN_INTERVAL,
    ) -> None:
        """Initialize the coordinator."""
        self.api = api
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=None,  # We'll set this in async_config_entry_first_refresh
        )
        self._scan_interval = scan_interval
        self._connected = False

    @property
    def connected(self) -> bool:
        """Return if the backend is connected."""
        return self._connected

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from API endpoint."""
        try:
            # Fetch all data in parallel
            rooms = await self.api.get_rooms()
            system = await self.api.get_system()
            registers = await self.api.get_grouped_registers()
            status = await self.api.get_status()
            
            self._connected = status.get("connected", False)
            
            return {
                "rooms": rooms,
                "system": system,
                "registers": registers,
                "status": status,
                "connected": self._connected,
            }
        except HVACApiError as err:
            self._connected = False
            raise UpdateFailed(f"Error communicating with API: {err}") from err

    def get_room_data(self, room_id: str) -> dict[str, Any] | None:
        """Get data for a specific room."""
        rooms = self.data.get("rooms", [])
        for room in rooms:
            if room.get("id") == room_id:
                return room
        return None

    def get_system_data(self) -> dict[str, Any]:
        """Get system control data."""
        return self.data.get("system", {})

    def get_registers_by_group(self, group: str) -> dict[str, Any]:
        """Get registers for a specific group."""
        registers = self.data.get("registers", {})
        group_data = registers.get(group, {})
        return group_data.get("registers", {})

    def get_register_value(self, group: str, register_name: str) -> Any:
        """Get a specific register value."""
        registers = self.get_registers_by_group(group)
        for addr, data in registers.items():
            if data.get("name") == register_name:
                return data.get("value")
        return None

    def get_register_data(self, address: int) -> dict[str, Any] | None:
        """Get register data by address."""
        for group_data in self.data.get("registers", {}).values():
            registers = group_data.get("registers", {})
            if address in registers:
                return registers[address]
        return None
