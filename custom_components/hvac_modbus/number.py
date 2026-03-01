"""Number platform for HVAC Modbus integration."""

import logging
from typing import Any

from homeassistant.components.number import NumberEntity, NumberDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import HVACDataCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up HVAC number platform."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    modbus = data["modbus"]
    
    entities = [
        HVACFanSpeedNumber(coordinator, modbus),
        HVACHeatingSetpointNumber(coordinator, modbus),
        HVACCoolingSetpointNumber(coordinator, modbus),
    ]
    
    async_add_entities(entities)


class HVACFanSpeedNumber(NumberEntity):
    """Number entity for fan speed control."""

    _attr_has_entity_name = True
    _attr_name = "新风风速"
    _attr_unique_id = "hvac_fan_speed"
    _attr_device_class = NumberDeviceClass.POWER_FACTOR
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_native_min_value = 0.0
    _attr_native_max_value = 100.0
    _attr_native_step = 5.0
    _attr_icon = "mdi:fan"

    def __init__(self, coordinator: HVACDataCoordinator, modbus) -> None:
        """Initialize the number."""
        self.coordinator = coordinator
        self._modbus = modbus

    @property
    def native_value(self) -> float | None:
        """Return the current value."""
        system_data = self.coordinator.get_system_data()
        return system_data.get("fan_speed")

    async def async_set_native_value(self, value: float) -> None:
        """Set the value."""
        await self._modbus.set_fan_speed(int(value))
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


class HVACHeatingSetpointNumber(NumberEntity):
    """Number entity for heating setpoint."""

    _attr_has_entity_name = True
    _attr_name = "制热供水设定点"
    _attr_unique_id = "hvac_heating_setpoint"
    _attr_device_class = NumberDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_native_min_value = 30.0
    _attr_native_max_value = 60.0
    _attr_native_step = 0.5
    _attr_icon = "mdi:thermometer"

    def __init__(self, coordinator: HVACDataCoordinator, modbus) -> None:
        """Initialize the number."""
        self.coordinator = coordinator
        self._modbus = modbus

    @property
    def native_value(self) -> float | None:
        """Return the current value."""
        york_data = self.coordinator.get_york_data()
        return york_data.get("heating_setpoint")

    async def async_set_native_value(self, value: float) -> None:
        """Set the value."""
        await self._modbus.set_heating_setpoint(value)
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


class HVACCoolingSetpointNumber(NumberEntity):
    """Number entity for cooling setpoint."""

    _attr_has_entity_name = True
    _attr_name = "制冷供水设定点"
    _attr_unique_id = "hvac_cooling_setpoint"
    _attr_device_class = NumberDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_native_min_value = 5.0
    _attr_native_max_value = 30.0
    _attr_native_step = 0.5
    _attr_icon = "mdi:thermometer"

    def __init__(self, coordinator: HVACDataCoordinator, modbus) -> None:
        """Initialize the number."""
        self.coordinator = coordinator
        self._modbus = modbus

    @property
    def native_value(self) -> float | None:
        """Return the current value."""
        york_data = self.coordinator.get_york_data()
        return york_data.get("cooling_setpoint")

    async def async_set_native_value(self, value: float) -> None:
        """Set the value."""
        await self._modbus.set_cooling_setpoint(value)
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
