import sys
import httpx

API_URL = "http://127.0.0.1:8000/auth"

def register_user():
    print("Registering user...")
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    payload = {"username": username, "password": password}

    response = httpx.post(f"{API_URL}/register", json=payload)
    if response.status_code == 200:
        print("Registration successful!")
    else:
        print(f"Error: {response.json()['detail']}")

def login_user():
    print("Logging in user...")
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    payload = {"username": username, "password": password}

    response = httpx.post(f"{API_URL}/login", json=payload)

    if response.status_code == 200:
        print("Login successful!")
        print("Access Token:", response.json()["access_token"])
    else:
        print(f"Error: {response.json()['detail']}")

def main():
    print("Welcome to the Terminal Chat Application")
    print("1. Register")
    print("2. Login")
    option = input("Choose an option (1 or 2): ")

    if option == "1":
        register_user()
    elif option == "2":
        login_user()
    else:
        print("Invalid option selected.")
        sys.exit(1)

if __name__ == "__main__":
    main()
