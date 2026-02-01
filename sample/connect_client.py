from ig_api import IGClient

def connect_demo():
    print("--- Connect Client Sample ---")
    client = IGClient()
    try:
        session_details = client.connect()
        print("Successfully connected!")
        print(f"Account ID: {session_details.get('account_id')}")
    except Exception as e:
        print(f"Failed to connect: {e}")

if __name__ == "__main__":
    connect_demo()
