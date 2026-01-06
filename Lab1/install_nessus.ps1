# PowerShell script for installing Nessus Essentials

# Do Not Use in Production. This is for testing only.

# Function to check if a command has executed successfully
function Check-Command {
    param (
        [string]$CommandName,
        [int]$ExitCode
    )
    if ($ExitCode -ne 0) {
        Write-Host "Error: $CommandName failed with exit code $ExitCode."
        exit
    }
}

# Step 1: Download Nessus Essentials
$downloadUrl = "https://downloads.nessus.org/nessus3dl.php?file=Nessus-10.6.0-x64.exe&licence_accept=yes&t=1684343228"
$installerPath = "C:\Users\$env:USERNAME\Downloads\Nessus-essentials.exe"

Write-Host "Downloading Nessus Essentials..."
Invoke-WebRequest -Uri $downloadUrl -OutFile $installerPath
Check-Command "Downloading Nessus Essentials" $LASTEXITCODE

# Step 2: Install Nessus Essentials
Write-Host "Installing Nessus Essentials..."
Start-Process -FilePath $installerPath -ArgumentList "/S" -Wait -NoNewWindow
Check-Command "Installing Nessus Essentials" $LASTEXITCODE

# Step 3: Start Nessus service
Write-Host "Starting Tenable Nessus service..."
Start-Service -Name "Tenable Nessus"
Check-Command "Starting Nessus service" $LASTEXITCODE

# Step 4: Enable Nessus to start at boot
Set-Service -Name "Tenable Nessus" -StartupType Automatic

# Step 5: Print installation complete message
Write-Host "Nessus Essentials installation complete."
Write-Host "Access Nessus at: https://localhost:8834"

# Step 6: Instructions for the initial setup
Write-Host "Please complete the configuration by navigating to https://localhost:8834 in your web browser."
Write-Host "Follow the prompts to configure your Nessus account and enter the activation code for Nessus Essentials."
