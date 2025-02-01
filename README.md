# Vocal-Separator  

A powerful AI-based tool that removes background noise and extracts vocals from any audio file. This model leverages **Demucs** with **Bag of 2** and **Bag of 4** configurations to separate music into clean vocals and other stems.  

---

## Features  

- **AI-Powered Separation** – Uses state-of-the-art deep learning models  
- **Bag of 2 Mode** – Splits audio into vocals and background  
- **Bag of 4 Mode** – Separates audio into **vocals, drums, bass, and others**  
- **High-Quality Output** – Retains vocal clarity while minimizing artifacts  
- **Supports Multiple Formats** – Works with WAV, MP3, and other common audio types  
- **Easy to Use** – Simple interface for uploading and processing files  

---

## Technologies Used  

- **Demucs** – Deep learning-based music source separation  
- **Python** – Main programming language for processing  
- **Torch (PyTorch)** – Framework for running the AI models  
- **Librosa** – Audio file handling and waveform visualization  
- **Flask** – API backend for web-based usage  

---

## Getting Started  

### Prerequisites  

- Python 3.8+  
- Install dependencies:  

```bash
pip install -r requirements.txt
