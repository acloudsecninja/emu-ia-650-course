#!/bin/bash

# Vulnerable Web Server Setup Script
# Educational Purpose Only - IA-650 Course
# This creates a deliberately vulnerable web server for testing

echo "[+] Setting up vulnerable web server for educational testing..."

# Update system
sudo apt update -y

# Install Apache and PHP
sudo apt install apache2 php php-mysql -y

# Start Apache
sudo systemctl start apache2
sudo systemctl enable apache2

# Create vulnerable login page
echo "[+] Creating vulnerable login page..."
sudo tee /var/www/html/login.php > /dev/null << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
    <style>
        body { font-family: Arial; text-align: center; margin-top: 100px; }
        .login { border: 1px solid #ccc; padding: 20px; display: inline-block; }
        input { margin: 10px; padding: 5px; }
        button { padding: 10px 20px; }
    </style>
</head>
<body>
    <div class="login">
        <h2>Admin Login</h2>
        <form method="post" action="auth.php">
            <input type="text" name="username" placeholder="Username" required><br>
            <input type="password" name="password" placeholder="Password" required><br>
            <button type="submit">Login</button>
        </form>
    </div>
</body>
</html>
EOF

# Create vulnerable authentication script
echo "[+] Creating vulnerable authentication script..."
sudo tee /var/www/html/auth.php > /dev/null << 'EOF'
<?php
// VULNERABLE AUTHENTICATION - FOR EDUCATIONAL PURPOSES ONLY
$username = $_POST['username'];
$password = $_POST['password'];

// VULNERABLE SQL QUERY - PRONE TO INJECTION
$conn = new mysqli("localhost", "root", "", "testdb");
$query = "SELECT * FROM users WHERE username='$username' AND password='$password'";
$result = $conn->query($query);

if ($result->num_rows > 0) {
    echo "<h1>Welcome Admin!</h1>";
    echo "<p>You have successfully logged in.</p>";
    echo "<a href='admin.php'>Go to Admin Panel</a>";
} else {
    echo "<h1>Login Failed</h1>";
    echo "<a href='login.php'>Try Again</a>";
}
?>
EOF

# Create vulnerable admin panel
echo "[+] Creating vulnerable admin panel..."
sudo tee /var/www/html/admin.php > /dev/null << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Admin Panel</title>
    <style>
        body { font-family: Arial; margin: 20px; }
        .panel { border: 1px solid #ccc; padding: 20px; }
        button { margin: 10px; padding: 10px; }
    </style>
</head>
<body>
    <div class="panel">
        <h1>Admin Control Panel</h1>
        <h2>File Upload</h2>
        <form method="post" action="upload.php" enctype="multipart/form-data">
            <input type="file" name="file" required><br><br>
            <button type="submit">Upload File</button>
        </form>
        
        <h2>View Files</h2>
        <form method="get" action="view.php">
            <input type="text" name="file" placeholder="Enter filename" required>
            <button type="submit">View File</button>
        </form>
    </div>
</body>
</html>
EOF

# Create vulnerable file upload script
echo "[+] Creating vulnerable file upload script..."
sudo tee /var/www/html/upload.php > /dev/null << 'EOF'
<?php
// VULNERABLE FILE UPLOAD - FOR EDUCATIONAL PURPOSES ONLY
if ($_FILES['file']['error'] == UPLOAD_ERR_OK) {
    $upload_dir = '/var/www/html/uploads/';
    $filename = basename($_FILES['file']['name']);
    
    // Create upload directory if it doesn't exist
    if (!file_exists($upload_dir)) {
        mkdir($upload_dir, 0777, true);
    }
    
    // VULNERABLE: No file type validation
    if (move_uploaded_file($_FILES['file']['tmp_name'], $upload_dir . $filename)) {
        echo "<h1>File Uploaded Successfully!</h1>";
        echo "<p>File: $filename</p>";
        echo "<p>Path: /uploads/$filename</p>";
        echo "<a href='admin.php'>Back to Admin</a>";
    } else {
        echo "<h1>Upload Failed</h1>";
    }
} else {
    echo "<h1>No file uploaded</h1>";
}
?>
EOF

# Create vulnerable file viewer
echo "[+] Creating vulnerable file viewer..."
sudo tee /var/www/html/view.php > /dev/null << 'EOF'
<?php
// VULNERABLE FILE VIEWER - FOR EDUCATIONAL PURPOSES ONLY
$filename = $_GET['file'];

// VULNERABLE: Directory traversal possible
$filepath = '/var/www/html/' . $filename;

if (file_exists($filepath)) {
    echo "<h1>File Contents: $filename</h1>";
    echo "<pre>" . htmlspecialchars(file_get_contents($filepath)) . "</pre>";
} else {
    echo "<h1>File not found: $filename</h1>";
}
echo "<a href='admin.php'>Back to Admin</a>";
?>
EOF

# Create uploads directory with permissive permissions
sudo mkdir -p /var/www/html/uploads
sudo chmod 777 /var/www/html/uploads

# Create test database and user table
echo "[+] Setting up vulnerable database..."
sudo mysql -u root -e "
CREATE DATABASE IF NOT EXISTS testdb;
USE testdb;
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL
);
INSERT INTO users (username, password) VALUES ('admin', 'password123');
"

# Set proper permissions
sudo chown -R www-data:www-data /var/www/html/
sudo chmod -R 755 /var/www/html/

# Create index page
sudo tee /var/www/html/index.html > /dev/null << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Welcome to Test Website</title>
    <style>
        body { font-family: Arial; text-align: center; margin-top: 100px; }
        h1 { color: #333; }
        .links { margin: 20px; }
        a { margin: 10px; text-decoration: none; color: #0066cc; }
    </style>
</head>
<body>
    <h1>Welcome to Our Test Website</h1>
    <p>This is a test website for security education.</p>
    <div class="links">
        <a href="login.php">Admin Login</a>
    </div>
</body>
</html>
EOF

# Get IP address
IP=$(hostname -I | awk '{print $1}')

echo "[+] Setup complete!"
echo "[+] Vulnerable web server is running at: http://$IP"
echo "[+] Test pages available:"
echo "    - Main page: http://$IP"
echo "    - Login page: http://$IP/login.php"
echo "    - Admin panel: http://$IP/admin.php (after login)"
echo ""
echo "[+] Default credentials:"
echo "    Username: admin"
echo "    Password: password123"
echo ""
echo "[!] WARNING: This server is intentionally VULNERABLE"
echo "[!] Use only for authorized educational testing"
echo "[!] Do not expose to production networks"
