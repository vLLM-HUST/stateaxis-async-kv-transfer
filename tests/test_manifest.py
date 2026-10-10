import hashlib
import json
from pathlib import Path

import pytest
from vllm_hust_ext.manifest import activation_blocker, load_manifest

import stateaxis_async_kv_transfer
from stateaxis_async_kv_transfer import AsyncKvTransferConfig, async_kv_transfer


def test_manifest_is_active_and_discoverable() -> None:
    manifest = load_manifest(
        Path(stateaxis_async_kv_transfer.__file__).with_name(
            "vllm-hust-extension-v0.3.json"
        )
    )
    assert manifest.bundle_id == "org.vllm-hust.stateaxis-async-kv-transfer"
    assert manifest.schema_version == "0.3-experimental"
    assert activation_blocker(manifest) is None


def test_activation_contract_is_exact_and_fail_closed() -> None:
    assert async_kv_transfer() == AsyncKvTransferConfig()
    with pytest.raises(ValueError, match="reviewed bounded contract"):
        AsyncKvTransferConfig(max_retries=1)


def test_activation_is_bound_to_research_manifest_bytes() -> None:
    package_root = Path(stateaxis_async_kv_transfer.__file__).parents[2]
    research_manifest = package_root / "RESEARCH_MANIFEST.json"
    extension_manifest = json.loads(
        Path(stateaxis_async_kv_transfer.__file__)
        .with_name("vllm-hust-extension-v0.3.json")
        .read_text(encoding="utf-8")
    )
    assert research_manifest.is_file()
    assert (
        hashlib.sha256(research_manifest.read_bytes()).hexdigest()
        == (
            extension_manifest["activation"]["additional_config"]["stateaxis_mod"][
                "manifest_sha256"
            ]
        )
    )
