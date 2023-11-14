# Encryption Procedure:

## Key Matrix Conversion:
The encryption process begins with the conversion of the user-defined key matrix into numerical values. Each character in the matrix is mapped to its corresponding position in the alphabet.

## Plaintext Conversion:
The plaintext is converted into a list of blocks. If the length of the plaintext is not a multiple of 3, padding is added to ensure it can be processed in blocks of three.

## Matrix Multiplication:
The key matrix is multiplied with each block of the plaintext matrix using matrix multiplication modulo 26.

## Conversion to Ciphertext:
The resulting numerical matrix is converted back to ciphertext characters, forming the encrypted message.


# Decryption Procedure:

## Key Matrix Conversion:
Similar to encryption, the key matrix is converted into numerical values.

## Determinant Calculation:
The determinant of the key matrix is calculated. 
For a 3 x 3 matrix determinant is found by multiplying the top left entry by the determinant of the 2 x 2 matrix formed by the entries that are not in the same row or column as that entry. Similar steps are done with the other two elements in the top row, and the middle value is subtracted from the sum of the other two.
If the determinant is zero or lacks a modular multiplicative inverse mod 26, decryption is not possible.

## Inverse Matrix Computation:
The adjugate matrix and cofactor matrix are computed, and then the inverse matrix is found by multiplying the modular multiplicative inverse of the determinant with the adjugate matrix.

### Find cofactor matrix:
Calculate determinant of the 2 x 2 matrix for all entries in the original key matrix
Then times it with thec o_factor_matrix_template = [[1, -1, 1], [-1, 1, -1], [1, -1, 1]]

### Find adjugate matrix:
Transpose the cofactor matrix by reflecting the cofactor matrix along the line from top left ot bottom right.
Then mod 26

### Find inverse matrix:
Multiply the adjugate matrix with the inverse determinant 

## Ciphertext Conversion:
The ciphertext is converted into a numerical matrix.

## Matrix Multiplication:
The inverse key matrix is multiplied with each block of the ciphertext matrix using matrix multiplication modulo 26.

## Conversion to Plaintext:
The resulting numerical matrix is converted back to plaintext characters, forming the decrypted message.

# Testing:
## Example 1: 
Plain text: THEQUICKBROWNZEBRA
Key: [["H", "I", "A"], ["L", "A", "T"], ["P", "Z", "O"]]
Encrypted text: HZWMQUQPIXHDFLSNLY
Decrypted text: THEQUICKBROWNZEBRA

## Example 2:
Plain text: THEQUICKBROWNZEBRA
Key: [["H", "I", "B"], ["L", "A", "T"], ["P", "Z", "O"]]
Encrypted text: HZWMQUQPIXHDFLSNLY
Decrypted text: Invalid Key Cannot Decrypt! (determinant = 0)

## Example 3: 
Plain text: WEAAFERE
Padding: S
Key: [["A", "L", "P"], ["H", "A", "B"], ["E", "T", "A"]]
Encrypted text: SYILERCHO
Decrypted text: WEAAFERE