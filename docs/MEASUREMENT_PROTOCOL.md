# Measurement protocol — proposed, not experimentally validated

Version 0.1.0. Use only within manufacturer-approved procedures and limits,
with appropriate instrumentation and qualified supervision. This document does
not authorize destructive tests or define a robot commissioning procedure.

## 1. Identify the configuration

Record hardware model/revision, serial or anonymized sample identity, transmission,
controller/firmware, command mode, axis mapping, supply, mounting, cooling,
ambient conditions and relevant calibration records. Define an axis at the
output, so motor-shaft and joint-output measurements are not silently mixed.

## 2. Preserve evidence

Retain timestamped raw data, data-processing version, calibration information,
filtering/resampling choices, source rights and an uncertainty statement.
Use a measurement report as a source locator. Keep personal or confidential
information out of a public profile. Each published number should be reproducible
from its evidence, subject to the disclosed uncertainty.

## 3. Define the observation before collecting it

| Property | Required observation definition |
|---|---|
| Continuous effort | Output effort and speed, duty, steady-state criterion, observation duration, environment and cooling |
| Burst effort | Initial state, burst duration, repetition/rest interval and manufacturer-approved envelope |
| Latency | Explicit start/end events, clock synchronization, command path, response threshold, sampling rate and repetitions |
| Backdrivability | Power/control state, external loading method, motion threshold, direction and hysteresis |
| Thermal derating | Sensor location, calibration, ambient/load/cooling conditions and the effort reference for each fraction |
| Effort-speed curve | Output units, direction, sampling points, steady-state criterion and configuration shared with other observations |

Example latency boundary: timestamp when a host emits a command to the instant
that output effort reaches a predeclared percentage of the commanded change.
The threshold must be stated in `boundary_detail`; do not treat this example
as a universally suitable test. Bus transit time and mechanical response time
are different quantities.

## 4. Report distributions and uncertainty

Record sample count, median, p95 and maximum from the same observation set.
Specify the percentile estimator and clock resolution in the source report.
Publish variability across repetitions and state whether trial order was
randomized. Do not compare p95 values collected under different boundaries as
though they measured the same thing. The validator warns below 100 samples for
a measured p95; that threshold is a reporting heuristic, not a statistical guarantee.

## 5. Compare only comparable observations

Match task, control mode, output reference, load, duty, temperature, power and
measurement boundary before making a comparison. Keep linear and rotary effort
separate. Do not derive torque density without a consistent mass definition.
Document what is not comparable. There is no aggregate Actuome Score in 0.1.

## 6. Separate two experiments

**Profile portability:** map supported properties into a selected tool, export
them back and compare units, values and lost fields. Report fidelity and limitations.

**Policy transfer:** if later studied, define source/target robots, policy and
adaptation method, training data access, task suite, baseline, trials and failure
criteria. Measure task outcomes. A successful profile conversion is not proof of
zero-shot policy transfer.

## First pilot acceptance criteria

- Two distinct actuators with traceable observations, not synthetic fixtures.
- Complete evidence and conditions for each published quantity.
- A documented mapping into one existing tool, with a round-trip check.
- Reproducible validation/report generation and a written limitations section.
- An independent reviewer can reproduce at least one result from the supplied data.

These are future milestones. No hardware pilot is claimed in the initial package.
