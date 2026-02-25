## ADDED Requirements

### Requirement: Room Temperature Reading
The system SHALL read and display current temperature and humidity for each room from Modbus registers.

#### Scenario: Read living room temperature
- **WHEN** system reads register 41085
- **THEN** value is divided by 10 and displayed in °C

#### Scenario: Read living room humidity
- **WHEN** system reads register 41087
- **THEN** value is divided by 10 and displayed in %

#### Scenario: Read bedroom temperature
- **WHEN** system reads register 41095 (主卧) / 41105 (次卧) / 41117 (书房)
- **THEN** value is divided by 10 and displayed in °C

#### Scenario: Read bedroom humidity
- **WHEN** system reads register 41097 (主卧) / 41107 (次卧) / 41119 (书房)
- **THEN** value is divided by 10 and displayed in %

### Requirement: Room Temperature Setting
The system SHALL allow users to set target temperature for each room via Modbus registers.

#### Scenario: Set living room temperature
- **WHEN** user sets living room target temperature to X °C
- **THEN** system writes value (X × 2) to register 41090

#### Scenario: Set master bedroom temperature
- **WHEN** user sets master bedroom target temperature to X °C
- **THEN** system writes value (X × 2) to register 41101

#### Scenario: Set second bedroom temperature
- **WHEN** user sets second bedroom target temperature to X °C
- **THEN** system writes value (X × 2) to register 41110

#### Scenario: Set study room temperature
- **WHEN** user sets study room target temperature to X °C
- **THEN** system writes value (X × 2) to register 41123

### Requirement: Room List Management
The system SHALL define and manage a list of controllable rooms.

#### Scenario: Default room configuration
- **WHEN** system initializes
- **THEN** following rooms are available:
  - 客厅 (Living Room)
  - 主卧 (Master Bedroom)
  - 次卧 (Second Bedroom)
  - 书房 (Study Room)

### Requirement: Room Status Display
The system SHALL display current status for all rooms including actual temperature, humidity, and target temperature.

#### Scenario: Display all room status
- **WHEN** user views room control panel
- **THEN** all rooms are displayed with current actual temperature, humidity, and target temperature
- **AND** data refreshes automatically every 3 seconds
