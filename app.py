"""Streamlit frontend for LSB image steganography."""

import io
import tempfile
import streamlit as st
from PIL import Image

from steganography import hide_data, show_data

st.set_page_config(page_title="Image Steganography", page_icon="🖼️", layout="wide")
st.title("🖼️ Image Steganography")
st.caption("Hide or reveal text inside images using LSB encoding. Optional password encryption.")

with st.expander("ℹ️ How it works"):
    st.markdown("""
    - **Encode:** Your message is hidden in the least significant bits of the image's red, green, and blue channels. The image looks unchanged. You can optionally set a **password** to encrypt the message before hiding it.
    - **Decode:** The hidden bits are read back and turned into text. If you used a password when encoding, enter the same password here to decrypt.
    - **Capacity:** Depends on image size (roughly 3 bits per pixel). Larger images can hold longer messages.
    """)

encode_tab, decode_tab = st.tabs(["🔒 Encode", "🔓 Decode"])

with encode_tab:
    st.subheader("Encode a message")
    cover_file = st.file_uploader("Choose a cover image", type=["png", "jpg", "jpeg"], key="encode_upload")
    if cover_file:
        img_preview = Image.open(cover_file)
        if img_preview.mode != "RGB":
            img_preview = img_preview.convert("RGB")
        w, h = img_preview.size
        max_bits = w * h * 3
        max_chars = max(0, (max_bits // 8) - 10)  # reserve for delimiter/overhead
        st.image(cover_file, caption="Cover image", use_container_width=False, width=280)
        st.caption(f"📐 Capacity: this image can hold **~{max_chars:,} characters** (plain text). Encrypted messages use a bit more space.")
    secret_msg = st.text_area("Secret message", placeholder="Enter the message to hide...", key="encode_msg", height=100)
    encode_password = st.text_input("Password (optional)", type="password", placeholder="Leave empty for no encryption", key="encode_pwd")
    if encode_password:
        st.caption("🔒 Message will be encrypted. Use the same password to decode.")
    if st.button("Encode", type="primary", key="encode_btn"):
        if not cover_file:
            st.warning("Please upload a cover image.")
        elif not secret_msg.strip():
            st.warning("Please enter a secret message.")
        else:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                tmp.write(cover_file.getvalue())
                tmp_path = tmp.name
            try:
                pwd = encode_password.strip() or None
                img = hide_data(tmp_path, secret_msg, output_path=None, password=pwd)
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                buf.seek(0)
                st.success("Message encoded successfully.")
                col_dl, col_preview = st.columns([1, 1])
                with col_dl:
                    st.download_button("Download stego image", data=buf.getvalue(), file_name="stego_image.png", mime="image/png", key="encode_dl")
                with col_preview:
                    buf.seek(0)
                    st.image(buf, caption="Stego image (preview)", use_container_width=False, width=280)
            except Exception as e:
                st.error(f"Encoding failed: {e}")

with decode_tab:
    st.subheader("Decode a message")
    stego_file = st.file_uploader("Choose a stego image", type=["png", "jpg", "jpeg"], key="decode_upload")
    if stego_file:
        st.image(stego_file, caption="Uploaded image", use_container_width=False, width=280)
    decode_password = st.text_input("Password (optional)", type="password", placeholder="Same password you used when encoding (if any)", key="decode_pwd")
    if st.button("Decode", type="primary", key="decode_btn"):
        if not stego_file:
            st.warning("Please upload a stego image.")
        else:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                tmp.write(stego_file.getvalue())
                tmp_path = tmp.name
            try:
                pwd = decode_password.strip() or None
                message = show_data(tmp_path, password=pwd)
                if not message:
                    st.info("No hidden message found in this image (or the image was not encoded with this tool).")
                else:
                    st.success("Message decoded.")
                    st.code(message, language=None)
            except ValueError as e:
                st.error(str(e))
            except Exception as e:
                st.error(f"Decoding failed: {e}")

st.divider()
st.caption("LSB steganography · Optional encryption")
