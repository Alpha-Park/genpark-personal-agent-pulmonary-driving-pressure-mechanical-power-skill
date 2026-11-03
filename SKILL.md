---
name: genpark-personal-agent-pulmonary-driving-pressure-mechanical-power-skill
version: 1.0.0
description: Calculates airway Driving Pressure (Delta P = Pplat - PEEP), Static Compliance (Cstat), and Mechanical Power (MP).
license: Apache-2.0
compatibility:
  python: ">=3.9"
  openclaw: ">=1.0.0"
  mcp: ">=1.0.0"
---

# Pulmonary Driving Pressure ($\Delta P$), Static Compliance & Mechanical Power Skill

A zero-dependency personal agent skill for monitoring lung-protective mechanical ventilation mechanics, cyclical alveolar strain, and cumulative mechanical power.

## Features
- **Airway Driving Pressure ($\Delta P$)**: Computes $\Delta P = P_{\text{plat}} - PEEP$, benchmarking against the Amato NEJM threshold ($\le 14\text{ cmH}_2\text{O}$).
- **Static Respiratory Compliance ($C_{\text{stat}}$)**: Calculates $C_{\text{stat}} = V_T / \Delta P$ to assess functional aerated lung size ("baby lung").
- **Mechanical Power of Ventilation ($MP$)**: Evaluates continuous energy transfer rate via Gattinoni's equation ($< 17.0\text{ J/min}$ safe limit).
- **VILI Risk Stratification**: Identifies excessive cyclical strain and volutrauma vulnerability.

## MCP Server Integration
Exposes `evaluate_ventilation_stress` for autonomous respiratory care, ICU triage, and pulmonary wellness monitoring.
