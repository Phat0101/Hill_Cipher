# Hill cipher Encryption and Decryption for 3x3 matrix
# Author: Patrick Nguyen
import copy
# Template for the cofactor matrix
co_factor_matrix_template = [[1, -1, 1], [-1, 1, -1], [1, -1, 1]]

# Convert alphabet characters to numerical values


def convert_alpha(matrix: list) -> list:
    m = copy.deepcopy(matrix)
    for i in range(3):
        for j in range(3):
            m[i][j] = ord(matrix[i][j]) - 65
    return m

# Convert a message to a 3x3 matrix, padding if necessary


def convert_message_to_matrix(message: str, padding: str) -> list:
    matrix = []
    i = 0
    while (i < len(message) / 3):
        matrix.append([])
        for j in range(3):
            if (i * 3 + j < len(message)):
                matrix[i].append(ord(message[i * 3 + j]) - 65)
        i += 1
    if len(matrix[len(matrix) - 1]) == 1:
        matrix[len(matrix) - 1].append(ord(padding) - 65)
        matrix[len(matrix) - 1].append(ord(padding) - 65)
    elif len(matrix[len(matrix) - 1]) == 2:
        matrix[len(matrix) - 1].append(ord(padding) - 65)
    return matrix

# Convert a numerical matrix back to a message


def convert_matrix_to_message(matrix: list, padding: str) -> str:
    message = ''
    for i in range(len(matrix)):
        message += chr(matrix[i] + 65)
    return message

# Multiply two matrices


def multiply_matrix_by_matrix(matrix1: list, matrix2: list) -> list:
    result = []
    for i in range(3):
        total = 0
        for j in range(3):
            total += matrix1[i][j] * matrix2[j]
        result.append(total % 26)
    return result

# Find the modular multiplicative inverse of a number


def find_modular_multiplicative_inverse(a: int) -> int:
    for x in range(1, 26, 2):  # Step 2 because even numbers do not have multiplicative inverse mod 26
        if ((a % 26 * x) % 26 == 1):
            return x
    return -1

# Find the determinant of a 3x3 matrix


def find_determinant_3_by_3(matrix: list) -> int:
    det = matrix[0][0] * (matrix[1][1] * matrix[2][2] -
                          matrix[2][1] * matrix[1][2])
    det = det - matrix[0][1] * (matrix[1][0] *
                                matrix[2][2] - matrix[2][0] * matrix[1][2])
    det = det + matrix[0][2] * (matrix[1][0] *
                                matrix[2][1] - matrix[2][0] * matrix[1][1])
    return det % 26

# Extract a 2x2 matrix from a 3x3 matrix


def find_2_by_2_matrix(row: int, col: int, matrix: list) -> list:
    small_matrix = [[], []]
    counter = 0
    for i in range(3):
        for j in range(3):
            if (i != row and j != col):
                small_matrix[int(counter / 2)].append(matrix[i][j])
                counter += 1
    return small_matrix

# Find the determinant of a 2x2 matrix


def find_determinant_2_by_2(matrix: list) -> int:
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

# Find the cofactor matrix of a 3x3 matrix


def find_cofactor_matrix(matrix: list) -> list:
    cofactor_matrix = []
    for i in range(3):
        cofactor_matrix.append([])
        for j in range(3):
            cofactor_matrix[i].append(find_determinant_2_by_2(
                find_2_by_2_matrix(i, j, matrix)) * co_factor_matrix_template[i][j])
    return cofactor_matrix

# Find the adjugate matrix of a matrix


def find_adjugate_matrix(matrix: list) -> list:
    # Transpose
    adjugate_matrix = copy.deepcopy(matrix)
    adjugate_matrix[0][1] = matrix[1][0]
    adjugate_matrix[0][2] = matrix[2][0]
    adjugate_matrix[1][0] = matrix[0][1]
    adjugate_matrix[1][2] = matrix[2][1]
    adjugate_matrix[2][0] = matrix[0][2]
    adjugate_matrix[2][1] = matrix[1][2]

    # Mod 26
    for i in range(3):
        for j in range(3):
            adjugate_matrix[i][j] = adjugate_matrix[i][j] % 26
    return adjugate_matrix

# Find the inverse of the key matrix


def find_inverse_matrix(matrix: list, inverse_determinant: list) -> list:
    # Multiply the Multiplicative Inverse of the Determinant by the Adjugate Matrix
    result = copy.deepcopy(matrix)
    for i in range(3):
        for j in range(3):
            result[i][j] = (result[i][j] * inverse_determinant) % 26
    return result

# Hill cipher encryption


def Encryption(key_matrix: list, plain_text: str, padding: str) -> str:
    key = convert_alpha(key_matrix)
    plain_text_matrix = convert_message_to_matrix(plain_text, padding)
    encrypted_text = ""
    for each in plain_text_matrix:
        encrypted_text += convert_matrix_to_message(
            multiply_matrix_by_matrix(key, each), padding)
    return encrypted_text

# Hill cipher decryption


def Decryption(key_matrix: list, cipher_text: str, padding: str) -> str:
    key_matrix = convert_alpha(key_matrix)
    determinant = find_determinant_3_by_3(key_matrix)
    if determinant == 0:
        return "Invalid Key Cannot Decrypt!"
    inverse_determinant = find_modular_multiplicative_inverse(determinant)
    if inverse_determinant == -1:
        return "Invalid Key Cannot Decrypt!"

    cipher_text_matrix = convert_message_to_matrix(cipher_text, "")
    inverse_key = find_inverse_matrix(find_adjugate_matrix(
        find_cofactor_matrix(key_matrix)), inverse_determinant)
    decrypted_text = ""
    for each in cipher_text_matrix:
        decrypted_text += convert_matrix_to_message(
            multiply_matrix_by_matrix(inverse_key, each), "")
    if decrypted_text[-1] == padding:
        decrypted_text = decrypted_text[:-1]
    if decrypted_text[-1] == padding:
        decrypted_text = decrypted_text[:-1]
    return decrypted_text


key = [["A", "L", "P"], ["H", "A", "B"], ["E", "T", "A"]]

text = input("Enter Text: ")
padding = input("Enter Padding (choose padding other than plain text): ")
eord = input("E for Encryption, D for Decryption: ")
if eord == "E":
    print("Encrypted text: ", Encryption(key, text, padding))
else:
    print("Decrypted text: ", Decryption(key, text, padding))
