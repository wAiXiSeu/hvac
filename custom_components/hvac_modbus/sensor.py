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
        HVACEnvironmentSensor(coordinator, "indoor_pm25", "室内 PM2.5", SensorDeviceClass.PM25, CONCENTRATION_MICROGRAMS_PER_CUBIC_METER),
        HVACEnvironmentSensor(coordinator, "indoor_co2", "室内 CO2", SensorDeviceClass.CO2, CONCENTRATION_PARTS_PER_MILLION),
        HVACEnvironmentSensor(coordinator, "outdoor_temp", "室外温度", SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS),
        HVACEnvironmentSensor(coordinator, "outdoor_humidity", "室外湿度", SensorDeviceClass.HUMIDITY, PERCENTAGE),
    ])
    
    # Room sensors
    for room_id in ROOM_IDS:
        room_name = ROOM_NAMES.get(room_id, room_id)
        entities.extend([
            HVACRoomSensor(coordinator, room_id, "temp", f"{room_name}温度", SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS),
            HVACRoomSensor(coordinator, room_id, "humidity", f"{room_name}湿度", SensorDeviceClass.HUMIDITY, PERCENTAGE),
            HVACRoomSensor(coordinator, room_id, "dew_point", f"{room_name}露点", SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS),
        ])
    
    # York sensors
    entities.extend([
        HVACYorkSensor(coordinator, "supply_temp", "约克供水温度", SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS),
        HVACYorkSensor(coordinator, "return_temp", "约克回水温度", SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS),
    ])
    
    # Fresh air sensors
    entities.extend([
        HVACFreshAirSensor(coordinator, "compressor_freq", "新风压缩机频率", SensorDeviceClass.FREQUENCY, UnitOfFrequency.HERTZ),
        HVACFreshAirSensor(coordinator, "supply_temp", "新风供水温度", SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS),
        HVACFreshAirSensor(coordinator, "return_temp", "新风回水温度", SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS),
    ])
    
    # Connection status sensor
    entities.append(HVACConnectionSensor(coordinator))
    
    async_add_entities(entities)


class HVACRoomSensor(SensorEntity):
    """Sensor entity for room data."""

    _attr_has_entity_name = True
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self,
        coordinator: HVACDataCoordinator,
        room_id: str,
        data_key: str,
        name: str,
        device_class: SensorDeviceClass | None,
        unit: str | None,
    ) -> None:
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._room_id = room_id
        self._data_key = data_key
        self._attr_unique_id = f"hvac_{room_id}_{data_key}"
        self._attr_name = name
        self._attr_device_class = device_class
        self._attr_native_unit_of_measurement = unit

    @property
    def native_value(self) -> float | None:
        """Return the native value."""
        room_data = self.coordinator.get_room_data(self._room_id)
        if room_data:
            return room_data.get(self._data_key)
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


class HVACEnvironmentSensor(SensorEntity):
    """Sensor entity for environment data."""

    _attr_has_entity_name = True
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self,
        coordinator: HVACDataCoordinator,
        data_key: str,
        name: str,
        device_class: SensorDeviceClass | None,
        unit: str | None,
    ) -> None:
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._data_key = data_key
        self._attr_unique_id = f"hvac_env_{data_key}"
        self._attr_name = name
        self._attr_device_class = device_class
        self._attr_native_unit_of_measurement = unit

    @property
    def native_value(self) -> float | None:
        """Return the native value."""
        env_data = self.coordinator.get_environment_data()
        return env_data.get(self._data_key)

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )


class HVACYorkSensor(SensorEntity):
    """Sensor entity for york data."""

    _attr_has_entity_name = True
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self,
        coordinator: HVACDataCoordinator,
        data_key: str,
        name: str,
        device_class: SensorDeviceClass | None,
        unit: str | None,
    ) -> None:
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._data_key = data_key
        self._attr_unique_id = f"hvac_york_{data_key}"
        self._attr_name = name
        self._attr_device_class = device_class
        self._attr_native_unit_of_measurement = unit

    @property
    def native_value(self) -> float | None:
        """Return the native value."""
        york_data = self.coordinator.get_york_data()
        return york_data.get(self._data_key)

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )


class HVACFreshAirSensor(SensorEntity):
    """Sensor entity for fresh air data."""

    _attr_has_entity_name = True
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self,
        coordinator: HVACDataCoordinator,
        data_key: str,
        name: str,
        device_class: SensorDeviceClass | None,
        unit: str | None,
    ) -> None:
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._data_key = data_key
        self._attr_unique_id = f"hvac_fresh_air_{data_key}"
        self._attr_name = name
        self._attr_device_class = device_class
        self._attr_native_unit_of_measurement = unit

    @property
    def native_value(self) -> float | None:
        """Return the native value."""
        fresh_air_data = self.coordinator.get_fresh_air_data()
        return fresh_air_data.get(self._data_key)

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )


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
        return {
            "host": self.coordinator.modbus.host,
            "port": self.coordinator.modbus.port,
        }
