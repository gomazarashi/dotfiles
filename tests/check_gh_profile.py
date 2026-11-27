"""Run with python tests/check_gh_profile.py (requires chezmoi and PowerShell)."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


source = Path(__file__).resolve().parents[1]
template = source / "home/readonly_Documents/PowerShell/Microsoft.PowerShell_profile.ps1.tmpl"
shell = shutil.which("pwsh") or shutil.which("powershell")
assert shell, "PowerShell is required"
with tempfile.TemporaryDirectory(prefix="gh-profile-") as temporary:
    root = Path(temporary).resolve()
    config = root / "chezmoi.json"

    def render(data):
        config.write_text(json.dumps({"sourceDir": str(source), "data": data}), encoding="utf-8")
        return subprocess.run(
            ["chezmoi", "--config", str(config), "execute-template", "--file", str(template)],
            capture_output=True, text=True, encoding="utf-8",
        )

    for data in ({}, {"alternateGh": {"enabled": False}}):
        result = render(data)
        assert result.returncode == 0 and "function gh" not in result.stdout

    settings = {"enabled": True, "repository": str(root / "repo with 'quote"),
                "configDirectory": str(root / "config with 'quote"), "account": "test'user"}
    for missing in ("repository", "configDirectory", "account"):
        assert render({"alternateGh": {k: v for k, v in settings.items() if k != missing}}).returncode != 0
    result = render({"alternateGh": settings})
    assert result.returncode == 0, result.stderr
    profile = root / "profile.ps1"
    profile.write_text(result.stdout, encoding="utf-8-sig")
    # 実際の GitHub 認証を使わず、引数・切り替え・拒否・環境変数の復元を確かめる。
    script = root / "check.ps1"
    script.write_text(r'''
param($ProfilePath, $Repository, $ConfigDirectory, $Account)
$ErrorActionPreference = 'Stop'
function Assert($Condition) { if (-not $Condition) { throw 'assertion failed' } }
function Get-Command { param($Name, $CommandType, $ErrorAction) @{ Source = 'Invoke-FakeGh' } }
function git { $global:LASTEXITCODE = $script:gitExit; $script:repositoryRoot }
function Invoke-FakeGh {
    $script:calls += ,@($env:GH_CONFIG_DIR, @($args))
    $global:LASTEXITCODE = 0
    if ($args[0] -eq 'api') { $script:actualAccount }
    if ($script:failCommand -and $args[0] -ne 'api') { throw 'command failed' }
}
. $ProfilePath
$env:GH_TOKEN = $null
$env:GITHUB_TOKEN = $null
$env:GH_CONFIG_DIR = 'original'
$script:gitExit = 0
$script:repositoryRoot = $Repository
$script:actualAccount = $Account
$script:calls = @()
gh issue list
Assert ($script:calls.Count -eq 2)
Assert ($script:calls[0][0] -eq $ConfigDirectory)
Assert (($script:calls[1][1] -join ' ') -eq 'issue list')
Assert ($env:GH_CONFIG_DIR -eq 'original')

foreach ($scenario in @('outside', 'no-repo', 'help', 'auth', 'token', 'wrong-account', 'failure')) {
    $script:calls = @()
    $script:gitExit = 0
    $script:repositoryRoot = $Repository
    $script:actualAccount = $Account
    $script:failCommand = $false
    $env:GH_TOKEN = $null
    switch ($scenario) {
        'outside' { $script:repositoryRoot = Split-Path $Repository }
        'no-repo' { $script:gitExit = 1; $script:repositoryRoot = $null }
        'token' { $env:GH_TOKEN = 'test-token' }
        'wrong-account' { $script:actualAccount = 'different-account' }
        'failure' { $script:failCommand = $true }
    }
    $failed = $false
    try {
        if ($scenario -eq 'help') { gh --help }
        elseif ($scenario -eq 'auth') { gh auth status }
        else { gh issue list }
    } catch { $failed = $true }
    Assert ($failed -eq ($scenario -in @('token', 'wrong-account', 'failure')))
    Assert ($env:GH_CONFIG_DIR -eq 'original')
    if ($scenario -in @('outside', 'no-repo')) {
        Assert ($script:calls.Count -eq 1 -and $script:calls[0][0] -eq 'original')
    }
    if ($scenario -in @('help', 'auth')) { Assert ($script:calls.Count -eq 1) }
    if ($scenario -eq 'token') { Assert ($script:calls.Count -eq 0) }
    if ($scenario -eq 'wrong-account') { Assert ($script:calls.Count -eq 1) }
}
''', encoding="utf-8-sig")
    subprocess.run([shell, "-NoProfile", "-NonInteractive", "-File", str(script), str(profile),
                    settings["repository"], settings["configDirectory"], settings["account"]], check=True)
print("PASS: optional/incomplete settings, quoting, routing, account/token checks, environment restoration")
