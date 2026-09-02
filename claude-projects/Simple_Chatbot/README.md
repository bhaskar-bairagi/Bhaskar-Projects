# Simple Chatbot — Claude API

A command-line chatbot built with the Anthropic Claude API, featuring persistent conversation memory across turns within a single session.

## Overview

This project demonstrates a minimal but complete conversational AI loop: user input is captured, sent to Claude along with the full conversation history, and the response is appended back into that history — allowing the model to maintain context across multiple turns (e.g. referencing "that answer" or "add 2 more" without repeating earlier values).

## Features

- Multi-turn conversation memory via a running `messages` list
- Clean separation of concerns: dedicated helper functions for user messages, assistant messages, and the API call itself
- Markdown/LaTeX-aware output rendering (bold text and mathematical notation render properly in Jupyter, not as raw syntax)
- Runs entirely from a Jupyter notebook — no external server or UI required

## Tech Stack

| Component        | Purpose                                  |
|-------------------|-------------------------------------------|
| Python            | Core language                             |
| Anthropic SDK     | Claude API client                         |
| python-dotenv     | Loads API key from environment file       |
| Jupyter Notebook  | Interactive execution environment         |

## Prerequisites

- Python 3.13+
- An Anthropic API key ([console.anthropic.com](https://console.anthropic.com/settings/keys))
- Jupyter (`pip install notebook`)

## Setup

1. **Clone the repository** and navigate to this project:
   ```bash
   cd Simple_Chatbot
   ```

2. **Install dependencies** (run inside the notebook, or via terminal):
   ```bash
   pip install anthropic python-dotenv
   ```

3. **API key**: this project reads `ANTHROPIC_API_KEY` from a `.env` file at the repository root (`Building_with_Claude_API/.env`), shared across all projects in this repo. No project-local `.env` is needed.

## Running the Chatbot

1. Open a terminal and navigate to the project folder:
   ```bash
   cd "E:\Studies\Anthropic\Building_with_Claude_API\Simple_Chatbot"
   ```

2. Start Jupyter:
   ```bash
   jupyter notebook
   ```

3. In the browser tab that opens (`http://localhost:8888/tree`), select **Simple_Chatbot**.

4. Run all cells sequentially, top to bottom.

   > **Tip:** The second cell loads the `.env` file — confirm it prints `True`, which verifies the API key was found successfully before proceeding.

5. Once the final cell is running, type a question at the `>` prompt and press Enter.

## Example Session

```
> add 23 and 34
_____
23 + 34 = 57
_____
> divide this with 789
_____
57 ÷ 789 ≈ 0.0722
_____
> make log base 5
_____
log₅(0.0722) ≈ -1.6329
_____
> create its laplace transformation
_____
L{c} = c / s, where c ≈ -1.6329
_____

```

Each answer builds on the conversation history — note how "divide **this**" and "add 2 more" correctly resolve to the previous result without the user restating it.

## Project Structure

```
Simple_Chatbot/
├── simple_chatbot.ipynb   # Main notebook
└── README.md              # This file
```

## Possible Future Improvements

- Add streaming responses for real-time output
- Persist conversation history to disk between sessions
- Wrap as a simple web UI (Flask/Streamlit) instead of a notebook loop
- Add error handling for API rate limits and connection failures

## License

Personal / educational project.
