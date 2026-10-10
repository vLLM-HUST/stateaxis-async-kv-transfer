# stateaxis-async-kv-transfer

Default-off StateAxis MOD for a bounded asynchronous host-to-device KV restore
lane. The MOD supplies an active Manifest 0.3 contract and a reusable Rust
coordinator; StateAxis owns the device stream, snapshot memory, and publication.

The coordinator admits only nonzero `(state_id, generation, snapshot_sha256)`
identities, coalesces exact duplicates, bounds both unique work and correlation
IDs, issues monotonically changing leases, and requires explicit commit or
abort. The StateAxis activation contract sets the retry budget to zero: any
device-transfer error rolls back and fails closed rather than replaying DMA.

The mechanism is not enabled by importing this package or setting an environment
variable directly. It must be selected by vLLM-HUST Extension Manager/ECPA and
accepted by StateAxis's hash-bound `--additional-config` parser.

## Validation

```bash
python -m pytest -q
ruff check .
ruff format --check .
cargo test --manifest-path native/Cargo.toml
cargo clippy --manifest-path native/Cargo.toml --all-targets -- -D warnings
```

See `EVIDENCE.md` for the strict boundary between historical evidence and fresh
version qualification.

Extension ID: `org.vllm-hust.stateaxis-async-kv-transfer`

Out-of-order bounded device KV transfer overlap with explicit ownership and drain.

This repository is the independent MOD boundary for StateAxis issues [#76](https://github.com/Qixin-Gaoke/stateaxis/issues/76).
It is deliberately `import_only`, default-off, and cannot be enabled. The split does
not inherit correctness, device, performance, or publication qualification from the
aggregate StateAxis repository.

## Evidence boundary

Status: **scoped-positive**.

Bounded device-overlap evidence is positive; it is not cross-instance tiering or a capacity claim.

The copied evidence and its SHA-256 are recorded in `PROVENANCE.json`. Negative,
failed, and inconclusive results are retained. Microbenchmarks and component results
must not be restated as online end-to-end gains.

## Install and inspect

```bash
python -m pip install .
vllm-hust-ext extension inspect org.vllm-hust.stateaxis-async-kv-transfer
vllm-hust-ext extension check org.vllm-hust.stateaxis-async-kv-transfer
```

Discovery does not enable the MOD. A future active revision must extract an
independently reviewable implementation, declare exclusive resources where needed,
and pass exactness, lifecycle, release, failure-recovery, and matched real-online
gates.

## Validate

```bash
python -m pip install -e '.[test]'
pytest -q
```

Maintainer: Shuhao Zhang (Tony), directly responsible; no advisor is declared.
