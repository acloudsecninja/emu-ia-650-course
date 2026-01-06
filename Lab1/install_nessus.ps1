# PowerShell script for installing Nessus Essentials

# Do Not Use in Production. This is for testing only.

## You must run the following command in Powershell before excuting the following script or the script not work without it.
### Set-ExecutionPolicy Unrestricted ###


# Define URL for Nessus Essentials installer
// ## $installerUrl = 'https://www.tenable.com/downloads/api/v2/pages/nessus/files/Nessus-10.11.1-x64.msi'
// ## $installerPath = "C:\Temp\Nessus-10.11.1-x64.msi"

# Create Temp directory if it doesn't exist
if (-Not (Test-Path "C:\Temp")) {
    New-Item -Path "C:\" -Name "Temp" -ItemType Directory
}

# Download Nessus Essentials installer using curl
& curl.exe --request GET --url $installerUrl --output $installerPath

# Start the installation
// ## Start-Process -FilePath $installerPath -ArgumentList "/quiet" -Wait

# Verify installation
if (Test-Path "C:\Program Files\Tenable\Nessus" -or Test-Path "C:\Program Files\Nessus") {
    Write-Host "Nessus Essentials has been installed successfully."
} else {
    Write-Host "Nessus Essentials installation failed or not found."
}

# Optionally, remove the installer after installation
Remove-Item -Path $installerPath -ErrorAction SilentlyContinue
