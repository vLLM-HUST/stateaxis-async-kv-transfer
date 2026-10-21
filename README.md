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

Extension ID: `org.vllm-hust.stateaxis-async-kv-transfer`

## Evidence boundary

Status: **historical matched real-NPU component-positive; active version
performance-unqualified**.

Original measured figures, raw records, failed attempts and limitations are now
maintained in [benchmark's frozen report](https://github.com/vLLM-HUST/vllm-hust-benchmark/blob/ddc4f6a3290e447260fc8f6c03ea36d3ca514e23/archive/mod-git-20261021/stateaxis-async-kv-transfer/snapshot/README.md) and
[original evidence index](https://github.com/vLLM-HUST/vllm-hust-benchmark/blob/ddc4f6a3290e447260fc8f6c03ea36d3ca514e23/archive/mod-git-20261021/stateaxis-async-kv-transfer/snapshot/EVIDENCE.md). See [EVIDENCE.md](EVIDENCE.md)
for immutable source links and verified external-cache retrieval.

Historical component-positive evidence does not qualify the active MOD.
Matched-process lifecycle checks use a deterministic worker, not accelerator
kernels; they establish no general serving performance gain.

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

Maintainer: Shuhao Zhang (Tony), directly responsible; no advisor is declared.
