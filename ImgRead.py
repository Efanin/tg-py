from stegano import exifHeader
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def ImgRead(password):
    password = password.encode()
    salt = b'+,\x8aJ\xb3x\x95{\xbb\x98\x01\x19\xad9i\xb9'#os.urandom(16)
    iv = b'\xf8@\xac]\x10\x0c\xa3\x1e\xa6\x9d1I\xee\xcb\xe5('#os.urandom(16)
    ciphertext_hex = exifHeader.reveal("image2.jpg").decode()  # Например: "1a2b3c4d5e6f..."
    ciphertext = bytes.fromhex(ciphertext_hex)  # Конвертируем hex в байты

    # 3. Расшифровка
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()

    # Убираем PKCS7-дополнение
    unpadder = padding.PKCS7(128).unpadder()
    decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()
    print("Расшифрованное сообщение:", decrypted.decode())