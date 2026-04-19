import msal 
import requests
import os
from dotenv import load_dotenv
load_dotenv()
TENANT_ID = os.getenv('TENANT_ID')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
GRAPH_URL = "https://graph.microsoft.com/v1.0/users"
SCOPE = ["https://graph.microsoft.com/.default"]