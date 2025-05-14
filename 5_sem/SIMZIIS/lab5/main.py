from Crypto.Util.number import getStrongPrime


FERMAT_NUMBERS = [65537, 257, 17]


def read_file(filename):
    with open(filename, 'r') as f:
        data = f.read()
    f.close()
    return data


def write_file(filename, message):
    with open(filename, "w") as f:
        f.write(message)
    f.close()


def exponentiation(x, degree, p):
    result = x
    bit_degree = bin(degree)[3:]
    for i in bit_degree:
        result = ((result ** 2) * x) % p\
            if i == '1'\
            else (result ** 2) % p
    return result


def multiplicative_reciprocal(e, e_func):
    x, old_x, y, old_y = 0, 1, 1, 0
    r, old_r = e_func, e
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_x, x = x, old_x - q * x
        old_y, y = y, old_y - q * y
    return old_x % e_func


def create_keys():
    p = getStrongPrime(1024)
    q = getStrongPrime(1024)
    while p == q:
        q = getStrongPrime(1024)
    n = p * q
    e_func = (p - 1) * (q - 1)
    e = 0
    for number in FERMAT_NUMBERS:
        if e_func % number != 0:
            e = number
            break
    d = multiplicative_reciprocal(e, e_func)
    write_file("open_key.txt", f"{n},{e}")
    write_file("secret_key.txt", f"{n},{d}")


def message_encryption():
    message = int(read_file("orig_mes.txt"))
    n, e = read_file("open_key.txt").split(",")
    c = exponentiation(int(message), int(e), int(n))
    write_file("encr_mes.txt", f"{c}")


def message_decryption():
    c = int(read_file("encr_mes.txt"))
    n, d = read_file("secret_key.txt").split(",")
    write_file("decr_mes.txt",
               f"{str(exponentiation(int(c), int(d), int(n)))}")


def signature_encryption():
    m = int(read_file("orig_mes.txt"))
    n, d = read_file("secret_key.txt").split(",")
    s = exponentiation(int(m), int(d), int(n))
    write_file("signature.txt", f"{s}")
    return s, m


def signature_decryption():
    s, m = signature_encryption()
    n, e = read_file("open_key.txt").split(",")
    m2 = exponentiation(int(s), int(e), int(n))
    if m2 == m:
        print("\nЭЦП соответствует")
    else:
        print("\nЭЦП не соответствует")


create_keys()
message_encryption()
message_decryption()
signature_decryption()
