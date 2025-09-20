import random
import string

# Define alphabet (A-Z and 0-9)
ALPHABET = string.ascii_uppercase + string.digits
SIZE = len(ALPHABET)

def generate_key(length):
    """Generate a random key of given length using A-Z0-9."""
    return ''.join(random.choice(ALPHABET) for _ in range(length))

def vigenere_encrypt(plaintext, key):
    """Encrypt plaintext using Vigenere cipher and provided key."""
    plaintext = plaintext.upper().replace(" ", "")
    key = key.upper()
    
    ciphertext = ""
    for i, char in enumerate(plaintext):
        if char not in ALPHABET:
            ciphertext += char  # keep characters outside alphabet
            continue
        shift = ALPHABET.index(key[i % len(key)])
        new_char = ALPHABET[(ALPHABET.index(char) + shift) % SIZE]
        ciphertext += new_char
    return ciphertext

def vigenere_decrypt(ciphertext, key):
    """Decrypt ciphertext using Vigenere cipher and provided key."""
    ciphertext = ciphertext.upper().replace(" ", "")
    key = key.upper()
    
    plaintext = ""
    for i, char in enumerate(ciphertext):
        if char not in ALPHABET:
            plaintext += char
            continue
        shift = ALPHABET.index(key[i % len(key)])
        new_char = ALPHABET[(ALPHABET.index(char) - shift) % SIZE]
        plaintext += new_char
    return plaintext

# === Demo ===
if __name__ == "__main__":
    choice = input("Choose (1) Encrypt or (2) Decrypt: ").strip()
    
    if choice == "1":
        plaintext = input("Enter plaintext: ")
        key = input("Enter key (leave empty for auto-generate): ").strip()
        if not key:
            key = generate_key(len(plaintext))
            print(f"Generated Key: {key}")
        ciphertext = vigenere_encrypt(plaintext, key)
        print(f"Ciphertext: {ciphertext}")
    
    elif choice == "2":
        ciphertext = input("Enter ciphertext: ")
        key = input("Enter key: ").strip()
        plaintext = vigenere_decrypt(ciphertext, key)
        print(f"Plaintext: {plaintext}")
    
    else:
        print("Invalid choice")
