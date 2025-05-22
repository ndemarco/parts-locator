# Parts Locator

A simple Flask web app to track parts by description, location, and creation date. Uses SQLite for storage and is intended for use in a workshop, lab, or parts storage system.

> **_NOTE:_**  the branch [convert-to-flask](https://github.com/ndemarco/parts-locator/tree/convert-to-flask) is currently the most interesting.

## Features

- Track part descriptions, physical storage locations, and creation dates
- Add, update, and delete entries via a web UI
- SQLite backend for easy setup and portability

## Requirements

- Python 3.8+
- Git
- Basic command line experience

## Getting Started

These steps work on both **Windows** and **Linux**.

### 1. Clone the Repository

```bash
git clone https://github.com/ndemarco/parts-locator.git
cd parts-locator
```

### 2. Create and Activate a Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the App

```bash
python app.py
```

The app will be available at http://127.0.0.1:5000, normally known as http://localhost:5000

On first run, a SQLite database file will be created in the instance/ folder.

---

## File Structure

```
parts-locator/
├── app.py               # Main Flask app
├── templates/           # HTML templates (index.html, base.html, etc.)
├── static/
│   └── css/main.css     # Styling
├── instance/
│   └── workshop-parts.db  # SQLite DB (auto-created)
├── README.md
└── .venv/               # Virtual environment (not checked into Git)
```

---

## Notes

- The `instance/` folder is created automatically and is where the SQLite DB lives.
- To reset all data, delete `instance/workshop-parts.db`.
- Use `ctrl+C` to stop the server.

---

## License

MIT