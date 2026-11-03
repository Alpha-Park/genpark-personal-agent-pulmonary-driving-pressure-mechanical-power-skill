"""
Example usage of Pulmonary Driving Pressure (Delta P), Static Compliance & Mechanical Power.
Demonstrates protective ventilation mechanics vs high mechanical power VILI risk.
"""

from client import PulmonaryDrivingPressureClient

def main():
    client = PulmonaryDrivingPressureClient()

    print("=== Case 1: Lung-Protective Mechanical Ventilation ===")
    protective_case = client.evaluate_ventilation_stress(
        plateau_pressure_cmh2o=20.0,
        peep_pressure_cmh2o=10.0,
        peak_pressure_cmh2o=24.0,
        tidal_volume_ml=420.0,
        respiratory_rate_bpm=16.0,
        patient_ideal_body_weight_kg=70.0
    )
    print("Ventilation Mechanics:")
    print(f"  Driving Pressure (Delta P): {protective_case['mechanics']['driving_pressure_delta_p_cmh2o']} cmH2O")
    print(f"  Static Compliance (Cstat):  {protective_case['mechanics']['static_compliance_cstat_ml_cmh2o']} mL/cmH2O")
    print(f"  Mechanical Power (MP):      {protective_case['mechanics']['mechanical_power_j_per_min']} J/min")
    print(f"  Status:                     {protective_case['clinical_safety_stratification']['driving_pressure_status']}")
    print(f"  Power Status:               {protective_case['clinical_safety_stratification']['mechanical_power_status']}")

    print("\n=== Case 2: ARDS with Elevated Cyclical Strain (High VILI Risk) ===")
    high_strain_case = client.evaluate_ventilation_stress(
        plateau_pressure_cmh2o=31.0,
        peep_pressure_cmh2o=12.0,
        peak_pressure_cmh2o=38.0,
        tidal_volume_ml=520.0,
        respiratory_rate_bpm=24.0,
        patient_ideal_body_weight_kg=65.0
    )
    print("Ventilation Mechanics:")
    print(f"  Driving Pressure (Delta P): {high_strain_case['mechanics']['driving_pressure_delta_p_cmh2o']} cmH2O (Excessive cyclical strain!)")
    print(f"  Static Compliance (Cstat):  {high_strain_case['mechanics']['static_compliance_cstat_ml_cmh2o']} mL/cmH2O")
    print(f"  Mechanical Power (MP):      {high_strain_case['mechanics']['mechanical_power_j_per_min']} J/min")
    print(f"  Status:                     {high_strain_case['clinical_safety_stratification']['driving_pressure_status']}")
    print(f"  Guidance:                   {high_strain_case['clinical_safety_stratification']['pathophysiology_guidance']}")

if __name__ == "__main__":
    main()
