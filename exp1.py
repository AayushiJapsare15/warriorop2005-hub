import numpy as np

# ---------------- Caesar Cipher ----------------
def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)


# ---------------- Playfair Cipher ----------------
def generate_playfair_matrix(key):
    key = key.upper().replace("J", "I")
    matrix = []

    for char in key:
        if char not in matrix and char.isalpha():
            matrix.append(char)

    for char in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if char not in matrix:
            matrix.append(char)

    return [matrix[i:i+5] for i in range(0, 25, 5)]


def process_playfair_text(text):
    text = text.upper().replace("J", "I")
    processed = []
    i = 0

    while i < len(text):
        a = text[i]
        if not a.isalpha():
            i += 1
            continue

        if i + 1 < len(text) and text[i+1].isalpha():
            b = text[i+1]
            if a == b:
                b = "X"
                i += 1
            else:
                i += 2
        else:
            b = "X"
            i += 1

        processed.append((a, b))
    return processed


def playfair_encrypt(text, key):
    matrix = generate_playfair_matrix(key)
    pos = {matrix[r][c]: (r, c) for r in range(5) for c in range(5)}
    pairs = process_playfair_text(text)
    result = ""

    for a, b in pairs:
        r1, c1 = pos[a]
        r2, c2 = pos[b]

        if r1 == r2:  # Same row
            result += matrix[r1][(c1+1)%5] + matrix[r2][(c2+1)%5]
        elif c1 == c2:  # Same column
            result += matrix[(r1+1)%5][c1] + matrix[(r2+1)%5][c2]
        else:  # Rectangle swap
            result += matrix[r1][c2] + matrix[r2][c1]
    return result


def playfair_decrypt(text, key):
    matrix = generate_playfair_matrix(key)
    pos = {matrix[r][c]: (r, c) for r in range(5) for c in range(5)}
    result = ""

    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]
        r1, c1 = pos[a]
        r2, c2 = pos[b]

        if r1 == r2:  # Same row
            result += matrix[r1][(c1-1)%5] + matrix[r2][(c2-1)%5]
        elif c1 == c2:  # Same column
            result += matrix[(r1-1)%5][c1] + matrix[(r2-1)%5][c2]
        else:  # Rectangle swap
            result += matrix[r1][c2] + matrix[r2][c1]
    return result


# ---------------- Hill Cipher ----------------
def mod_inverse_matrix(matrix, mod=26):
    det = int(round(np.linalg.det(matrix))) % mod
    det_inv = pow(det, -1, mod)

    n = len(matrix)
    adjugate = np.zeros((n, n), dtype=int)

    for i in range(n):
        for j in range(n):
            minor = np.delete(np.delete(matrix, i, axis=0), j, axis=1)
            cofactor = ((-1) ** (i + j)) * int(round(np.linalg.det(minor)))
            adjugate[j][i] = cofactor % mod

    return (det_inv * adjugate) % mod


def text_to_numbers(text):
    return [ord(c) - ord('A') for c in text.upper() if c.isalpha()]


def numbers_to_text(nums):
    return ''.join(chr(n % 26 + ord('A')) for n in nums)


def hill_encrypt(text, key_matrix):
    text_nums = text_to_numbers(text)

    while len(text_nums) % len(key_matrix) != 0:
        text_nums.append(ord('X') - ord('A'))

    result = []
    for i in range(0, len(text_nums), len(key_matrix)):
        block = np.array(text_nums[i:i+len(key_matrix)])
        enc_block = np.dot(key_matrix, block) % 26
        result.extend(enc_block)

    return numbers_to_text(result)


def hill_decrypt(text, key_matrix):
    inv_matrix = mod_inverse_matrix(key_matrix)
    text_nums = text_to_numbers(text)
    result = []

    for i in range(0, len(text_nums), len(key_matrix)):
        block = np.array(text_nums[i:i+len(key_matrix)])
        dec_block = np.dot(inv_matrix, block) % 26
        result.extend(dec_block)

    return numbers_to_text(result)


# ---------------- Menu ----------------
def main():
    while True:
        print("\n=== Substitution Techniques Menu ===")
        print("1. Caesar Cipher")
        print("2. Playfair Cipher")
        print("3. Hill Cipher")
        print("4. Quit")

        choice = input("Enter choice: ")

        if choice == '1':
            text = input("Enter text: ")
            shift = int(input("Enter shift value: "))
            encrypted = caesar_encrypt(text, shift)
            decrypted = caesar_decrypt(encrypted, shift)
            print("Encrypted:", encrypted)
            print("Decrypted:", decrypted)

        elif choice == '2':
            text = input("Enter text: ")
            key = input("Enter key: ")
            encrypted = playfair_encrypt(text, key)
            decrypted = playfair_decrypt(encrypted, key)
            print("Encrypted:", encrypted)
            print("Decrypted:", decrypted)

        elif choice == '3':
            text = input("Enter text: ")
            size = int(input("Enter size of key matrix (2 or 3): "))
            print("Enter key matrix row by row:")

            key_matrix = []
            for _ in range(size):
                row = input().split()
                new_row = []
                for item in row:
                    if item.isalpha():
                        new_row.append(ord(item.upper()) - ord('A'))
                    else:
                        new_row.append(int(item))
                key_matrix.append(new_row)

            key_matrix = np.array(key_matrix)

            encrypted = hill_encrypt(text, key_matrix)
            decrypted = hill_decrypt(encrypted, key_matrix)
            print("Encrypted:", encrypted)
            print("Decrypted:", decrypted)

        elif choice == '4':
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
