import math

def is_prime(n):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.isqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def simple_sieve(limit):
    primes = []
    mark = [True] * (limit + 1)
    for num in range(2, limit + 1):
        if mark[num]:
            primes.append(num)
            for multiple in range(num * num, limit + 1, num):
                mark[multiple] = False
    return primes


def segmented_sieve(l, r):
    limit = int(math.isqrt(r)) + 1
    base_primes = simple_sieve(limit)
    mark = [True] * (r - l + 1)
    for p in base_primes:
        start = max(p * p, (l + p - 1) // p * p)
        for j in range(start, r + 1, p):
            mark[j - l] = False
    return [i + l for i in range(r - l + 1) if mark[i] and (i + l) > 1]

if __name__ == "__main__":
    print("1. FIND PRIME NUMBER")
    print("2. RANGE")
    choice = input("CHOOSE: ")

    if choice == "1":
        n = int(input("INPUT NUMBER : "))
        print("YES" if is_prime(n) else "NO")

    elif choice == "2":
        start, end = map(int, input("RANGE START TO END: ").split())
        primes = segmented_sieve(start, end)
        print("PRIME NUMBERS:", *primes)
        print("COUNT:", len(primes))