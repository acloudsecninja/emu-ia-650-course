#!/usr/bin/env python3
"""
Troubleshooting script for offensive_security_ai.py
Checks system resources and dependencies
"""

import os
import sys
import platform
import subprocess
import logging

def check_python_version():
    """Check Python version compatibility"""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required")
        return False
    else:
        print("✅ Python version OK")
        return True

def check_system_resources():
    """Check available system resources"""
    try:
        import psutil
        
        # Memory info
        memory = psutil.virtual_memory()
        print(f"Total RAM: {memory.total / (1024**3):.2f} GB")
        print(f"Available RAM: {memory.available / (1024**3):.2f} GB")
        print(f"Memory usage: {memory.percent}%")
        
        if memory.available < 2 * (1024**3):  # Less than 2GB available
            print("⚠️  Low memory available - may cause issues")
        else:
            print("✅ Memory OK")
            
        # CPU info
        cpu_count = psutil.cpu_count()
        print(f"CPU cores: {cpu_count}")
        
        return True
    except ImportError:
        print("❌ psutil not installed - cannot check system resources")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'torch', 'transformers', 'requests', 'rich', 'numpy', 'scikit-learn'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing.append(package)
    
    if missing:
        print(f"\nMissing packages: {', '.join(missing)}")
        print("Install with: pip install -r requirements.txt")
        return False
    else:
        print("✅ All dependencies OK")
        return True

def check_gpu():
    """Check GPU availability"""
    try:
        import torch
        
        if torch.cuda.is_available():
            gpu_count = torch.cuda.device_count()
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)
            print(f"✅ GPU available: {gpu_name}")
            print(f"   GPU memory: {gpu_memory:.2f} GB")
            print(f"   GPU count: {gpu_count}")
        else:
            print("ℹ️  No GPU available - will use CPU")
            
        return True
    except ImportError:
        print("❌ PyTorch not installed")
        return False

def check_network():
    """Check network connectivity"""
    try:
        import requests
        response = requests.get("https://huggingface.co", timeout=10)
        if response.status_code == 200:
            print("✅ Network connectivity OK")
            return True
        else:
            print(f"⚠️  Network issue: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Network connectivity failed: {e}")
        return False

def main():
    print("🔧 Offensive Security AI - Troubleshooting Tool")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("System Resources", check_system_resources),
        ("Dependencies", check_dependencies),
        ("GPU Support", check_gpu),
        ("Network", check_network)
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n📋 {name}:")
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Error checking {name}: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 Summary:")
    
    if all(results):
        print("✅ All checks passed - should work fine")
        print("\nRecommended command:")
        print("python3 offensive_security_ai.py --model gpt2 --device cpu")
    else:
        print("⚠️  Some issues detected - see above")
        print("\nMinimal requirements command:")
        print("python3 offensive_security_ai.py --model gpt2 --device cpu --attack-type payload")

if __name__ == "__main__":
    main()
