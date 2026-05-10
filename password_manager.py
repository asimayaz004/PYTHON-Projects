from cryptography.fernet import Fernet
import json
import os

KEY_FILE = "secret.key"
DATA_FILE = "passwords.json"


# -----------------------------------
# Generate Encryption Key
# -----------------------------------

def generate_key():
    key = Fernet.generate_key()

    with open(KEY_FILE, "wb") as file:
        file.write(key)


def load_key():
    return open(KEY_FILE, "rb").read()


# -----------------------------------
# Initialize
# -----------------------------------

if not os.path.exists(KEY_FILE):
    generate_key()

key = load_key()
cipher = Fernet(key)


# -----------------------------------
# Save Password
# -----------------------------------

def save_password():
    website = input("Website: ")
    username = input("Username: ")
    password = input("Password: ")

    encrypted_password = cipher.encrypt(password.encode()).decode()

    data = {}

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            try:
                data = json.load(file)
            except:
                data = {}

    data[website] = {
        "username": username,
        "password": encrypted_password
    }

    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

    print("Password saved successfully!")


# -----------------------------------
# View Password
# -----------------------------------

def view_password():
    website = input("Enter website: ")

    if not os.path.exists(DATA_FILE):
        print("No passwords stored.")
        return

    with open(DATA_FILE, "r") as file:
        data = json.load(file)

    if website in data:
        username = data[website]["username"]
        encrypted_password = data[website]["password"]

        decrypted_password = cipher.decrypt(
            encrypted_password.encode()
        ).decode()

        print("\nSaved Details:")
        print("Username:", username)
        print("Password:", decrypted_password)

    else:
        print("Website not found.")


# -----------------------------------
# Main Menu
# -----------------------------------

def main():
    while True:
        print("\n===== PASSWORD MANAGER =====")
        print("1. Save Password")
        print("2. View Password")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            save_password()

        elif choice == "2":
            view_password()

        elif choice == "3":
            print("Exiting...")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()