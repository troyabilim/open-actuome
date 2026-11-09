# Interoperability map

Status: design guidance only. No simulator adapter has been implemented or tested.
The working integration shipped today is JSON profile → validation → Markdown report.

| OpenActuome observation | Existing representation to investigate | Mapping limitation |
|---|---|---|
| Rotary/linear effort and speed | MuJoCo joint/actuator limits; Isaac Lab effort and velocity limits | Actuator input vs joint output, gear mapping and backend enforcement differ |
| Effort-speed curve | Isaac Lab DC motor envelope or explicit custom actuator model | A general sampled curve is not necessarily a linear DC motor law |
| Latency observations | Isaac Lab delayed actuators | A delay distribution is not fully described by median/p95/max; controller and physics periods differ |
| Transmission classification | MuJoCo transmission configuration; URDF-related models | A category is insufficient to reconstruct mechanism geometry or gear ratios |
| Thermal observations | Custom runtime/model logic | No automatic thermal solver is shipped |
| Provenance and conditions | Sidecar metadata linked to configuration | Metadata does not establish parameter correctness |

Before implementing an adapter, pick an exact tool version, state reference frames,
record unit conversions, and specify every dropped field. Test output back against
the source profile. Never substitute an assumed value for an unknown measurement.

Primary references:

- [MuJoCo actuation model](https://mujoco.readthedocs.io/en/stable/computation/index.html).
- [Isaac Lab actuators](https://isaac-sim.github.io/IsaacLab/main/source/concepts/actuators.html).
- [ros2_control documentation](https://control.ros.org/rolling/index.html).

These references establish relevant existing work, not endorsement or compatibility
certification of OpenActuome.
