"""
Pulmonary Driving Pressure (Delta P), Static Compliance & Mechanical Power Client.
Zero-mock pure Python standard library implementation.
Calculates Airway Driving Pressure (Delta P = Pplat - PEEP), Static Respiratory System
Compliance (Cstat = Vt / Delta P), and Mechanical Power (Gattinoni equation) to protect against VILI.
"""

import math
from typing import Dict, Any, Optional


class PulmonaryDrivingPressureClient:
    """
    Evaluates lung-protective ventilation mechanics and mechanical stress:
    - Delta P = Pplat - PEEP (cmH2O)
    - Cstat = Vt / Delta P (mL / cmH2O)
    - Mechanical Power (MP in J/min) = 0.098 * RR * (Vt / 1000) * (Ppeak - Delta P / 2)
    - Driving pressure target <= 14 cmH2O (Amato NEJM trial)
    - Mechanical power safe limit < 17.0 J/min
    """

    def __init__(self):
        pass

    def evaluate_ventilation_stress(
        self,
        plateau_pressure_cmh2o: float,
        peep_pressure_cmh2o: float,
        peak_pressure_cmh2o: float,
        tidal_volume_ml: float,
        respiratory_rate_bpm: Optional[float] = 16.0,
        patient_ideal_body_weight_kg: Optional[float] = 70.0
    ) -> Dict[str, Any]:
        """
        Calculates driving pressure, static compliance, and mechanical power.
        plateau_pressure_cmh2o: end-inspiratory plateau airway pressure (e.g. 22.0 cmH2O).
        peep_pressure_cmh2o: positive end-expiratory pressure (e.g. 10.0 cmH2O).
        peak_pressure_cmh2o: maximum inspiratory dynamic airway pressure (e.g. 28.0 cmH2O).
        tidal_volume_ml: delivered tidal volume in mL (e.g. 420.0 mL).
        respiratory_rate_bpm: ventilatory frequency in breaths/min (default 16.0).
        """
        if tidal_volume_ml <= 0 or respiratory_rate_bpm <= 0:
            raise ValueError("Tidal volume and respiratory rate must be strictly positive.")
        if plateau_pressure_cmh2o < peep_pressure_cmh2o:
            raise ValueError("Plateau pressure cannot be lower than PEEP.")
        if peak_pressure_cmh2o < plateau_pressure_cmh2o:
            raise ValueError("Peak pressure cannot be lower than plateau pressure.")

        # Driving Pressure (Delta P in cmH2O)
        delta_p = plateau_pressure_cmh2o - peep_pressure_cmh2o

        # Static Compliance (Cstat in mL/cmH2O)
        cstat = (tidal_volume_ml / delta_p) if delta_p > 0 else 0.0

        # Tidal volume in Liters
        vt_liters = tidal_volume_ml / 1000.0

        # Tidal volume per kg ideal body weight (mL/kg IBW)
        vt_per_kg = tidal_volume_ml / patient_ideal_body_weight_kg if patient_ideal_body_weight_kg > 0 else 6.0

        # Mechanical Power of Ventilation (MP in Joules/min)
        # Gattinoni simplified equation: 0.098 * RR * Vt * (Ppeak - Delta P / 2)
        mechanical_power_j_min = 0.098 * respiratory_rate_bpm * vt_liters * (peak_pressure_cmh2o - (delta_p / 2.0))

        # Dynamic Pressure Drop / Resistive Component (cmH2O)
        delta_p_resistive = peak_pressure_cmh2o - plateau_pressure_cmh2o

        # Clinical Lung-Protective Risk Stratification (Amato NEJM / Gattinoni Intensive Care):
        # Driving pressure <= 14 cmH2O: Safe protective range
        # Driving pressure > 14 cmH2O: Elevated cyclic parenchymal strain
        # Driving pressure > 18 cmH2O: Severe transpulmonary stress / high VILI risk
        if delta_p > 18.0:
            driving_pressure_status = "Critically Elevated Driving Pressure (High Volutrauma / VILI Risk)"
            clinical_risk = "Excessive alveolar cyclical strain on functional lung units; urgent down-titration of tidal volume or PEEP optimization required."
        elif delta_p > 14.0:
            driving_pressure_status = "Borderline / Elevated Driving Pressure (> 14 cmH2O)"
            clinical_risk = "Increased cyclical strain exceeding Amato threshold; consider reducing tidal volume towards 6 mL/kg PBW."
        else:
            driving_pressure_status = "Protective Driving Pressure (<= 14 cmH2O)"
            clinical_risk = "Optimal parenchymal lung protection; cyclical strain within safe physiological limits."

        # Mechanical Power Staging
        # MP < 17 J/min: Safe protective energy transfer
        # MP 17 - 22 J/min: Moderate mechanical power exposure
        # MP > 22 J/min: High cumulative mechanical power (baro/volutrauma risk)
        if mechanical_power_j_min > 22.0:
            power_status = "Excessive Mechanical Power (> 22 J/min)"
        elif mechanical_power_j_min >= 17.0:
            power_status = "Intermediate Mechanical Power (17 - 22 J/min)"
        else:
            power_status = "Protective Mechanical Power (< 17 J/min)"

        return {
            "status": "success",
            "mechanics": {
                "driving_pressure_delta_p_cmh2o": round(delta_p, 1),
                "static_compliance_cstat_ml_cmh2o": round(cstat, 1),
                "mechanical_power_j_per_min": round(mechanical_power_j_min, 1),
                "resistive_pressure_drop_cmh2o": round(delta_p_resistive, 1),
                "tidal_volume_ml_per_kg_ibw": round(vt_per_kg, 1)
            },
            "ventilator_pressures_cmh2o": {
                "plateau_pressure_cmh2o": round(plateau_pressure_cmh2o, 1),
                "peep_pressure_cmh2o": round(peep_pressure_cmh2o, 1),
                "peak_pressure_cmh2o": round(peak_pressure_cmh2o, 1)
            },
            "clinical_safety_stratification": {
                "driving_pressure_status": driving_pressure_status,
                "mechanical_power_status": power_status,
                "pathophysiology_guidance": clinical_risk
            }
        }
