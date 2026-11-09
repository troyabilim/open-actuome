# OpenActuome 0.1.0 specification

Status: experimental draft; schema ID `urn:openactuome:spec:0.1.0`.
The URN is an identifier, not a claim to a live website or registry.

## Representation and scope

Profiles are UTF-8 JSON. Duplicate keys, non-finite numbers and unknown fields
are rejected by the supplied validator. JSON Schema 2020-12 describes structure;
the semantic rules below are additional requirements. YAML ingestion is not shipped.

An `axis` is one **actuated scalar degree of freedom**, not necessarily one
mechanical joint. Several axes may share a joint name, but axis IDs must be
unique. Floating-base coordinates are excluded from `total_actuated_dof`.
Coupled/spherical actuation cannot be represented as a full coupled model in
0.1. Scalar axis entries may document separate observations, with coupling
limitations disclosed in `notes`. There are no multi-axis tensors in this draft.

`coverage: complete` means that the number of axis records equals the declared
actuated DoF. It does not mean that every physical property has been measured.
`partial` requires fewer axis records than declared actuated DoF. Zero records
are not a useful profile and are rejected.

## Fields and units

| Field | Meaning |
|---|---|
| `platform` | Name, manufacturer, exact revision and total actuated DoF |
| `data_status` | Common axis evidence basis, or `mixed` for differing bases |
| `sources` | Stable source ID, type, locator, title and rights note |
| `interfaces` | Declared connection metadata; cycle time is not action latency |
| `axis_id`, `joint_name` | Unique scalar axis and corresponding mechanical joint |
| `motion` | `rotary` or `linear` |
| `effort_unit` | `N*m` for rotary, `N` for linear |
| `velocity_unit` | `rad/s` for rotary, `m/s` for linear |
| `motor_type`, `transmission` | Separate motor and transmission classifications |
| `limits.continuous_effort` | Nonnegative maximum continuous output-effort magnitude for the declared conditions |
| `continuous_effort_at_velocity` | Nonnegative output-speed magnitude at which the continuous value applies |
| `peak_effort`, `peak_duration_s` | Burst effort and permitted duration for stated conditions; not an unconditional safe limit |
| `max_velocity` | Nonnegative output-speed envelope for the same configuration |
| `latency` | Nonnegative median, p95 and maximum delay in milliseconds with explicit observation boundaries |
| `backdrivable` | `yes`, `no` or `unknown` under the recorded test conditions |
| `backdrive_threshold_effort` | External effort magnitude at onset of observable motion, in the axis effort unit |
| `thermal.limit_c` | Reported temperature limit in degrees Celsius, with sensor location |
| `thermal.derating_curve` | Temperature versus allowed fraction of the stated effort reference |
| `effort_speed_curve` | Speed magnitude versus continuous effort magnitude; same units and conditions as axis limits |

The current envelope assumes a stated symmetric magnitude summary. Directional
asymmetry, regenerative operation and negative-speed curves require disclosure
and are not represented fully. A housing temperature is not a winding temperature.
No values are converted between Celsius and other temperature units implicitly.

`null` means unknown or not supplied. It never means zero. Missing optional
curves are not treated as constant curves. Nonnegative does not mean safe.

## Evidence

Every axis has one evidence record for its stated physical observations. Do not
mix measured and invented quantities inside one axis record: use unknown values
or separate, clearly scoped profiles. The available basis labels are:

- `measured`: requires a source, timestamp with timezone, sample count, instrument,
  uncertainty note, method and non-null ambient temperature, supply voltage,
  load and cooling conditions. Mounting and controller descriptions are required.
- `manufacturer_declared`: a source document and conditions are required; do not
  relabel a catalogue value as a laboratory measurement.
- `simulated`: a simulation artifact, version/configuration description and conditions.
- `synthetic`: invented fixture values used only to demonstrate the format.
- `unknown`: physical values stay null and no curves or categorical backdrive
  claim are asserted.

An illustrative source cannot substantiate measured, declared or simulated data.
Locators are citations, never instructions to execute or retrieve files.
References must resolve within the source registry. The validator does not fetch
sources, verify ownership, or determine whether an experiment actually happened.

## Semantic rules enforced outside JSON Schema

1. Coverage and actuated DoF agree; source, interface and axis IDs are unique.
2. Evidence and interface references resolve; top-level status agrees with axes.
3. Rotary and linear units match their motion types.
4. Peak effort is at least continuous effort when both are known; a stated peak
   has a positive duration; continuous effort has a reference speed.
5. A known reference speed is within a known maximum speed.
6. Known latency quantiles are ordered; numeric latency needs a defined boundary.
7. Curves have strictly increasing speed or temperature values. Effort-speed
   points remain within known continuous-effort and speed envelopes.
8. Temperature fractions stay between 0 and 1. A thermal curve names a sensor.
9. Unknown provenance cannot carry asserted physical measurements.
10. `--measured-only` rejects all non-measured axes. This is a declaration gate,
    not independent verification of the underlying data.

## Compatibility and versioning

This validator accepts only `0.1.0`. Incompatible field or interpretation changes
need a new version and migration notes. Proposals go through an issue, a documented
example and tests. The identifier is deliberately independent of an unclaimed
GitHub organization or domain. No web endpoint is needed for offline validation.

## Supported structural subset

The dependency-free validator covers the keywords actually used here: local
`$defs`/`$ref`, `type`, `enum`, `const`, `properties`, `required`,
`additionalProperties: false`, `items`, array/string bounds, numeric bounds,
`pattern`, and `anyOf`, plus annotations. It fails closed on an unsupported
schema keyword. It is not a replacement for a general Draft 2020-12 engine.
