# OpenActuome: An Evidence-Carrying Description of Robot Actuation

**Technical concept note, draft 0.1.0 — not submitted to arXiv**

Project owner: Troya Science (https://troyascience.com). Individual research authors
and contributions are to be confirmed before any academic submission.

## Abstract

Robot actuation properties are often interpreted through tool-specific models,
manufacturer declarations and experiments with different operating conditions.
We propose OpenActuome, a small interchange profile that records scalar actuation
properties alongside units, provenance, operating conditions and coverage.
The initial artifact consists of a JSON schema, a version-specific offline
validator, a report exporter and synthetic examples. It distinguishes measured,
declared, simulated, synthetic and unknown data. The contribution is a proposal
for evidence organization, not a new actuator model or an algorithm for policy
transfer. We define an empirical evaluation plan using two measured actuators
and a documented mapping into an existing tool. No real-hardware validation or
cross-robot performance improvement is claimed in this draft.

## 1. Motivation

Reusable robot learning depends on assumptions about the system that executes
actions. Properties such as effort limits, command delay, transmission behavior
and thermal constraints are meaningful only with units and conditions. We
hypothesize that an explicit interchange profile could reduce ambiguity during
engineering review and tool integration. This hypothesis remains to be evaluated.

## 2. Existing work

MuJoCo includes models of transmission, activation dynamics and force generation
[1]. Isaac Lab includes delayed actuators and motor effort-speed behavior [2].
Open X-Embodiment shows beneficial transfer across multiple robot embodiments
[3]. These efforts establish that neither actuation modeling nor cross-robot
transfer is absent. The proposed profile complements such work by making evidence
scope and conditions explicit; it does not replace their models or learning methods.

## 3. Proposed artifact

The schema represents scalar actuated axes. Rotary effort uses N*m and linear
effort uses N. Profiles identify the platform revision, total actuated DoF,
coverage, connection metadata and evidence registry. Axis observations include
continuous/burst effort, the associated speed/duration, latency boundaries,
backdrivability and optional thermal and effort-speed information.

Structural validation is followed by semantic checks for references, coverage,
units, envelope consistency and evidence declarations. Unknown quantities are
null. Synthetic examples are visibly labelled. A measured-only gate is a metadata
requirement, not an independent check of experimental truth.

## 4. Evaluation design

The initial software checks assess acceptance of valid fixtures and rejection of
inconsistent units, counts, references, ranges and provenance. They establish
implementation behavior only. Hardware evaluation is planned as follows:

1. Collect repeatable observations on two distinct accessible actuators under
   a shared protocol and preserve raw data and calibration records.
2. Ask an independent engineer to reconstruct selected observations from the
   evidence and record disagreements and missing information.
3. Map supported fields into one version-pinned tool and quantify round-trip
   value preservation, unit conversion errors and unrepresented fields.
4. Evaluate configuration effort against an explicitly defined baseline, if
   enough independent users participate. Avoid extrapolating from a single user.

Policy-transfer evaluation is a separate later experiment requiring a controller
or learning method, source/target systems, tasks, baselines and repeated trials.
The profile by itself provides no such mechanism.

## 5. Limitations

No measured robot data, validated simulator adapter, external adoption, or
performance ranking is included. The scalar representation omits coupled models,
geometry, full friction/hysteresis and high-frequency telemetry. Metadata cannot
guarantee measurement validity. A broader schema may not be useful unless it
fits a real engineering workflow. These limitations motivate the proposed pilot.

## 6. Availability and disclosure

The original code and documentation are provided under MIT at
https://github.com/troyabilim/open-actuome. No DOI or arXiv identifier exists for this draft. AI assistance was used to prepare the initial
implementation and text. Named human authors must review the claims, code and
responsibilities before academic submission.

## References

[1] [MuJoCo computation](https://mujoco.readthedocs.io/en/stable/computation/index.html).

[2] [Isaac Lab actuators](https://isaac-sim.github.io/IsaacLab/main/source/concepts/actuators.html).

[3] [Open X-Embodiment: Robotic Learning Datasets and RT-X Models](https://robotics-transformer-x.github.io/).

Legal rights holder: **TROYA BİLİM EĞİTİM ORGANİZASYON TEKNOLOJİ LİMİTED ŞİRKETİ**.
