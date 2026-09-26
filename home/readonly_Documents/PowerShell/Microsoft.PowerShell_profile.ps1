# Microsoft.PowerShell_profile.ps1

try {
    $utf8 = [System.Text.UTF8Encoding]::new($false)
    [Console]::InputEncoding = $utf8
    [Console]::OutputEncoding = $utf8
    $OutputEncoding = $utf8
}
catch {}

function codex {
    $codexCommand = Get-Command codex -CommandType Application -ErrorAction Stop |
        Select-Object -First 1

    if ($args -contains '--no-daemon') {
        & $codexCommand.Source @args
    }
    else {
        & $codexCommand.Source --no-daemon @args
    }
}
