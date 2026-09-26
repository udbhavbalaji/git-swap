import json
import subprocess
import sys


def run(*args, env=None):
    return subprocess.run([sys.executable, "git_swap.py", *args], text=True, capture_output=True, env=env)


def test_add_list_and_use(tmp_path):
    env = {"XDG_CONFIG_HOME": str(tmp_path / "config")}
    added = run("add", "work", "--name", "Work User", "--email", "work@example.com", env=env)
    assert added.returncode == 0
    listed = run("list", env=env)
    assert "work\tWork User <work@example.com>" in listed.stdout


def test_duplicate_requires_force(tmp_path):
    env = {"XDG_CONFIG_HOME": str(tmp_path / "config")}
    assert run("add", "x", "--name", "A", "--email", "a@x.com", env=env).returncode == 0
    duplicate = run("add", "x", "--name", "B", "--email", "b@x.com", env=env)
    assert duplicate.returncode == 1
    data = json.loads((tmp_path / "config" / "git-swap" / "profiles.json").read_text())
    assert data["profiles"]["x"]["name"] == "A"
