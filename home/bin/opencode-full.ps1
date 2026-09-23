#Requires -Version 5.1
<#
.SYNOPSIS
  Launch OpenCode with PONYTAIL_DEFAULT_MODE=full (process scope only).

.DESCRIPTION
  Child `opencode` inherits it; user/machine environment is untouched,
  so Codex's global Ponytail default (`defaultMode: off`) is unaffected.
  Forwards all arguments; preserves the exit code.

.EXAMPLE
  powershell -NoProfile -ExecutionPolicy Bypass -File opencode-full.ps1 --version
#>
$env:PONYTAIL_DEFAULT_MODE = 'full'

& opencode @args
exit $LASTEXITCODE
