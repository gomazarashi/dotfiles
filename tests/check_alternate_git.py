"""Run with python tests/check_alternate_git.py (requires chezmoi and git)."""
import json
import os
from pathlib import Path
import shlex
import subprocess
import tempfile
import tomllib


def run(*args, env=None):
    result = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", env=env)
    assert result.returncode == 0, f"{args[0]} failed (output suppressed)"
    return result.stdout


source = Path(__file__).resolve().parents[1] / "home"
with tempfile.TemporaryDirectory(prefix="alternate-git-") as temporary:
    # Windows の短縮名 (WAKABA~1) のままだと Git の解決後パスと一致しない
    root = Path(temporary).resolve()
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

    def render(data, filename, stdin=None):
        config.write_text(json.dumps({"sourceDir": str(source.parent), "data": data}), encoding="utf-8")
        args = ["chezmoi", "--config", str(config), "execute-template", "--file", str(source / filename)]
        if stdin is None:
            return run(*args)
        result = subprocess.run(args + ["--with-stdin"], input=stdin, capture_output=True, text=True, encoding="utf-8")
        assert result.returncode == 0, f"{filename} failed (output suppressed)"
        return result.stdout

    # 必須値が欠けた有効化は、全リポジトリへの誤適用ではなく失敗にする
    for missing in ("directory", "sshKey"):
        data = {"enabled": True, "directory": "/work", "name": "N", "email": "e@example.invalid", "sshKey": "/k"}
        del data[missing]
        for filename in ("dot_gitconfig.tmpl", "private_dot_gitconfig-alternate.tmpl"):
            config.write_text(json.dumps({"sourceDir": str(source.parent), "data": {"alternateGit": data}}), encoding="utf-8")
            failed = subprocess.run(["chezmoi", "--config", str(config), "execute-template", "--file", str(source / filename)], capture_output=True)
            assert failed.returncode != 0, f"{filename} rendered without {missing}"

    # Codex: アプリが書いた state は残し、repo の値で上書きし、削除済みの値だけ除く
    stale = '[computer_use.windows]\nalways_allowed_app_ids = ["python.exe"]\n'
    codex = tomllib.loads(render({}, "dot_codex/modify_private_config.toml", 'model = "old"\n[projects."C:/x"]\ntrust_level = "trusted"\n' + stale))
    assert codex["projects"]["C:/x"]["trust_level"] == "trusted" and codex["model"] != "old" and "computer_use" not in codex
    own = tomllib.loads(render({}, "dot_codex/modify_private_config.toml", stale.replace("python.exe", "other.exe")))
    assert own["computer_use"]["windows"]["always_allowed_app_ids"] == ["other.exe"]

    # Claude: /model などの変更と未知のキーは残し、repo の settings.json は上書きする
    claude = json.loads(render({}, "dot_claude/modify_settings.json", '{"model": "sonnet", "custom": 1, "autoCompactEnabled": false}'))
    assert claude["model"] == "sonnet" and claude["custom"] == 1 and claude["autoCompactEnabled"] is True
    assert json.loads(render({}, "dot_claude/modify_settings.json", ""))["model"] == "opus"

    local = root / ".gitconfig-local"
    local.write_text('[user]\n name = Local User\n email = local@example.invalid\n[safe]\n directory = /local-only\n', encoding="utf-8")
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
        normal.write_text(normal.read_text(encoding="utf-8").replace("~/.gitconfig-alternate", alternate.as_posix()).replace("~/.gitconfig-local", local.as_posix()).replace("~/.gitconfig-alternate-local", (root / "missing-alternate-local").as_posix()), encoding="utf-8")
        for key, expected in (("user.name", 'Example "Name"'), ("user.email", "example@example.invalid")):
            assert run("git", "-C", str(inside), "config", "--get", key, env=env).strip() == expected
            assert ".gitconfig-alternate" in run("git", "-C", str(inside), "config", "--show-origin", "--get", key, env=env)
        command = run("git", "-C", str(inside), "config", "--get", "core.sshCommand", env=env)
        assert shlex.split(command) == ["ssh", "-i", data["alternateGit"]["sshKey"].replace("\\", "/"), "-o", "IdentitiesOnly=yes"]
        assert run("git", "-C", str(outside), "config", "--get", "user.name", env=env).strip() == "Local User"
        assert run("git", "-C", str(outside), "config", "--get", "user.email", env=env).strip() == "local@example.invalid"
        assert run("git", "-C", str(outside), "config", "--get-all", "safe.directory", env=env).strip() == "/local-only"
print("PASS: absent/disabled/incomplete data, path separators, conditional identity, SSH config, Codex/Claude merge")
