"""Streamlit frontend for LSB image steganography."""

import io
import tempfile
import streamlit as st

from steganography import hide_data, show_data

st.set_page_config(page_title="Image Steganography", page_icon="🖼️", layout="centered")
st.title("🖼️ Image Steganography")
st.caption("Hide or reveal text inside images using LSB encoding")

encode_tab, decode_tab = st.tabs(["Encode", "Decode"])

with encode_tab:
    st.subheader("Encode a message")
    cover_file = st.file_uploader("Choose a cover image", type=["png", "jpg", "jpeg"], key="encode_upload")
    secret_msg = st.text_area("Secret message", placeholder="Enter the message to hide...", key="encode_msg")
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
                st.download_button("Download stego image", data=buf, file_name="stego_image.png", mime="image/png", key="encode_dl")
            except Exception as e:
                st.error(f"Encoding failed: {e}")

with decode_tab:
    st.subheader("Decode a message")
    stego_file = st.file_uploader("Choose a stego image", type=["png", "jpg", "jpeg"], key="decode_upload")
    decode_password = st.text_input("Password (optional)", type="password", placeholder="Required if you set one when encoding", key="decode_pwd")
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
                st.success("Message decoded.")
                st.text_area("Decoded message", value=message, height=120, disabled=True, key="decode_out")
            except ValueError as e:
                st.error(str(e))
            except Exception as e:
                st.error(f"Decoding failed: {e}")
