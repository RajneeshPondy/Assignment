"""
The Atbash cipher is an encryption method in which each letter of a word is replaced with its
"mirror" letter in the alphabet: A <=> Z; B <=> Y; C <=> X; etc.
"""

import string
import unittest
import csv



def cipher_encryption(sentence):

    upper_cipher = {k:v for k, v in zip(string.ascii_uppercase, string.ascii_uppercase[::-1])}
    lower_cipher = {k:v for k, v in zip(string.ascii_lowercase, string.ascii_lowercase[::-1])}

    list_sentence = list(sentence)
    
    for index, char in enumerate(sentence):
        if char.islower():
            list_sentence[index] = lower_cipher[char]
        elif char.isupper():
            list_sentence[index] = upper_cipher[char]
        
    return "".join(list_sentence)


class TestAtbashCipher(unittest.TestCase):
    def test_cipher_encryption(self):
        """Will succeed"""
        with open('data.csv', "rt", encoding='ascii') as infile:
            read = csv.reader(infile)
            for row in read :
                input = row[0].strip()
                output = row[1].strip()
                self.assertEqual(cipher_encryption(input),output)

if __name__ == "__main__":
    unittest.main()