import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set the working directory to backend
os.chdir(os.path.dirname(os.path.abspath(__file__)))

try:
    from app.config import settings
    print("✓ Configuration loaded successfully!")
    print(f"  App Name: {settings.APP_NAME}")
    print(f"  Version: {settings.APP_VERSION}")
    print(f"  Debug: {settings.DEBUG}")
    print(f"  Database URL: {settings.DATABASE_URL}")
    print(f"  Secret Key: {'*' * 20} (hidden)")
except Exception as e:
    print(f"✗ Configuration failed: {e}")
    import traceback
    traceback.print_exc()

# Made with Bob
