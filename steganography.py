"""LSB image steganography: hide and reveal text in RGB images."""

import base64
from PIL import Image

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

DELIMITER = "#####"
DELIMITER_BYTES = b"#####"
_SALT = b"stego_salt_v1"


def _derive_key(password: str) -> bytes:
    """Derive a 32-byte key from password for Fernet."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=_SALT,
        iterations=480000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))


def _encrypt(plaintext: str, password: str) -> bytes:
    """Encrypt plaintext with password; returns ciphertext bytes."""
    key = _derive_key(password)
    f = Fernet(key)
    return f.encrypt(plaintext.encode("utf-8"))


def _decrypt(ciphertext: bytes, password: str) -> str:
    """Decrypt ciphertext with password; returns plaintext string."""
    key = _derive_key(password)
    f = Fernet(key)
    return f.decrypt(ciphertext).decode("utf-8")


def message_to_binary(data):
    """Convert text, bytes, or int to binary string."""
    if isinstance(data, str):
        return "".join(format(ord(ch), "08b") for ch in data)
    elif isinstance(data, (bytes, bytearray)):
        return "".join(format(byte, "08b") for byte in data)
    elif isinstance(data, int):
        return format(data, "08b")
    else:
        raise TypeError("Unsupported type for binary conversion")


def hide_data(image_path, secret_msg, output_path=None, password=None):
    """Hide secret message inside image using LSB. If password is set, message is encrypted before hiding. Returns PIL Image if output_path is None, else output_path."""
    if password:
        payload = _encrypt(secret_msg, password) + DELIMITER_BYTES
        binary_msg = message_to_binary(payload)
    else:
        secret_msg += DELIMITER
        binary_msg = message_to_binary(secret_msg)
    data_len = len(binary_msg)

    img = Image.open(image_path)
    if img.mode != "RGB":
        img = img.convert("RGB")

    data_index = 0
    pixels = list(img.getdata())
    new_pixels = []

    for pixel in pixels:
        r, g, b = pixel
        if data_index < data_len:
            r = (r & ~1) | int(binary_msg[data_index])
            data_index += 1
        if data_index < data_len:
            g = (g & ~1) | int(binary_msg[data_index])
            data_index += 1
        if data_index < data_len:
            b = (b & ~1) | int(binary_msg[data_index])
            data_index += 1
        new_pixels.append((r, g, b))

    img.putdata(new_pixels)

    if output_path:
        img.save(output_path)
        return output_path
    return img


def show_data(image_path, password=None):
    """Decode and retrieve hidden message from stego image. If password is set, payload is decrypted (must match the password used when encoding)."""
    img = Image.open(image_path)
    binary_data = ""
    for pixel in list(img.getdata()):
        r, g, b = pixel
        binary_data += str(r & 1)
        binary_data += str(g & 1)
        binary_data += str(b & 1)

    all_bytes = [binary_data[i : i + 8] for i in range(0, len(binary_data), 8)]
    payload_bytes = _extract_payload_bytes(all_bytes)
    if payload_bytes is None:
        return ""  # delimiter not found

    if password:
        try:
            return _decrypt(payload_bytes, password)
        except Exception:
            raise ValueError("Decryption failed. Wrong password or image was not encoded with a password.")
    return payload_bytes.decode("latin-1")


def _extract_payload_bytes(byte_list):
    """From list of 8-bit binary strings, build bytes and return payload before delimiter b'#####'."""
    raw = bytes(int(b, 2) for b in byte_list)
    idx = raw.find(DELIMITER_BYTES)
    if idx == -1:
        return None
    return raw[:idx]
