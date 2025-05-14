import pandas as pd
import time

alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЭЮЯ"
print(f"Алфавит без сдвига: `{alphabet}`")

def encrypt_alphabet(alphabet: str, shift: int) -> str:
    cipher_alphabet = ''
    for char in alphabet:
        shifted_index = (alphabet.index(char) + shift) % len(alphabet)
        cipher_char = alphabet[shifted_index]
        cipher_alphabet += cipher_char

    return cipher_alphabet

shift = int(input("Введите сдвиг (целое число от -33 до 33): "))
encrypted_alphabet = encrypt_alphabet(alphabet=alphabet, shift=shift)

print(f"Алфавит со сдвигом: `{encrypted_alphabet}`\n")


class CaesarEncryptor:

    def __init__(self, alphabet: str, alphabet_encrypter, shift: int) -> None:
        self._alphabet = alphabet
        self._encrypted_alphabet = alphabet_encrypter(alphabet, shift)

    def apply(self, string: str) -> str:
        string = string.upper()
        result = ""
        for char in string:
            if char in alphabet:
                result += self._encrypted_alphabet[self._alphabet.find(char)]
            else:
                result += char
        return result

key = CaesarEncryptor(alphabet=alphabet, alphabet_encrypter=encrypt_alphabet, shift=shift)

t1 = "Семеро одного не ждут"
t2 = "Поспешишь — людей насмешишь"
t3 = "Один в поле не воин"
e1 = key.apply(t1)
e2 = key.apply(t2)
e3 = key.apply(t3)

df = pd.DataFrame([
    [t1, e1], [t2, e2], [t3, e3]
], columns=["Оригинальный текст", "Зашифрованный текст"], index=None)
print('\n', df)

decryptor = CaesarEncryptor(alphabet=alphabet, alphabet_encrypter=encrypt_alphabet, shift=-shift)

start_time = time.time()
d1 = decryptor.apply(e1)
d2 = decryptor.apply(e2)
d3 = decryptor.apply(e3)
end_time = time.time()

df = pd.DataFrame([
    [e1, d1], [e2, d2], [e3, d3]
], columns=["Зашифрованный текст", "Расшифрованный текст"])

print('\n', df)

print(f'время взлома: {(end_time - start_time)}\n')

possible_original_texts = []

for shift in range(len(alphabet)):
    possible_decryptor = CaesarEncryptor(alphabet=alphabet, alphabet_encrypter=encrypt_alphabet, shift=shift)
    possible_original_texts.append([shift, possible_decryptor.apply(e1)])

df = pd.DataFrame(possible_original_texts, columns=["Сдвиг", "Текст"])
print('\n', df)


class BetterCaesarEncryptor:

    def __init__(self, alphabet: str, alphabet_encrypter, shift_supplier) -> None:
        self._alphabet = alphabet
        self._alphabet_encrypter = alphabet_encrypter
        self._shift_supplier = shift_supplier

    def apply(self, string: str) -> str:
        string = string.upper()
        result = ""
        for pos, char in enumerate(string):
            if char in alphabet:
                encrypted_alphabet = self._alphabet_encrypter(alphabet, self._shift_supplier(pos))
                result += encrypted_alphabet[self._alphabet.find(char)]
            else:
                result += char
        return result


def key_function(pos: int) -> int:
    return 39 * (pos ** 2) + 17 * pos - 518

encryptor = BetterCaesarEncryptor(
    alphabet=alphabet,
    alphabet_encrypter=encrypt_alphabet,
    shift_supplier=key_function
)

e1 = encryptor.apply(t1)
e2 = encryptor.apply(t2)
e3 = encryptor.apply(t3)

df = pd.DataFrame([
    [t1, e1], [t2, e2], [t3, e3]
], columns=["Оригинальный текст", "Зашифрованный текст"], index=None)
print('\n', df)

decryptor = BetterCaesarEncryptor(
    alphabet=alphabet,
    alphabet_encrypter=encrypt_alphabet,
    shift_supplier=lambda pos: -key_function(pos)
)

d1 = decryptor.apply(e1)
d2 = decryptor.apply(e2)
d3 = decryptor.apply(e3)

df = pd.DataFrame([
    [e1, d1], [e2, d2], [e3, d3]
], columns=["Зашифрованный текст", "Расшифровнный текст"], index=None)

print('\n', df)
