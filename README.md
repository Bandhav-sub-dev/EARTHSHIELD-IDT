# EARTHSHIELD — IDT

## Intelligent Disaster Threat Monitoring & Assistance System

> A research and educational prototype for monitoring hazards, visualizing geographic risk, identifying potentially affected demo populations, and connecting them with nearby emergency facilities.

---

## Project Information

| Field | Value |
|---|---|
| Project | IDT |
| System | EARTHSHIELD |
| Current Version | V1.0.0 |
| Status | V1 Baseline |
| Interface | Streamlit |
| Language | Python |
| Deployment | Google Colab / Python |

---

## 1. What is EARTHSHIELD?

EARTHSHIELD is an experimental disaster-monitoring and emergency-assistance platform.

The objective is to create a single command-center interface capable of combining disaster information, environmental information, geographic analysis, population data, emergency facilities, and assistance recommendations.

The V1 implementation establishes the foundation for future multi-hazard development.

---

## 2. Core Workflow

```text
              LIVE DATA SOURCES
                     |
                     v
            HAZARD MONITORING
                     |
                     v
              RISK ANALYSIS
                     |
                     v
              IMPACT ZONE
                     |
             +-------+-------+
             |               |
             v               v
       PEOPLE DATA      FACILITY DATA
             |               |
             +-------+-------+
                     |
                     v
             ASSISTANCE ENGINE
                     |
          +----------+----------+
          |                     |
          v                     v
    NEAREST SHELTER         SMS DEMO
```

---

## 3. V1 Features

### Earthquake Monitoring

- Earthquake location
- Magnitude
- Depth
- Severity classification
- Geographic visualization
- Impact-radius demonstration
- Earthquake map markers
- Heatmap visualization

### Weather Monitoring

- Temperature
- Apparent temperature
- Rainfall conditions
- Wind
- Thunderstorm conditions
- Extreme temperature conditions

### Interactive Mapping

- OpenStreetMap
- Satellite imagery
- Terrain visualization
- Disaster markers
- Impact zones
- People markers
- Emergency-facility markers

### People Assistance

The V1 prototype contains a synthetic demonstration population.

Example fields include:

- Person ID
- Name
- Latitude
- Longitude
- City
- State
- Mobility information
- Notification preference

### Emergency Facilities

The demonstration dataset contains fictional emergency facilities such as:

- Shelters
- Hospitals
- Fire stations
- Relief centers
- Water/relief facilities

Facility information can include:

- Facility name
- Type
- Address
- Latitude
- Longitude
- Capacity
- Occupancy
- Available capacity
- Medical support
- Food
- Water
- Accessibility
- Operational status

---

## 4. Location-Based Assistance

The V1 system demonstrates the following workflow:

```text
Disaster
   |
   v
Impact Radius
   |
   v
Affected Demo People
   |
   v
Suitable Emergency Facilities
   |
   v
Distance Calculation
   |
   v
Nearest Suitable Shelter
```

The interface can display:

- Shelter name
- Full demonstration address
- Distance
- Available capacity
- Medical support
- Food availability
- Water availability
- Accessibility
- Facility status

---

## 5. SMS Demonstration

EARTHSHIELD V1 includes an SMS-style emergency notification demonstration.

A generated message can contain:

- Disaster type
- Severity
- Affected area
- Safety instructions
- Recommended shelter
- Shelter address
- Shelter distance

**Important:** SMS functionality is simulation-only in V1.

No actual SMS is sent.

---

## 6. Demonstration Data

The current people and emergency-facility datasets are synthetic.

They are intended only for:

- Academic demonstrations
- Software testing
- UI development
- Algorithm testing
- Disaster scenario simulation

**Real personal information must not be committed to this repository.**

---

## 7. Disaster Scenarios

V1 supports demonstration scenarios so the system can be tested without waiting for a real disaster.

A scenario can contain:

- Disaster type
- Area
- State
- Coordinates
- Severity
- Impact radius
- Description
- Recommended facility types
- Safety message

---

## 8. Current Architecture

```text
EARTHSHIELD
|
+-- app/
|   +-- dashboard.py
|   +-- pages/
|
+-- data/
|   +-- demo/
|   |   +-- people_demo.json
|   |   +-- emergency_facilities_demo.json
|   |   +-- disaster_test_scenarios.json
|   |
|   +-- source_registry.json
|
+-- backups/
|
+-- README.md
+-- VERSION.json
+-- PROJECT_STATUS.md
+-- LICENSE
+-- .gitignore
```

---

## 9. Technology Stack

- Python
- Streamlit
- Pandas
- Folium
- Streamlit-Folium
- JSON
- Public disaster/weather data sources
- Geographic map tile services

---

## 10. V2 Roadmap

V2 will be developed separately from the V1 baseline.

### Multi-Hazard Detection

- Earthquake
- Flood
- Cyclone
- Wildfire
- Landslide
- Tsunami
- Drought
- Heatwave
- Cold wave
- Severe storms
- Air-quality hazards

### Climate Intelligence

- El Niño monitoring
- La Niña monitoring
- Climate anomalies
- Rainfall anomalies
- Drought indicators
- Seasonal risk intelligence

### Advanced Flood Analysis

Future flood modelling may combine:

```text
Rainfall
+ Forecast Rainfall
+ River / Water Level
+ Elevation
+ Terrain
+ Historical Flood Information
          |
          v
      FLOOD RISK
```

### Advanced Geographic Intelligence

- Dynamic hazard zones
- Population density
- Road accessibility
- Safe-route analysis
- Multiple shelter recommendations
- Facility safety analysis

---

## 11. El Niño and La Niña

El Niño and La Niña are planned as climate-intelligence components rather than ordinary point-event alerts.

The planned workflow is:

```text
Ocean / Atmospheric Indicators
              |
              v
        ENSO Analysis
              |
              v
       Climate Condition
              |
              v
     Regional Risk Analysis
```

The purpose is to investigate how large-scale climate conditions may be incorporated into longer-term hazard intelligence.

---

## 12. Development Branches

### main

The stable IDT V1 baseline.

### v2-development

The development branch for future EARTHSHIELD V2 functionality.

The V1 baseline should remain unchanged unless changes are intentionally reviewed and merged.

---

## 13. Development Philosophy

EARTHSHIELD is being developed incrementally.

```text
V1 FOUNDATION
      |
      v
MULTI-HAZARD ENGINE
      |
      v
RISK INTELLIGENCE
      |
      v
POPULATION IMPACT
      |
      v
EMERGENCY ASSISTANCE
      |
      v
ADVANCED DISASTER RESPONSE
```

---

## 14. Running the Project

From the EARTHSHIELD directory:

```bash
cd EARTHSHIELD
streamlit run app/dashboard.py
```

Google Colab can expose Streamlit through the Colab port proxy.

---

## 15. Safety and Privacy

EARTHSHIELD is an experimental research and educational prototype.

It should not be considered an authoritative emergency-warning system.

A real deployment would require:

- Authoritative data sources
- Redundant data feeds
- Security controls
- Privacy protection
- Reliable communications
- Emergency-management integration
- Extensive validation
- Human oversight
- Fail-safe mechanisms

The V1 project intentionally uses synthetic population and facility information.

---

## 16. Project Objective

The long-term objective of EARTHSHIELD is to investigate whether multiple disaster-information and geographic-intelligence components can be brought together into one system that can answer:

```text
WHAT HAPPENED?
      |
      v
WHERE?
      |
      v
HOW SEVERE?
      |
      v
WHO MAY BE AFFECTED?
      |
      v
WHAT HELP IS NEARBY?
      |
      v
WHICH FACILITY IS SUITABLE?
      |
      v
WHAT SAFETY INFORMATION SHOULD BE SHOWN?
```

---

## 17. Disclaimer

EARTHSHIELD is a research and educational prototype.

It is not a replacement for official disaster-warning systems, emergency services, government authorities, meteorological agencies, or professional disaster-management infrastructure.

For real emergencies, users should follow verified instructions from appropriate official authorities.

---

## EARTHSHIELD

**Intelligent Disaster Threat Monitoring & Assistance System**

**IDT Project — V1 Baseline**
