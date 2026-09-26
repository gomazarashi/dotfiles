# Microsoft.PowerShell_profile.ps1

function opencode {
    # 実際の OpenCode 実行ファイルを取得
    $openCodeCommand = Get-Command opencode -CommandType Application -ErrorAction Stop |
        Select-Object -First 1

    # 現在の設定を保存
    $previousCodePage = [Console]::OutputEncoding.CodePage
    $previousInputEncoding = [Console]::InputEncoding
    $previousOutputEncoding = [Console]::OutputEncoding
    $previousPipelineEncoding = $OutputEncoding

    try {
        # OpenCode 実行中のみ UTF-8 に統一
        chcp 65001 > $null

        $utf8 = [System.Text.UTF8Encoding]::new($false)

        [Console]::InputEncoding = $utf8
        [Console]::OutputEncoding = $utf8
        $OutputEncoding = $utf8

        # 引数をそのまま OpenCode に渡す
        & $openCodeCommand.Source @args
    }
    finally {
        # OpenCode 終了後に元へ戻す
        chcp $previousCodePage > $null

        [Console]::InputEncoding = $previousInputEncoding
        [Console]::OutputEncoding = $previousOutputEncoding
        $OutputEncoding = $previousPipelineEncoding
    }
}

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