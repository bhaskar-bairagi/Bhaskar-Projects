# Document summarization lab

An educational, fully local comparison of two **extractive** summarization baselines: take the opening sentences, or select sentences using word frequency. The included synthetic incident report lets you inspect what each method preserves and omits. This project does not train or implement an encoder–decoder GAN.

## Run locally

With Python 3.10+, from this directory:

```bash
python -m venv .venv
source .venv/bin/activate          # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Click **Compare summaries** with the default text. Change the sentence count or paste another non-confidential document. Run `python -m unittest discover -p 'test_*.py'` to check the scoring functions.

## What the diagnostics mean

| Metric | Definition | Limitation |
|---|---|---|
| Source sentence support | Every selected sentence occurs in the source | Does not establish completeness or correct interpretation |
| Key term coverage | Fraction of user-entered terms appearing in the summary | Depends on a subjective list and exact wording |
| Word ratio | Summary content words divided by source content words | Shorter is not necessarily better |

Both methods select original sentences, preserving their order. Frequency scoring counts non-stopword occurrences, averages by sentence length, and breaks ties by source order. It is a simple baseline, not a semantic model. Long documents, sentence boundaries, synonyms, and key facts expressed indirectly can defeat these diagnostics.

## Explore further

Create a small manually annotated evaluation set and compare the baselines against a locally available pretrained encoder–decoder model, with attention to factual consistency and compute cost. The [encoder–decoder GAN summarization research repository](https://github.com/tathagata1/Text-Summarization-Using-Encoder-Decoder-Generative-Adversarial-Networks) motivated this topic; this project uses original code and a different, lightweight method.
