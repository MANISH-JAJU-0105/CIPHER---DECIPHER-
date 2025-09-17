def check(x, y):
    """Return how many padding characters are needed so x is divisible by y."""
    if x % y == 0:
        return 0
    a = x // y
    b = y * (a + 1)
    return b - x

def build_order(key):
    """Build order array from key list (1-based ranks).
    Example: key = [3,1,2] -> order = [1,2,0]
    order[i] = index of column that has rank (i+1).
    """
    l1 = len(key)
    # validate key is a permutation of 1..l1
    if set(key) != set(range(1, l1 + 1)):
        raise ValueError("Key must be a permutation of 1..len(key). Example: [3,1,2]")
    order = [0] * l1
    for rank in range(1, l1 + 1):
        for idx in range(l1):
            if key[idx] == rank:
                order[rank - 1] = idx
                break
    return order

def encrypt(plaintext, key, depth=1, pad_char='X'):
    """Columnar transposition encryption (multi-depth).
    plaintext: string (spaces removed)
    key: list of ints (permutation of 1..len(key))
    depth: number of times to apply the transposition
    """
    l1 = len(key)
    # remove spaces and convert to uppercase
    cleaned = ''.join(plaintext.split()).upper()
    l2 = len(cleaned)

    pad = check(l2, l1)
    padded = cleaned + pad_char * pad
    r = (l2 + pad) // l1

    order = build_order(key)

    p = list(padded)
    for _ in range(depth):
        # fill rows
        rows = [p[i:i + l1] for i in range(0, len(p), l1)]
        # read out columns in order of ranks
        new_p = []
        for rank_idx in range(l1):
            col = order[rank_idx]
            for row in rows:
                new_p.append(row[col])
        p = new_p

    return ''.join(p)

def decrypt(ciphertext, key, depth=1, remove_padding=True, pad_char='X'):
    """Reverse columnar transposition encryption.
    ciphertext: string (letters, no spaces required)
    key: list of ints (permutation of 1..len(key))
    depth: how many times encryption was applied
    remove_padding: if True, strip trailing pad_char characters
    """
    l1 = len(key)
    s = ''.join(ciphertext.split()).upper()
    l2 = len(s)
    if l2 % l1 != 0:
        raise ValueError("Ciphertext length must be a multiple of key length.")

    r = l2 // l1
    order = build_order(key)

    p = list(s)
    for _ in range(depth):
        # reconstruct rows by filling columns in the same order encryption used
        rows = [[''] * l1 for _ in range(r)]
        count = 0
        for rank_idx in range(l1):
            col = order[rank_idx]
            for row_idx in range(r):
                rows[row_idx][col] = p[count]
                count += 1
        # flatten row-wise to get the intermediate text
        p = [ch for row in rows for ch in row]

    result = ''.join(p)
    if remove_padding:
        # strip trailing pad_char characters (only at the end)
        result = result.rstrip(pad_char)
    return result

def interactive():
    print("Columnar Transposition (multi-depth).")
    mode = input("Choose mode (encrypt/decrypt): ").strip().lower()

    if mode == 'encrypt':
        plaintext = input("Enter plaintext: ")
        key = list(map(int, input("Enter key sequence (e.g. 3 1 2): ").split()))
        depth = int(input("Enter depth (>=1): "))
        ct = encrypt(plaintext, key, depth=depth)
        print("\nKey:", key)
        print("Depth:", depth)
        print("Ciphertext:", ct)

    elif mode == 'decrypt':
        ciphertext = input("Enter ciphertext: ")
        key = list(map(int, input("Enter key sequence (e.g. 3 1 2): ").split()))
        depth = int(input("Enter depth (>=1): "))
        pt = decrypt(ciphertext, key, depth=depth)
        print("\nKey:", key)
        print("Depth:", depth)
        print("Plaintext:", pt)

    else:
        print("Invalid choice. Type 'encrypt' or 'decrypt'.")

if __name__ == '__main__':
    interactive()
