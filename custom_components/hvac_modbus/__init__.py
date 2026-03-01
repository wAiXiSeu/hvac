"""The HVAC Modbus integration."""

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .modbus import HVACModbusClient
from .const import CONF_HOST, CONF_PORT, CONF_SLAVE_ID, CONF_SCAN_INTERVAL, DOMAIN, DEFAULT_PORT, DEFAULT_SLAVE_ID
from .coordinator import HVACDataCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.CLIMATE,
    Platform.SENSOR,
    Platform.SWITCH,
    Platform.SELECT,
    Platform.NUMBER,
]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the HVAC Modbus component."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_migrate_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Migrate old entry to new version."""
    _LOGGER.info("Migrating from version %s to version 2", config_entry.version)

    if config_entry.version == 1:
        # v1 used HTTP API, v2 uses direct Modbus
        # Keep host, change port to Modbus default (502), add slave_id
        new_data = {
            CONF_HOST: config_entry.data.get(CONF_HOST, "192.168.110.200"),
            CONF_PORT: DEFAULT_PORT,  # Modbus port 502
            CONF_SLAVE_ID: DEFAULT_SLAVE_ID,
            CONF_SCAN_INTERVAL: config_entry.data.get(CONF_SCAN_INTERVAL, 30),
        }
        
        hass.config_entries.async_update_entry(
            config_entry,
            data=new_data,
            version=2,
        )
        
        _LOGGER.info(
            "Migration successful: updated to Modbus direct connection at %s:%s",
            new_data[CONF_HOST],
            new_data[CONF_PORT],
        )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up HVAC Modbus from a config entry."""
    host = entry.data[CONF_HOST]
    port = entry.data[CONF_PORT]
    slave_id = entry.data.get(CONF_SLAVE_ID, 1)
    scan_interval = entry.options.get(
        CONF_SCAN_INTERVAL, entry.data.get(CONF_SCAN_INTERVAL, 30)
    )
    
    # Create Modbus client
    modbus = HVACModbusClient(host=host, port=port, slave_id=slave_id)
    
    # Connect to Modbus device
    connected = await modbus.connect()
    if not connected:
        _LOGGER.error("Failed to connect to Modbus device at %s:%s", host, port)
        # Still proceed - coordinator will handle reconnection
    
    coordinator = HVACDataCoordinator(
        hass=hass,
        modbus=modbus,
        scan_interval=scan_interval,
    )
    
    # Fetch initial data
    await coordinator.async_config_entry_first_refresh()
    
    hass.data[DOMAIN][entry.entry_id] = {
        "modbus": modbus,
        "coordinator": coordinator,
    }
    
    # Set up platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    # Set up update listener for options
    entry.async_on_unload(entry.add_update_listener(async_update_options))
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        data = hass.data[DOMAIN].pop(entry.entry_id)
        await data["modbus"].disconnect()
    
    return unload_ok


async def async_update_options(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Update options."""
    await hass.config_entries.async_reload(entry.entry_id)
