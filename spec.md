# Civic Pulse
## Project Specification (spec.md)

### 1. Project Overview
Civic Pulse is an offline-first digital governance and emergency alert system designed to help citizens request immediate assistance during critical situations. The system provides a one-tap emergency button that detects the user's GPS location and sends an emergency alert to designated authorities through SMS whenever cellular service is available, without requiring mobile internet.

When communication is unavailable, the emergency alert is stored locally and automatically retried when connectivity becomes available.

### 2. Problem Statement
Citizens often face difficulties contacting emergency services during medical emergencies, accidents, and personal safety threats. Many emergency applications depend on internet connectivity or require multiple steps to report a situation. People without mobile data, recharge, or reliable network access may struggle to request help.

Civic Pulse addresses these challenges by developing an offline-first emergency alert system that uses GPS location, local alert storage, and SMS-based communication to improve emergency reporting and response.

### 3. Objectives
- Provide a one-tap emergency alert system.
- Enable GPS-based location detection without internet.
- Send emergency messages through SMS when cellular service is available.
- Support emergency alert generation without mobile data.
- Store emergency alerts locally when communication is unavailable.
- Automatically retry sending stored alerts when connectivity returns.
- Improve public safety and emergency response coordination.

### 4. Target Users
- Citizens
- Elderly people
- People with medical conditions
- Individuals facing safety threats
- People in areas with poor internet connectivity
- Government emergency response teams

### 5. Functional Requirements

#### 5.1 User Registration
- Users can register with their name and phone number.
- Users can add emergency contact details.
- User details are stored securely.

#### 5.2 Emergency Alert Button
- Provide a clearly visible emergency button.
- Allow users to trigger an alert with a single tap.
- Generate an emergency message automatically.

#### 5.3 GPS Location Detection
- Detect the user's current location using GPS.
- GPS location detection should work without mobile internet.
- Store latitude and longitude in the emergency alert.
- Generate a location link when possible.

#### 5.4 Offline Emergency Alert
- Generate emergency alerts without internet connectivity.
- Store alert details locally on the device.
- Record the emergency time and location.
- Display the alert status to the user.

#### 5.5 SMS Communication
- Send emergency alerts through SMS when cellular service is available.
- SMS functionality should not depend on mobile data.
- Include user details, emergency type, location, and timestamp.
- Sending SMS without recharge depends on the mobile operator's available services and active SIM status.

#### 5.6 Automatic Alert Retry
- Detect when network connectivity becomes available.
- Automatically retry sending pending emergency alerts.
- Update the alert status after successful transmission.

#### 5.7 Emergency Categories
- Medical Emergency
- Accident
- Personal Safety
- Other Emergency

#### 5.8 Government Dashboard
- Display received emergency alerts.
- Show emergency location on a map.
- Display user details, emergency type, and timestamp.
- Allow authorities to update emergency status.

#### 5.9 Alert Status Tracking
- Pending
- Saved Offline
- Sending
- Alert Sent
- Assistance Dispatched
- Resolved

### 6. Non-Functional Requirements

- **Usability:** Simple and easy-to-use interface.
- **Performance:** Generate emergency alerts immediately.
- **Reliability:** Store alerts safely during network failure.
- **Offline Capability:** Support emergency generation and GPS detection without internet.
- **Security:** Protect personal information and location data.
- **Accessibility:** Emergency button should be easily visible.
- **Scalability:** Support multiple emergency alerts and users.

### 7. Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python Flask |
| Database | MySQL |
| Local Storage | SQLite / Device Storage |
| Location | GPS |
| Communication | SMS |
| Maps | Google Maps API / OpenStreetMap |
| Development Environment | VS Code |

### 8. System Workflow

1. Citizen opens the Civic Pulse application.
2. Citizen presses the Emergency Alert button.
3. System detects GPS location without requiring internet.
4. Emergency details are generated.
5. System checks cellular network availability.
6. If cellular service is available, an SMS alert is sent.
7. If network is unavailable, the alert is saved locally.
8. System automatically retries pending alerts when connectivity returns.
9. Government authorities receive the alert.
10. Authorities respond and update the emergency status.

### 9. Offline Capabilities
- GPS location detection without internet.
- Emergency alert generation.
- Local storage of emergency information.
- Emergency timestamp recording.
- Pending alert management.
- Automatic retry after connectivity restoration.

### 10. Limitations
- GPS location accuracy depends on environmental conditions.
- SMS delivery requires cellular network coverage and compatible SIM service.
- Sending SMS without recharge is not guaranteed and depends on the mobile operator.
- Alerts cannot reach remote authorities without a communication channel.
- Automatic retry requires the application or supported system service to remain capable of running.

### 11. Expected Outcome
Civic Pulse aims to provide an offline-first emergency alert solution that enables citizens to generate emergency alerts even without internet access. Through GPS location detection, local storage, SMS communication, and automatic retry functionality, the system improves emergency accessibility and supports faster response from authorities.

### 12. Future Enhancements
- Live location tracking.
- Voice-activated emergency alerts.
- Satellite-based emergency communication.
- LoRa-based communication for remote areas.
- Multilingual interface.
- Integration with police and ambulance services.
- AI-based emergency classification.
- Wearable emergency button integration.

### 13. Project Motto
"One Click. One Alert. Immediate Help."
