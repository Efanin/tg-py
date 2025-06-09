from stegano import exifHeader
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

async def ImgWrite(password, message, path):
    password = password.encode()
    message = message.encode('utf-8')
    salt = b'+,\x8aJ\xb3x\x95{\xbb\x98\x01\x19\xad9i\xb9'#os.urandom(16)
    iv = b'\xf8@\xac]\x10\x0c\xa3\x1e\xa6\x9d1I\xee\xcb\xe5('#os.urandom(16)
    # 2. Генерация ключа из пароля (PBKDF2)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # 256-битный ключ для AES-256
        salt=salt,
        iterations=100000,  # чем больше, тем безопаснее (но медленнее)
        backend=default_backend()
    )
    key = kdf.derive(password)  # ключ для AES

    # 3. Шифрование сообщения AES-256 (режим CBC)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Дополнение сообщения до кратного 16 байт (требуется для AES-CBC)
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(message) + padder.finalize()

    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    print("Зашифрованное сообщение (hex):", ciphertext.hex())
    await exifHeader.hide(path, path, ciphertext.hex())
