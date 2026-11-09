# The Actuome Manifesto
## Make the physical assumptions of embodied AI inspectable

**OpenActuome · Experimental proposal 0.1.0 · 9 November 2026**  
Project owner: **[Troya Science](https://troyascience.com)**

### Intelligence has a physical interface

A robot policy produces actions. Whether those actions become useful motion
depends on the system that executes them: motors, transmissions, controllers,
communications, power, temperature, and contact with the world. An action that
works under one set of conditions may behave differently under another.

This is not a newly discovered problem. Robotics has long studied dynamics,
system identification and control. MuJoCo provides actuator and transmission
models [1]. Isaac Lab includes torque-speed envelopes and delayed actuators [2].
Cross-embodiment research has already demonstrated useful transfer between
robots [3]. A credible new project should acknowledge that foundation.

What we want to improve is how physical assumptions travel between teams and
tools. A headline torque number does not explain whether it is continuous or
transient. A latency value is incomplete without its start and end events.
A thermal limit is ambiguous without a sensor location and operating conditions.
An unmeasured property should remain unknown, rather than become a convenient zero.

### A name for the description

We propose **actuome** as a name for an embodied system's described actuation
capabilities and constraints, accompanied by their sources and conditions.
We use **actuomics** for the proposed practice of measuring, analysing and
comparing those descriptions. These are definitions introduced by this project,
not claims that an established scientific discipline already exists.

The biological analogy is a naming aid. A robot is not a genome, and a profile
is not a complete physical model. We prefer an explicit, useful subset to a
claim of completeness that the data cannot support.

### Start with evidence, not rankings

OpenActuome 0.1 describes scalar actuated axes, units, continuous and burst effort,
velocity, defined latency observations, backdrivability, optional thermal
information, and optional effort-speed curves. Every axis carries an evidence
label: measured, manufacturer-declared, simulated, synthetic, or unknown.

Profiles distinguish complete coverage from a partial description. They identify
the hardware revision, sources, measurement conditions, and limitations. A
validator checks structure and cross-field consistency. A report exporter
makes those declarations visible without inventing a universal performance score.

The examples shipped with this proposal are synthetic or unmeasured templates.
They are not specifications for Tesla, Figure, Unitree, Boston Dynamics, or any
other manufacturer. No real-robot comparative result is being announced.

### Interoperability is a testable objective

A portable description may reduce repeated data collection and make assumptions
easier to review. It does not itself adapt a learned policy, supply missing
calibration, or make robot operation safe. We will evaluate interoperability
through explicit mappings and round-trip tests with existing tools, rather than
present a JSON document as a universal action compiler.

The first empirical milestone is modest: publish traceable profiles for two
different actuators using a common protocol; map the supported fields into one
tool; document what survives the mapping and what does not. Any later claim
about transfer or performance must include a baseline, test conditions, repeated
trials, and uncertainty.

### An open invitation

We invite hardware engineers, control researchers, simulator maintainers and
robotics teams to challenge this draft. Which fields are ambiguous? Which
measurements are practical? Which existing representations should be reused?
Which part of the proposed interchange format would save real work?

Our ambition is straightforward: make actuation assumptions easier to inspect,
share and test. OpenActuome earns relevance through useful contributions and
independent adoption—not through declaring itself an industry standard.

Initiated by **Troya Science — [troyascience.com](https://troyascience.com)**.

### References

1. [MuJoCo computation and actuation model](https://mujoco.readthedocs.io/en/stable/computation/index.html).
2. [Isaac Lab actuator models](https://isaac-sim.github.io/IsaacLab/main/source/concepts/actuators.html).
3. [Open X-Embodiment: Robotic Learning Datasets and RT-X Models](https://robotics-transformer-x.github.io/).

Legal rights holder: **TROYA BİLİM EĞİTİM ORGANİZASYON TEKNOLOJİ LİMİTED ŞİRKETİ**.
