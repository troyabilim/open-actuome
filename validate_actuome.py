#!/usr/bin/env python3
"""Offline OpenActuome 0.1 validator. No robot I/O and no third-party dependencies.

The structural validator supports ONLY the JSON Schema subset used by the bundled
schema. It is not advertised as a general JSON Schema implementation. Validation
does not establish that measurements are true or that a robot is safe to operate.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import math
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent
SCHEMA_PATH = ROOT / "spec" / "0.1.0" / "actuome.schema.json"
SUPPORTED = {"$schema", "$id", "$defs", "$ref", "title", "description", "examples",
             "type", "enum", "const", "properties", "required", "additionalProperties",
             "items", "minItems", "maxItems", "minLength", "maxLength", "pattern",
             "minimum", "maximum", "exclusiveMinimum", "anyOf"}


def reject_constant(value):
    raise ValueError(f"Non-finite JSON number: {value}")


def unique_object(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError(f"Duplicate JSON key: {key}")
        obj[key] = value
    return obj


def load_json(path):
    with Path(path).open(encoding="utf-8-sig") as handle:
        return json.load(handle, parse_constant=reject_constant, object_pairs_hook=unique_object)


def check_schema_subset(schema):
    """Fail closed if the bundled schema evolves beyond this validator's subset."""
    if not isinstance(schema, dict):
        raise ValueError("Schema nodes must be objects")
    unknown = set(schema) - SUPPORTED
    if unknown:
        raise ValueError(f"Unsupported schema keywords: {sorted(unknown)}")
    if "$ref" in schema and (len(schema) != 1 or not schema["$ref"].startswith("#/$defs/")):
        raise ValueError("Only local, standalone $defs references are supported")
    for group in ("$defs", "properties"):
        for child in schema.get(group, {}).values():
            check_schema_subset(child)
    if "items" in schema:
        check_schema_subset(schema["items"])
    for child in schema.get("anyOf", []):
        check_schema_subset(child)


def is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def matches_type(value, kind):
    return {"object": lambda: isinstance(value, dict),
            "array": lambda: isinstance(value, list),
            "string": lambda: isinstance(value, str),
            "number": lambda: is_number(value),
            "integer": lambda: is_number(value) and value == int(value),
            "boolean": lambda: isinstance(value, bool),
            "null": lambda: value is None}[kind]()


def structurally_validate(value, schema, root, path="$"):
    errors = []
    if "$ref" in schema:
        name = schema["$ref"].split("/")[-1]
        if name not in root.get("$defs", {}):
            raise ValueError(f"Unknown schema reference: {name}")
        return structurally_validate(value, root["$defs"][name], root, path)
    if "anyOf" in schema and not any(
        not structurally_validate(value, branch, root, path) for branch in schema["anyOf"]
    ):
        return [f"{path}: does not match any allowed value shape"]
    if "type" in schema and not matches_type(value, schema["type"]):
        return [f"{path}: expected {schema['type']}"]
    # The bundled enums/constants are strings, so Python's bool/int equality cannot leak in.
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: invalid option {value!r}")
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: expected {schema['const']!r}")
    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{path}: missing {key}")
        props = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for key in value.keys() - props.keys():
                errors.append(f"{path}: unknown field {key}")
        for key in value.keys() & props.keys():
            errors.extend(structurally_validate(value[key], props[key], root, f"{path}.{key}"))
    elif isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path}: too few items")
        if len(value) > schema.get("maxItems", float("inf")):
            errors.append(f"{path}: too many items")
        if "items" in schema:
            for i, child in enumerate(value):
                errors.extend(structurally_validate(child, schema["items"], root, f"{path}[{i}]"))
    elif isinstance(value, str):
        if len(value) < schema.get("minLength", 0) or len(value) > schema.get("maxLength", float("inf")):
            errors.append(f"{path}: invalid string length")
        if "pattern" in schema and re.search(schema["pattern"], value) is None:
            errors.append(f"{path}: invalid string pattern")
    elif is_number(value):
        for key, fails in (("minimum", lambda v: value < v), ("maximum", lambda v: value > v),
                           ("exclusiveMinimum", lambda v: value <= v)):
            if key in schema and fails(schema[key]):
                errors.append(f"{path}: violates {key} {schema[key]}")
    return errors


def validate_profile(data, measured_only=False):
    schema = load_json(SCHEMA_PATH)
    check_schema_subset(schema)
    errors = structurally_validate(data, schema, schema)
    warnings = []
    if errors:
        return {"valid": False, "errors": sorted(errors), "warnings": warnings}

    axes = data["axes"]
    count = len(axes)
    total = data["platform"]["total_actuated_dof"]
    if data["coverage"] == "complete" and count != total:
        errors.append("Complete coverage requires one axis per declared actuated DoF")
    if data["coverage"] == "partial" and count >= total:
        errors.append("Partial coverage requires fewer described axes than total actuated DoF")
    for group, id_key in (("axes", "axis_id"), ("sources", "source_id"), ("interfaces", "interface_id")):
        ids = [entry[id_key] for entry in data[group]]
        if len(ids) != len(set(ids)):
            errors.append(f"{group}: duplicate {id_key}")
    sources = {s["source_id"]: s for s in data["sources"]}
    interfaces = {b["interface_id"] for b in data["interfaces"]}
    bases = set()
    for axis in axes:
        prefix = axis["axis_id"]
        evidence = axis["evidence"]
        basis = evidence["basis"]
        bases.add(basis)
        expected = ("N*m", "rad/s") if axis["motion"] == "rotary" else ("N", "m/s")
        if (axis["effort_unit"], axis["velocity_unit"]) != expected:
            errors.append(f"{prefix}: units do not match motion type")
        if axis["interface_ref"] not in interfaces:
            errors.append(f"{prefix}: unknown interface_ref")
        if len(evidence["source_refs"]) != len(set(evidence["source_refs"])):
            errors.append(f"{prefix}: duplicate source_refs")
        for ref in evidence["source_refs"]:
            if ref not in sources:
                errors.append(f"{prefix}: unknown evidence source {ref}")
            elif sources[ref]["kind"] == "illustration" and basis != "synthetic":
                errors.append(f"{prefix}: illustrative source cannot substantiate non-synthetic data")
        if basis in ("measured", "manufacturer_declared", "simulated"):
            if not evidence["source_refs"]:
                errors.append(f"{prefix}: non-synthetic data requires a source")
        if basis == "measured":
            for key in ("measured_at", "sample_count", "instrument", "uncertainty_note"):
                if key not in evidence:
                    errors.append(f"{prefix}: measured evidence requires {key}")
            for key in ("ambient_temperature_c", "supply_voltage_v", "load_description", "cooling"):
                if evidence["conditions"].get(key) is None:
                    errors.append(f"{prefix}: measured evidence requires condition {key}")
            stamp = evidence.get("measured_at")
            if stamp:
                try:
                    parsed = dt.datetime.fromisoformat(stamp.replace("Z", "+00:00"))
                    if parsed.tzinfo is None or parsed.utcoffset() is None:
                        raise ValueError("timezone missing")
                except ValueError:
                    errors.append(f"{prefix}: measured_at must be an ISO datetime with timezone")
        limits = axis["limits"]
        continuous, peak = limits["continuous_effort"], limits["peak_effort"]
        if continuous is not None and peak is not None and peak < continuous:
            errors.append(f"{prefix}: peak effort is below continuous effort")
        if peak is not None and limits["peak_duration_s"] is None:
            errors.append(f"{prefix}: peak effort requires a defined burst duration")
        if continuous is not None and limits["continuous_effort_at_velocity"] is None:
            errors.append(f"{prefix}: continuous effort requires its reference velocity")
        if (limits["max_velocity"] is not None and limits["continuous_effort_at_velocity"] is not None
                and limits["continuous_effort_at_velocity"] > limits["max_velocity"]):
            errors.append(f"{prefix}: reference velocity exceeds max velocity")
        latency = axis["latency"]
        values = [latency[k] for k in ("median_ms", "p95_ms", "max_ms")]
        known = [v for v in values if v is not None]
        if known != sorted(known):
            errors.append(f"{prefix}: latency quantiles must be ordered median <= p95 <= max")
        if known and latency["boundary"] == "unknown":
            errors.append(f"{prefix}: latency numbers require a stated measurement boundary")
        if basis == "measured" and latency["p95_ms"] is not None and evidence.get("sample_count", 0) < 100:
            warnings.append(f"{prefix}: fewer than 100 latency samples; p95 estimate may be unstable")
        curve = axis.get("effort_speed_curve", [])
        speeds = [point["speed"] for point in curve]
        if any(a >= b for a, b in zip(speeds, speeds[1:])):
            errors.append(f"{prefix}: curve speeds must be strictly increasing")
        if continuous is not None and any(point["continuous_effort"] > continuous for point in curve):
            errors.append(f"{prefix}: curve exceeds stated continuous effort envelope")
        if limits["max_velocity"] is not None and any(v > limits["max_velocity"] for v in speeds):
            errors.append(f"{prefix}: curve exceeds stated velocity envelope")
        thermal = axis.get("thermal", {})
        derating = thermal.get("derating_curve", [])
        temps = [p["temperature_c"] for p in derating]
        if any(a >= b for a, b in zip(temps, temps[1:])):
            errors.append(f"{prefix}: derating temperatures must be strictly increasing")
        if derating and thermal.get("sensor_location", "unknown") == "unknown":
            errors.append(f"{prefix}: thermal curve requires sensor location")
        if basis == "unknown":
            numeric_fields = list(limits.values()) + values
            numeric_fields += [axis["backdrive_threshold_effort"], thermal.get("limit_c")]
            if any(v is not None for v in numeric_fields) or curve or derating or axis["backdrivable"] != "unknown":
                errors.append(f"{prefix}: unknown evidence cannot carry asserted physical measurements")
        if measured_only and basis != "measured":
            errors.append(f"{prefix}: measured-only mode rejects {basis} evidence")
        if basis != "measured":
            warnings.append(f"{prefix}: {basis} data; not a measured hardware profile")
    expected_status = next(iter(bases)) if len(bases) == 1 else "mixed"
    if data["data_status"] != expected_status:
        errors.append(f"data_status must match axis evidence ({expected_status})")
    if data["coverage"] == "partial":
        warnings.append(f"Partial coverage: {count} of {total} actuated DoF described")
    return {"valid": not errors, "profile_id": data["profile_id"], "data_status": data["data_status"],
            "described_actuated_dof": count, "declared_actuated_dof": total,
            "errors": sorted(errors), "warnings": sorted(warnings),
            "physical_measurements_verified": False}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", type=Path)
    parser.add_argument("--measured-only", action="store_true", help="Reject non-measured evidence labels")
    parser.add_argument("--json", action="store_true", help="Machine-readable validation result")
    args = parser.parse_args(argv)
    try:
        result = validate_profile(load_json(args.profile), args.measured_only)
    except (OSError, ValueError, json.JSONDecodeError, OverflowError, RecursionError) as exc:
        result = {"valid": False, "errors": [f"Input error: {exc}"], "warnings": []}
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("PASS: profile structure and consistency" if result["valid"] else "FAIL: invalid profile")
        for error in result["errors"]:
            print(f"  ERROR: {error}")
        for warning in result["warnings"]:
            print(f"  NOTE: {warning}")
        print("Validation does not verify physical measurements or operating safety.")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
