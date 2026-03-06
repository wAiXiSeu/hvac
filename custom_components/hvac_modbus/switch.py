"""Switch platform for HVAC Modbus integration."""

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, ROOM_IDS, ROOM_NAMES
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
    modbus = data["modbus"]
    
    entities = [
        HVACPowerSwitch(coordinator, modbus),
        HVACHomeModeSwitch(coordinator, modbus),
        HVACKitchenRadiantSwitch(coordinator, modbus),
        HVACHumidifierSwitch(coordinator, modbus),
    ]
    
    # 新增房间辐射开关
    for room_id in ROOM_IDS:
        room_name = ROOM_NAMES.get(room_id, room_id)
        entities.append(HVACRoomRadiantSwitch(coordinator, modbus, room_id, room_name))
    
    async_add_entities(entities)


class HVACPowerSwitch(SwitchEntity):
    """Switch entity for HVAC system power."""

    _attr_has_entity_name = True
    _attr_unique_id = "hvac_system_power"
    _attr_name = "系统电源"
    _attr_icon = "mdi:power"

    def __init__(self, coordinator: HVACDataCoordinator, modbus) -> None:
        """Initialize the switch."""
        self.coordinator = coordinator
        self._modbus = modbus

    @property
    def is_on(self) -> bool:
        """Return True if entity is on."""
        system_data = self.coordinator.get_system_data()
        return system_data.get("power", False)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        await self._modbus.set_system_power(True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        await self._modbus.set_system_power(False)
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


class HVACHomeModeSwitch(SwitchEntity):
    """Switch entity for home mode."""

    _attr_has_entity_name = True
    _attr_unique_id = "hvac_home_mode"
    _attr_name = "在家模式"
    _attr_icon = "mdi:home"

    def __init__(self, coordinator: HVACDataCoordinator, modbus) -> None:
        """Initialize the switch."""
        self.coordinator = coordinator
        self._modbus = modbus

    @property
    def is_on(self) -> bool:
        """Return True if entity is on."""
        system_data = self.coordinator.get_system_data()
        return system_data.get("home_mode", False)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        await self._modbus.set_home_mode(True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        await self._modbus.set_home_mode(False)
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


class HVACKitchenRadiantSwitch(SwitchEntity):
    """Switch entity for kitchen radiant."""

    _attr_has_entity_name = True
    _attr_unique_id = "hvac_kitchen_radiant"
    _attr_name = "厨卫辐射"
    _attr_icon = "mdi:radiator"

    def __init__(self, coordinator: HVACDataCoordinator, modbus) -> None:
        """Initialize the switch."""
        self.coordinator = coordinator
        self._modbus = modbus

    @property
    def is_on(self) -> bool:
        """Return True if entity is on."""
        kitchen_data = self.coordinator.get_kitchen_data()
        return kitchen_data.get("radiant", False)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        await self._modbus.set_kitchen_radiant(True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        await self._modbus.set_kitchen_radiant(False)
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


class HVACHumidifierSwitch(SwitchEntity):
    """Switch entity for humidifier."""

    _attr_has_entity_name = True
    _attr_unique_id = "hvac_humidifier"
    _attr_name = "加湿功能"
    _attr_icon = "mdi:water"

    def __init__(self, coordinator: HVACDataCoordinator, modbus) -> None:
        """Initialize the switch."""
        self.coordinator = coordinator
        self._modbus = modbus

    @property
    def is_on(self) -> bool:
        """Return True if entity is on."""
        fresh_air_data = self.coordinator.get_fresh_air_data()
        return fresh_air_data.get("humidifier", False)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        await self._modbus.set_humidifier(True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        await self._modbus.set_humidifier(False)
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


class HVACRoomRadiantSwitch(SwitchEntity):
    """Switch entity for room radiant."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:radiator"

    def __init__(self, coordinator: HVACDataCoordinator, modbus, room_id: str, room_name: str) -> None:
        """Initialize the switch."""
        self.coordinator = coordinator
        self._modbus = modbus
        self._room_id = room_id
        self._attr_unique_id = f"hvac_{room_id}_radiant"
        self._attr_name = f"{room_name}辐射"

    @property
    def is_on(self) -> bool:
        """Return True if entity is on."""
        room_data = self.coordinator.get_room_data(self._room_id)
        if room_data:
            return room_data.get("radiant", False)
        return False

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        await self._modbus.set_room_radiant(self._room_id, True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        await self._modbus.set_room_radiant(self._room_id, False)
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
