# PromptVault

PromptVault is a simple Flask web application to save, search, and copy useful prompts.

## Features

- Save prompts with title, category, and description
- Search prompts by keyword across title/category/content
- Copy prompts with one click
- Clean modern UI built with Tailwind CSS

## Tech Stack

- **Frontend:** HTML, Tailwind CSS, JavaScript
- **Backend:** Python + Flask
- **Storage:** SQLite

## Project Structure

```text
PromptVault_Codex_Demo/
├── app.py
├── requirements.txt
├── prompts.db (created automatically on first run)
├── static/
│   └── js/
│       └── app.js
└── templates/
    ├── base.html
    ├── home.html
    ├── add_prompt.html
    └── search.html
```

## Run Locally

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the app:

```bash
python app.py
```

4. Open `http://127.0.0.1:5000` in your browser.
