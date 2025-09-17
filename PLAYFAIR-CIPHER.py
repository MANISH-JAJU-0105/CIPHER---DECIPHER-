import string
import random

ALPHABET = string.ascii_lowercase.replace('j', '')  # 'a'..'z' excluding 'j'


def generate_key_table_from_keyword(key):
    """Create 5x5 key table from a keyword (preserve order, i/j treated same)."""
    k = ''.join(ch for ch in key.lower() if ch.isalpha())
    k = k.replace('j', 'i')
    seen = []
    for ch in k:
        if ch not in seen and ch in ALPHABET:
            seen.append(ch)
    for ch in ALPHABET:
        if ch not in seen:
            seen.append(ch)
    table = [seen[i:i+5] for i in range(0, 25, 5)]
    return table


def generate_random_key_table():
    letters = list(ALPHABET)
    random.shuffle(letters)
    table = [letters[i:i+5] for i in range(0, 25, 5)]
    return table


def table_to_key_string(table):
    return ''.join(ch for row in table for ch in row)


def print_key_table(table):
    for row in table:
        print(' '.join(row))
    print()


def find_position(table, ch):
    if ch == 'j':
        ch = 'i'
    for r in range(5):
        for c in range(5):
            if table[r][c] == ch:
                return r, c
    raise ValueError(f"Character {ch} not in key table")


def make_digraphs(text):
    """Prepare plaintext by removing non-alpha, replacing j->i,
    inserting 'x' between duplicate letters in a digraph, and padding with 'z'."""
    s = ''.join(ch for ch in text.lower() if ch.isalpha())
    s = s.replace('j', 'i')
    digraphs = []
    i = 0
    while i < len(s):
        a = s[i]
        b = s[i+1] if i+1 < len(s) else ''
        if b == '':
            # last single char -> pad with 'z'
            digraphs.append(a + 'z')
            i += 1
        elif a == b:
            # duplicate pair -> insert filler 'x' after first char
            digraphs.append(a + 'x')
            i += 1
        else:
            digraphs.append(a + b)
            i += 2
    return digraphs


def encrypt_pair(a, b, table):
    r1, c1 = find_position(table, a)
    r2, c2 = find_position(table, b)
    if r1 == r2:  # same row -> shift right
        return table[r1][(c1 + 1) % 5], table[r2][(c2 + 1) % 5]
    if c1 == c2:  # same column -> shift down
        return table[(r1 + 1) % 5][c1], table[(r2 + 1) % 5][c2]
    # rectangle
    return table[r1][c2], table[r2][c1]


def decrypt_pair(a, b, table):
    r1, c1 = find_position(table, a)
    r2, c2 = find_position(table, b)
    if r1 == r2:  # same row -> shift left
        return table[r1][(c1 - 1) % 5], table[r2][(c2 - 1) % 5]
    if c1 == c2:  # same column -> shift up
        return table[(r1 - 1) % 5][c1], table[(r2 - 1) % 5][c2]
    # rectangle
    return table[r1][c2], table[r2][c1]


def playfair_encrypt(plaintext, key_table):
    digraphs = make_digraphs(plaintext)
    cipher = []
    for pair in digraphs:
        c1, c2 = encrypt_pair(pair[0], pair[1], key_table)
        cipher.append(c1)
        cipher.append(c2)
    return ''.join(cipher)


def playfair_decrypt(ciphertext, key_table):
    s = ''.join(ch for ch in ciphertext.lower() if ch.isalpha())
    if len(s) % 2 != 0:
        # pad if oddly-length ciphertext (shouldn't normally happen)
        s += 'z'
    plain = []
    for i in range(0, len(s), 2):
        p1, p2 = decrypt_pair(s[i], s[i+1], key_table)
        plain.append(p1)
        plain.append(p2)
    return ''.join(plain)


def clean_decrypted_text(pt):
    """Attempt to remove filler 'x' between duplicated letters and trailing 'z' padding.
    This is heuristic — it may remove legitimate 'x' or 'z' in rare cases."""
    lst = list(pt)
    i = 1
    while i < len(lst) - 1:
        if lst[i] == 'x' and lst[i-1] == lst[i+1]:
            del lst[i]
        else:
            i += 1
    # remove trailing padding 'z' if present
    if lst and lst[-1] == 'z':
        lst.pop()
    return ''.join(lst)


def main():
    print("Playfair Cipher (i/j treated same).")
    mode = input("Choose mode (encrypt/decrypt): ").strip().lower()

    if mode == 'encrypt':
        plaintext = input("Enter plaintext: ")
        key_input = input("Enter key (leave blank to generate random key): ").strip()
        if key_input == '':
            key_table = generate_random_key_table()
            key_string = table_to_key_string(key_table)
            print("\nGenerated key table:")
            print_key_table(key_table)
            print(f"Key (flattened): {key_string}\n")
        else:
            key_table = generate_key_table_from_keyword(key_input)
            print("\nKey table from keyword:")
            print_key_table(key_table)
            print(f"Key (flattened): {table_to_key_string(key_table)}\n")

        ciphertext = playfair_encrypt(plaintext, key_table)
        print(f"Ciphertext: {ciphertext}")

    elif mode == 'decrypt':
        ciphertext = input("Enter ciphertext (letters only or with spaces): ")
        key_input = input("Enter key/keyword: ").strip()
        if key_input == '':
            print("Error: decryption requires a key/keyword.")
            return
        key_table = generate_key_table_from_keyword(key_input)
        print("\nKey table built from keyword:")
        print_key_table(key_table)
        print(f"Key (flattened): {table_to_key_string(key_table)}\n")

        raw_plain = playfair_decrypt(ciphertext, key_table)
        cleaned = clean_decrypted_text(raw_plain)
        print(f"Raw decrypted (letters-only): {raw_plain}")
        print(f"Cleaned decrypted (attempt to remove fillers): {cleaned}")

    else:
        print("Invalid choice. Type 'encrypt' or 'decrypt'.")


if __name__ == '__main__':
    main()
