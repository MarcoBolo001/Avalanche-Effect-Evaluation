import timeit
from ciphers import transposition_cipher, vigenere_cipher, vigenere_cipher_ascii, transposition_cipher_ascii, caesar_cipher
from Cbc import encrypt_cbc



# Flips olny one bit, keeping the alphabet between 'a' and 'z'
def flip_last_valid_bit(text):
    def flip_bit(char, bit_position):
        ascii_val = ord(char)
        flipped_val = ascii_val ^ (1 << bit_position)
        return chr(flipped_val)

    for i, char in enumerate(text):
        if char.isalpha():  # Check if the character is a letter

            if 'A' <= char <= 'Z':
                for bit_position in range(0, 7):  # Flipping only the lower bits
                    flipped_char = flip_bit(char, bit_position)
                    if 'A' <= flipped_char <= 'Z':
                        return text[:i] + flipped_char + text[i + 1:]
            elif 'a' <= char <= 'z':
                for bit_position in range(0, 7):  # Flipping only the lower bits
                    flipped_char = flip_bit(char, bit_position)
                    if 'a' <= flipped_char <= 'z':
                        return text[:i] + flipped_char + text[i + 1:]


def character_difference_percentage(text1, text2):
    # Assicurati che le stringhe abbiano la stessa lunghezza
    if len(text1) != len(text2):
        raise ValueError("Le stringhe devono avere la stessa lunghezza per il confronto.")

    # Conta i caratteri differenti
    differing_chars = sum(1 for a, b in zip(text1, text2) if a != b)
    print(f"char diversi: {differing_chars}")
    print(text1)
    print(text2)
    # Calcola la differenza percentuale
    percentage_difference = (differing_chars / len(text1)) * 100

    return percentage_difference


def bit_difference_percentage(text1, text2):
    if len(text1) != len(text2):
        raise ValueError("Strings must be of equal length.")

    # Converti i testi in rappresentazioni binarie
    bin_text1 = ''.join(format(ord(c), '08b') for c in text1)
    bin_text2 = ''.join(format(ord(c), '08b') for c in text2)

    # Calcola il numero di bit diversi
    differing_bits = sum(b1 != b2 for b1, b2 in zip(bin_text1, bin_text2))

    # Calcola il numero totale di bit
    total_bits = len(bin_text1)
    print(f"Bit diversi: {differing_bits}")
    # Calcola la percentuale di bit diversi
    percentage_difference = (differing_bits / total_bits) * 100
    return percentage_difference


def initial_avalanche_effect(plain_text, transposition_key, vigenere_key):
    # Encrypt the original plaintext
    #original_ciphertext = vigenere_cipher(transposition_cipher(plain_text, transposition_key), vigenere_key)
    original_ciphertext = transposition_cipher(vigenere_cipher(plain_text, vigenere_key), transposition_key)
    # change the first character
    modified_text = flip_last_valid_bit(plain_text)

    # Encrypt the modified plaintext
    #modified_ciphertext = vigenere_cipher(transposition_cipher(modified_text, transposition_key), vigenere_key)
    modified_ciphertext = transposition_cipher(vigenere_cipher(modified_text, vigenere_key), transposition_key)

    # Calculate the percentage of differing characters
    diff_char_percentage = character_difference_percentage(original_ciphertext, modified_ciphertext)
    diff_bit_percentage = bit_difference_percentage(original_ciphertext, modified_ciphertext)
    return original_ciphertext, modified_ciphertext, diff_char_percentage, diff_bit_percentage


def repeated_avalanche_effect(plain_text, transposition_key, vigenere_key, rounds):
    # Change the first character
    modified_text = flip_last_valid_bit(plain_text)

    avalanche_effects_char = []
    avalanche_effects_bit = []
    computation_times = []

    current_text = plain_text
    modified_current_text = modified_text

    previous_time = 0

    for i in range(rounds):
        start_time = timeit.default_timer()  # Start the timer
        #encrypted_text = vigenere_cipher(transposition_cipher(current_text, transposition_key), vigenere_key)
        encrypted_text = transposition_cipher(vigenere_cipher(current_text,vigenere_key), transposition_key)
        end_time = timeit.default_timer()  # Stop the timer after the encryption

        #encrypted_modified_text = vigenere_cipher(transposition_cipher(modified_current_text, transposition_key),vigenere_key)
        encrypted_modified_text = transposition_cipher(vigenere_cipher(modified_current_text,vigenere_key), transposition_key)
        # Calculate the avalanche effect by comparing the modified ciphertext with the original
        diff_char_percentage = character_difference_percentage(encrypted_text, encrypted_modified_text)

        avalanche_effects_char.append(diff_char_percentage)

        diff_bit_percentage = bit_difference_percentage(encrypted_text, encrypted_modified_text)
        avalanche_effects_bit.append(diff_bit_percentage)
        # Update the text for the next round of encryption
        current_text = encrypted_text
        modified_current_text = encrypted_modified_text

        computation_times.append(end_time - start_time + previous_time)
        previous_time += end_time - start_time

    return avalanche_effects_char, avalanche_effects_bit, computation_times


def repeated_avalanche_effect_all_ascii(plain_text, transposition_key, vigenere_key, rounds):
    # Change the first character
    modified_text = flip_last_valid_bit(plain_text)

    avalanche_effects_bit = []
    avalanche_effects_char = []
    computation_times = []

    current_text = plain_text
    modified_current_text = modified_text

    previous_time = 0

    for i in range(rounds):
        start_time = timeit.default_timer()  # Start the timer
        encrypted_text = vigenere_cipher_ascii(transposition_cipher_ascii(current_text, transposition_key),
                                               vigenere_key)
        end_time = timeit.default_timer()  # Stop the timer after the encryption

        encrypted_modified_text = vigenere_cipher_ascii(
            transposition_cipher_ascii(modified_current_text, transposition_key),
            vigenere_key)

        diff_bit_percentage = bit_difference_percentage(encrypted_text, encrypted_modified_text)
        avalanche_effects_bit.append(diff_bit_percentage)

        diff_char_percentage = character_difference_percentage(encrypted_text, encrypted_modified_text)
        avalanche_effects_char.append(diff_char_percentage)
        # Update the text for the next round of encryption
        current_text = encrypted_text
        modified_current_text = encrypted_modified_text

        computation_times.append(end_time - start_time + previous_time)
        previous_time += end_time - start_time

    return avalanche_effects_char, avalanche_effects_bit, computation_times


def repeated_avalanche_effect_CBC(plain_text, transposition_key, vigenere_key, rounds):
    # Change the first character
    modified_text = flip_last_valid_bit(plain_text)

    avalanche_effects_bit = []
    avalanche_effects_char = []
    computation_times = []

    current_text = plain_text
    modified_current_text = modified_text

    previous_time = 0

    for i in range(rounds):
        start_time = timeit.default_timer()  # Start the timer
        encrypted_text = encrypt_cbc(current_text, transposition_key, vigenere_key)
        end_time = timeit.default_timer()  # Stop the timer after the encryption

        encrypted_modified_text = encrypt_cbc(modified_current_text, transposition_key, vigenere_key)

        diff_bit_percentage = bit_difference_percentage(encrypted_text, encrypted_modified_text)
        avalanche_effects_bit.append(diff_bit_percentage)

        diff_char_percentage = character_difference_percentage(encrypted_text, encrypted_modified_text)
        avalanche_effects_char.append(diff_char_percentage)
        # Update the text for the next round of encryption
        current_text = encrypted_text
        modified_current_text = encrypted_modified_text

        computation_times.append(end_time - start_time + previous_time)
        previous_time += end_time - start_time

    return avalanche_effects_char, avalanche_effects_bit, computation_times


def repeated_avalanche_effect_caesar(plain_text, transposition_key, caesar_shift, rounds):
    # Change the first character
    modified_text = flip_last_valid_bit(plain_text)

    avalanche_effects_bit = []
    avalanche_effects_char = []
    computation_times = []

    current_text = plain_text
    modified_current_text = modified_text

    previous_time = 0

    for i in range(rounds):
        start_time = timeit.default_timer()  # Start the timer
        encrypted_text = caesar_cipher(transposition_cipher(current_text, transposition_key),
                                               caesar_shift)
        end_time = timeit.default_timer()  # Stop the timer after the encryption

        encrypted_modified_text = caesar_cipher(transposition_cipher(modified_current_text, transposition_key),
                                               caesar_shift)

        diff_bit_percentage = bit_difference_percentage(encrypted_text, encrypted_modified_text)
        avalanche_effects_bit.append(diff_bit_percentage)

        diff_char_percentage = character_difference_percentage(encrypted_text, encrypted_modified_text)
        avalanche_effects_char.append(diff_char_percentage)
        # Update the text for the next round of encryption
        current_text = encrypted_text
        modified_current_text = encrypted_modified_text

        computation_times.append(end_time - start_time + previous_time)
        previous_time += end_time - start_time

    return avalanche_effects_char, avalanche_effects_bit, computation_times