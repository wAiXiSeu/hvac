## ADDED Requirements

### Requirement: System Overview Panel Display
The system SHALL display a system overview panel containing three sub-sections: Environment Monitoring, System Control, and York Host Status.

#### Scenario: Panel renders with all sections
- **WHEN** user loads the main page
- **THEN** system displays the system overview panel with three visible sub-sections

#### Scenario: Sub-sections are properly labeled
- **WHEN** system overview panel is rendered
- **THEN** each sub-section displays its title ("环境监测", "系统控制", "约克主机")

### Requirement: Environment Monitoring Section (Read-Only)
The system SHALL display environment monitoring data in a read-only format with visual indicators that the data cannot be modified.

#### Scenario: Display environment data
- **WHEN** environment monitoring section is rendered
- **THEN** system displays PM2.5, CO2, outdoor temperature, and outdoor humidity values

#### Scenario: Visual read-only indicators
- **WHEN** environment monitoring section is rendered
- **THEN** section has gray background color (`#f5f5f5`) and no interactive elements

#### Scenario: Data updates automatically
- **WHEN** backend provides updated environment data
- **THEN** displayed values update without page refresh within 5 seconds

### Requirement: System Control Section (Interactive)
The system SHALL provide interactive controls for system power, home/away mode, run mode, and fan speed.

#### Scenario: Display control options
- **WHEN** system control section is rendered
- **THEN** system displays toggle switches for power and home mode, and dropdown selectors for run mode and fan speed

#### Scenario: Visual editable indicators
- **WHEN** system control section is rendered
- **THEN** section has white background (`#ffffff`), border, and hover effects on interactive elements

#### Scenario: Toggle system power
- **WHEN** user clicks the power toggle switch
- **THEN** system sends PUT request to `/api/system` with new power state and displays loading indicator

#### Scenario: Change run mode
- **WHEN** user selects a run mode from dropdown (制热/制冷/除湿/通风)
- **THEN** system sends PUT request with selected mode value (1/2/3/4)

#### Scenario: Adjust fan speed
- **WHEN** user changes fan speed slider value
- **THEN** system sends PUT request with new fan speed percentage

#### Scenario: Operation feedback
- **WHEN** control operation succeeds
- **THEN** system displays success indicator for 2 seconds

#### Scenario: Operation error handling
- **WHEN** control operation fails
- **THEN** system displays error message and reverts UI to previous state

### Requirement: York Host Section (Read-Only)
The system SHALL display York host status information in a read-only format including supply and return water temperatures.

#### Scenario: Display York host data
- **WHEN** York host section is rendered
- **THEN** system displays supply water temperature, return water temperature, heating setpoint, and cooling setpoint

#### Scenario: Visual read-only indicators
- **WHEN** York host section is rendered
- **THEN** section has gray background color (`#f5f5f5`) with data display icon (📊)

#### Scenario: Data updates automatically
- **WHEN** backend provides updated York host data
- **THEN** displayed values update without page refresh within 5 seconds
