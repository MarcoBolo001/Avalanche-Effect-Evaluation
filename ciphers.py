import string


def caesar_cipher(text, shift):
    text = text.lower()  # Text to lowercase
    text = text.replace(' ', '')  # Remove spaces
    result = ''
    for char in text:
        if char.isalpha():
            shift_base = ord('a')
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            result += char
    return result


def vigenere_cipher(text, key):
    alphabet = string.ascii_lowercase
    text = text.lower()  # Text to lowercase
    text = text.replace(' ', '')  # Remove spaces
    key = key.lower()

    key_extended = (key + text)[:len(text)]  # Vigenere autokey generation

    ciphertext = []

    for i in range(len(text)):
        if text[i] in alphabet:
            shift = alphabet.index(key_extended[i])
            shifted_index = (alphabet.index(text[i]) + shift) % 26
            ciphertext.append(alphabet[shifted_index])
        else:
            ciphertext.append(text[i])  # if character is not in the alphabet, append it as it is

    return ''.join(ciphertext)

def vigenere_decipher(ciphertext, key):
    alphabet = string.ascii_lowercase
    ciphertext = ciphertext.lower()
    key = key.lower()

    plaintext = []

    for i in range(len(ciphertext)):
        if ciphertext[i] in alphabet:
            shift = alphabet.index(key[i])
            shifted_index = (alphabet.index(ciphertext[i]) - shift) % 26
            plain_char = alphabet[shifted_index]
            plaintext.append(plain_char)
            key += plain_char  # Add the decrypted character to the key
        else:
            plaintext.append(ciphertext[i])  # Add non-alphabet characters to the plaintext
            key += ciphertext[i]  # Add non-alphabet characters to the key

    return ''.join(plaintext)

def vigenere_cipher_ascii(text, key):
    key_extended = (key + text)[:len(text)]
    ciphertext = []

    for i in range(len(text)):
        char = text[i]
        shift = ord(key_extended[i])
        shifted_index = (ord(char) + shift) % 256
        ciphertext.append(chr(shifted_index))

    return ''.join(ciphertext)

def vigenere_decipher_ascii(ciphertext, key):
    key_extended = key  # Initialize the key with the original key
    plaintext = []

    for i in range(len(ciphertext)):
        char = ciphertext[i]
        shift = ord(key_extended[i])
        shifted_index = (ord(char) - shift) % 256
        decrypted_char = chr(shifted_index)
        plaintext.append(decrypted_char)
        key_extended += decrypted_char  # Add the decrypted character to the key

    return ''.join(plaintext)



def transposition_cipher(text, key):
    text = text.lower()  # Text to lowercase
    text = text.replace(' ', '')  # Remove spaces

    matrix = []

    # Fills the matrix with the text in a row-wise manner, adding random characters at the end if necessary
    for i in range(0, len(text), len(key)):
        row = list(text[i:i + len(key)])
        if len(row) < len(key):
            row.extend('x' for _ in range(len(key) - len(row)))  # Fills the remaining characters with 'x'
                                                                # to better evaluate the avalanche effect

            # random characters is a better choice in real scenarios
            # row.extend(random.choice(string.ascii_lowercase) for _ in range(len(key) - len(row)))
        matrix.append(row)

     # Transpose the matrix based on the key
    transposed_matrix = [''] * len(key)
    for i in range(len(key)):
        for row in matrix:
            transposed_matrix[int(key[i]) - 1] += row[i]

    ciphertext = ''.join(transposed_matrix)

    return ciphertext

def invert_key(key):
    inverted_key = [''] * len(key)
    for i, k in enumerate(key):   # create the inverted key for decryption
        inverted_key[int(k) - 1] = str(i + 1)
    return ''.join(inverted_key)

def transposition_decipher(ciphertext, key):
    num_rows = len(ciphertext) // len(key)
    num_cols = len(key)
    key = invert_key(key)
    matrix = [''] * num_cols
    index = 0

    # Fill the matrix with the columns of the ciphertext
    for i in range(len(key)):
        col_length = num_rows
        matrix[int(key[i]) - 1] = ciphertext[index:index + col_length]
        index += col_length

    # Reconstruct the plaintext by reading the columns in the order specified by the key
    plaintext = ''
    for i in range(num_rows):
        for j in range(num_cols):
            plaintext += matrix[j][i]

    return plaintext

def transposition_cipher_ascii(text, key):

    matrix = []

    # Fills the matrix with the text in a row-wise manner, adding random characters at the end if necessary
    for i in range(0, len(text), len(key)):
        row = list(text[i:i + len(key)])
        if len(row) < len(key):
            row.extend('x' for _ in range(len(key) - len(row)))  # Fills the remaining characters with 'x'
                                                                # to better evaluate the avalanche effect

            # random characters is a better choice in real scenarios
            # row.extend(random.choice(string.ascii_lowercase) for _ in range(len(key) - len(row)))
        matrix.append(row)

    # Transpose the matrix based on the key
    transposed_matrix = [''] * len(key)
    for i in range(len(key)):
        for row in matrix:
            transposed_matrix[int(key[i]) - 1] += row[i]

    ciphertext = ''.join(transposed_matrix)

    return ciphertext


def transposition_decipher_ascii(ciphertext, key):
    num_rows = len(ciphertext) // len(key)
    key = invert_key(key)
    matrix = [''] * num_rows
    index = 0
    for i in range(len(key)):
        col_len = num_rows
        for j in range(col_len):
            matrix[j] += ciphertext[index]
            index += 1

    plaintext = [''] * len(ciphertext)
    for i, char in enumerate(key):
        col_index = int(char) - 1
        for j in range(num_rows):
            plaintext[col_index + j * len(key)] = matrix[j][i]

    return ''.join(plaintext).rstrip('x')  # Remove any padding
