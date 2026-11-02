# コンソールの入出力と外部コマンドへの受け渡しを UTF-8 (BOM なし) にする
# コンソールがない環境では設定に失敗するため、その場合は何もしない
try {
    $utf8 = [System.Text.UTF8Encoding]::new($false)
    [Console]::InputEncoding = $utf8
    [Console]::OutputEncoding = $utf8
    $OutputEncoding = $utf8
}
catch {}
