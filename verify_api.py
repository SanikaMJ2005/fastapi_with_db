import requests

BASE_URL = "http://127.0.0.1:8000"

def test_api():
    # 1. Signup
    print("Signing up...")
    res = requests.post(f"{BASE_URL}/singnup", json={"email": "userA@example.com", "password": "password123"})
    print(res.status_code, res.json())

    # 2. Login User A
    print("\nLogging in User A...")
    res = requests.post(f"{BASE_URL}/login", json={"email": "userA@example.com", "password": "password123"})
    tokenA = res.json()["access_token"]
    print(f"Token A: {tokenA[:10]}...")

    # 3. Ask AI as User A
    print("\nAsking AI as User A...")
    res = requests.post(f"{BASE_URL}/ask", json={"prompt": "Hello from User A"}, headers={"Authorization": f"Bearer {tokenA}"})
    print(res.status_code, res.json())

    # 4. Check history for User A
    print("\nChecking history for User A...")
    res = requests.get(f"{BASE_URL}/history", headers={"Authorization": f"Bearer {tokenA}"})
    historyA = res.json()
    print(f"History A count: {len(historyA)}")
    for h in historyA:
        print(f" - {h['prompt']}: {h['response'][:20]}...")

    # 5. Signup User B
    print("\nSigning up User B...")
    requests.post(f"{BASE_URL}/singnup", json={"email": "userB@example.com", "password": "password123"})

    # 6. Login User B
    print("\nLogging in User B...")
    res = requests.post(f"{BASE_URL}/login", json={"email": "userB@example.com", "password": "password123"})
    tokenB = res.json()["access_token"]

    # 7. Check history for User B (should be empty)
    print("\nChecking history for User B (should be empty)...")
    res = requests.get(f"{BASE_URL}/history", headers={"Authorization": f"Bearer {tokenB}"})
    historyB = res.json()
    print(f"History B count: {len(historyB)}")

if __name__ == "__main__":
    test_api()
