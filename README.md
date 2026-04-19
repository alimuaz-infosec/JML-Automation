# Entra ID JML Automation Suite

A professional-grade identity lifecycle management suite designed to automate the Joiner, Mover, and Leaver (JML) processes in Microsoft Entra ID. Built using **Python** and the **Microsoft Graph API**.

## 🚀 Features

* **Joiner:** Automated account provisioning with secure temporary credential handling and attribute mapping.
* **Mover:** Dynamic `PATCH` operations that update user attributes (Department, Title, Office) without overwriting existing data.
* **Leaver:** A high-security offboarding utility that disables accounts and forces the immediate revocation of all active sign-in sessions.

## 🛠 Tech Stack
* **Language:** Python
* **API:** Microsoft Graph API (v1.0)
* **Authentication:** OAuth 2.0 Client Credentials Grant (Service Principal)
* **Governance:** Principle of Least Privilege

## ⚙️ Prerequisites

1. **App Registration:** Create an App Registration in your Entra ID tenant.
2. **API Permissions:** Grant the following Application permissions:
   - `User.ReadWrite.All`
   - `Directory.ReadWrite.All`
3. **Admin Consent:** Click "Grant admin consent" for your organization.
4. **Environment Variables:** Create a `.env` file in the project root(you have to create env file in same folder then python can fetch):
   ```text
   TENANT_ID=your-tenant-id-here
   CLIENT_ID=your-client-id-here
   CLIENT_SECRET=your-client-secret-here
