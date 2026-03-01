"""Switch platform for HVAC Modbus integration."""

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, REGISTER_ADDRESSES
from .coordinator import HVACDataCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up HVAC switch platform."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    
    entities = [
        HVACSystemSwitch(coordinator, "系统电源", "system_power", "system"),
        HVACSystemSwitch(coordinator, "在家模式", "home_mode", "system"),
        HVACRegisterSwitch(coordinator, "厨卫辐射", "kitchen_radiant", REGISTER_ADDRESSES["kitchen_radiant"]),
        HVACRegisterSwitch(coordinator, "加湿功能", "humidifier", REGISTER_ADDRESSES["humidifier"]),
    ]
    
    async_add_entities(entities)


class HVACSystemSwitch(SwitchEntity):
    """Switch entity for HVAC system control."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: HVACDataCoordinator,
        name: str,
        key: str,
        group: str,
    ) -> None:
        """Initialize the switch."""
        self.coordinator = coordinator
        self._key = key
        self._group = group
        self._attr_unique_id = f"hvac_{key}"
        self._attr_name = name
        self._attr_icon = "mdi:power" if "power" in key else "mdi:home"

    @property
    def is_on(self) -> bool:
        """Return True if entity is on."""
        if self._group == "system":
            system_data = self.coordinator.get_system_data()
            key_data = system_data.get(self._key, {})
            return key_data.get("value", 0) == 1
        return False

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        if self._group == "system":
            if self._key == "system_power":
                await self.coordinator.api.set_system(power=True)
            elif self._key == "home_mode":
                await self.coordinator.api.set_system(home_mode=True)
            await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        if self._group == "system":
            if self._key == "system_power":
                await self.coordinator.api.set_system(power=False)
            elif self._key == "home_mode":
                await self.coordinator.api.set_system(home_mode=False)
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
        if self._group == "system":
            system_data = self.coordinator.get_system_data()
            key_data = system_data.get(self._key, {})
            if key_data:
                attrs["register_address"] = key_data.get("address")
                attrs["raw_value"] = key_data.get("raw")
        return attrs


class HVACRegisterSwitch(SwitchEntity):
    """Switch entity for register-based controls."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: HVACDataCoordinator,
        name: str,
        unique_id_suffix: str,
        register_address: int,
    ) -> None:
        """Initialize the switch."""
        self.coordinator = coordinator
        self._register_address = register_address
        self._attr_unique_id = f"hvac_{unique_id_suffix}"
        self._attr_name = name
        self._attr_icon = "mdi:water" if "humidifier" in unique_id_suffix else "mdi:radiator"

    @property
    def register_data(self) -> dict[str, Any] | None:
        """Get register data."""
        return self.coordinator.get_register_data(self._register_address)

    @property
    def is_on(self) -> bool:
        """Return True if entity is on."""
        if self.register_data:
            return self.register_data.get("value", 0) == 1
        return False

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        await self.coordinator.api.write_register(self._register_address, 1)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        await self.coordinator.api.write_register(self._register_address, 0)
        await self.coordinator.async_request_refresh()

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success and self.register_data is not None

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        attrs = {}
        if self.register_data:
            attrs["register_address"] = self.register_data.get("address")
            attrs["raw_value"] = self.register_data.get("raw")
            attrs["description"] = self.register_data.get("desc")
        return attrs
