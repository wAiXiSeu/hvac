"""Select platform for HVAC Modbus integration."""

import logging
from typing import Any

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, RUN_MODES, RUN_MODE_REVERSE
from .coordinator import HVACDataCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up HVAC select platform."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    
    entities = [
        HVACRunModeSelect(coordinator),
    ]
    
    async_add_entities(entities)


class HVACRunModeSelect(SelectEntity):
    """Select entity for run mode."""

    _attr_has_entity_name = True
    _attr_name = "运行模式"
    _attr_unique_id = "hvac_run_mode"
    _attr_icon = "mdi:air-conditioner"
    _attr_options = list(RUN_MODE_REVERSE.keys())

    def __init__(self, coordinator: HVACDataCoordinator) -> None:
        """Initialize the select."""
        self.coordinator = coordinator

    @property
    def current_option(self) -> str | None:
        """Return the current option."""
        system_data = self.coordinator.get_system_data()
        run_mode_data = system_data.get("run_mode", {})
        run_mode = run_mode_data.get("value")
        
        if run_mode and run_mode in RUN_MODES:
            return RUN_MODES[run_mode]
        return None

    async def async_select_option(self, option: str) -> None:
        """Set the option."""
        if option in RUN_MODE_REVERSE:
            run_mode = RUN_MODE_REVERSE[option]
            await self.coordinator.api.set_system(run_mode=run_mode)
            await self.coordinator.async_request_refresh()

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        attrs = {}
        system_data = self.coordinator.get_system_data()
        run_mode_data = system_data.get("run_mode", {})
        if run_mode_data:
            attrs["register_address"] = run_mode_data.get("address")
            attrs["raw_value"] = run_mode_data.get("raw")
            attrs["description"] = run_mode_data.get("desc")
        return attrs
