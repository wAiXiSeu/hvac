"""Constants for the HVAC Modbus integration."""

DOMAIN = "hvac_modbus"

# Configuration keys
CONF_HOST = "host"
CONF_PORT = "port"
CONF_API_KEY = "api_key"
CONF_SCAN_INTERVAL = "scan_interval"

# Default values
DEFAULT_HOST = "localhost"
DEFAULT_PORT = 8000
DEFAULT_SCAN_INTERVAL = 30

# API endpoints
API_ENDPOINTS = {
    "rooms": "/api/rooms",
    "system": "/api/system",
    "status": "/api/status",
    "registers": "/api/registers/grouped",
}

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
