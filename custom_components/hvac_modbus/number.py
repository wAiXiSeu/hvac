"""Number platform for HVAC Modbus integration."""

import logging
from typing import Any

from homeassistant.components.number import NumberEntity, NumberDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfTemperature
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
    """Set up HVAC number platform."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    
    entities = [
        HVACFanSpeedNumber(coordinator),
        HVACRegisterNumber(
            coordinator,
            "制热供水设定点",
            "heating_setpoint",
            REGISTER_ADDRESSES["heating_setpoint"],
            NumberDeviceClass.TEMPERATURE,
            UnitOfTemperature.CELSIUS,
            30.0,
            60.0,
            0.5,
        ),
        HVACRegisterNumber(
            coordinator,
            "制冷供水设定点",
            "cooling_setpoint",
            REGISTER_ADDRESSES["cooling_setpoint"],
            NumberDeviceClass.TEMPERATURE,
            UnitOfTemperature.CELSIUS,
            5.0,
            30.0,
            0.5,
        ),
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

    def __init__(self, coordinator: HVACDataCoordinator) -> None:
        """Initialize the number."""
        self.coordinator = coordinator

    @property
    def native_value(self) -> float | None:
        """Return the current value."""
        system_data = self.coordinator.get_system_data()
        fan_speed_data = system_data.get("fan_speed", {})
        return fan_speed_data.get("value")

    async def async_set_native_value(self, value: float) -> None:
        """Set the value."""
        await self.coordinator.api.set_system(fan_speed=int(value))
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
        fan_speed_data = system_data.get("fan_speed", {})
        if fan_speed_data:
            attrs["register_address"] = fan_speed_data.get("address")
            attrs["raw_value"] = fan_speed_data.get("raw")
            attrs["description"] = fan_speed_data.get("desc")
        return attrs


class HVACRegisterNumber(NumberEntity):
    """Number entity for register-based values."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: HVACDataCoordinator,
        name: str,
        unique_id_suffix: str,
        register_address: int,
        device_class: NumberDeviceClass | None,
        unit: str | None,
        min_value: float,
        max_value: float,
        step: float,
    ) -> None:
        """Initialize the number."""
        self.coordinator = coordinator
        self._register_address = register_address
        self._attr_unique_id = f"hvac_{unique_id_suffix}"
        self._attr_name = name
        self._attr_device_class = device_class
        self._attr_native_unit_of_measurement = unit
        self._attr_native_min_value = min_value
        self._attr_native_max_value = max_value
        self._attr_native_step = step
        self._attr_icon = "mdi:thermometer"

    @property
    def register_data(self) -> dict[str, Any] | None:
        """Get register data."""
        return self.coordinator.get_register_data(self._register_address)

    @property
    def native_value(self) -> float | None:
        """Return the current value."""
        if self.register_data:
            return self.register_data.get("value")
        return None

    async def async_set_native_value(self, value: float) -> None:
        """Set the value."""
        await self.coordinator.api.write_register(self._register_address, value)
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
