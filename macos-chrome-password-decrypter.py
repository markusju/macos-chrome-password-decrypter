import pbkdf2
import pyaes
import getpass

SALT = "saltysalt"
AES_BYTES = 16
AES_BITS = AES_BYTES * 8
IV = " " * AES_BYTES
ITERATIONS = 1003
DATA = None

print("Welcome to the Google Chrome Password Decrypter!")
print("This is a dialog-based program. We are intentionally not using command line arguments, so that sensitive information does not end up in your shell history.")
print("Please make sure to follow the provided instructions before proceeding.")
print()
res = input("Do you want to continue (y/n)? ")

if res not in ("y", "Y", "yes", "Yes"):
    exit(0)
print("Please provide the Google Chrome 'Safe Storage' encryption key (characters will not show).")

key = getpass.getpass("Enter Encryption Key: ")

if len(key) == 0:
    print("No encryption key provided. Exiting")
    exit(1)

print()

while True:
    print("Please provide the encrypted password as a hex string. String must be 19 bytes long.")
    print("Enter with or without spaces. For example: 'de ad be ef ...' or 'deadbeef ...'")
    encrypted_pw = input("Enter Hex Dump: ")
    DATA = bytes.fromhex(encrypted_pw)

    if len(DATA) != 19:
        print("The encrypted password is of incorrect length. Make sure you provide 19 Bytes!")
        print("Try again.")
        continue

    if DATA[:3] != b'v10':
        print("The encrypted password must begin with 76 31 30")
        print("Try again.")
        continue


    DATA = DATA[3:]

    secret_key = pbkdf2.PBKDF2(passphrase=key, salt=SALT, iterations=ITERATIONS).read(AES_BYTES)
    aes = pyaes.AESModeOfOperationCBC(secret_key, iv=IV)
    decrypted = aes.decrypt(DATA)

    try:
        print("Password: " + decrypted.decode("utf-8"))
    except UnicodeDecodeError:
        print("Decrypted Password could not be decoded. This usually means, you have very likely provided an incorrect encryption key. ")
    print()
    print("Press Ctrl+C to exit.")
    print()
