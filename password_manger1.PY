import json
import os
from cryptography.fernet import Fernet

# Generate a key for encryption
def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

# Load the encryption key
def load_key():
    return open("key.key", "rb").read()

# Encrypt password
def encrypt_password(password, key):
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    return encrypted_password

# Decrypt password
def decrypt_password(encrypted_password, key):
    f = Fernet(key)
    decrypted_password = f.decrypt(encrypted_password).decode()
    return decrypted_password

# Save password to a file
def save_password(account, password):
    key = load_key()
    encrypted_password = encrypt_password(password, key)
    if os.path.exists("passwords.json"):
        with open("passwords.json", "r+") as file:
            data = json.load(file)
            data[account] = encrypted_password.decode()
            file.seek(0)
            json.dump(data, file, indent=4)
    else:
        with open("passwords.json", "w") as file:
            json.dump({account: encrypted_password.decode()}, file, indent=4)

# Retrieve password from the file
def get_password(account):
    key = load_key()
    with open("passwords.json", "r") as file:
        data = json.load(file)
        encrypted_password = data.get(account)
        if encrypted_password:
            return decrypt_password(encrypted_password.encode(), key)
        else:
            return None

# Main function to run the program
def main():
    generate_key()  # Run this only once to create the key
    while True:
        choice = input("Do you want to (s)ave a password or (g)et a password? (q to quit): ")
        if choice == 's':
            account = input("Enter the account name: ")
            password = input("Enter the password: ")
            save_password(account, password)
            print("Password saved!")
        elif choice == 'g':
            account = input("Enter the account name: ")
            password = get_password(account)
            if password:
                print(f"Password for {account}: {password}")
            else:
                print("Account not found.")
        elif choice == 'q':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
