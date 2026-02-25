## ADDED Requirements

### Requirement: Dashboard Overview
The system SHALL provide a main dashboard that displays an overview of all HVAC system data in a single view.

#### Scenario: Dashboard displays all sections
- **WHEN** user accesses the main dashboard
- **THEN** the following sections are visible:
  - Connection status indicator
  - System control panel (power, mode, fan speed)
  - Environment data summary (PM2.5, CO2, outdoor temp/humidity)
  - Room status cards (all rooms with temp/humidity)

#### Scenario: Auto-refresh dashboard
- **WHEN** dashboard is active
- **THEN** all data refreshes automatically every 3 seconds
- **AND** visual indicators show when data was last updated

### Requirement: Real-time Status Indicators
The system SHALL provide clear visual indicators for connection and system status.

#### Scenario: Connection status indicator
- **WHEN** Modbus is connected
- **THEN** green indicator with "已连接" text is displayed

- **WHEN** Modbus is disconnected
- **THEN** red indicator with "未连接" text is displayed
- **AND** control buttons are disabled

#### Scenario: System power indicator
- **WHEN** system is powered on
- **THEN** power indicator shows green "运行中"

- **WHEN** system is powered off
- **THEN** power indicator shows gray "已关闭"

### Requirement: Data Visualization
The system SHALL present numerical data in a clear, readable format with appropriate units.

#### Scenario: Temperature display
- **WHEN** temperature value is displayed
- **THEN** value is shown with 1 decimal place and "°C" unit

#### Scenario: Humidity display
- **WHEN** humidity value is displayed
- **THEN** value is shown with 1 decimal place and "%" unit

#### Scenario: PM2.5 display
- **WHEN** PM2.5 value is displayed
- **THEN** value is shown with "μg/m³" unit

#### Scenario: CO2 display
- **WHEN** CO2 value is displayed
- **THEN** value is shown with "PPM" unit
