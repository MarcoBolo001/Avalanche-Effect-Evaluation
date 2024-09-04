from ciphers import transposition_cipher_ascii, vigenere_cipher_ascii, vigenere_decipher_ascii, transposition_decipher_ascii

def xor_blocks(block1, block2):
    return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(block1, block2))



def encrypt_cbc(message, transpose_key, vigenere_key):
    block_size = 2*len(transpose_key)
    padded_message = message.ljust((len(message) + block_size - 1) // block_size * block_size)
    blocks = [padded_message[i:i + block_size] for i in range(0, len(padded_message), block_size)]

    previous_block = '\x00' * block_size  # initial padding block for CBC
    encrypted_blocks = []

    for block in blocks:
        transposed_block = transposition_cipher_ascii(block, transpose_key)
        vigenere_block = vigenere_cipher_ascii(transposed_block, vigenere_key)
        encrypted_block = xor_blocks(vigenere_block, previous_block)
        encrypted_blocks.append(encrypted_block)
        previous_block = encrypted_block

    return ''.join(encrypted_blocks)


def decrypt_cbc(encrypted_message, transpose_key, vigenere_key):
    block_size = 2 * len(transpose_key)
    blocks = [encrypted_message[i:i + block_size] for i in range(0, len(encrypted_message), block_size)]

    previous_block = '\x00' * block_size  # initial padding block for CBC
    decrypted_blocks = []

    for block in blocks:
        vigenere_block = xor_blocks(block, previous_block)
        transposed_block = vigenere_decipher_ascii(vigenere_block, vigenere_key)
        decrypted_block = transposition_decipher_ascii(transposed_block, transpose_key)
        decrypted_blocks.append(decrypted_block)
        previous_block = block

    decrypted_message = ''.join(decrypted_blocks)
    return decrypted_message.rstrip()  # Remove any padding