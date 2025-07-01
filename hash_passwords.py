# hash_passwords.py
from streamlit_authenticator.utilities.hasher import Hasher

passwords = ['12345']

hasher = Hasher()
hashed_passwords = hasher.generate(passwords)

print(hashed_passwords)
