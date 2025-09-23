
import subprocess
import shutil

def check_command(cmd, name):
    print(f"Checking {name}...")
    result = shutil.which(cmd)
    if result:
        try:
            version = subprocess.check_output([cmd, '--version'], stderr=subprocess.STDOUT)
            print(f"✅ {name} is installed: {version.decode().strip()}")
        except Exception as e:
            print(f"⚠️ {name} is installed but version check failed: {e}")
    else:
        print(f"❌ {name} is NOT installed.")

print("🔍 Starting environment check for backend project setup...\n")

check_command("python", "Python")
check_command("pip", "pip (Python package manager)")
check_command("git", "Git (version control)")
check_command("psql", "PostgreSQL client (psql)")

print("\n💡 If you see any ❌ items above, install them before continuing Week 1.")
print("✅ You're ready to start if all required tools are installed!")
