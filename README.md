# Bhaskar's Architecture and AI Projects

Locally runnable learning projects across cloud architecture, data, and AI. Each project separates working code from its cloud reference design and uses synthetic examples.

## Structure

| Folder | Description |
|---|---|
| [`claude-projects/`](./claude-projects) | Projects built with the Anthropic Claude API |
| [`openai-projects/`](./openai-projects) | Projects built with the OpenAI API |
| [`gcp-projects/`](./gcp-projects) | Local exercises for GCP data and migration architecture |
| [`docs/`](./docs) | Portfolio documentation |

## Featured Projects

- **[Finance reconciliation lab](./gcp-projects/finance-reconciliation/)** — match synthetic payment feeds and review exceptions in Streamlit; includes a GCP architecture mapping
- **[Azure to GCP migration decision lab](./gcp-projects/azure-to-gcp-migration-lab/)** — assess a sample VM workload, compare migration routes, and generate a validation and rollback checklist
- **[Invoice Organizer](./openai-projects/intelligent-invoice-platform/)** — extract structured invoice fields from PDFs with a free demo and optional API mode
- **[Simple Chatbot](./claude-projects/Simple_Chatbot)** — Command-line multi-turn chatbot using the Claude API
- **[Streamlit Chatbot](./claude-projects/Streamlit_Chatbot)** — Web UI chatbot with streaming responses, citations, file upload, and web search

## Setup

Each project folder contains setup steps. The two GCP exercises need no API keys or cloud account. AI projects may need their respective API keys; keep them in an untracked `.env` file or your environment and never commit credentials or real customer documents.
