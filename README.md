# Image Steganography (LSB)

Hide or reveal text inside images using least-significant-bit (LSB) encoding.

## Setup

```bash
pip install -r requirements.txt
```

## Run the Streamlit app (recommended)

```bash
streamlit run app.py
```

Open the URL in your browser. Use **Encode** to hide a message in an image and download the stego image; use **Decode** to upload a stego image and read the message.

## Run the notebook locally

1. Open `ImageSteganography.ipynb` in Cursor (or Jupyter).
2. Run all cells. Skip or ignore the Colab Drive cells.
3. Use local paths when prompted (e.g. `.\image.png` or `C:\Users\gowth\Desktop\V\image.png`).
4. Run the last cell to start the encode/decode menu.

## Project layout

- **`steganography.py`** — Core logic: `hide_data()`, `show_data()`
- **`app.py`** — Streamlit web UI
- **`ImageSteganography.ipynb`** — Notebook (CLI menu) using the same core
- **`requirements.txt`** — Pillow, matplotlib, streamlit

## File overview

| File | Purpose |
|------|--------|
| **`steganography.py`** | Core LSB logic. Defines `message_to_binary()` (text/bytes → 8-bit binary), `hide_data()` (writes message bits into the least significant bit of each R,G,B channel and optionally saves the stego image), and `show_data()` (reads LSBs from an image and reconstructs the message until the delimiter). Used by both the Streamlit app and the notebook. |
| **`app.py`** | Streamlit web UI. Two tabs: **Encode** (upload cover image, enter message, encode, download stego image) and **Decode** (upload stego image, decode, show message). Uses temp files for uploads and calls `steganography.hide_data` / `show_data`. Run with `streamlit run app.py`. |
| **`ImageSteganography.ipynb`** | Jupyter notebook for a CLI-style workflow. Imports from `steganography.py`, sets a local `dataset_path`, and provides `preview_image()`, `encode_image()`, and `decode_image()` that prompt for paths. The last cell runs a menu loop (1=Encode, 2=Decode, 3=Exit). Use when you prefer terminal prompts over the web UI. |
| **`requirements.txt`** | Python dependencies: **Pillow** (image I/O and pixel access), **matplotlib** (notebook image preview), **streamlit** (web app). Install with `pip install -r requirements.txt`. |
| **`README.md`** | This file: project description, setup, how to run the app and notebook, and file overview. |
