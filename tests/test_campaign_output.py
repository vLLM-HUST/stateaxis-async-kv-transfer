import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
spec = importlib.util.spec_from_file_location(
    "campaign_wrapper", ROOT / "tools/run_matched_campaign.py"
)
wrapper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wrapper)


def test_campaign_rejects_repository_output():
    with pytest.raises(ValueError, match="outside"):
        wrapper.output_directory(str(ROOT / "new-results"))


def test_campaign_rejects_relative_output():
    with pytest.raises(ValueError, match="absolute"):
        wrapper.output_directory("results")


def test_campaign_rejects_reused_output(tmp_path):
    (tmp_path / "previous").write_text("do not overwrite")
    with pytest.raises(ValueError, match="never reuse"):
        wrapper.output_directory(str(tmp_path))


def test_campaign_rejects_symlink_into_repository(tmp_path):
    (tmp_path / "link").symlink_to(ROOT, target_is_directory=True)
    with pytest.raises(ValueError, match="outside"):
        wrapper.output_directory(str(tmp_path / "link"))


def test_campaign_accepts_empty_external_output(tmp_path):
    assert wrapper.output_directory(str(tmp_path)) == tmp_path.resolve()
