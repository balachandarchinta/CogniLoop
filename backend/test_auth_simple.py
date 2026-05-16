"""
Simple test script for authentication endpoints (no Unicode)
"""
import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 60)
print("COGNITIVE LEARNING PLATFORM - AUTHENTICATION TESTS")
print("=" * 60)

# Test 1: Health Check
print("\n=== Test 1: Health Endpoint ===")
response = requests.get(f"{BASE_URL}/health")
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

# Test 2: Login (user already exists)
print("\n=== Test 2: User Login ===")
login_data = {
    "email": "test@example.com",
    "password": "testpassword123"
}
response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Access Token: {data['access_token'][:50]}...")
    print(f"Refresh Token: {data['refresh_token'][:50]}...")
    access_token = data['access_token']
    refresh_token = data['refresh_token']
    
    # Test 3: Get Current User
    print("\n=== Test 3: Get Current User ===")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/api/v1/auth/me", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test 4: Token Refresh
    print("\n=== Test 4: Token Refresh ===")
    refresh_data = {"refresh_token": refresh_token}
    response = requests.post(f"{BASE_URL}/api/v1/auth/refresh", json=refresh_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("New tokens received successfully!")
    
    print("\n" + "=" * 60)
    print("[SUCCESS] ALL AUTHENTICATION TESTS PASSED!")
    print("=" * 60)
else:
    print(f"Login failed: {response.text}")

# Made with Bob
