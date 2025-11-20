import random
from math import gcd

# -------------------------------------------------
#           PRIME UTILITIES (MILLER–RABIN)
# -------------------------------------------------
def is_prime(n: int, k: int = 5) -> bool:
    """Probabilistic Miller–Rabin primality test."""
    if n <= 3:
        return n == 2 or n == 3
    if n % 2 == 0:
        return False

    # Write n - 1 as 2^r * d with d odd
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Witness loop
    for _ in range(k):
        a = random.randrange(2, n - 2)
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_prime(bit_length: int) -> int:
    """Generate a probable prime of given bit length."""
    while True:
        # random odd number with MSB and LSB set
        num = random.getrandbits(bit_length)
        num |= (1 << (bit_length - 1)) | 1
        if is_prime(num):
            return num


# -------------------------------------------------
#        RSA KEY GENERATION & UTILITIES
# -------------------------------------------------
def mod_inverse(e: int, phi: int) -> int:
    """Return d such that d * e ≡ 1 (mod phi) using Extended Euclid."""
    old_r, r = e, phi
    old_s, s = 1, 0  # old_s corresponds to coefficient of e

    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s

    # old_r is gcd(e, phi); we assume gcd(e, phi) == 1
    d = old_s % phi
    return d


def generate_keys(bit_length: int):
    """Generate RSA public and private keys."""
    p = generate_prime(bit_length)
    q = generate_prime(bit_length)
    while p == q:
        q = generate_prime(bit_length)

    n = p * q
    phi = (p - 1) * (q - 1)

    # Choose e
    e = 65537
    if gcd(e, phi) != 1:
        e = 3
        while gcd(e, phi) != 1:
            e += 2

    d = mod_inverse(e, phi)

    print("\n🔐 RSA Keys Generated Successfully:")
    print("Public Key (e, n):")
    print(f"  e = {e}")
    print(f"  n = {n}")
    print("Private Key (d, n):")
    print(f"  d = {d}")
    print(f"  n = {n}")

    return e, d, n


# -------------------------------------------------
#        ENCRYPTION & DECRYPTION
# -------------------------------------------------
def encrypt_message(message: str, e: int, n: int) -> int:
    """Encrypt a UTF-8 string using public key (e, n)."""
    m = int.from_bytes(message.encode("utf-8"), byteorder="big")
    if m >= n:
        raise ValueError("Message too long for the current key size.")
    c = pow(m, e, n)
    print("\n🔒 Encrypted Ciphertext:\n", c)
    return c


def decrypt_message(ciphertext: int, d: int, n: int) -> str:
    """Decrypt integer ciphertext using private key (d, n)."""
    m = pow(ciphertext, d, n)
    # Convert back to bytes/string
    byte_len = (m.bit_length() + 7) // 8
    message_bytes = m.to_bytes(byte_len, byteorder="big")
    plaintext = message_bytes.decode("utf-8")
    print("\n🔓 Decrypted Message:\n", plaintext)
    return plaintext


# -------------------------------------------------
#                    MENU SYSTEM
# -------------------------------------------------
def menu():
    e = d = n = None

    while True:
        print("\n====== RSA Cryptosystem Menu ======")
        print("1) Generate RSA Keys")
        print("2) Encrypt Message")
        print("3) Decrypt Message")
        print("4) Quit")

        choice = input("Select an option (1-4): ").strip()

        if choice == "1":
            try:
                bit_length = int(
                    input("Enter bit length for prime numbers (e.g. 512): ")
                )
                e, d, n = generate_keys(bit_length)
            except ValueError:
                print("Invalid bit length. Please enter an integer.")

        elif choice == "2":
            if e is None or n is None:
                print("Please generate keys first (option 1).")
                continue

            plaintext = input("Enter message to encrypt: ")
            try:
                encrypt_message(plaintext, e, n)
            except Exception as err:
                print(f"Error: {err}")

        elif choice == "3":
            if d is None or n is None:
                print("Please generate keys first (option 1).")
                continue

            try:
                ciphertext_str = input("Enter ciphertext (number): ").strip()
                ciphertext = int(ciphertext_str)
                decrypt_message(ciphertext, d, n)
            except ValueError:
                print("Ciphertext must be an integer number.")
            except Exception as err:
                print(f"Error: {err}")

        elif choice == "4":
            print("Exiting RSA Program.")
            break
        else:
            print("Invalid choice. Please enter 1–4.")


# -------------------------------------------------
#                    ENTRY POINT
# -------------------------------------------------
if __name__ == "__main__":
    menu()
