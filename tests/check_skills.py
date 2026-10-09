"""Run with python tests/check_skills.py (requires chezmoi)."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


def run(*args):
    env = dict(os.environ)
    for name in ("PAGER", "GIT_PAGER", "GH_PAGER"):
        env.pop(name, None)
    result = subprocess.run(args, capture_output=True, env=env)
    assert result.returncode == 0, result.stderr.decode("utf-8", errors="replace")
    return result.stdout


source = Path(__file__).resolve().parents[1] / "home"
with tempfile.TemporaryDirectory(prefix="dotfiles-skills-") as temporary:
    root = Path(temporary)
    repo = root / "repo"
    home = repo / "home"
    for directory in (".skills", "dot_agents/skills", "dot_claude/skills"):
        shutil.copytree(source / directory, home / directory)
    (repo / ".chezmoiroot").write_text("home\n", encoding="utf-8")
    original = home / ".skills/dotfiles-test"
    contents = {
        "SKILL.md": b"---\nname: dotfiles-test\ndescription: Temporary test only\n---\n{{ untouched }}\n",
        "references/guide.md": "日本語\n{{ untouched }}\n".encode("utf-8"),
        "scripts/run.sh": b"#!/bin/sh\nprintf '%s\\n' test\n",
        "assets/image.bin": bytes(range(256)),
        "assets/empty.txt": b"",
        "assets/dot_example.tmpl": b"{{ literal template example }}\n",
    }
    for name, content in contents.items():
        path = original / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)

    def add_wrappers():
        for name in contents:
            relative = Path(name)
            filename = relative.name + ".tmpl"
            if name == "scripts/run.sh":
                filename = "executable_" + filename
            elif name == "assets/empty.txt":
                filename = "empty_" + filename
            elif name == "assets/dot_example.tmpl":
                filename = "literal_dot_example.tmpl.literal.tmpl"
            for target in ("dot_agents/skills", "dot_claude/skills"):
                wrapper = home / target / "dotfiles-test" / relative.parent / filename
                wrapper.parent.mkdir(parents=True, exist_ok=True)
                wrapper.write_text('{{- include ".skills/dotfiles-test/' + name + '" -}}\n',
                                   encoding="utf-8")

    add_wrappers()

    for platform in ("linux", "windows"):
        destination = root / platform
        destination.mkdir()
        sentinel = destination / ".claude/skills/synced/account/keep.txt"
        sentinel.parent.mkdir(parents=True)
        sentinel.write_bytes(b"account skill")
        unmanaged = destination / ".agents/skills/unmanaged/SKILL.md"
        unmanaged.parent.mkdir(parents=True)
        unmanaged.write_bytes(b"unmanaged skill")
        config = root / (platform + ".json")
        config.write_text(json.dumps({"sourceDir": str(repo), "destDir": str(destination)}), encoding="utf-8")
        command = ("chezmoi", "--config", str(config), "--persistent-state",
                   str(root / (platform + ".state")), "--override-data",
                   json.dumps({"chezmoi": {"os": platform}}))
        managed = run(*command, "managed").decode("utf-8").replace("\\", "/")
        assert ".config/opencode/skills" not in managed
        assert ".codex/skills" not in managed
        assert ".gitkeep" not in managed
        for target in (".agents/skills", ".claude/skills"):
            assert target + "/dotfiles-test/SKILL.md" in managed
        run(*command, "diff")
        run(*command, "apply", "--dry-run", "--verbose")
        assert not (destination / ".agents/skills/dotfiles-test").exists()
        run(*command, "apply")
        for target in (".agents/skills", ".claude/skills"):
            for name, content in contents.items():
                path = destination / target / "dotfiles-test" / name
                assert path.read_bytes() == content, (platform, target, name)
                assert not path.is_symlink()
        assert sentinel.read_bytes() == b"account skill"
        assert unmanaged.read_bytes() == b"unmanaged skill"
        if os.name != "nt":
            assert (destination / ".agents/skills/dotfiles-test/scripts/run.sh").stat().st_mode & 0o111
        assert run(*command, "diff") == b""
        # Editing just the original updates both copies.
        (original / "references/guide.md").write_bytes(b"updated\n")
        run(*command, "apply")
        for target in (".agents/skills", ".claude/skills"):
            assert (destination / target / "dotfiles-test/references/guide.md").read_bytes() == b"updated\n"
        (original / "references/guide.md").write_bytes(contents["references/guide.md"])
        # Removing source wrappers must leave deployed and unmanaged files alone.
        shutil.rmtree(home / "dot_agents/skills/dotfiles-test")
        shutil.rmtree(home / "dot_claude/skills/dotfiles-test")
        run(*command, "apply", "--dry-run", "--verbose")
        run(*command, "apply")
        assert (destination / ".agents/skills/dotfiles-test/SKILL.md").exists()
        assert sentinel.read_bytes() == b"account skill"
        assert unmanaged.read_bytes() == b"unmanaged skill"
        add_wrappers()
print("PASS: Windows/Linux paths, raw text/binary includes, updates, dry-run and unmanaged file retention")
