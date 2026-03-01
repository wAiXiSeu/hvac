"""Climate platform for HVAC Modbus integration."""

import logging
from typing import Any

from homeassistant.components.climate import ClimateEntity, ClimateEntityFeature
from homeassistant.components.climate.const import HVACMode, PRESET_HOME, PRESET_AWAY
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
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
    """Set up HVAC climate platform."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    
    entities = []
    for room_id in ROOM_IDS:
        entities.append(HVACRoomClimate(coordinator, room_id))
    
    async_add_entities(entities)


class HVACRoomClimate(ClimateEntity):
    """Climate entity for a room."""

    _attr_has_entity_name = True
    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_target_temperature_step = 0.5
    _attr_min_temp = 16.0
    _attr_max_temp = 30.0
    _attr_hvac_modes = [HVACMode.OFF, HVACMode.HEAT, HVACMode.COOL]
    _attr_preset_modes = [PRESET_HOME, PRESET_AWAY]
    _attr_supported_features = (
        ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.PRESET_MODE
    )

    def __init__(self, coordinator: HVACDataCoordinator, room_id: str) -> None:
        """Initialize the climate entity."""
        self.coordinator = coordinator
        self._room_id = room_id
        self._attr_unique_id = f"hvac_{room_id}_climate"
        self._attr_translation_key = f"hvac_{room_id}"
        self._attr_name = f"{ROOM_NAMES.get(room_id, room_id)} 恒温器"

    @property
    def room_data(self) -> dict[str, Any] | None:
        """Get room data from coordinator."""
        return self.coordinator.get_room_data(self._room_id)

    @property
    def current_temperature(self) -> float | None:
        """Return current temperature."""
        if self.room_data:
            temp_data = self.room_data.get("temp", {})
            return temp_data.get("value")
        return None

    @property
    def target_temperature(self) -> float | None:
        """Return target temperature."""
        if self.room_data:
            setpoint_data = self.room_data.get("setpoint", {})
            return setpoint_data.get("value")
        return None

    @property
    def hvac_mode(self) -> HVACMode:
        """Return hvac mode."""
        # Get from system run mode
        system_data = self.coordinator.get_system_data()
        run_mode_data = system_data.get("run_mode", {})
        run_mode = run_mode_data.get("value")
        
        if run_mode == 1:  # 制冷
            return HVACMode.COOL
        elif run_mode == 2:  # 制热
            return HVACMode.HEAT
        else:
            return HVACMode.OFF

    @property
    def preset_mode(self) -> str:
        """Return preset mode."""
        system_data = self.coordinator.get_system_data()
        home_mode_data = system_data.get("home_mode", {})
        home_mode = home_mode_data.get("value", 1)
        return PRESET_HOME if home_mode == 1 else PRESET_AWAY

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set new target temperature."""
        temperature = kwargs.get("temperature")
        if temperature is None:
            return
        
        api = self.coordinator.api
        await api.set_room_setpoint(self._room_id, temperature)
        await self.coordinator.async_request_refresh()

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set hvac mode."""
        # Map HVAC mode to run mode
        run_mode_map = {
            HVACMode.COOL: 1,
            HVACMode.HEAT: 2,
            HVACMode.OFF: 0,
        }
        run_mode = run_mode_map.get(hvac_mode, 0)
        
        if run_mode > 0:
            api = self.coordinator.api
            await api.set_system(run_mode=run_mode)
            await self.coordinator.async_request_refresh()

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        """Set preset mode."""
        home_mode = preset_mode == PRESET_HOME
        api = self.coordinator.api
        await api.set_system(home_mode=home_mode)
        await self.coordinator.async_request_refresh()

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success and self.room_data is not None

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        attrs = {}
        if self.room_data:
            # Add humidity
            humidity_data = self.room_data.get("humidity", {})
            if humidity_data.get("value") is not None:
                attrs["humidity"] = humidity_data.get("value")
            
            # Add dew point
            dew_point_data = self.room_data.get("dew_point", {})
            if dew_point_data.get("value") is not None:
                attrs["dew_point"] = dew_point_data.get("value")
            
            # Add register info
            temp_data = self.room_data.get("temp", {})
            if temp_data:
                attrs["temp_register"] = temp_data.get("address")
                attrs["temp_raw"] = temp_data.get("raw")
            
            setpoint_data = self.room_data.get("setpoint", {})
            if setpoint_data:
                attrs["setpoint_register"] = setpoint_data.get("address")
                attrs["setpoint_raw"] = setpoint_data.get("raw")
        
        return attrs
