# PowerShell script for installing Nessus Essentials

# Do Not Use in Production. This is for testing only.

## You must run the following command in Powershell before excuting the following script or the script not work without it.
### Set-ExecutionPolicy Unrestricted ###


# Define URL for Nessus Essentials installer
$installerUrl = "https://www.tenable.com/downloads/api/v1/public/pages/nessus-essentials/downloads/XXXXX" # Replace XXXXX with the actual version number
$installerPath = "C:\Temp\NessusEssentials.exe"

# Create Temp directory if it doesn't exist
if (-Not (Test-Path "C:\Temp")) {
    New-Item -Path "C:\" -Name "Temp" -ItemType Directory
}

# Download Nessus Essentials installer
Invoke-WebRequest -Uri $installerUrl -OutFile $installerPath

# Start the installation
Start-Process -FilePath $installerPath -ArgumentList "/S" -Wait

# Optionally, remove the installer after installation
Remove-Item -Path $installerPath
