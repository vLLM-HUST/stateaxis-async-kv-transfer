"""Run the retained campaign code with verified inputs and external output."""

import argparse
import json
import runpy
from pathlib import Path

from benchmark_evidence import ROOT, fetch

CAMPAIGN = "evidence/ecpa-matched-process-20261010/run_matched_campaign.py"
CONFIG = "evidence/ecpa-matched-process-20261010/manager-config.json"


def output_directory(value):
    destination = Path(value)
    if not destination.is_absolute():
        raise ValueError("Campaign output must be an absolute external directory")
    destination = destination.resolve()
    if destination == ROOT or ROOT in destination.parents:
        raise ValueError("Campaign output must be outside the MOD repository")
    if destination.exists() and any(destination.iterdir()):
        raise ValueError("Campaign output must be empty; never reuse a previous run")
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    destination = output_directory(args.output)
    destination.mkdir(parents=True, exist_ok=True)
    fetch(destination / "inputs", [CONFIG])
    # Keep the verified original intact; relocate only its local manifest path.
    config = json.loads((destination / "inputs" / CONFIG).read_text())
    config["research_manifest_path"] = str(ROOT / "RESEARCH_MANIFEST.json")
    runtime_config = destination / "runtime-manager-config.json"
    runtime_config.write_text(json.dumps(config, indent=2) + "\n")
    # Execute only repository-owned source, never downloaded archival scripts.
    campaign = runpy.run_path(str(ROOT / CAMPAIGN))
    entrypoint = campaign["main"]
    entrypoint.__globals__.update(
        ROOT=destination, CONFIGURE=runtime_config, MOD_REPO=ROOT
    )
    entrypoint()


if __name__ == "__main__":
    main()
