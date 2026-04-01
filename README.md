# Daikin AC Label OCR Tool

A fast desktop application for Daikin service centers to extract **Model Number** and **Serial Number** from AC unit label photos using Tesseract OCR.

---

## Folder Structure

```
daikin_ocr/
â”œâ”€â”€ main.py           â† Entry point (run this)
â”œâ”€â”€ ocr_engine.py     â† Image preprocessing + Tesseract OCR
â”œâ”€â”€ extractor.py      â† Daikin-specific regex & extraction logic
â”œâ”€â”€ ui.py             â† Tkinter desktop UI
â”œâ”€â”€ requirements.txt  â† Python dependencies
â””â”€â”€ daikin_ocr.spec   â† PyInstaller packaging config
```

---

## Prerequisites

### 1. Install Tesseract OCR (system binary)

| Platform | Command |
|----------|---------|
| **Windows** | Download from [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki) and install to `C:\Program Files\Tesseract-OCR\` |
| **macOS**   | `brew install tesseract` |
| **Ubuntu/Debian** | `sudo apt install tesseract-ocr` |

Verify: `tesseract --version`

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

> **Note:** On some Linux distros you may also need: `sudo apt install python3-tk`

---

## Running the App

```bash
python main.py
```

**Keyboard shortcuts:**
- `Ctrl+O` â€” Upload image
- `Enter`  â€” Run OCR

---

## How It Works

### Preprocessing Pipeline (`ocr_engine.py`)
1. **Auto-rotate** â€” Corrects upside-down or tilted label photos
2. **Grayscale conversion** â€” Removes colour noise
3. **Contrast enhancement** â€” Alpha=2.0, Beta=40 (sharpens text)
4. **Gaussian blur** â€” Removes camera grain
5. **Adaptive thresholding** â€” Binarises image for Tesseract

### Extraction Logic (`extractor.py`)
| Field | Strategy |
|-------|----------|
| **Model Number** | Context search near "MODEL" / "M/N" keywords, then regex `[A-Z]{2,5}[0-9]{2}[A-Z0-9]{3,8}` |
| **Serial Number** | Context search near "SER" / "S/NO" keywords, then regex `\b\d{6,9}\b` |

**OCR error corrections applied:**
- `O â†’ 0`, `I â†’ 1`, `B â†’ 8`, `S â†’ 5`, `Z â†’ 2`, `G â†’ 6`

### Fallback Strategy
- Pass 1: Block-text PSM config on standard preprocessing
- Pass 2 (if confidence < 50%): Sparse PSM with inverted thresholding
- The higher-confidence result is used automatically

---

## Features

| Feature | Details |
|---------|---------|
| Single image upload | JPG, PNG, BMP, TIFF |
| Batch processing | Queue multiple images, export all to Excel |
| Image preview | Shows original or preprocessed view |
| Detection highlights | Green boxes around matched keywords |
| Confidence score | 0â€“100% OCR confidence meter |
| Copy to clipboard | One-click copy of Model / Serial |
| Export to Excel | `.xlsx` with all batch results |
| Processing time | Target: < 2 seconds per image |

---

## Packaging as .exe (Windows)

```bash
pip install pyinstaller
pyinstaller daikin_ocr.spec
```

Before packaging, edit `daikin_ocr.spec` to point `binaries` at your Tesseract installation path.

Output will be in `dist/DaikinOCR/DaikinOCR.exe`.

---

## Tested Label Format

Validated against Daikin outdoor condensing unit labels with layout:

```
MODEL  RKM50XV16MKA          SER. NO.  0007836
```

Other supported model patterns:
- `FTKM50U`
- `FTKM50YV16KMB`
- `RKM50XV16MKA`
- `ATM50MV1W9`

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `TesseractNotFoundError` | Install Tesseract binary; on Windows set the path in `main.py` |
| Model not detected | Use better lighting; try the "Show preprocessed" toggle to check image quality |
| Low confidence score | Ensure label is flat, well-lit, in focus; avoid glare |
| App opens but crashes | Ensure `python-tk` is installed on Linux |

---

## Tech Stack

- **Python 3.10+**
- **OpenCV** â€” Image preprocessing
- **pytesseract** â€” Tesseract OCR wrapper
- **Pillow** â€” Tkinter image integration
- **pandas + openpyxl** â€” Excel export
- **Tkinter** â€” Cross-platform GUI# OCR-APP
