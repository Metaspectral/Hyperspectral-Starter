# Determine the script directory
$scriptPath = $MyInvocation.MyCommand.Path
$appDir = Split-Path $scriptPath

# Set up paths
$localEnvPath = Join-Path $appDir "venv"
$requirementsSpecPath = Join-Path $appDir "requirements.in"
$requirementsPath = Join-Path $appDir "requirements.txt"
$activatePath = Join-Path $localEnvPath "bin\Activate.ps1"

$needsInstall = $false
$needsRecompile = $false
if ($args[0] -eq "--install") {
    $needsInstall = $true
    $args = $args[1..$args.Length]
} elseif ($args[0] -eq "--recompile") {
    $needsInstall = $true
    $needsRecompile = $true
    $args = $args[1..$args.Length]
} elseif (-not (Test-Path $activatePath)) {
    $needsInstall = $true
}

# Initialize virtual environment
if ($needsInstall) {
    Write-Host "Installing..."
    Remove-Item $localEnvPath -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "Creating a virtual environment 'venv' in $appDir..."
    python3.10 -m venv $localEnvPath
}

# Activate the virtual environment
& "$activatePath"

# Update packages
if ($needsInstall) {
    Write-Host "Initialized $appDir"
    if ($needsRecompile) {
        pip3.10 install pip-tools
        pip-compile $requirementsSpecPath -o $requirementsPath
    }
    pip3.10 install -r "$appDir/requirements.txt" --quiet
}

# Run the python script
python3.10 "$appDir/main.py" $args
