## ADDED Requirements

### Requirement: Modbus Connection Configuration
The system SHALL allow users to configure Modbus TCP connection parameters including IP address, port number, slave ID, and connection timeout.

#### Scenario: Default configuration loads
- **WHEN** the system starts for the first time
- **THEN** default values (192.168.110.200:502, slave_id=1, timeout=5s) are loaded

#### Scenario: User updates connection settings
- **WHEN** user submits new IP/port configuration via Web UI
- **THEN** the configuration is validated and saved
- **AND** system attempts to reconnect with new settings

#### Scenario: Invalid configuration input
- **WHEN** user provides invalid IP address or port number
- **THEN** the system displays validation error message
- **AND** previous valid configuration remains active

### Requirement: Connection Status Monitoring
The system SHALL continuously monitor and display the Modbus connection status in real-time.

#### Scenario: Connection active
- **WHEN** Modbus TCP connection is successfully established
- **THEN** Web UI displays "Connected" status with green indicator

#### Scenario: Connection lost
- **WHEN** Modbus TCP connection is lost or times out
- **THEN** Web UI displays "Disconnected" status with red indicator
- **AND** system attempts automatic reconnection every 10 seconds

#### Scenario: Manual reconnection
- **WHEN** user clicks "Reconnect" button
- **THEN** system terminates existing connection if any
- **AND** attempts to establish new connection with current configuration
