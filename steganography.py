"""LSB image steganography: hide and reveal text in RGB images."""

from PIL import Image

DELIMITER = "#####"


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


def hide_data(image_path, secret_msg, output_path=None):
    """Hide secret message inside image using LSB. Returns PIL Image if output_path is None, else output_path."""
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


def show_data(image_path):
    """Decode and retrieve hidden message from stego image."""
    img = Image.open(image_path)
    binary_data = ""
    for pixel in list(img.getdata()):
        r, g, b = pixel
        binary_data += str(r & 1)
        binary_data += str(g & 1)
        binary_data += str(b & 1)

    all_bytes = [binary_data[i : i + 8] for i in range(0, len(binary_data), 8)]
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data.endswith(DELIMITER):
            break
    return decoded_data[: -len(DELIMITER)]
