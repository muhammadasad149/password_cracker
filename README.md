---

# 🔓 PDF Password Cracker – Streamlit Web App

A powerful and user-friendly **Streamlit-based PDF Password Cracker** that helps you:

✔ Crack password-protected PDFs using a wordlist
✔ Generate custom wordlists
✔ Test a password instantly
✔ View real-time cracking speed & progress
✔ Download results
✔ All inside a clean, modern UI

⚠️ **For educational and legal use only. Use only on PDFs you own!**

---

## 🚀 Features

### 🔓 **1. Crack PDF Password**

* Upload a protected PDF
* Use default or custom wordlist
* Set maximum attempts
* Live progress bar with:

  * Attempts per second
  * Estimated time
  * Real-time logs
* Result download as `.txt`
* Smart error handling

---

### 📝 **2. Generate Wordlist**

* Generate a sample dictionary (60,000+ passwords)
* Supports:

  * Years
  * Numeric combinations
  * Common variations
* Preview first 50 entries
* Download generated wordlist

---

### 🧪 **3. Test Password**

* Upload PDF and instantly test a password
* Shows:

  * Encryption status
  * Number of pages
  * PDF metadata
* Instant success/failure message

---

## 🎨 UI / UX Highlights

* Gradient header
* Beautiful message containers (success / warning / info / error)
* Sidebar with app details
* Detailed real-time analytics
* Clean responsive layout
* Auto deletion of temp files

---

## 🛡 Security & Legal Notice

* Processes files only in memory / temp
* No logs stored
* Educational purpose only
* **Do NOT use for illegal access to documents**

---

## 📦 Installation

### **1. Install dependencies**

```bash
pip install streamlit pikepdf
```

### **2. Run the App**

```bash
streamlit run streamlit_pdf_cracker.py
```

---

## 📁 Project Structure

```
📦 pdf-password-cracker
 ┣ 📜 streamlit_pdf_cracker.py
 ┣ 📜 requirements.txt
 ┣ 📜 README.md
 ┗ 📁 wordlists/ (optional)
```

---

## 🧰 Requirements

* Python 3.8+
* Streamlit
* PikePDF (v8+ recommended)

---

## 🧪 Sample Commands

Generate optimized wordlist:

```python
python streamlit_pdf_cracker.py --generate-wordlist
```

Run brute-force cracking from UI:

```bash
streamlit run streamlit_pdf_cracker.py
```

---

## 🤝 Contributing

Pull requests are welcome!
If you want to add features (GPU cracking, cloud support, multiprocessing), feel free to contribute.

---

## 📜 License

MIT License — free to use, modify & distribute.

---

## ⭐ Support

If you like this project, give it a **star ⭐ on GitHub** to support development.

---
