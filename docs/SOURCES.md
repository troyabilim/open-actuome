# Sources and claim boundaries

Sources consulted 9 November 2026. These are existing-work references, not
benchmark evidence for the supplied synthetic examples.

| Source | What it supports | What it does not establish |
|---|---|---|
| [MuJoCo computation](https://mujoco.readthedocs.io/en/stable/computation/index.html) | Existing transmission, activation and force-generation models | That no actuation-description framework exists |
| [Isaac Lab actuators](https://isaac-sim.github.io/IsaacLab/main/source/concepts/actuators.html) | Existing actuator envelopes and delay models | Compatibility of the new draft without an adapter test |
| [Open X-Embodiment](https://robotics-transformer-x.github.io/) | Published cross-robot learning/transfer results | Universal transfer to arbitrary robot hardware |
| [Gemini Robotics 1.5](https://deepmind.google/blog/gemini-robotics-15-brings-ai-agents-into-the-physical-world/) | Reported cross-embodiment capability examples | Transfer between the particular manufacturer pairs named in the initial draft |
| [JSON Schema 2020-12](https://json-schema.org/draft/2020-12) | The structural schema dialect | Physical validation or the extra semantic rules |

## Claim boundaries

The examples contain no manufacturer benchmark evidence. The draft does not
establish an industry standard, compute a universal performance score, compile
action tokens or guarantee cross-robot policy transfer. The schema and pilot
plan are project proposals, not findings inferred from the cited sources.
