import json
import os
from cryptography.fernet import Fernet

# Generate a key for encryption (only run once)
def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

# Load the encryption key
def load_key():
    try:
        return open("key.key", "rb").read()
    except FileNotFoundError:
        print("Encryption key not found. Generating a new one.")
        generate_key()
        return open("key.key", "rb").read()

# Encrypt a password
def encrypt_password(password, key):
    f = Fernet(key)
    return f.encrypt(password.encode())

# Decrypt a password
def decrypt_password(encrypted_password, key):
    f = Fernet(key)
    return f.decrypt(encrypted_password).decode()

# Save password to JSON file
def save_password(account, password):
    key = load_key()
    encrypted_password = encrypt_password(password, key)

    data = {}
    if os.path.exists("passwords.json"):
        with open("passwords.json", "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                pass

    data[account] = encrypted_password.decode()

    with open("passwords.json", "w") as file:
        json.dump(data, file, indent=4)

# Retrieve a password from JSON file
def get_password(account):
    key = load_key()
    if not os.path.exists("passwords.json"):
        return None

    with open("passwords.json", "r") as file:
        data = json.load(file)

    encrypted_password = data.get(account)
    if encrypted_password:
        return decrypt_password(encrypted_password.encode(), key)
    else:
        return None

# Main function to run the program
def main():
    if not os.path.exists("key.key"):
        generate_key()

    while True:
        choice = input("Do you want to (s)ave a password or (g)et a password? (q to quit): ").strip().lower()
        if choice == 's':
            account = input("Enter the account name: ").strip()
            password = input("Enter the password: ").strip()
            save_password(account, password)
            print("Password saved successfully!")
        elif choice == 'g':
            account = input("Enter the account name: ").strip()
            password = get_password(account)
            if password:
                print(f"Password for {account}: {password}")
            else:
                print("Account not found or file missing.")
        elif choice == 'q':
            break
        else:
            print("Invalid choice. Please enter 's', 'g', or 'q'.")

if __name__ == "__main__":
    main()
