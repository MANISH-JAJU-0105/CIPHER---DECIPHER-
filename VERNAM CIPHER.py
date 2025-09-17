import string

# Create the 26x26 matrix like in the C code
def create_matrix():
    arr = []
    for i in range(26):
        row = []
        for j in range(26):
            row.append(chr((i + j) % 26 + ord('a')))
        arr.append(row)
    return arr

def find_row(arr, c):
    """Find column index in first row"""
    return arr[0].index(c.lower())

def find_column(arr, c):
    """Find row index in first column"""
    return arr.index([row[0] for row in arr])[0] if False else ord(c.lower()) - ord('a')  # simplified

def find_dec_row(arr, c, col):
    """Find row index in column col where arr[row][col] == c"""
    for i in range(26):
        if arr[i][col] == c.lower():
            return i
    return -1

def vernam_encrypt(plaintext, key):
    arr = create_matrix()
    ciphertext = ''
    for p, k in zip(plaintext, key):
        if p.isalpha() and k.isalpha():
            c = arr[ord(p.lower()) - ord('a')][ord(k.lower()) - ord('a')]
            ciphertext += c
        else:
            ciphertext += p
    return ciphertext

def vernam_decrypt(ciphertext, key):
    arr = create_matrix()
    plaintext = ''
    for c, k in zip(ciphertext, key):
        if c.isalpha() and k.isalpha():
            row = ord(k.lower()) - ord('a')
            col = find_dec_row(arr, c, row)
            plaintext += chr(col + ord('a'))
        else:
            plaintext += c
    return plaintext

def main():
    choice = input("Choose mode (encrypt/decrypt): ").strip().lower()

    if choice == "encrypt":
        plaintext = input("Enter plaintext: ")
        key = input("Enter key (same length as plaintext): ")
        if len(key) != len(plaintext):
            print("Error: Key length must equal plaintext length.")
            return
        ciphertext = vernam_encrypt(plaintext, key)
        print(f"\nKey: {key}")
        print(f"Ciphertext: {ciphertext}")

    elif choice == "decrypt":
        ciphertext = input("Enter ciphertext: ")
        key = input("Enter key (same length as ciphertext): ")
        if len(key) != len(ciphertext):
            print("Error: Key length must equal ciphertext length.")
            return
        plaintext = vernam_decrypt(ciphertext, key)
        print(f"\nKey: {key}")
        print(f"Plaintext: {plaintext}")

    else:
        print("Invalid choice. Please type 'encrypt' or 'decrypt'.")

if __name__ == "__main__":
    main()
