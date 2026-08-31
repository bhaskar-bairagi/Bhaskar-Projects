# Easy AI Invoice Organizer

A small personal project that reads invoice PDFs, extracts useful fields, suggests clean filenames, and lets you download the results as a CSV.

It has two ways to learn and test:

1. **Streamlit app** — easiest and visual.
2. **Jupyter notebook** — step-by-step exploration.

The included demo works without an API key or API cost. The optional AI mode uses the OpenAI Responses API.

## What it extracts

- Invoice date
- Vendor
- Invoice number
- Total amount and currency
- Suggested filename such as `2026-05-08_northbeam-strategy_nb-2026-0142.pdf`

## Run the Streamlit app

Open Git Bash in the project folder:

```bash
cd /e/Bhaskar-Projects/openai-projects/intelligent-invoice-platform
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
streamlit run app.py
```

Your browser should open automatically. Start by clicking **Load free demo results**.

## Optional: test with OpenAI

Paste an API key into the app sidebar, or set it in Git Bash:

```bash
export OPENAI_API_KEY="your-api-key"
streamlit run app.py
```

Upload one invoice first to keep testing inexpensive. The application does not save the key.

## Run the notebook

```bash
jupyter notebook invoice_organizer.ipynb
```

Run each cell from top to bottom. Change `PDF_PATH` to your file. The notebook tries high-detail PDF extraction first, falls back to locally extracted text, displays detailed warnings, and provides a manual correction cell before CSV export. This notebook requires your API key because it is intended for testing new invoices.

## Resume description

**AI Invoice Organizer — Python, Streamlit, OpenAI API**

- Built a lightweight Streamlit application that extracts structured invoice information from PDFs and generates standardized filename suggestions and downloadable CSV reports.
- Added a no-cost sample mode and an optional OpenAI-powered mode for testing personal documents.

## Safety

The application displays results and creates a CSV; it does not rename, delete, or move original invoices. Avoid uploading confidential documents while experimenting.
