"""Offline tests for strict cross-repository pin checks (Python standard library)."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from verify_integration_baseline import check  # noqa: E402


def git(folder: Path, *args: str) -> str:
    p = subprocess.run(
        ["git", "-C", str(folder), *args],
        text=True, capture_output=True, check=True,
    )
    return p.stdout.strip()


def init(folder: Path, filename: str, content: str) -> str:
    folder.mkdir()
    git(folder, "init", "-q")
    git(folder, "config", "user.name", "CI Test")
    git(folder, "config", "user.email", "ci-test@example.invalid")
    (folder / filename).write_text(content, encoding="utf-8")
    git(folder, "add", ".")
    git(folder, "commit", "-qm", "initial")
    return git(folder, "rev-parse", "HEAD")


class BaselineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.contract = base / "contract"
        self.frontend = base / "frontend"
        self.backend = base / "backend"
        self.contract_sha = init(self.contract, "openapi.yaml", "openapi: 3.0.3\n")
        init(self.frontend, "contract.sha", self.contract_sha + "\n")
        init(self.backend, "contract.sha", self.contract_sha + "\n")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_matching_pins_and_existing_commit_pass(self) -> None:
        result = check(self.contract, self.frontend, self.backend)
        self.assertEqual(result["gates"]["G0_cross_repo_baseline"], "PASS")
        self.assertEqual(result["gates"]["G3_real_auth_integration"], "NOT_RUN")
        self.assertEqual(result["release_readiness"], "NOT_VERIFIED")

    def test_mismatch_fails(self) -> None:
        (self.backend / "contract.sha").write_text("a" * 40 + "\n")
        result = check(self.contract, self.frontend, self.backend)
        self.assertEqual(result["checks"]["TC-INT-011"], "FAIL")
        self.assertTrue(any("mismatch" in s for s in result["failures"]))

    def test_missing_repository_fails(self) -> None:
        result = check(self.contract, self.frontend, self.backend / "absent")
        self.assertEqual(result["gates"]["G0_cross_repo_baseline"], "FAIL")

    def test_invalid_pin_fails(self) -> None:
        (self.backend / "contract.sha").write_text("not a SHA\n")
        result = check(self.contract, self.frontend, self.backend)
        self.assertEqual(result["gates"]["G0_cross_repo_baseline"], "FAIL")

    def test_nonexistent_commit_fails(self) -> None:
        fake = "b" * 40
        (self.frontend / "contract.sha").write_text(fake + "\n")
        (self.backend / "contract.sha").write_text(fake + "\n")
        result = check(self.contract, self.frontend, self.backend)
        self.assertEqual(result["gates"]["G0_cross_repo_baseline"], "FAIL")
        self.assertTrue(any("not available locally" in s for s in result["failures"]))


if __name__ == "__main__":
    unittest.main()
