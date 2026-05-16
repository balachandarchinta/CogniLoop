"""
Test script for authentication endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("\n=== Testing Health Endpoint ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_register():
    """Test user registration"""
    print("\n=== Testing User Registration ===")
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User",
        "age": 25,
        "education_level": "Bachelor's"
    }
    response = requests.post(f"{BASE_URL}/api/v1/auth/register", json=user_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 201

def test_login():
    """Test user login"""
    print("\n=== Testing User Login ===")
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        return data.get("access_token"), data.get("refresh_token")
    else:
        print(f"Response: {response.text}")
        return None, None

def test_get_current_user(access_token):
    """Test getting current user info"""
    print("\n=== Testing Get Current User ===")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/api/v1/auth/me", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_refresh_token(refresh_token):
    """Test token refresh"""
    print("\n=== Testing Token Refresh ===")
    refresh_data = {"refresh_token": refresh_token}
    response = requests.post(f"{BASE_URL}/api/v1/auth/refresh", json=refresh_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return True
    else:
        print(f"Response: {response.text}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("COGNITIVE LEARNING PLATFORM - AUTHENTICATION TESTS")
    print("=" * 60)
    
    try:
        # Test health endpoint
        if not test_health():
            print("\n❌ Health check failed!")
            return
        
        # Test registration
        if not test_register():
            print("\n⚠️  Registration failed (user might already exist)")
        
        # Test login
        access_token, refresh_token = test_login()
        if not access_token:
            print("\n❌ Login failed!")
            return
        
        # Test get current user
        if not test_get_current_user(access_token):
            print("\n❌ Get current user failed!")
            return
        
        # Test token refresh
        if not test_refresh_token(refresh_token):
            print("\n❌ Token refresh failed!")
            return
        
        print("\n" + "=" * 60)
        print("✅ ALL AUTHENTICATION TESTS PASSED!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Could not connect to server. Make sure it's running on http://localhost:8000")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")

if __name__ == "__main__":
    main()

# Made with Bob
