from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from Crypto.Cipher import AES
from Crypto import Random
import pickle
import io

def encrypt(filename, password, pd):
    backend = default_backend()
    salt = Random.new().read(AES.block_size)
    salt_iv = Random.new().read(AES.block_size)
    key_derivation = PBKDF2HMAC(
        algorithm = hashes.SHA256(),
        length = 32,
        salt = salt,
        iterations = 150000,
        backend = backend)
    iv_derivation = PBKDF2HMAC(
        algorithm = hashes.SHA256(),
        length = AES.block_size,
        salt = salt_iv,
        iterations = 100000,
        backend = backend)
    key = key_derivation.derive(password.encode())
    iv = iv_derivation.derive(password.encode())
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    with open(filename, 'wb') as f:
        pd_bytes = io.BytesIO(pickle.dumps(pd, pickle.HIGHEST_PROTOCOL))
        f.write(salt + salt_iv)
        finished = False
        
        while not finished:
            data = pd_bytes.read(1024 * AES.block_size)
            if len(data) == 0 or len(data) % AES.block_size != 0:
                pad_length = AES.block_size - (len(data) % AES.block_size)
                data += (chr(pad_length) * pad_length).encode()
                finished = True
            f.write(cipher.encrypt(data))

def decrypt(filename, password):
    backend = default_backend()
    data = b''
    
    with open(filename, 'rb') as f:
        salt = f.read(AES.block_size)
        salt_iv = f.read(AES.block_size)
        key_derivation = PBKDF2HMAC(
            algorithm = hashes.SHA256(),
            length = 32,
            salt = salt,
            iterations = 150000,
            backend = backend)
        iv_derivation = PBKDF2HMAC(
            algorithm = hashes.SHA256(),
            length = AES.block_size,
            salt = salt_iv,
            iterations = 100000,
            backend = backend)
        key = key_derivation.derive(password.encode())
        iv = iv_derivation.derive(password.encode())
        cipher = AES.new(key, AES.MODE_CBC, iv)
        finished = False
        
        while not finished:
            next = cipher.decrypt(f.read(1024 * AES.block_size))
            data += next
            if len(next) == 0:
                finished = True
                
        try:
            pd = pickle.loads(data)
        except pickle.UnpicklingError:
            raise ValueError
        
        return pd
    