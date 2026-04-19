import msal
import requests
import os
from dotenv import load_dotenv
load_dotenv()
TENANT_ID = os.getenv('TENANT_ID')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
#now lets make strings
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
GRAPH_URL = "https://graph.microsoft.com/v1.0/users"
SCOPE = ["https://graph.microsoft.com/.default"]
def get_access_token():
    app=msal.ConfidentialClientApplication(
      CLIENT_ID,
      authority = AUTHORITY,
      client_credential = CLIENT_SECRET

    )
    result=app.acquire_token_for_client(scopes=SCOPE)
    if "access_token" in result:
        return result["access_token"]
    else:
        print(f"auth error {result.get("error description")}")

def mover_entra_user(token,upn,job_title=None,office_location=None,department=None):
    url=f"https://graph.microsoft.com/v1.0/users/{upn}"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    user_data={}
    if job_title: user_data["jobTitle"]=job_title
    if department: user_data["department"]=department
    if office_location: user_data["officeLocation"]= office_location
    if not user_data:
        print("no data provided to update")
        return
    print(f"patchin user ... {upn}")
    response= requests.patch(url,json=user_data,headers=headers)
    if response.status_code == 204:
        print(f"✅ MOVER SUCCESS: {upn} has been updated in Entra ID.")
    else:
        print(f"❌ ERROR {response.status_code}: {response.text}")
if __name__ == "__main__":
    my_token =get_access_token()
    if my_token:
        targetuser= "zain@896.onmicrosoft.com"
        mover_entra_user(
            token=my_token,
            upn=targetuser,
            job_title="Senior IAM Automation Engineer",
            department="Cybersecurity Ops",
            office_location="Lahore HQ"
        )
    