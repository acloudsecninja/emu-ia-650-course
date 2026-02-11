# Lab 4: Website Defacement Testing

## ⚠️ Safety and Ethics

### Important Warnings
- **Educational Purpose Only**: This tool is designed for educational and authorized security testing only
- **Legal Compliance**: Only use on systems you own or have explicit permission to test
- **Network Isolation**: Test in isolated lab environments

## Overview
This lab demonstrates website defacement testing techniques using Python on Kali Linux. The purpose is educational - to help students understand how attackers compromise and deface websites, and how to defend against such attacks.

## Learning Objectives
- Understand common web vulnerabilities leading to defacement
- Learn to identify security weaknesses in web applications
- Practice responsible disclosure and security testing
- Create proper security assessment reports

## Tools Required
- Kali Linux (recommended)
- Python 3.x
- Target Ubuntu system with web server (Apache/Nginx)
- Metasploitable or similar vulnerable VM for testing

## Setup Instructions

### 1. Environment Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required Python packages
pip3 install requests

# Ensure script is executable
chmod +x website_deface_test.py
```

### 2. Target System Setup
On your Ubuntu target system:
```bash
# Install Apache
sudo apt install apache2 -y

# Start Apache service
sudo systemctl start apache2
sudo systemctl enable apache2

# Create a vulnerable test page (for educational purposes)
sudo nano /var/www/html/login.php
```

### 3. Network Configuration
Ensure both systems can communicate:
```bash
# Test connectivity from Kali to Ubuntu
ping <ubuntu-ip>
curl http://<ubuntu-ip>
```

## Usage

### Basic Usage
```bash
python3 website_deface_test.py <target-url>
```

### Examples
```bash
# Test basic vulnerability scanning
python3 website_deface_test.py http://192.168.1.100

# Test with authentication
python3 website_deface_test.py http://192.168.1.100 -u admin -p password

# Save report to file
python3 website_deface_test.py http://192.168.1.100 -o security_report.txt
```

## What the Script Tests

### 1. SQL Injection
- Tests login forms for SQL injection vulnerabilities
- Uses common payload patterns
- Checks for successful authentication bypass

### 2. Directory Traversal
- Tests for file system access vulnerabilities
- Attempts to read sensitive files
- Checks for successful file access

### 3. File Upload
- Tests insecure file upload functionality
- Attempts to upload PHP files
- Checks for successful upload

### 4. Authentication Bypass
- Tests for unprotected admin panels
- Checks common admin paths
- Identifies access control issues

## Defacement Simulation

The script simulates website defacement by:
1. Identifying vulnerabilities
2. Generating defacement HTML content
3. Explaining the attack process
4. Creating security recommendations

**Note**: This is educational only - no actual defacement occurs

## Sample Output

```
============================================================
WEBSITE DEFACEMENT TESTING TOOL
Educational Purpose Only - IA-650 Course
============================================================
[+] Testing http://192.168.1.100 for vulnerabilities...
[*] Testing SQL Injection...
[!] Potential SQL Injection found with payload: ' OR '1'='1
[*] Testing Directory Traversal...
[*] Testing File Upload...
[*] Testing Authentication Bypass...

[!] VULNERABILITIES FOUND: SQL Injection

[!] Simulating defacement via SQL Injection...
[+] Defacement page content generated:
<!DOCTYPE html>
<html>
<head>
    <title>SECURITY TEST</title>
    ...
</head>
<body>
    <h1>HACKED BY IA-650 STUDENT</h1>
    ...
</body>
</html>
```

## Defense Strategies

### Prevention Techniques
1. **Input Validation**
   - Sanitize all user inputs
   - Use whitelist validation
   - Implement length limits

2. **SQL Injection Protection**
   - Use parameterized queries
   - Implement prepared statements
   - Use ORM frameworks

3. **File Upload Security**
   - Validate file types
   - Scan for malware
   - Store uploads outside web root

4. **Access Control**
   - Implement proper authentication
   - Use principle of least privilege
   - Regular access audits

### Detection Methods
1. **Web Application Firewalls (WAF)**
2. **Intrusion Detection Systems (IDS)**
3. **File integrity monitoring**
4. **Regular security scanning**

## Lab Exercises

### Exercise 1: Vulnerability Identification
- Run the script against a vulnerable test system
- Document all found vulnerabilities
- Research each vulnerability type

### Exercise 2: Defense Implementation
- Patch identified vulnerabilities
- Re-run the script to verify fixes
- Document the defense mechanisms

### Exercise 3: Report Writing
- Generate a comprehensive security report
- Include risk assessments
- Provide remediation recommendations

## Troubleshooting

### Common Issues
1. **Connection Refused**
   - Check target system firewall
   - Verify web server is running
   - Confirm network connectivity

2. **Time Out Errors**
   - Increase timeout values
   - Check network stability
   - Verify target responsiveness

3. **Permission Denied**
   - Check script permissions
   - Run with appropriate privileges
   - Verify file access rights

## Further Learning

### Advanced Topics
- Metasploit framework
- Burp Suite web testing
- OWASP Top 10 vulnerabilities
- Web application penetration testing

### Resources
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [Kali Linux Tools](https://www.kali.org/tools/)
- [Web Security Academy](https://portswigger.net/web-security)

## Disclaimer

This laboratory exercise is designed for educational purposes in a controlled environment. The techniques demonstrated should only be used on systems where you have explicit permission to test. The authors and educational institution are not responsible for misuse of this information.
