# Pulmonary Driving Pressure ($\Delta P$), Static Compliance & Mechanical Power Skill

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)
[![Python: 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![Model Context Protocol](https://img.shields.io/badge/MCP-Standard-green.svg)](https://modelcontextprotocol.io/)
[![Zero External Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen.svg)](requirements.txt)
[![Status: Production-Ready](https://img.shields.io/badge/status-production--ready-success.svg)](https://github.com/alphaparkinc)

A zero-dependency, mathematically rigorous personal agent skill that computes airway driving pressure, static respiratory compliance, and mechanical power of ventilation to prevent ventilator-induced lung injury (VILI).

## Architecture

```mermaid
flowchart TD
    A[Inspiratory/Expiratory Pause Manometry] --> B[Sample Pplat, PEEP, Ppeak, and Tidal Volume]
    B --> C[Compute Driving Pressure Delta P = Pplat - PEEP]
    C --> D[Compute Static Compliance Cstat = Vt / Delta P]
    D --> E[Compute Gattinoni Mechanical Power MP]
    E --> F[Lung Protection Stratification & Guidance]
```

## Quick Start

```python
from client import PulmonaryDrivingPressureClient

client = PulmonaryDrivingPressureClient()
result = client.evaluate_ventilation_stress(
    plateau_pressure_cmh2o=20.0,
    peep_pressure_cmh2o=10.0,
    peak_pressure_cmh2o=24.0,
    tidal_volume_ml=420.0,
    respiratory_rate_bpm=16.0
)
print("Driving Pressure (cmH2O):", result["mechanics"]["driving_pressure_delta_p_cmh2o"])
print("Static Compliance (mL/cmH2O):", result["mechanics"]["static_compliance_cstat_ml_cmh2o"])
print("Status:", result["clinical_safety_stratification"]["driving_pressure_status"])
```

## License
Apache-2.0
