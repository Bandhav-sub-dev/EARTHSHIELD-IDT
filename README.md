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

---

## V2 Development Plan — Multi-Hazard Disaster Intelligence

### 1. V2 Vision

EARTHSHIELD V2 will evolve the V1 disaster monitoring system into a
**multi-hazard intelligent disaster threat monitoring and assistance
platform**.

V1 establishes the foundation for:

- Live earthquake monitoring
- Weather monitoring
- Interactive geographic visualization
- Affected-person identification
- Emergency facility discovery
- Simulated emergency notifications
- Safe-shelter selection

V2 will extend this foundation to monitor multiple hazard types,
combine information from different environmental sources, calculate
risk, and provide more intelligent assistance.

### 2. V2 Objectives

The main objectives of V2 are:

1. Expand from earthquake/weather monitoring to multi-hazard monitoring.
2. Add flood detection and flood-risk analysis.
3. Add cyclone and severe-weather intelligence.
4. Add wildfire and landslide monitoring.
5. Add tsunami and coastal-risk indicators where suitable data are available.
6. Add heatwave, cold-wave and extreme-weather monitoring.
7. Introduce climate intelligence such as El Niño, La Niña and rainfall anomalies.
8. Build a common hazard-engine architecture.
9. Improve geographic risk analysis.
10. Connect hazard information with affected people and emergency facilities.
11. Improve shelter and emergency-response recommendations.
12. Establish a foundation for future AI-assisted disaster-risk analysis.

### 3. V2 High-Level Architecture

```text
                    EARTHSHIELD V2
                           |
          +----------------+----------------+
          |                                 |
          v                                 v
   LIVE HAZARD DATA                  CLIMATE SIGNALS
          |                                 |
   +------+------+------+            +-----+------+
   |      |      |      |            |            |
   v      v      v      v            v            v
Earth-   Flood  Cyclone Wildfire   El Nino    La Nina
quake
   |      |      |      |
   +------+------+------+
                 |
                 v
           HAZARD ENGINE
                 |
                 v
             RISK ENGINE
                 |
        +--------+--------+
        |                 |
        v                 v
   PEOPLE IMPACT     FACILITY IMPACT
        |                 |
        +--------+--------+
                 |
                 v
          ASSISTANCE ENGINE
                 |
        +--------+--------+--------+
        |                 |        |
        v                 v        v
      ALERT           SHELTER   RESPONSE
```

### 4. Multi-Hazard Monitoring

#### Earthquake

V1 provides the foundation for earthquake monitoring.

V2 will expand earthquake intelligence with:

- Magnitude
- Depth
- Epicenter
- Geographic impact estimation
- Event severity
- Affected population estimation
- Facility exposure
- Historical earthquake context
- Event clustering

#### Flood

Flood intelligence will combine available information such as:

- Rainfall intensity
- Accumulated rainfall
- Rainfall forecasts
- River and water-level information where available
- Elevation and terrain
- Flood-prone areas
- Historical flood information
- Population exposure
- Emergency-facility exposure

Planned workflow:

```text
Rainfall / Water Data
        |
        v
Flood Detection
        |
        v
Flood Risk
        |
        v
Impact Area
        |
        v
People + Facilities
```

#### Cyclone

The cyclone module will investigate:

- Storm location
- Wind conditions
- Precipitation
- Storm movement/track information
- Geographic proximity
- Expected impact region
- Evacuation and shelter requirements

#### Wildfire

The wildfire module will investigate available fire and environmental data:

- Active fire indicators
- Fire location
- Fire proximity
- Affected region
- Environmental conditions
- Evacuation areas

#### Landslide

The landslide module will investigate:

- Rainfall
- Terrain
- Slope
- Elevation
- Geological susceptibility where available
- Historical landslide information

#### Tsunami

The tsunami module will investigate appropriate public warning data.

Potential inputs include:

- Earthquake events
- Earthquake location and depth
- Coastal proximity
- Tsunami advisories
- Warning information from authoritative sources

#### Extreme Weather

V2 will expand environmental monitoring to include:

- Heatwaves
- Cold waves
- Extreme rainfall
- Severe thunderstorms
- High winds
- Extreme temperature
- Drought indicators
- Air-quality-related environmental risk

### 5. Climate Intelligence

V2 will distinguish between immediate hazards and large-scale climate signals.

Immediate hazards include:

- Earthquakes
- Floods
- Cyclones
- Wildfires
- Landslides
- Tsunamis

Climate signals include:

- El Niño
- La Niña
- Rainfall anomalies
- Temperature anomalies
- Drought indicators
- Seasonal climate patterns

Climate signals will provide environmental context rather than being
treated as a single local disaster event.

```text
Climate Signal
      |
      v
Regional Climate Conditions
      |
      v
Environmental Risk Context
      |
      v
Hazard Monitoring
```

### 6. Hazard Engine

V2 will introduce a common hazard-processing architecture.

Planned modules:

```text
app/core/
|
+-- hazard_engine.py
+-- earthquake_detector.py
+-- flood_detector.py
+-- cyclone_detector.py
+-- wildfire_detector.py
+-- landslide_detector.py
+-- tsunami_detector.py
+-- extreme_weather_detector.py
+-- climate_detector.py
```

Each detector will convert source information into a normalized hazard representation.

Example:

```text
Hazard
|-- hazard_id
|-- hazard_type
|-- timestamp
|-- latitude
|-- longitude
|-- severity
|-- confidence
|-- impact_radius
|-- source
+-- source_timestamp
```

### 7. Risk Engine

V2 will introduce a dedicated risk-calculation layer.

The planned concept is:

```text
HAZARD
   +
EXPOSURE
   +
VULNERABILITY
   +
GEOGRAPHIC FACTORS
   =
RISK
```

Potential factors include:

- Hazard severity
- Distance
- Population exposure
- Geographic location
- Facility exposure
- Environmental conditions
- Supporting scientific data

Risk results should remain explainable and traceable to their inputs.

### 8. People Impact Engine

The V1 people-assistance system will be expanded.

Planned workflow:

```text
Hazard detected
      |
      v
Impact area calculated
      |
      v
People inside/near impact area
      |
      v
Risk level
      |
      v
Suitable safe facility
      |
      v
Emergency assistance information
```

Future versions may support:

- Population density
- Accessibility considerations
- Language preferences
- Facility capacity
- Facility availability
- Changing hazard conditions

Real personal data will require appropriate consent, security and privacy controls.

### 9. Emergency Facility Intelligence

V2 will expand the facility model with:

- Facility type
- Location
- Capacity
- Current occupancy
- Available capacity
- Medical support
- Food availability
- Water availability
- Accessibility
- Operating status
- Disaster suitability
- Distance from affected population
- Distance from hazard
- Geographic safety conditions

The shelter engine will continue enforcing safety conditions.

A facility inside a danger zone must not be recommended merely because it is close.

### 10. Alert and Notification Engine

V1 currently provides notification simulation.

V2 will develop a structured alert engine.

Planned levels:

```text
INFO
WATCH
ADVISORY
WARNING
HIGH
CRITICAL
```

Planned flow:

```text
Hazard
  |
  v
Validation
  |
  v
Risk calculation
  |
  v
Affected area
  |
  v
Affected people
  |
  v
Alert generation
  |
  v
Recommended action
```

Real notification integrations will require authentication, privacy, consent and safety controls.

### 11. Geographic Intelligence

V2 will improve the mapping system with:

- Hazard locations
- Impact zones
- Risk zones
- Population exposure
- Emergency facilities
- Safe facilities
- Evacuation areas
- Terrain and elevation
- Satellite imagery
- Weather layers
- Historical hazard layers

The goal is to move from displaying hazard points toward understanding spatial relationships between hazards, people and infrastructure.

### 12. Data Source Architecture

V2 will maintain a source registry so that external datasets have documented provenance.

Each source should record:

```text
Source
|-- name
|-- provider
|-- URL
|-- data type
|-- update frequency
|-- geographic coverage
|-- license / usage information
|-- last successful retrieval
+-- reliability notes
```

Potential categories include:

- Seismic data
- Weather data
- Rainfall data
- River and water-level data
- Cyclone information
- Wildfire information
- Climate indices
- Satellite/geographic data
- Elevation/terrain data

Authoritative government, scientific and public datasets will be preferred where available.

### 13. AI-Assisted Intelligence

AI will be introduced after deterministic monitoring and risk processing are stable.

Potential applications include:

- Event summarization
- Multi-source information synthesis
- Anomaly explanation
- Natural-language incident reports
- Disaster-response planning assistance
- Historical event analysis
- Operator question answering

AI will not replace authoritative hazard measurements.

Planned architecture:

```text
Authoritative Data
       |
       v
Deterministic Detection
       |
       v
Risk / Geographic Analysis
       |
       v
AI-Assisted Explanation
       |
       v
Human Decision
```

### 14. V2 Development Phases

#### Phase 2.1 — V2 Architecture

- Common hazard schema
- Hazard engine
- Risk engine
- Common source interface
- Project configuration
- Testing framework

#### Phase 2.2 — Flood Intelligence

- Rainfall ingestion
- Rainfall accumulation
- Flood-risk prototype
- Geographic impact estimation
- People integration
- Shelter integration

#### Phase 2.3 — Cyclone and Severe Weather

- Cyclone monitoring
- Severe-weather indicators
- Geographic impact
- Evacuation-support workflow

#### Phase 2.4 — Wildfire and Landslide

- Wildfire indicators
- Landslide-risk indicators
- Terrain/rainfall integration
- Affected-area analysis

#### Phase 2.5 — Climate Intelligence

- El Niño monitoring
- La Niña monitoring
- Rainfall anomalies
- Temperature anomalies
- Drought indicators
- Seasonal risk context

#### Phase 2.6 — Advanced Geographic Intelligence

- Improved map layers
- Terrain/elevation
- Satellite visualization
- Population exposure
- Risk overlays
- Historical hazard visualization

#### Phase 2.7 — AI-Assisted Analysis

- Incident summaries
- Multi-source analysis
- Natural-language reports
- Operator assistance
- Explainable risk reports

#### Phase 2.8 — V2 Integration and Testing

- End-to-end testing
- Source failure testing
- False-positive testing
- Missing-data testing
- Map testing
- Shelter testing
- Notification testing
- Performance testing
- Documentation

### 15. V2 Success Criteria

- [ ] Multiple hazard types can be monitored.
- [ ] Hazard sources are documented.
- [ ] Hazard data use a common internal representation.
- [ ] Risk calculations are explainable.
- [ ] Geographic impact can be visualized.
- [ ] People exposure can be calculated.
- [ ] Emergency facilities can be evaluated.
- [ ] Safe-shelter rules remain enforced.
- [ ] Climate signals are separated from immediate disaster events.
- [ ] Source failures do not crash the dashboard.
- [ ] Missing or incomplete data are handled safely.
- [ ] Alerts identify their source and timestamp.
- [ ] AI-generated information is separated from authoritative measurements.
- [ ] V2 functionality is tested before release.

### 16. V1 to V2 Evolution

| Capability | V1 | V2 Plan |
|---|---|---|
| Earthquake monitoring | Implemented | Expanded |
| Weather monitoring | Implemented | Expanded |
| Interactive map | Implemented | Advanced layers |
| People assistance | Implemented | Expanded |
| Emergency facilities | Implemented | Expanded |
| Safe shelter selection | Implemented | Advanced |
| Flood intelligence | Foundation | Planned |
| Cyclone monitoring | Demo scenario | Planned live monitoring |
| Wildfire | Demo scenario | Planned |
| Landslide | Not implemented | Planned |
| Tsunami | Limited indicator | Planned |
| Heatwave | Weather foundation | Planned |
| Drought | Not implemented | Planned |
| Air quality | Not implemented | Planned |
| El Niño | Not implemented | Planned |
| La Niña | Not implemented | Planned |
| Climate anomalies | Not implemented | Planned |
| Risk engine | Basic hazard logic | Planned |
| AI analysis | Not implemented | Planned |
| Geographic intelligence | Basic | Advanced planned |

### 17. Academic Project Direction

EARTHSHIELD V2 is intended to demonstrate how multiple environmental and disaster data sources can be combined into a unified monitoring and assistance architecture.

The project follows the principle:

> **Detect → Understand → Assess → Locate → Assist**

Where:

```text
DETECT
Identify relevant hazards from trusted data.

UNDERSTAND
Normalize and contextualize incoming information.

ASSESS
Estimate geographic and population exposure.

LOCATE
Identify affected people and available emergency facilities.

ASSIST
Provide transparent response and shelter information.
```

### V2 Planned Deliverable

The planned V2 release will provide a unified **Multi-Hazard Disaster Intelligence Dashboard** capable of combining:

```text
Earthquakes
Floods
Cyclones
Wildfires
Landslides
Tsunamis
Extreme Weather
Climate Signals
      |
      v
Hazard Intelligence
      |
      v
Risk Analysis
      |
      v
Geographic Impact
      |
      v
People + Facilities
      |
      v
Emergency Assistance
```

V2 development will begin only after the V1 baseline has been validated and documented.

### Current Development Status

**V1:** Stable baseline / completed

**V2:** Planned development phase

**Current branch strategy:**

- `main` → stable project baseline
- `v2-development` → V2 development work

V2 changes should be developed and tested separately before being promoted to the stable `main` branch.
