import secrets
import hashlib
import sys
import textwrap
from typing import Tuple


# ---------- Primality Testing (Miller–Rabin) ----------

def _miller_rabin_witness(a: int, d: int, n: int, r: int) -> bool:
    """Single Miller–Rabin witness test; returns True if 'a' shows n is composite."""
    x = pow(a, d, n)
    if x == 1 or x == n - 1:
        return False
    for _ in range(r - 1):
        x = (x * x) % n
        if x == n - 1:
            return False
    return True  # composite


def is_probable_prime(n: int, rounds: int = 32) -> bool:
    """Probabilistic primality test using Miller–Rabin."""
    if n < 2:
        return False

    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    for p in small_primes:
        if n % p == 0:
            return n == p

    # Write n-1 as 2^r * d with d odd
    d = n - 1
    r = 0
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(rounds):
        a = secrets.randbelow(n - 3) + 2  # random in [2, n-2]
        if _miller_rabin_witness(a, d, n, r):
            return False
    return True


def gen_prime(bits: int) -> int:
    """Generate a probable prime of given bit-length."""
    while True:
        candidate = secrets.randbits(bits) | (1 << (bits - 1)) | 1  # set MSB & make odd
        if is_probable_prime(candidate):
            return candidate


def gen_safe_prime(bits: int) -> Tuple[int, int]:
    """
    Generate a safe prime p and corresponding q where:
    p = 2q + 1 and both p, q are prime.
    """
    while True:
        q = gen_prime(bits - 1)
        p = 2 * q + 1
        if is_probable_prime(p):
            return p, q


def gen_subgroup_generator(p: int, q: int) -> int:
    """
    Generate a generator g of the order-q subgroup modulo p.
    """
    while True:
        h = secrets.randbelow(p - 3) + 2  # random in [2, p-2]
        g = pow(h, 2, p)                  # square to force subgroup membership
        if g != 1 and pow(g, q, p) == 1:
            return g


# ---------- RFC 3526 Group 14 (predefined 2048-bit MODP group) ----------

RFC3526_GROUP14_P_HEX = """
FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E08
8A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B
302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9
A63A3620FFFFFFFFFFFFFFFF
""".replace("\n", "").replace(" ", "")


def get_rfc3526_group14() -> Tuple[int, int]:
    """Return (p, g) for RFC 3526 Group 14 (2048-bit MODP)."""
    p = int(RFC3526_GROUP14_P_HEX, 16)
    g = 2
    return p, g


# ---------- KDF & Simple XOR Stream Encryption Demo ----------

def kdf_sha256_from_K(K: int) -> bytes:
    """Derive 256-bit key from shared secret K using SHA-256."""
    K_bytes = K.to_bytes((K.bit_length() + 7) // 8, "big")
    return hashlib.sha256(K_bytes).digest()


def xor_stream_encrypt(key32: bytes, data: bytes, nonce: bytes) -> bytes:
    """
    Simple XOR stream “cipher”:
    keystream = SHA256(key || nonce || counter)
    NOT secure for real use, only for lab demo.
    """
    out = bytearray()
    counter = 0
    offset = 0

    while offset < len(data):
        ctr_bytes = counter.to_bytes(8, "big")
        block_key = hashlib.sha256(key32 + nonce + ctr_bytes).digest()
        block = data[offset: offset + len(block_key)]
        out.extend(bytes(a ^ b for a, b in zip(block, block_key[:len(block)])))

        offset += len(block)
        counter += 1

    return bytes(out)


# ---------- State Container for DH Session ----------

class DHState:
    def __init__(self):
        self.p = None
        self.g = None

        self.a = None  # Alice private
        self.b = None  # Bob private
        self.A = None  # Alice public
        self.B = None  # Bob public

        self.KA = None  # Alice shared secret
        self.KB = None  # Bob shared secret

        self.derived_key = None  # KDF output


# ---------- Operations ----------

def op_select_params(state: DHState):
    print("\n[1] Select / Generate Public Parameters (p, g)")
    print(" 1) Use standard 2048-bit MODP group (RFC 3526 Group 14)")
    print(" 2) Generate a demo safe prime (~512-bit)")

    choice = input("Choose [1/2]: ").strip()

    if choice == "1":
        state.p, state.g = get_rfc3526_group14()
        print("\nSelected RFC 3526 Group 14 (2048-bit).")
    elif choice == "2":
        print("\nGenerating a ~512-bit safe prime p = 2q+1 and subgroup generator g ...")
        p, q = gen_safe_prime(512)
        g = gen_subgroup_generator(p, q)
        state.p, state.g = p, g
        print("Generated safe prime p (~512 bits) and generator g.")
    else:
        print("Invalid choice.")
        return

    print("\nPublic parameters:")
    print(f"p = {state.p}")
    print(f"g = {state.g}")
    print(f"Bitlength(p) = {state.p.bit_length()} bits")


def op_generate_keys(state: DHState):
    if state.p is None or state.g is None:
        print("Set (p, g) first (menu option 1).")
        return

    # Private exponents a, b in [2, p-2]
    state.a = secrets.randbelow(state.p - 3) + 2
    state.b = secrets.randbelow(state.p - 3) + 2

    # Public values
    state.A = pow(state.g, state.a, state.p)
    state.B = pow(state.g, state.b, state.p)

    print("\n[2] Generated keys for Alice and Bob.")
    show_priv = input("Show private exponents? [y/N]: ").strip().lower()
    if show_priv == "y":
        print(f"Alice private a = {state.a}")
        print(f"Bob   private b = {state.b}")

    print(f"Alice public A = {state.A}")
    print(f"Bob   public B = {state.B}")


def op_compute_shared(state: DHState):
    if state.A is None or state.B is None:
        print("Generate keys first (menu option 2).")
        return

    state.KA = pow(state.B, state.a, state.p)  # Alice computes
    state.KB = pow(state.A, state.b, state.p)  # Bob computes

    print("\n[3] Computed shared secrets.")
    print(f"K_A = {state.KA}")
    print(f"K_B = {state.KB}")
    print("Verification:", "Equal" if state.KA == state.KB else "Mismatch!")


def op_derive_and_demo(state: DHState):
    if state.KA is None:
        print("Compute shared secret first (menu option 3).")
        return

    key = kdf_sha256_from_K(state.KA)
    state.derived_key = key

    print("\n[4] Derived symmetric key (SHA-256):")
    print(key.hex())

    msg = input("Enter plaintext: ").encode()
    nonce = secrets.token_bytes(12)

    ct = xor_stream_encrypt(key, msg, nonce)
    print("\n--- Encryption Demo ---")
    print(f"Nonce      : {nonce.hex()}")
    print(f"Ciphertext : {ct.hex()}")

    pt = xor_stream_encrypt(key, ct, nonce)
    print(f"Recovered  : {pt.decode(errors='replace')}")


# ---------- Menu & Main ----------

def banner():
    print("\n" + "=" * 80)
    print("Experiment No. 4 - Implement Diffie-Hellman Key Exchange Algorithm")
    print("=" * 80)
    print(textwrap.dedent("""
        Menu:
        1) Select / Generate Public Parameters (p, g)
        2) Generate Keys for Alice and Bob
        3) Compute Shared Secret
        4) Derive Symmetric Key & Demo Encrypt/Decrypt
        0) Exit
    """).strip())
    print("=" * 80)


def main():
    state = DHState()

    while True:
        banner()
        choice = input("Enter choice: ").strip()

        if choice == "1":
            op_select_params(state)
        elif choice == "2":
            op_generate_keys(state)
        elif choice == "3":
            op_compute_shared(state)
        elif choice == "4":
            op_derive_and_demo(state)
        elif choice == "0":
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.")
        sys.exit(0)
