import requests
import os
from dotenv import load_dotenv

# --- AUTHENTICATION ---
def get_access_token():
    load_dotenv()
    # Ensure these are set in your .env file
    tenant_id = os.getenv("TENANT_ID")
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    data = {
        "client_id": client_id,
        "scope": "https://graph.microsoft.com/.default",
        "client_secret": client_secret,
        "grant_type": "client_credentials",
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print(f"❌ Auth Error: {response.text}")
        return None

# --- LEAVER LOGIC ---
def process_leaver(token, upn):
    """
    1. Disable Account (Prevent new logins)
    2. Revoke Sessions (Kill active connections)
    """
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    # Step 1: Disable the Account
    update_url = f"https://graph.microsoft.com/v1.0/users/{upn}"
    payload = {"accountEnabled": False}
    
    print(f"📡 Disabling account: {upn}...")
    res1 = requests.patch(update_url, json=payload, headers=headers)
    
    # Step 2: Revoke Sign-in Sessions (The Security Kill-Switch)
    revoke_url = f"https://graph.microsoft.com/v1.0/users/{upn}/revokeSignInSessions"
    
    print(f"🔒 Revoking active sessions...")
    res2 = requests.post(revoke_url, headers=headers)

    # Check results
    if res1.status_code == 204 and res2.status_code == 200:
        print(f"✅ LEAVER SUCCESS: {upn} is fully locked out.")
    else:
        print(f"⚠️ Warning: Check errors - Disable Status: {res1.status_code}, Revoke Status: {res2.status_code}")

if __name__ == "__main__":
    token = get_access_token()
    if token:
        # Replace with the UPN of the user to be offboarded
        target_user = "zain@896.omnimicrosoft.com" 
        process_leaver(token, target_user)