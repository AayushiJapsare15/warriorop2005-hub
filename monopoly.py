import string

# ==============================
#  MONOALPHABETIC SUBSTITUTION
# ==============================

def build_mono_maps(key: str):
    """
    key: 26-letter permutation of A–Z (e.g. 'QWERTYUIOPASDFGHJKLZXCVBNM')
    Returns (enc_map, dec_map) for uppercase letters.
    """
    key = key.upper()
    assert len(key) == 26, "Key must be 26 letters."
    assert set(key) == set(string.ascii_uppercase), "Key must be a permutation of A–Z."

    enc_map = {plain: cipher for plain, cipher in zip(string.ascii_uppercase, key)}
    dec_map = {cipher: plain for plain, cipher in zip(string.ascii_uppercase, key)}
    return enc_map, dec_map


def mono_encrypt(plaintext: str, key: str) -> str:
    enc_map, _ = build_mono_maps(key)
    result = []

    for ch in plaintext:
        if ch.isalpha():
            is_upper = ch.isupper()
            c = ch.upper()
            mapped = enc_map[c]
            result.append(mapped if is_upper else mapped.lower())
        else:
            result.append(ch)
    return "".join(result)


def mono_decrypt(ciphertext: str, key: str) -> str:
    _, dec_map = build_mono_maps(key)
    result = []

    for ch in ciphertext:
        if ch.isalpha():
            is_upper = ch.isupper()
            c = ch.upper()
            mapped = dec_map[c]
            result.append(mapped if is_upper else mapped.lower())
        else:
            result.append(ch)
    return "".join(result)


# ==============================
#  POLYALPHABETIC (VIGENÈRE)
# ==============================

def _shift_char(ch: str, shift: int) -> str:
    """Shift one alphabetic character by 'shift' positions, preserve case."""
    if ch.isupper():
        base = ord('A')
        return chr((ord(ch) - base + shift) % 26 + base)
    elif ch.islower():
        base = ord('a')
        return chr((ord(ch) - base + shift) % 26 + base)
    else:
        return ch


def vigenere_encrypt(plaintext: str, key: str) -> str:
    key = "".join([k for k in key if k.isalpha()])  # remove non-letters
    if not key:
        raise ValueError("Key must contain at least one letter.")

    key = key.lower()
    key_len = len(key)
    result = []
    j = 0  # index in key (only advances on letters)

    for ch in plaintext:
        if ch.isalpha():
            k_shift = ord(key[j % key_len]) - ord('a')
            result.append(_shift_char(ch, k_shift))
            j += 1
        else:
            result.append(ch)
    return "".join(result)


def vigenere_decrypt(ciphertext: str, key: str) -> str:
    key = "".join([k for k in key if k.isalpha()])
    if not key:
        raise ValueError("Key must contain at least one letter.")

    key = key.lower()
    key_len = len(key)
    result = []
    j = 0

    for ch in ciphertext:
        if ch.isalpha():
            k_shift = ord(key[j % key_len]) - ord('a')
            result.append(_shift_char(ch, -k_shift))
            j += 1
        else:
            result.append(ch)
    return "".join(result)


# ==============================
#  SIMPLE MENU TO TEST
# ==============================

def main():
    while True:
        print("\n=== Classical Ciphers Menu ===")
        print("1) Monoalphabetic Substitution")
        print("2) Polyalphabetic (Vigenère)")
        print("3) Quit")

        choice = input("Enter choice (1–3): ").strip()

        if choice == "1":
            print("\n--- Monoalphabetic Substitution ---")
            text = input("Enter text: ")
            print("Enter 26-letter key (permutation of A–Z), e.g.")
            print("QWERTYUIOPASDFGHJKLZXCVBNM")
            key = input("Key: ").strip()

            try:
                enc = mono_encrypt(text, key)
                dec = mono_decrypt(enc, key)
                print("\nEncrypted:", enc)
                print("Decrypted:", dec)
            except AssertionError as e:
                print("Key error:", e)

        elif choice == "2":
            print("\n--- Vigenère Cipher (Polyalphabetic) ---")
            text = input("Enter text: ")
            key = input("Enter key (letters only recommended): ").strip()

            try:
                enc = vigenere_encrypt(text, key)
                dec = vigenere_decrypt(enc, key)
                print("\nEncrypted:", enc)
                print("Decrypted:", dec)
            except ValueError as e:
                print("Key error:", e)

        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()
