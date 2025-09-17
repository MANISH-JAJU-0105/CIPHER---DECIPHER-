import numpy as np
import random

# Convert letters to numbers (a=0..z=25)
def text_to_numbers(text):
    return [ord(ch) - ord('a') for ch in text.lower() if ch.isalpha()]

# Convert numbers back to text
def numbers_to_text(nums):
    return ''.join(chr(int(round(num)) % 26 + ord('a')) for num in nums)

# Generate a random invertible 3x3 key matrix modulo 26
def generate_key_matrix():
    while True:
        key = np.random.randint(0, 26, size=(3, 3))
        det = int(round(np.linalg.det(key)))
        if np.gcd(det, 26) == 1:  # determinant must be coprime with 26
            return key

# Encryption: C = K * P mod 26
def hill_encrypt(plaintext, key):
    nums = text_to_numbers(plaintext)
    if len(nums) % 3 != 0:
        # pad with 'x'
        nums += [ord('x') - ord('a')] * (3 - len(nums) % 3)

    ciphertext = []
    for i in range(0, len(nums), 3):
        block = np.array(nums[i:i+3]).reshape(3, 1)
        enc_block = np.dot(key, block) % 26
        ciphertext.extend(enc_block.flatten())
    return numbers_to_text(ciphertext)

# Decryption: P = K^-1 * C mod 26
def hill_decrypt(ciphertext, key):
    nums = text_to_numbers(ciphertext)
    if len(nums) % 3 != 0:
        raise ValueError("Ciphertext length must be a multiple of 3.")

    det = int(round(np.linalg.det(key)))
    det_inv = pow(det % 26, -1, 26)  # modular inverse of determinant

    # adjugate (classical adjoint) * det_inv mod 26
    key_inv = (
        det_inv * np.round(det * np.linalg.inv(key)).astype(int)
    ) % 26

    plaintext = []
    for i in range(0, len(nums), 3):
        block = np.array(nums[i:i+3]).reshape(3, 1)
        dec_block = np.dot(key_inv, block) % 26
        plaintext.extend(dec_block.flatten())
    return numbers_to_text(plaintext)

def main():
    choice = input("Choose mode (encrypt/decrypt): ").strip().lower()

    if choice == "encrypt":
        plaintext = input("Enter plaintext: ")
        key = generate_key_matrix()
        ciphertext = hill_encrypt(plaintext, key)
        print("\nGenerated Key matrix:\n", key)
        print("Ciphertext:", ciphertext)

    elif choice == "decrypt":
        ciphertext = input("Enter ciphertext: ")
        print("Enter the 3x3 key matrix (row by row, 9 integers):")
        key = []
        for i in range(3):
            row = list(map(int, input(f"Row {i+1}: ").split()))
            key.append(row)
        key = np.array(key)

        plaintext = hill_decrypt(ciphertext, key)
        print("\nKey matrix:\n", key)
        print("Plaintext:", plaintext)

    else:
        print("Invalid choice. Please type 'encrypt' or 'decrypt'.")

if __name__ == "__main__":
    main()
