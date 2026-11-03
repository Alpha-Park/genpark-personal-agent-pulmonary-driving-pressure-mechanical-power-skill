"""
MCP Server for Pulmonary Driving Pressure (Delta P), Static Compliance & Mechanical Power.
Exposes tools for lung-protective ventilation and mechanical strain assessment.
"""

import json
from typing import Dict, Any, Optional
from client import PulmonaryDrivingPressureClient


def handle_evaluate_ventilation_stress(params: Dict[str, Any]) -> Dict[str, Any]:
    plateau_pressure_cmh2o = float(params.get("plateau_pressure_cmh2o", 22.0))
    peep_pressure_cmh2o = float(params.get("peep_pressure_cmh2o", 10.0))
    peak_pressure_cmh2o = float(params.get("peak_pressure_cmh2o", 28.0))
    tidal_volume_ml = float(params.get("tidal_volume_ml", 420.0))
    respiratory_rate_bpm = float(params.get("respiratory_rate_bpm", 16.0))
    patient_ideal_body_weight_kg = float(params.get("patient_ideal_body_weight_kg", 70.0))

    client = PulmonaryDrivingPressureClient()
    return client.evaluate_ventilation_stress(
        plateau_pressure_cmh2o=plateau_pressure_cmh2o,
        peep_pressure_cmh2o=peep_pressure_cmh2o,
        peak_pressure_cmh2o=peak_pressure_cmh2o,
        tidal_volume_ml=tidal_volume_ml,
        respiratory_rate_bpm=respiratory_rate_bpm,
        patient_ideal_body_weight_kg=patient_ideal_body_weight_kg
    )


TOOLS = {
    "evaluate_ventilation_stress": {
        "description": "Calculates airway Driving Pressure (Delta P = Pplat - PEEP), Static Compliance (Cstat), and Mechanical Power (Gattinoni equation) for lung-protective monitoring.",
        "parameters": {
            "type": "object",
            "properties": {
                "plateau_pressure_cmh2o": {
                    "type": "number",
                    "description": "End-inspiratory pause airway plateau pressure in cmH2O (e.g. 22.0)."
                },
                "peep_pressure_cmh2o": {
                    "type": "number",
                    "description": "Positive end-expiratory pressure in cmH2O (e.g. 10.0)."
                },
                "peak_pressure_cmh2o": {
                    "type": "number",
                    "description": "Peak dynamic inspiratory pressure in cmH2O (e.g. 28.0)."
                },
                "tidal_volume_ml": {
                    "type": "number",
                    "description": "Delivered tidal volume in mL (e.g. 420.0)."
                },
                "respiratory_rate_bpm": {
                    "type": "number",
                    "description": "Ventilator respiratory frequency in breaths/min, default 16.0."
                },
                "patient_ideal_body_weight_kg": {
                    "type": "number",
                    "description": "Ideal/predicted body weight in kg, default 70.0."
                }
            },
            "required": ["plateau_pressure_cmh2o", "peep_pressure_cmh2o", "peak_pressure_cmh2o", "tidal_volume_ml"]
        },
        "handler": handle_evaluate_ventilation_stress
    }
}


def process_request(request_str: str) -> str:
    try:
        req = json.loads(request_str)
        method = req.get("method")
        req_id = req.get("id")

        if method == "tools/list":
            tools_list = [
                {
                    "name": name,
                    "description": spec["description"],
                    "inputSchema": spec["parameters"]
                }
                for name, spec in TOOLS.items()
            ]
            return json.dumps({"jsonrpc": "2.0", "id": req_id, "result": {"tools": tools_list}})

        elif method == "tools/call":
            params = req.get("params", {})
            tool_name = params.get("name")
            args = params.get("arguments", {})

            if tool_name not in TOOLS:
                return json.dumps({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Tool '{tool_name}' not found"}
                })

            result = TOOLS[tool_name]["handler"](args)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2)
                        }
                    ]
                }
            })

        else:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32600, "message": f"Unsupported method '{method}'"}
            })

    except Exception as e:
        return json.dumps({
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32000, "message": str(e)}
        })


if __name__ == "__main__":
    import sys
    for line in sys.stdin:
        if line.strip():
            print(process_request(line))
            sys.stdout.flush()
