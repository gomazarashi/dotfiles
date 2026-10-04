"""Run with python tests/check_alternate_git.py (requires chezmoi and git)."""
import json
import os
from pathlib import Path
import shlex
import subprocess
import tempfile


def run(*args, env=None):
    result = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", env=env)
    assert result.returncode == 0, f"{args[0]} failed (output suppressed)"
    return result.stdout


source = Path(__file__).resolve().parents[1] / "home"
with tempfile.TemporaryDirectory(prefix="alternate-git-") as temporary:
    root = Path(temporary)
    config = root / "chezmoi.json"
    normal = root / ".gitconfig"
    alternate = root / ".gitconfig-alternate"
    inside = root / "repositories with spaces" / "nested"
    outside = root / "ordinary"
    for repo in (inside, outside):
        run("git", "init", "--quiet", str(repo))
    env = dict(os.environ, GIT_CONFIG_GLOBAL=str(normal), GIT_CONFIG_NOSYSTEM="1")
    for variable in ("GIT_DIR", "GIT_WORK_TREE", "GIT_CONFIG_COUNT", "GIT_CONFIG_PARAMETERS"):
        env.pop(variable, None)

    def render(data, filename):
        config.write_text(json.dumps({"sourceDir": str(source.parent), "data": data}), encoding="utf-8")
        return run("chezmoi", "--config", str(config), "execute-template", "--file", str(source / filename))

    baseline = None
    for data in ({}, {"alternateGit": {"enabled": False}}):
        text = render(data, "dot_gitconfig.tmpl")
        assert "includeIf" not in text
        baseline = text if baseline is None else baseline
        assert text == baseline
        assert render(data, "private_dot_gitconfig-alternate.tmpl") == ""
        assert ".gitconfig-alternate" in render(data, ".chezmoiignore")

    for directory in (str(inside.parent).replace("\\", "/"), str(inside.parent)):
        data = {"alternateGit": {"enabled": True, "directory": directory,
                "name": 'Example "Name"', "email": "example@example.invalid",
                "sshKey": str(root / "key with space and 'quote")}}
        normal.write_text(render(data, "dot_gitconfig.tmpl"), encoding="utf-8")
        alternate.write_text(render(data, "private_dot_gitconfig-alternate.tmpl"), encoding="utf-8")
        assert ".gitconfig-alternate" not in render(data, ".chezmoiignore")
        # Redirect only the include destination to the isolated test directory.
        normal.write_text(normal.read_text(encoding="utf-8").replace("~/.gitconfig-alternate", alternate.as_posix()), encoding="utf-8")
        for key, expected in (("user.name", 'Example "Name"'), ("user.email", "example@example.invalid")):
            assert run("git", "-C", str(inside), "config", "--get", key, env=env).strip() == expected
            assert ".gitconfig-alternate" in run("git", "-C", str(inside), "config", "--show-origin", "--get", key, env=env)
        command = run("git", "-C", str(inside), "config", "--get", "core.sshCommand", env=env)
        assert shlex.split(command) == ["ssh", "-i", data["alternateGit"]["sshKey"].replace("\\", "/"), "-o", "IdentitiesOnly=yes"]
        assert run("git", "-C", str(outside), "config", "--get", "user.name", env=env).strip() == "gomazarashi"
        assert run("git", "-C", str(outside), "config", "--get", "user.email", env=env).strip() == "gomazarashi0426@gmail.com"
print("PASS: absent/disabled data, path separators, conditional identity and SSH config")
