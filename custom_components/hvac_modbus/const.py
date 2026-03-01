"""Constants for the HVAC Modbus integration."""

DOMAIN = "hvac_modbus"

# Configuration keys
CONF_HOST = "host"
CONF_PORT = "port"
CONF_SLAVE_ID = "slave_id"
CONF_SCAN_INTERVAL = "scan_interval"

# Default values
DEFAULT_HOST = "192.168.110.200"
DEFAULT_PORT = 502
DEFAULT_SLAVE_ID = 1
DEFAULT_SCAN_INTERVAL = 30

# Room IDs
ROOM_IDS = ["living_room", "master_bedroom", "second_bedroom", "study_room"]

# Room names (Chinese to English mapping)
ROOM_NAMES = {
    "living_room": "客厅",
    "master_bedroom": "主卧",
    "second_bedroom": "次卧",
    "study_room": "书房",
}

# Run mode mapping
RUN_MODES = {
    1: "制冷",
    2: "制热",
    3: "通风",
    4: "除湿",
}

RUN_MODE_REVERSE = {v: k for k, v in RUN_MODES.items()}

# Register addresses for direct access
REGISTER_ADDRESSES = {
    "system_power": 1033,
    "home_mode": 1034,
    "run_mode": 1041,
    "fan_speed": 1047,
    "kitchen_radiant": 1133,
    "humidifier": 1168,
    "heating_setpoint": 1062,
    "cooling_setpoint": 1066,
}
