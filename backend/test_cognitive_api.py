import requests
import json
import time

BASE_URL = "http://localhost:8001"

def get_auth_token():
    print("\n--- Getting Auth Token ---")
    # Register dummy user or login
    user_data = {
        "email": "cognitive_test@example.com",
        "password": "testpassword123",
        "full_name": "Cognitive Test User",
        "age": 30,
        "education_level": "Master's"
    }
    requests.post(f"{BASE_URL}/api/v1/auth/register", json=user_data)
    
    login_data = {"email": "cognitive_test@example.com", "password": "testpassword123"}
    resp = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
    if resp.status_code == 200:
        return resp.json()["access_token"]
    return None

def test_analyze_attention(token):
    print("\n--- Testing Analyze Attention Endpoint ---")
    headers = {"Authorization": f"Bearer {token}"}
    
    events = [
        {"type": "scroll", "time_spent": 10},
        {"type": "video_play", "time_spent": 120},
        {"type": "tab_switch", "time_spent": 5},
    ]
    
    resp = requests.post(f"{BASE_URL}/api/v1/cognitive/attention/analyze", json=events, headers=headers)
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        print(f"Response: {json.dumps(resp.json(), indent=2)}")
    else:
        print(f"Error: {resp.text}")

def test_ingest_events(token):
    print("\n--- Testing Ingest Events Endpoint ---")
    headers = {"Authorization": f"Bearer {token}"}
    
    events = [
        {"type": "quiz_complete", "time_spent": 300, "metadata": {"score": 85}},
        {"type": "video_complete", "time_spent": 600}
    ]
    
    resp = requests.post(f"{BASE_URL}/api/v1/cognitive/events", json=events, headers=headers)
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.json() if resp.status_code == 202 else resp.text}")

def test_get_profile(token):
    print("\n--- Testing Get Profile Endpoint ---")
    headers = {"Authorization": f"Bearer {token}"}
    
    resp = requests.get(f"{BASE_URL}/api/v1/cognitive/profile", headers=headers)
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        print(f"Response: {json.dumps(resp.json(), indent=2)}")
    else:
        print(f"Error: {resp.text}")

if __name__ == "__main__":
    token = get_auth_token()
    if token:
        test_analyze_attention(token)
        test_ingest_events(token)
        test_get_profile(token)
    else:
        print("Failed to get auth token")
