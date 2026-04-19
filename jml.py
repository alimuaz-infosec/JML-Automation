import msal
import requests
import os
from dotenv import load_dotenv

# --- STEP 1: LOAD ENVIRONMENT FIRST ---
# This must happen before we define the AUTHORITY variable
load_dotenv()

TENANT_ID = os.getenv('TENANT_ID')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

# --- STEP 2: BUILD STRINGS AFTER LOADING ---
# Now TENANT_ID has a value, so AUTHORITY won't be ".../None"
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
GRAPH_URL = "https://graph.microsoft.com/v1.0/users"
SCOPE = ["https://graph.microsoft.com/.default"]

def get_access_token():
    """Authenticates with Microsoft and returns an Access Token"""
    app = msal.ConfidentialClientApplication(
        CLIENT_ID, 
        authority=AUTHORITY, 
        client_credential=CLIENT_SECRET
    )
    
    # Request the token
    result = app.acquire_token_for_client(scopes=SCOPE)
    
    if "access_token" in result:
        return result["access_token"]
    else:
        print(f"❌ AUTH ERROR: {result.get('error_description')}")
        return None

def create_entra_user(token, display_name, upn, temp_password):
    """Sends the actual request to create the user in the cloud"""
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    user_payload = {
        "accountEnabled": True,
        "displayName": display_name,
        "mailNickname": display_name.replace(" ", "").lower(),
        "userPrincipalName": upn,
        "passwordProfile": {
            "forceChangePasswordNextSignIn": True,
            "password": temp_password
        }
    }
    
    print(f"📡 Sending request to: {GRAPH_URL}")
    response = requests.post(GRAPH_URL, json=user_payload, headers=headers)
    
    if response.status_code == 201:
        print(f"✅ SUCCESS: User '{display_name}' created in Entra ID.")
    else:
        print(f"❌ API ERROR: {response.status_code}")
        print(f"Details: {response.text}")

# --- STEP 3: RUN THE PROCESS ---
if __name__ == "__main__":
    print("🚀 Starting JML Joiner Process...")
    
    # Debug: Confirming we have the ID
    if not TENANT_ID:
        print("❌ ERROR: TENANT_ID is missing! Check your .env file location.")
    else:
        print(f"🔎 Using Tenant ID: {TENANT_ID[:6]}... (Loaded successfully)")
        
        my_token = get_access_token()
        
        if my_token:
            # Change the UPN below to match your specific domain!
            create_entra_user(
                token=my_token,
                display_name="Usama Test User",
                upn="Usama.test@896.onmicrosoft.com",
                temp_password="SecurePassword2026!"
            )