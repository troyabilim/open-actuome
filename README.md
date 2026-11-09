# OpenActuome

**Describe actuation. Preserve the evidence.**

An experimental, openly licensed interchange profile for the actuation properties
of embodied systems. **Draft 0.1.0 · 9 November 2026**.

Initiated and owned by **[Troya Science](https://troyascience.com)**.
Legal rights holder: **TROYA BİLİM EĞİTİM ORGANİZASYON TEKNOLOJİ LİMİTED ŞİRKETİ**.

[Türkçe](README_TR.md) · [Manifesto](docs/MANIFESTO_EN.md) · [Measurement protocol](docs/MEASUREMENT_PROTOCOL.md)

## What is an actuome?

We propose *actuome* as a name for an embodied system's described actuation
capabilities and constraints, together with their evidence and operating
conditions. *Actuomics* is our proposed term for their measurement, analysis,
and comparison. These are project definitions, not established disciplines.

OpenActuome 0.1 is a small, testable first step: a JSON profile, a validator,
three example/template files, and a measurement protocol. It does not describe
all of a robot's physics and it does not make policies transfer automatically.

## Run locally

Python 3.10+; no third-party packages or network access required.

```sh
git clone https://github.com/troyabilim/open-actuome.git
cd open-actuome
python validate_actuome.py examples/demo_bench.synthetic.json
python validate_actuome.py examples/partial_platform.synthetic.json --json
python tools/profile_report.py examples/demo_bench.synthetic.json
python -m unittest discover -s tests -v
```

For a provenance gate requiring *measured* labels and measurement metadata:

```sh
python validate_actuome.py examples/demo_bench.synthetic.json --measured-only
```

This command **must fail**: the supplied fixture is synthetic. Even a measured-only
pass verifies declarations and consistency, not the truth of an experiment.

## What is included

| Item | Purpose |
|---|---|
| `spec/0.1.0/actuome.schema.json` | JSON Schema 2020-12 structure |
| `validate_actuome.py` | Offline structure and cross-field checks |
| `examples/demo_bench.synthetic.json` | Fictional two-axis complete profile |
| `examples/partial_platform.synthetic.json` | Explicitly partial profile |
| `examples/unmeasured.template.json` | Unknown values represented by null |
| `tools/profile_report.py` | Validated, provenance-labelled Markdown report |
| `docs/SPECIFICATION.md` | Field meanings, units and versioning |
| `docs/MEASUREMENT_PROTOCOL.md` | Reproducible collection and evidence requirements |
| `docs/INTEROPERABILITY.md` | Mapping to existing tools; no untested adapter claims |
| `benchmarks/INDEX_TEMPLATE.md` | Unscored evidence registry |
| `docs/MANIFESTO_EN.md`, `docs/MANIFESTO_TR.md` | Public explanation in two languages |
| `VALIDATION_REPORT.md` | Local test results and verification limits |
| `paper/RESEARCH_NOTE_EN.md` | Research concept note; not submitted |

## Existing work and our proposed contribution

MuJoCo already models transmission, activation dynamics and force generation.
Isaac Lab already includes motor envelopes and delayed actuator models. Open
X-Embodiment has demonstrated useful cross-robot transfer. We build on this
context; we do not claim to have discovered dynamics or hardware transfer.

Our proposed contribution is a portable *evidence-carrying description*: explicit
units, source labels, operating conditions, coverage, and consistency checks.
Whether it improves real engineering workflows is a question for external pilots.

## Limits of 0.1

- No real-robot benchmark results or independently measured profiles are included.
- No robot ranking, aggregate performance score, thermal safety certificate, or
  claimed zero-shot policy transfer is supplied.
- Each record describes one actuated scalar axis. Floating-base coordinates,
  coupled actuation, tensors, detailed friction/hysteresis and complete geometry
  are outside this draft. A multi-axis joint needs separately identified axes;
  this does not model cross-axis coupling.
- The dependency-free validator implements only the subset used by the bundled
  schema. Use a full Draft 2020-12 implementation for general schema validation;
  also run our validator for semantic checks that JSON Schema alone cannot express.
- The report exporter is a working file-to-report integration, not a simulator
  adapter or robot controller. No physical robot commands are sent.

## Contribute

Start with a sourced profile and the measurement protocol, or review one semantic
rule. Report the robot revision, test conditions, uncertainty and limitations.
See [CONTRIBUTING.md](CONTRIBUTING.md), the [roadmap](docs/ROADMAP.md), and
[sources](docs/SOURCES.md). Do not upload confidential manufacturer information.

## License and status

MIT for this repository's original code, schema, documentation and synthetic
examples. Third-party material retains its own rights. OpenActuome is an
experimental community proposal, not an approved industry standard.

Project repository: [https://github.com/troyabilim/open-actuome](https://github.com/troyabilim/open-actuome). The owner website is a separate corporate link.
