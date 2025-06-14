import os

# Generate a 32-byte (256-bit) secret key
secret_key = os.urandom(32).hex()
print(secret_key)