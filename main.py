from ig_api import IGClient
import sys

def main():
    client = IGClient()
    try:
        # 1. Connect
        session_details = client.connect()
        print(f"\n[1] Connected: CST={session_details['cst'][:10]}...")
        
        # 2. Read Session
        details = client.session.read()
        print(f"\n[2] Read Session: ClientID={details.get('clientId')}")

        # 3. Switch Account (Try switching to same account)
        if client.session.account_id:
             client.session.switch_account(client.session.account_id)
        
        # 4. Logout
        logout_success = client.logout()
        print(f"\n[4] Logout Successful: {logout_success}")
        
    except Exception as e:
        print(f"\n[!] Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
