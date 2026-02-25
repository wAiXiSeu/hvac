## ADDED Requirements

### Requirement: Fresh Air System Status Display
The system SHALL display fresh air system status including compressor frequency, supply/return water temperatures, and operating state.

#### Scenario: Display fresh air status data
- **WHEN** fresh air section is rendered
- **THEN** system displays compressor frequency, internal supply temperature, internal return temperature, and system status code

#### Scenario: Status interpretation
- **WHEN** fresh air status code is 0x8104
- **THEN** system displays "正常运行" (Normal Operation) status indicator

#### Scenario: Abnormal status warning
- **WHEN** fresh air status code is not 0x8104
- **THEN** system displays warning indicator with status code

#### Scenario: Data updates automatically
- **WHEN** backend provides updated fresh air data
- **THEN** displayed values update without page refresh within 5 seconds

### Requirement: Fresh Air Fan Speed Control
The system SHALL provide a slider control to adjust fresh air fan speed from 0% to 100%.

#### Scenario: Display fan speed slider
- **WHEN** fresh air control section is rendered
- **THEN** system displays a slider control with current fan speed percentage value

#### Scenario: Visual editable indicators
- **WHEN** fan speed control is displayed
- **THEN** control has white background, border, and interactive slider element

#### Scenario: Adjust fan speed via slider
- **WHEN** user drags the slider to a new position
- **THEN** system displays the new percentage value in real-time

#### Scenario: Commit fan speed change
- **WHEN** user releases the slider
- **THEN** system sends PUT request to `/api/registers/write` with address 1047 and new speed value

#### Scenario: Fan speed validation
- **WHEN** user attempts to set fan speed outside 0-100% range
- **THEN** system constrains the value to valid range

#### Scenario: Fan speed change feedback
- **WHEN** fan speed update succeeds
- **THEN** system displays success indicator for 2 seconds

#### Scenario: Fan speed change error
- **WHEN** fan speed update fails
- **THEN** system displays error message and reverts slider to previous position

### Requirement: Fresh Air Humidifier Control
The system SHALL provide a toggle control for the panel humidifier function.

#### Scenario: Display humidifier toggle
- **WHEN** fresh air control section is rendered
- **THEN** system displays a toggle switch labeled "加湿功能" with current on/off state

#### Scenario: Toggle humidifier on
- **WHEN** user clicks the humidifier toggle to turn it on
- **THEN** system sends PUT request to `/api/registers/write` with address 1168 and value 1

#### Scenario: Toggle humidifier off
- **WHEN** user clicks the humidifier toggle to turn it off
- **THEN** system sends PUT request to `/api/registers/write` with address 1168 and value 0

#### Scenario: Humidifier control feedback
- **WHEN** humidifier control operation succeeds
- **THEN** system updates toggle state and displays success indicator

#### Scenario: Humidifier control error handling
- **WHEN** humidifier control operation fails
- **THEN** system displays error message and reverts toggle to previous state

### Requirement: Fresh Air Control Section Layout
The system SHALL display fresh air controls in a card layout with clear separation between read-only status and editable controls.

#### Scenario: Card layout structure
- **WHEN** fresh air section is rendered
- **THEN** system displays a card with two sub-sections: "系统状态" (read-only) and "控制面板" (editable)

#### Scenario: Visual separation of read/write areas
- **WHEN** fresh air card is rendered
- **THEN** read-only status section has gray background (`#f5f5f5`) and control panel section has white background (`#ffffff`)
