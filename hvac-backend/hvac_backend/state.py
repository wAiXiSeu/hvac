from dataclasses import dataclass


@dataclass
class Room:
    id: str
    name: str
    temp_register: int
    humidity_register: int
    setpoint_register: int


class AppState:
    def __init__(self, config: dict, modbus_client):
        self.config = config
        self.modbus_client = modbus_client
        
        # Room configurations
        self.rooms = [
            Room(
                id=room["id"],
                name=room["name"],
                temp_register=room["temp_register"],
                humidity_register=room["humidity_register"],
                setpoint_register=room["setpoint_register"]
            )
            for room in config.get("rooms", [])
        ]
