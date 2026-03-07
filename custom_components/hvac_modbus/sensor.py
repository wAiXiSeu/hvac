"""Sensor platform for HVAC Modbus integration."""

import logging
from typing import Any

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfTemperature, CONCENTRATION_PARTS_PER_MILLION, CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, UnitOfFrequency, UnitOfElectricCurrent
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
    
    # System threshold sensors (新增)
    entities.extend([
        HVACSystemSensor(coordinator, "heating_supply_temp_limit", "制热送风温度下限", SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS),
        HVACSystemSensor(coordinator, "cooling_supply_temp_set", "制冷送风温度设定", SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS),
        HVACSystemSensor(coordinator, "humidity_stop_limit", "加湿停止上限", SensorDeviceClass.HUMIDITY, PERCENTAGE),
        HVACSystemSensor(coordinator, "fresh_air_outlet_humidity", "新风机送风口湿度", SensorDeviceClass.HUMIDITY, PERCENTAGE),
    ])
    
    # Room sensors (扩展)
    for room_id in ROOM_IDS:
        room_name = ROOM_NAMES.get(room_id, room_id)
        entities.extend([
            HVACRoomSensor(coordinator, room_id, "temp", f"{room_name}温度", SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS),
            HVACRoomSensor(coordinator, room_id, "humidity", f"{room_name}湿度", SensorDeviceClass.HUMIDITY, PERCENTAGE),
            HVACRoomSensor(coordinator, room_id, "dew_point", f"{room_name}露点", SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS),
            # 新增房间传感器
            HVACRoomSensor(coordinator, room_id, "design_temp", f"{room_name}设计基准温", SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS),
            HVACRoomSensor(coordinator, room_id, "panel_temp", f"{room_name}面板温度", SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS),
            HVACRoomRadiantSensor(coordinator, room_id, "panel_radiant", f"{room_name}面板辐射"),
        ])
    
    # York sensors (扩展)
    entities.extend([
        HVACYorkSensor(coordinator, "supply_temp", "约克供水温度", SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS),
        HVACYorkSensor(coordinator, "return_temp", "约克回水温度", SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS),
        HVACYorkRunModeSensor(coordinator, "run_mode_feedback", "约克运行模式反馈"),
    ])
    
    # Fresh air sensors (扩展)
    entities.extend([
        HVACFreshAirStatusCodeSensor(coordinator, "status_code1", "新风机状态码"),
        HVACFreshAirSensor(coordinator, "compressor_freq", "新风压缩机频率", SensorDeviceClass.FREQUENCY, UnitOfFrequency.HERTZ),
        HVACFreshAirSensor(coordinator, "total_current", "新风机整机电流", SensorDeviceClass.CURRENT, UnitOfElectricCurrent.AMPERE),
        HVACFreshAirSensor(coordinator, "compressor_current", "新风机压缩机电流", SensorDeviceClass.CURRENT, UnitOfElectricCurrent.AMPERE),
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


class HVACFreshAirStatusCodeSensor(SensorEntity):
    """Sensor entity for fresh air status code."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:information-outline"

    def __init__(
        self,
        coordinator: HVACDataCoordinator,
        data_key: str,
        name: str,
    ) -> None:
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._data_key = data_key
        self._attr_unique_id = f"hvac_fresh_air_{data_key}"
        self._attr_name = name

    @property
    def native_value(self) -> str | None:
        """Return the native value as hex string."""
        fresh_air_data = self.coordinator.get_fresh_air_data()
        value = fresh_air_data.get(self._data_key)
        if value is not None:
            return f"0x{value:04X}"
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        fresh_air_data = self.coordinator.get_fresh_air_data()
        value = fresh_air_data.get(self._data_key)
        attrs = {}
        if value is not None:
            attrs["raw_value"] = value
            attrs["decimal"] = value
            attrs["hex"] = f"0x{value:04X}"
            attrs["binary"] = f"0b{value:016b}"
            # 状态描述
            if value == 0x8104:
                attrs["status"] = "正常运行"
            else:
                attrs["status"] = "未知状态"
        return attrs

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )


class HVACSystemSensor(SensorEntity):
    """Sensor entity for system threshold data."""

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
        self._attr_unique_id = f"hvac_{data_key}"
        self._attr_name = name
        self._attr_device_class = device_class
        self._attr_native_unit_of_measurement = unit

    @property
    def native_value(self) -> float | None:
        """Return the native value."""
        system_data = self.coordinator.get_system_data()
        return system_data.get(self._data_key)

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )


class HVACRoomRadiantSensor(SensorEntity):
    """Sensor entity for room panel radiant status."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:radiator"

    def __init__(
        self,
        coordinator: HVACDataCoordinator,
        room_id: str,
        data_key: str,
        name: str,
    ) -> None:
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._room_id = room_id
        self._data_key = data_key
        self._attr_unique_id = f"hvac_{room_id}_{data_key}"
        self._attr_name = name

    @property
    def native_value(self) -> str | None:
        """Return the native value."""
        room_data = self.coordinator.get_room_data(self._room_id)
        if room_data:
            value = room_data.get(self._data_key)
            if value is not None:
                return "开" if value else "关"
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


class HVACYorkRunModeSensor(SensorEntity):
    """Sensor entity for York run mode feedback."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:air-conditioner"

    RUN_MODE_MAP = {
        0: "制冷",
        1: "制热",
        8: "循环",
    }

    def __init__(
        self,
        coordinator: HVACDataCoordinator,
        data_key: str,
        name: str,
    ) -> None:
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._data_key = data_key
        self._attr_unique_id = f"hvac_york_{data_key}"
        self._attr_name = name

    @property
    def native_value(self) -> str | None:
        """Return the native value."""
        york_data = self.coordinator.get_york_data()
        value = york_data.get(self._data_key)
        if value is not None:
            return self.RUN_MODE_MAP.get(value, f"未知({value})")
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
