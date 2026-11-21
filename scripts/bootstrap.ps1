# Bootstrap the Claude.ai Uncensored Plugin on Windows.
$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Resolve-Path (Join-Path $here "..")

Write-Host "[+] Installing Python dependencies..."
python -m pip install -r (Join-Path $root "requirements.txt")

Write-Host "[+] Registering plugin in HKCU..."
python -m claude_uncensored_plugin.installer.register --install-dir $root

Write-Host "[+] Done. Launch with: python -m claude_uncensored_plugin"