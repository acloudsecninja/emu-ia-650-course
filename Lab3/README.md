# Offensive Security Testing with Hugging Face AI Models

## ⚠️ Safety and Ethics

### Important Warnings
- **Educational Purpose Only**: This tool is designed for educational and authorized security testing only
- **Legal Compliance**: Only use on systems you own or have explicit permission to test
- **Network Isolation**: Test in isolated lab environments
- **Responsible Disclosure**: Report any discovered vulnerabilities responsibly

## 🚀 Overview
This lab demonstrates how to use Hugging Face AI models for testing offensive security tactics on Ubuntu systems against Windows targets.

The Python script leverages state-of-the-art AI models from Hugging Face to generate and test various offensive security techniques including:
- Phishing email generation
- PowerShell payload creation
- Network reconnaissance
- Privilege escalation techniques
- Lateral movement methods
- Persistence mechanisms

## 📋 Prerequisites

### System Requirements
- Ubuntu 20.04+ (recommended)
- Python 3.8+
- GPU support (optional, for faster model inference)
- Internet connection (to download AI models)

### Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

## 🛠️ Installation

1. **Clone or download the lab files:**
   ```bash
   # Ensure you're in the Lab3 directory
   cd Lab3
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Additional Requirements on Ubuntu (Optional / or If Required and you must be Root):**
   ```bash
   apt-get update
   apt-get upgrade
   apt install python3-pip
   pip install -r requirements.txt
   python3
   ```
- Once you run Python3 you should get a new prompt which means python is installed and ready to use.

4. **Verify installation:**
   ```bash
   python3 offensive_security_ai.py --help
   ```
- You should get an output of help commands which means the packages are installed and the python script is working correctly.

## 🎯 Usage

### Basic Usage

Run the script with default settings:
```bash
python3 offensive_security_ai.py
```

### Advanced Usage

Customize the testing parameters:

```bash
# Test specific attack type against a target
python3 offensive_security_ai.py --target UPDATE_WITH_TARGET_IP --attack-type payload

# Use a different AI model
python3 offensive_security_ai.py --model distilgpt2 --attack-type phishing

# Perform comprehensive reconnaissance
python3 offensive_security_ai.py --target UPDATE_WITH_TARGET_NETWORK/24 --scan-type comprehensive

# Generate custom report
python3 offensive_security_ai.py --output my_security_report.json
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--model` | Hugging Face model name | `microsoft/DialoGPT-medium` |
| `--target` | Target IP address | `127.0.0.1` |
| `--attack-type` | Type of attack to generate | `payload` |
| `--scan-type` | Type of reconnaissance scan | `basic` |
| `--output` | Output report file | `security_test_report.json` |
| `--device` | Device to run model on | `auto` |

### Attack Types

1. **phishing** - Generate realistic phishing email templates
2. **payload** - Create obfuscated PowerShell payloads
3. **recon** - Suggest reconnaissance commands and techniques
4. **privilege_escalation** - Generate privilege escalation techniques
5. **lateral_movement** - Create lateral movement methods
6. **persistence** - Suggest persistence mechanisms

### Scan Types

1. **basic** - Simple ping test and connectivity check
2. **comprehensive** - Full port scan with OS detection (requires nmap)
3. **stealth** - Quiet scanning techniques (future enhancement)

## 📊 Output

The script generates several outputs:

1. **Console Output** - Real-time progress and results display
2. **Log File** - Detailed execution log (`offensive_security_ai.log`)
3. **JSON Report** - Comprehensive test report (default: `security_test_report.json`)

### Report Structure
```json
{
  "test_metadata": {
    "timestamp": "2024-01-01T12:00:00",
    "model_used": "microsoft/DialoGPT-medium",
    "device": "cpu",
    "target_os": "windows"
  },
  "attack_results": [...],
  "summary": {
    "total_tests": 3,
    "successful_tests": 2
  }
}
```

### Safety Features
- Payload analysis without execution
- Sandbox testing environment
- Comprehensive logging for audit trails
- Non-destructive reconnaissance techniques

## 🔧 Configuration

### Model Selection
Choose from various Hugging Face models:
- `microsoft/DialoGPT-medium` (default, balanced)
- `distilgpt2` (lighter, faster)
- `gpt2` (standard)
- `gpt2-medium` (more capable)

### Device Optimization
- `auto` - Automatically selects best available device
- `cpu` - Force CPU usage
- `cuda` - Use GPU acceleration (if available)

## 🐛 Troubleshooting

### Common Issues

1. **Model Download Fails**
   ```bash
   # Check internet connection
   ping huggingface.co
   
   # Try different model
   python offensive_security_ai.py --model distilgpt2
   ```

2. **CUDA Out of Memory**
   ```bash
   # Use CPU instead
   python offensive_security_ai.py --device cpu
   
   # Or use smaller model
   python offensive_security_ai.py --model distilgpt2
   ```

3. **Permission Denied**
   ```bash
   # Ensure proper permissions
   chmod +x offensive_security_ai.py
   
   # Install with user permissions
   pip install --user -r requirements.txt
   ```

4. **Nmap Not Found**
   ```bash
   # Install nmap
   sudo apt install nmap
   
   # Or use basic scan only
   python offensive_security_ai.py --scan-type basic
   ```

## 📚 Learning Objectives

After completing this lab, you will understand:
- How to integrate AI models into security testing workflows
- Techniques for generating realistic attack vectors
- Methods for analyzing and testing security payloads
- Approaches for automated reconnaissance
- Best practices for responsible security research

## 🔗 Additional Resources

- [Hugging Face Models](https://huggingface.co/models)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [MITRE ATT&CK Framework](https://attack.mitre.org/)
- [Python Security Tools](https://github.com/topics/python-security)

## 📄 License

This educational material is provided for academic purposes. Please ensure compliance with your institution's policies and applicable laws when using security testing tools.

## 🤝 Contributing

This is a learning laboratory. Suggestions for improvements and additional features are welcome through proper academic channels.

---

**⚠️ Disclaimer**: This tool is for educational and authorized security testing only. Users are responsible for ensuring compliance with all applicable laws and regulations.
