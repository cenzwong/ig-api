from ig_api import IGClient

def main():
    client = IGClient()
    try:
        session_details = client.connect()
        print(f"Session Details: {session_details}")
    except Exception as e:
        print("Failed to run application.")

if __name__ == "__main__":
    main()
