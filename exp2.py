import math

# -------------------------------------------------------------
#                       RAIL FENCE CIPHER
# -------------------------------------------------------------
class RailFenceCipher:
    """Implementation of Rail Fence Cipher with encryption and decryption"""

    @staticmethod
    def encrypt(plaintext, rails):
        if rails == 1:
            return plaintext

        text = plaintext.replace(' ', '').upper()
        rail_matrix = [['\n' for _ in range(len(text))] for _ in range(rails)]

        direction_down = False
        row = 0

        for col in range(len(text)):
            if row == 0 or row == rails - 1:
                direction_down = not direction_down

            rail_matrix[row][col] = text[col]

            row = row + 1 if direction_down else row - 1

        ciphertext = ""
        for i in range(rails):
            for j in range(len(text)):
                if rail_matrix[i][j] != '\n':
                    ciphertext += rail_matrix[i][j]

        return ciphertext

    @staticmethod
    def decrypt(ciphertext, rails):
        if rails == 1:
            return ciphertext

        rail_matrix = [['\n' for _ in range(len(ciphertext))] for _ in range(rails)]

        direction_down = None
        row = 0

        for col in range(len(ciphertext)):
            if row == 0:
                direction_down = True
            if row == rails - 1:
                direction_down = False

            rail_matrix[row][col] = '*'
            row = row + 1 if direction_down else row - 1

        index = 0
        for i in range(rails):
            for j in range(len(ciphertext)):
                if rail_matrix[i][j] == '*' and index < len(ciphertext):
                    rail_matrix[i][j] = ciphertext[index]
                    index += 1

        plaintext = ""
        direction_down = None
        row = 0

        for col in range(len(ciphertext)):
            if row == 0:
                direction_down = True
            if row == rails - 1:
                direction_down = False

            plaintext += rail_matrix[row][col]
            row = row + 1 if direction_down else row - 1

        return plaintext


# -------------------------------------------------------------
#            COLUMNAR TRANSPOSITION CIPHER
# -------------------------------------------------------------
class ColumnarTranspositionCipher:
    def __init__(self, key):
        self.key = key.upper()
        self.key_order = self._get_key_order()

    def _get_key_order(self):
        indexed_key = [(char, i) for i, char in enumerate(self.key)]
        sorted_key = sorted(indexed_key)
        order = [0] * len(self.key)

        for new_pos, (char, old_pos) in enumerate(sorted_key):
            order[old_pos] = new_pos

        return order

    def encrypt(self, plaintext):
        text = plaintext.replace(' ', '').upper()

        cols = len(self.key)
        rows = math.ceil(len(text) / cols)
        padded_text = text + 'X' * (rows * cols - len(text))

        matrix = []
        for i in range(rows):
            row = []
            for j in range(cols):
                row.append(padded_text[i * cols + j])
            matrix.append(row)

        ciphertext = ""
        for order_pos in range(cols):
            col_index = self.key_order.index(order_pos)
            for row in range(rows):
                ciphertext += matrix[row][col_index]

        return ciphertext

    def decrypt(self, ciphertext):
        cols = len(self.key)
        rows = len(ciphertext) // cols

        matrix = [['' for _ in range(cols)] for _ in range(rows)]

        index = 0
        for order_pos in range(cols):
            col_index = self.key_order.index(order_pos)
            for row in range(rows):
                matrix[row][col_index] = ciphertext[index]
                index += 1

        plaintext = ""
        for row in range(rows):
            for col in range(cols):
                plaintext += matrix[row][col]

        return plaintext.rstrip('X')


# -------------------------------------------------------------
#            DOUBLE TRANSPOSITION CIPHER
# -------------------------------------------------------------
class DoubleTranspositionCipher:
    def __init__(self, key1, key2):
        self.cipher1 = ColumnarTranspositionCipher(key1)
        self.cipher2 = ColumnarTranspositionCipher(key2)

    def encrypt(self, plaintext):
        step1 = self.cipher1.encrypt(plaintext)
        return self.cipher2.encrypt(step1)

    def decrypt(self, ciphertext):
        step1 = self.cipher2.decrypt(ciphertext)
        return self.cipher1.decrypt(step1)


# -------------------------------------------------------------
#                        MENU SYSTEM
# -------------------------------------------------------------
def display_menu():
    print("\n" + "=" * 65)
    print("   CRYPTOGRAPHY LAB - TRANSPOSITION CIPHER IMPLEMENTATION")
    print("=" * 65)
    print("1. Rail Fence Cipher")
    print("2. Columnar Transposition Cipher")
    print("3. Double Transposition Cipher")
    print("4. Quit")
    print("=" * 65)


def rail_fence_menu():
    print("\n--- Rail Fence Cipher ---")
    try:
        rails = int(input("Enter number of rails (2 or more): "))
        if rails < 2:
            print("Rails must be 2 or more.")
            return

        plaintext = input("Enter plaintext: ")

        encrypted = RailFenceCipher.encrypt(plaintext, rails)
        decrypted = RailFenceCipher.decrypt(encrypted, rails)

        print(f"\nOriginal Text: {plaintext}")
        print(f"Encrypted: {encrypted}")
        print(f"Decrypted: {decrypted}")

    except ValueError:
        print("Invalid rails number!")


def columnar_transposition_menu():
    print("\n--- Columnar Transposition Cipher ---")
    key = input("Enter keyword: ").strip()

    if not key.isalpha():
        print("Key must be alphabets only.")
        return

    plaintext = input("Enter plaintext: ")

    cipher = ColumnarTranspositionCipher(key)
    encrypted = cipher.encrypt(plaintext)
    decrypted = cipher.decrypt(encrypted)

    print(f"\nOriginal Text: {plaintext}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")


def double_transposition_menu():
    print("\n--- Double Transposition Cipher ---")
    key1 = input("Enter first key: ").strip()
    key2 = input("Enter second key: ").strip()

    if not key1.isalpha() or not key2.isalpha():
        print("Keys must contain alphabets only.")
        return

    plaintext = input("Enter plaintext: ")

    cipher = DoubleTranspositionCipher(key1, key2)
    encrypted = cipher.encrypt(plaintext)
    decrypted = cipher.decrypt(encrypted)

    print(f"\nOriginal Text: {plaintext}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")


def main():
    print("Welcome to Cryptography Lab - Experiment 02!")

    while True:
        display_menu()
        choice = input("Enter choice (1–4): ").strip()

        if choice == '1':
            rail_fence_menu()
        elif choice == '2':
            columnar_transposition_menu()
        elif choice == '3':
            double_transposition_menu()
        elif choice == '4':
            print("\nThank you! Exiting program.")
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
