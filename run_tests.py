#!/usr/bin/env python3
"""
Test runner script for Eva Coloring Sheet AI
"""

import os
import sys
import subprocess
from pathlib import Path

def run_tests():
    """Run all tests with proper configuration"""
    
    print("🧪 Running Eva Coloring Sheet AI Tests")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("❌ Error: pyproject.toml not found. Please run from project root.")
        sys.exit(1)
    
    # Set up environment
    os.environ.setdefault("PYTHONPATH", ".")
    
    # Run pytest with coverage
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "--cov=src",
        "--cov-report=term-missing",
        "--cov-report=html",
        "--tb=short"
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        print("\n✅ All tests passed!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Tests failed with exit code {e.returncode}")
        return False

def run_specific_test(test_file):
    """Run a specific test file"""
    
    print(f"🧪 Running specific test: {test_file}")
    print("=" * 50)
    
    test_path = Path("tests") / test_file
    if not test_path.exists():
        print(f"❌ Test file not found: {test_path}")
        sys.exit(1)
    
    cmd = [
        sys.executable, "-m", "pytest",
        str(test_path),
        "-v",
        "--tb=short"
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        print(f"\n✅ Test {test_file} passed!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Test {test_file} failed with exit code {e.returncode}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Run specific test
        test_file = sys.argv[1]
        success = run_specific_test(test_file)
    else:
        # Run all tests
        success = run_tests()
    
    sys.exit(0 if success else 1) 