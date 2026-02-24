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
