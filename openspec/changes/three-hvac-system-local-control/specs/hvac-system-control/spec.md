## ADDED Requirements

### Requirement: System Power Control
The system SHALL allow users to power on/off the HVAC system via Modbus register 41033.

#### Scenario: Power on system
- **WHEN** user clicks "Power On" button
- **THEN** system writes value 1 to register 41033
- **AND** confirms the operation was successful

#### Scenario: Power off system
- **WHEN** user clicks "Power Off" button
- **THEN** system writes value 0 to register 41033
- **AND** confirms the operation was successful

### Requirement: Home/Away Mode Control
The system SHALL allow users to switch between Home and Away modes via register 41034.

#### Scenario: Set Home mode
- **WHEN** user selects "Home" mode
- **THEN** system writes value 1 to register 41034

#### Scenario: Set Away mode
- **WHEN** user selects "Away" mode
- **THEN** system writes value 0 to register 41034

### Requirement: Operation Mode Control
The system SHALL allow users to select HVAC operation mode via register 41041.

#### Scenario: Set Heating mode
- **WHEN** user selects "Heating" mode
- **THEN** system writes value 1 to register 41041

#### Scenario: Set Cooling mode
- **WHEN** user selects "Cooling" mode
- **THEN** system writes value 2 to register 41041

#### Scenario: Set Dehumidify mode
- **WHEN** user selects "Dehumidify" mode
- **THEN** system writes value 3 to register 41041

#### Scenario: Set Airflow mode
- **WHEN** user selects "Airflow" mode
- **THEN** system writes value 4 to register 41041

### Requirement: Fresh Air Fan Speed Control
The system SHALL allow users to adjust fresh air fan speed via register 41047.

#### Scenario: Set fan speed
- **WHEN** user adjusts fan speed slider (0-100%)
- **THEN** system writes corresponding value to register 41047

### Requirement: System Status Display
The system SHALL display current system status including power state, mode, and fan speed.

#### Scenario: Display system status
- **WHEN** user views system control panel
- **THEN** current power state, operation mode, and fan speed are displayed
- **AND** status updates automatically every 2 seconds
