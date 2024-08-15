import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from utils import generate_salt, hash_password
#Creates a new user in the database with a unique username and a securely hashed master password
def create_user(conn, username, master_password):
    cursor = conn.cursor()

    #Checks if the username already exists in the database
    cursor.execute('SELECT COUNT(*) FROM Users WHERE Username = ?', (username,))
    count = cursor.fetchone()[0]

    if count > 0:
        print("Username already exists. Please choose a different username.")
        return #Return the warning message if the username is already taken

    #Generates a unique salt for the user
    salt = generate_salt()
    master_password_hash = hash_password(master_password, salt) #Hashes the master password using the generated salt

    #Registers the new user into the database with the hashed password and salt
    cursor.execute('''
    INSERT INTO Users (Username, MasterPasswordHash, MasterPasswordSalt)
    VALUES (?, ?, ?)
    ''', (username, base64.b64encode(master_password_hash).decode(), base64.b64encode(salt).decode()))
    #Saves the changes to the database
    conn.commit()
    print("User created successfully.")
