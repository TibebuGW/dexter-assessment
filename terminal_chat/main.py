import sys
import httpx
import time

API_URL = "http://127.0.0.1:8000"
TOKEN = None  

def register_user():
    print("Registering user...")
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    payload = {"username": username, "password": password}

    response = httpx.post(f"{API_URL}/auth/register", json=payload)
    if response.status_code == 200:
        print("Registration successful!")
    else:
        print(f"Error: {response.json()['detail']}")

def login_user():
    global TOKEN
    print("Logging in user...")
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    payload = {"username": username, "password": password}

    response = httpx.post(f"{API_URL}/auth/login", json=payload)

    if response.status_code == 200:
        print("Login successful!")
        TOKEN = response.json()["access_token"]
    else:
        print(f"Error: {response.json()['detail']}")

def get_all_users():
    if not TOKEN:
        print("You need to log in first.")
        return []

    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = httpx.get(f"{API_URL}/chat/users", headers=headers)
    if response.status_code == 200:
        users = response.json()
        return users
    else:
        print(f"Error: {response.json()['detail']}")
        return []

def send_message(sender_id, receiver_id, content):
    if not TOKEN:
        print("You need to log in first.")
        return

    headers = {"Authorization": f"Bearer {TOKEN}"}
    payload = {"sender_id": sender_id, "receiver_id": receiver_id, "content": content}
    response = httpx.post(f"{API_URL}/chat/send_message", headers=headers, json=payload)
    if response.status_code == 200:
        print("\n")
    else:
        print(f"Error: {response.json()['detail']}")

def get_messages(user_id, chat_with_id):
    if not TOKEN:
        print("You need to log in first.")
        return []

    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = httpx.get(f"{API_URL}/chat/messages/{chat_with_id}", headers=headers)
    
    if response.status_code == 200:
        messages = response.json()
        return messages
    else:
        print(f"Error: {response.json()['detail']}")
        return []

def chat_interface(current_user):
    print("Fetching list of users...")
    users = get_all_users()
    if not users:
        print("No users available to chat with.")
        return
    
    id_to_username_map = {current_user['id']: 'You'}

    print("Select a user to chat with:")
    for user in users:
        cur_id = user['id']
        cur_username = user['username']
        print(f"{cur_id} - {cur_username}")
        id_to_username_map[user["id"]] = user["username"]
    
    selected_user_idx = int(input("Enter the id of the user you want to chat with: "))

    print(f"Starting chat with {id_to_username_map[selected_user_idx]}. Type 'exit' to quit.")

    last_seen_timestamp = time.time() 

    while True:
        message_content = input("You: ")
        if message_content.lower() == "exit":
            break
        
        send_message(current_user['id'], selected_user_idx, message_content)

        new_messages = get_new_messages(current_user['id'], selected_user_idx, last_seen_timestamp)
        
        if new_messages:
            for msg in new_messages:
                current_user_name = id_to_username_map[msg['sender_id']]
                message = msg['content']
                print(f"{current_user_name}: {message}\n")
            
            last_seen_timestamp = time.time()

        time.sleep(2)

def get_new_messages(sender_id, receiver_id, last_seen_timestamp):
    messages = get_messages(sender_id, receiver_id)
    new_messages = [msg for msg in messages if msg['timestamp'] > str(last_seen_timestamp)]
    return new_messages[::-1]

def main():
    print("Welcome to the Terminal Chat Application")
    print("1. Register")
    print("2. Login")
    option = input("Choose an option (1 or 2): ")

    if option == "1":
        register_user()
    elif option == "2":
        login_user()
        if TOKEN:
            current_user = {"id": 1, "username": "dummy_user"}
            chat_interface(current_user)  
    else:
        print("Invalid option selected.")
        sys.exit(1)

if __name__ == "__main__":
    main()
