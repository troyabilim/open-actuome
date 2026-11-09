# OpenActuome profile: demo-bench-2-synthetic

Data status: **synthetic**. Coverage: **complete**.
Described actuated DoF: 2 / 2.

Structure and consistency passed. Physical measurements have NOT been independently verified.

| Axis | Basis | Continuous effort | Peak / duration | Max speed | Median / p95 latency | Boundary |
|---|---|---|---|---|---|---|
| bench_rotation | synthetic | 4.0 N*m | 8.0 N*m / 0.5 s | 6.0 rad/s | 2.0 / 3.0 ms | command_to_effort |
| bench_translation | synthetic | 50.0 N | 80.0 N / 0.2 s | 0.1 m/s | 2.0 / 3.0 ms | command_to_effort |

## Evidence and conditions

### bench_rotation

Method: Hand-authored values to exercise the schema. No hardware measurement.

Sources: synthetic-design

Latency boundary: Illustrative host timestamp to output effort at 90% of commanded step; no measurement.

- ambient_temperature_c: 23.0
- supply_voltage_v: 24.0
- load_description: Invented constant-load bench scenario; no experiment performed.
- cooling: Illustrative passive air cooling
- controller_configuration: Fictional controller; no executable gains supplied
- mounting: Fictional rigid benchtop fixture

### bench_translation

Method: Hand-authored values to exercise the schema. No hardware measurement.

Sources: synthetic-design

Latency boundary: Illustrative host timestamp to output effort at 90% of commanded step; no measurement.

- ambient_temperature_c: 23.0
- supply_voltage_v: 24.0
- load_description: Invented constant-load bench scenario; no experiment performed.
- cooling: Illustrative passive air cooling
- controller_configuration: Fictional controller; no executable gains supplied
- mounting: Fictional rigid benchtop fixture

## Source registry

- synthetic-design: OpenActuome synthetic fixture — examples/demo_bench.synthetic.json

No aggregate score or cross-platform ranking is calculated.
