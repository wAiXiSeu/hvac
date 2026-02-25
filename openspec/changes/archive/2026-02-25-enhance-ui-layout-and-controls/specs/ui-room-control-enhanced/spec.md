## ADDED Requirements

### Requirement: Room Control Panel Grid Layout
The system SHALL display all room control panels in a responsive grid layout showing living room, master bedroom, second bedroom, study room, and kitchen/bathroom controls.

#### Scenario: Grid renders all rooms
- **WHEN** user loads the room section
- **THEN** system displays 5 room control cards (4 bedrooms + kitchen/bathroom)

#### Scenario: Responsive layout adaptation
- **WHEN** viewport width is greater than 1200px
- **THEN** system displays room cards in a 3-column grid

#### Scenario: Tablet layout adaptation
- **WHEN** viewport width is between 768px and 1200px
- **THEN** system displays room cards in a 2-column grid

#### Scenario: Mobile layout adaptation
- **WHEN** viewport width is less than 768px
- **THEN** system displays room cards in a single column

### Requirement: Room Temperature Display and Control
The system SHALL display current temperature, humidity, and allow inline editing of target temperature for each room.

#### Scenario: Display room data
- **WHEN** room card is rendered
- **THEN** system displays room name, current temperature, current humidity, and target temperature

#### Scenario: Visual editable indicators
- **WHEN** target temperature field is displayed
- **THEN** field has white background, border, and cursor pointer to indicate it's editable

#### Scenario: Enter temperature edit mode
- **WHEN** user clicks on the target temperature value
- **THEN** system displays an input field with current value and OK/Cancel buttons

#### Scenario: Confirm temperature change
- **WHEN** user enters a new temperature value and clicks OK button
- **THEN** system sends PUT request to `/api/rooms/{room_id}` and displays loading indicator

#### Scenario: Cancel temperature change
- **WHEN** user clicks Cancel button during edit
- **THEN** system reverts to display mode without sending API request

#### Scenario: Temperature validation
- **WHEN** user enters a temperature value outside 16-30°C range
- **THEN** system displays validation error and prevents submission

#### Scenario: Temperature change success feedback
- **WHEN** temperature update succeeds
- **THEN** system exits edit mode, updates displayed value, and shows success indicator

### Requirement: Kitchen and Bathroom Radiant Control
The system SHALL provide a toggle control for kitchen and bathroom radiant heating/cooling system.

#### Scenario: Display kitchen/bathroom control
- **WHEN** kitchen/bathroom control card is rendered
- **THEN** system displays a toggle switch for radiant heating/cooling control

#### Scenario: Toggle radiant control
- **WHEN** user clicks the radiant control toggle
- **THEN** system sends PUT request to `/api/registers/write` with address 1133 and new state value

#### Scenario: Radiant control feedback
- **WHEN** radiant control operation succeeds
- **THEN** system updates toggle state and displays success indicator

#### Scenario: Radiant control error handling
- **WHEN** radiant control operation fails
- **THEN** system displays error message and reverts toggle to previous state

### Requirement: Room Data Auto-Refresh
The system SHALL automatically refresh room data at regular intervals without user interaction.

#### Scenario: Periodic data polling
- **WHEN** room section is mounted
- **THEN** system polls `/api/rooms` endpoint every 5 seconds

#### Scenario: Stop polling on unmount
- **WHEN** user navigates away from the page
- **THEN** system stops all room data polling requests

#### Scenario: Pause polling on window blur
- **WHEN** browser window loses focus
- **THEN** system pauses data polling to conserve resources

#### Scenario: Resume polling on window focus
- **WHEN** browser window regains focus
- **THEN** system resumes data polling immediately
