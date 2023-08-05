import json
import binascii
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from .config import PACKAGE_LENGTH, ENCODING


def get_message(client, key=None):
    """
    Получение сообщений из сокета.

    :param client: сокет
    :param key: AES ключ, если шифрование установлено
    :return: None
    """
    data = client.recv(PACKAGE_LENGTH)
    data = binascii.unhexlify(data)
    if data == b'':
        return None
    if isinstance(data, bytes):
        if key:
            session_key = key['session_key']
            iv = key['iv']
            decipher = AES.new(session_key, AES.MODE_CFB, iv=iv)
            data = decipher.decrypt(data)
        try:
            text = data.decode(ENCODING)
            if text == "":
                return None
            json_data = json.loads(text)
        except json.JSONDecodeError:
            return {"error_data": data}
        except UnicodeDecodeError:
            return {"error_data": data}
        if isinstance(json_data, dict):
            return json_data
        else:
            return None
    else:
        return None


def send_message(sock, data, key=None):
    """
    Отправка сообщений в сокет

    :param sock: сокет
    :param data: данные
    :param key: AES ключ, если шифрование установлено
    :return: None
    """
    message = json.dumps(data)
    enc_message = f'{message}\n'.encode(ENCODING)
    if key:
        session_key = key['session_key']
        iv = key['iv']
        cipher = AES.new(session_key, AES.MODE_CFB, iv=iv)
        enc_message = cipher.encrypt(enc_message)
    enc_message = binascii.hexlify(enc_message)
    sock.send(enc_message)


if __name__ == '__main__':
    data = b'Some simple text'
    session_key = get_random_bytes(32)
    cipher = AES.new(session_key, AES.MODE_CBC)
    iv = cipher.iv
    ciphertext = cipher.encrypt(pad(data, AES.block_size))
    session_key = binascii.hexlify(session_key).decode('ascii')
    iv = binascii.hexlify(cipher.iv).decode('ascii')
    key = {"session_key": session_key, "iv": iv}
    print(f'Key: {key}')
    print(key['session_key'].encode('ascii'))
    print(f'Data: {data}')
    print(f'Session key: {session_key}')
    print(f'Cipher: {cipher}')
    print(f'IV: {iv}')
    print(f'Cipher text: {ciphertext}')
    #
    decipher = AES.new(binascii.unhexlify(session_key), AES.MODE_CBC,
                       iv=binascii.unhexlify(iv))
    decrypt_data = unpad(decipher.decrypt(ciphertext), AES.block_size)
