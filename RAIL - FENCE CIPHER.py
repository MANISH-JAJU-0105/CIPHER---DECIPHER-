def rail_fence_encrypt(plaintext):
    # Split into even and odd index characters
    even_chars = plaintext[::2]
    odd_chars = plaintext[1::2]
    ciphertext = even_chars + odd_chars
    return ciphertext

def rail_fence_decrypt(ciphertext):
    l = len(ciphertext)
    if l % 2 == 0:
        k = l // 2
    else:
        k = (l // 2) + 1
    # Reconstruct the plaintext
    plaintext = [''] * l
    # Fill even positions
    plaintext[::2] = ciphertext[:k]
    # Fill odd positions
    plaintext[1::2] = ciphertext[k:]
    return ''.join(plaintext)

def main():
    choice = input("Choose mode (encrypt/decrypt): ").strip().lower()

    if choice == "encrypt":
        plaintext = input("Enter plaintext: ")
        ciphertext = rail_fence_encrypt(plaintext)
        print(f"\nCiphertext: {ciphertext}")

    elif choice == "decrypt":
        ciphertext = input("Enter ciphertext: ")
        plaintext = rail_fence_decrypt(ciphertext)
        print(f"\nPlaintext: {plaintext}")

    else:
        print("Invalid choice. Please type 'encrypt' or 'decrypt'.")

if __name__ == "__main__":
    main()
