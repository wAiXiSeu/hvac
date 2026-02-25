## ADDED Requirements

### Requirement: Environment Data Collection
The system SHALL continuously poll and collect environmental data from the Modbus device, including PM2.5, CO2 levels, and outdoor temperature/humidity.

#### Scenario: Periodic data polling
- **WHEN** Modbus connection is active
- **THEN** system polls environment registers every 3 seconds
- **AND** stores latest values in memory

#### Scenario: PM2.5 reading
- **WHEN** system reads register 41024
- **THEN** the value is displayed directly as μg/m³

#### Scenario: CO2 reading
- **WHEN** system reads register 41026
- **THEN** the value is displayed directly as PPM

#### Scenario: Outdoor temperature reading
- **WHEN** system reads register 41027
- **THEN** the value is divided by 10 and displayed in °C

#### Scenario: Outdoor humidity reading
- **WHEN** system reads register 41028
- **THEN** the value is divided by 10 and displayed in %

### Requirement: Real-time Environment Display
The system SHALL display collected environment data on the Web UI with auto-refresh capability.

#### Scenario: Environment panel displays current data
- **WHEN** user navigates to environment panel
- **THEN** all available environment metrics are displayed
- **AND** data refreshes automatically every 3 seconds
