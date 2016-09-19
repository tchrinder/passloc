"""This module handles file encryption and decryption"""

import io
import pickle
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from Crypto.Cipher import AES
from Crypto import Random

def encrypt(filename, password, pd):
    """Encrypt credential dictionary to given file"""
    backend = default_backend()
    #generate salts
    salt = Random.new().read(AES.block_size)
    salt_iv = Random.new().read(AES.block_size)
    
    #initialize key and iv derivation functions
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
     
    #derive key and iv
    key = key_derivation.derive(password.encode())
    iv = iv_derivation.derive(password.encode())
    #initialize cipher
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    with open(filename, 'wb') as f:
        #convert dictionary object into byte stream
        pd_bytes = io.BytesIO(pickle.dumps(pd, pickle.HIGHEST_PROTOCOL))
        f.write(salt + salt_iv)
        finished = False
        
        while not finished:
            #encrypt byte stream in chunks
            data = pd_bytes.read(1024 * AES.block_size)
            if len(data) == 0 or len(data) % AES.block_size != 0:
                pad_length = AES.block_size - (len(data) % AES.block_size)
                data += (chr(pad_length) * pad_length).encode()
                finished = True
            f.write(cipher.encrypt(data))

def decrypt(filename, password):
    """Decrypt and return credential dictionary from a given file"""
    backend = default_backend()
    data = b''
    
    with open(filename, 'rb') as f:
        #read salts
        salt = f.read(AES.block_size)
        salt_iv = f.read(AES.block_size)
        
        #initialize derivation functions
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
            
        #derive key and iv
        key = key_derivation.derive(password.encode())
        iv = iv_derivation.derive(password.encode())
        #initialize cipher
        cipher = AES.new(key, AES.MODE_CBC, iv)
        finished = False
        
        while not finished:
            #decrypt in chunks
            next = cipher.decrypt(f.read(1024 * AES.block_size))
            data += next
            if len(next) == 0:
                finished = True
                
        #convert byte object into dictionary object
        try:
            pd = pickle.loads(data)
        except pickle.UnpicklingError:
            raise ValueError
        
        return pd