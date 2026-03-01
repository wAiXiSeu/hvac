"""Sensor platform for HVAC Modbus integration."""

import logging
from typing import Any

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfTemperature, CONCENTRATION_PARTS_PER_MILLION, CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, UnitOfFrequency
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
    """Set up HVAC sensor platform."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    
    entities = []
    
    # Environment sensors
    entities.extend([
        HVACSensor(coordinator, "environment", "室内 PM2.5", "indoor_pm25", SensorDeviceClass.PM25, CONCENTRATION_MICROGRAMS_PER_CUBIC_METER),
        HVACSensor(coordinator, "environment", "室内 CO2", "indoor_co2", SensorDeviceClass.CO2, CONCENTRATION_PARTS_PER_MILLION),
        HVACSensor(coordinator, "environment", "室外温度", "outdoor_temp", SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS),
        HVACSensor(coordinator, "environment", "室外湿度", "outdoor_humidity", SensorDeviceClass.HUMIDITY, PERCENTAGE),
    ])
    
    # Room sensors
    for room_id in ROOM_IDS:
        room_name = ROOM_NAMES.get(room_id, room_id)
        entities.extend([
            HVACSensor(coordinator, room_id, f"{room_name}实际温度", f"{room_id}_temp", SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS),
            HVACSensor(coordinator, room_id, f"{room_name}实际湿度", f"{room_id}_humidity", SensorDeviceClass.HUMIDITY, PERCENTAGE),
            HVACSensor(coordinator, room_id, f"{room_name}露点温度", f"{room_id}_dew_point", SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS),
        ])
    
    # York sensors
    entities.extend([
        HVACSensor(coordinator, "york", "约克供水温度", "york_supply_temp", SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS),
        HVACSensor(coordinator, "york", "约克回水温度", "york_return_temp", SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS),
    ])
    
    # Fresh air sensors
    entities.extend([
        HVACSensor(coordinator, "fresh_air", "新风压缩机频率", "fresh_air_compressor_freq", SensorDeviceClass.FREQUENCY, UnitOfFrequency.HERTZ),
        HVACSensor(coordinator, "fresh_air", "新风内部供水温", "fresh_air_supply_temp", SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS),
        HVACSensor(coordinator, "fresh_air", "新风内部回水温", "fresh_air_return_temp", SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS),
    ])
    
    # Connection status sensor
    entities.append(HVACConnectionSensor(coordinator))
    
    async_add_entities(entities)


class HVACSensor(SensorEntity):
    """Sensor entity for HVAC data."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: HVACDataCoordinator,
        group: str,
        register_name: str,
        unique_id_suffix: str,
        device_class: SensorDeviceClass | None,
        unit: str | None,
    ) -> None:
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._group = group
        self._register_name = register_name
        self._attr_unique_id = f"hvac_{unique_id_suffix}"
        self._attr_name = register_name
        self._attr_device_class = device_class
        self._attr_native_unit_of_measurement = unit
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> float | None:
        """Return the native value."""
        registers = self.coordinator.get_registers_by_group(self._group)
        for addr, data in registers.items():
            if data.get("name") == self._register_name:
                return data.get("value")
        return None

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
        registers = self.coordinator.get_registers_by_group(self._group)
        for addr, data in registers.items():
            if data.get("name") == self._register_name:
                attrs["register_address"] = data.get("address")
                attrs["raw_value"] = data.get("raw")
                attrs["unit"] = data.get("unit")
                attrs["description"] = data.get("desc")
                break
        return attrs


class HVACConnectionSensor(SensorEntity):
    """Sensor for connection status."""

    _attr_has_entity_name = True
    _attr_name = "HVAC 连接状态"
    _attr_unique_id = "hvac_connection_status"
    _attr_icon = "mdi:connection"

    def __init__(self, coordinator: HVACDataCoordinator) -> None:
        """Initialize the sensor."""
        self.coordinator = coordinator

    @property
    def native_value(self) -> str:
        """Return the connection status."""
        return "connected" if self.coordinator.connected else "disconnected"

    @property
    def available(self) -> bool:
        """Always available."""
        return True

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        status = self.coordinator.data.get("status", {})
        return {
            "host": status.get("host"),
            "port": status.get("port"),
        }
