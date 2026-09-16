# Media Monitoring NLP Pipeline

Hybrid keyword + LLM pipeline for classifying social media posts into custom themes, extracting named entities, and ranking top influencers per theme with automated sentiment summarization.

## Features

- **Ingest with resume**: load data from Google Drive (.xlsx), save a checkpoint so you don't have to re-run everything from scratch if the session drops
- **Media account filtering**: separate official news/media accounts (built-in Indonesian + regional whitelist) from personal/organic accounts before further processing
- **Text cleaning**: strip URLs/mentions, unwrap hashtags, convert emoji to text, normalize Indonesian slang ("gak" -> "tidak", etc.), deduplicate identical/retweeted posts
- **Hybrid theme classification**: fast keyword prefilter first, remaining texts sent to the LLM (Gemini) for multi-label few-shot classification
- **NER**: extract locations, institutions, and persons from text via the LLM
- **Top-author ranking**: combined score of post count + engagement + followers per theme
- **Summary & sentiment per top author**: the LLM reads all posts from each top author and produces a narrative summary + overall sentiment (positive/negative/controversial), exported to Excel

## Tech Stack

| Category | Tools |
|---|---|
| LLM | Google Gemini API (`google-genai`) |
| Data processing | pandas |
| Progress tracking | tqdm |
| Text processing | emoji, regex |
| Ingest | gdown, openpyxl |

## Project Structure

```
media-monitoring-nlp-pipeline/
├── README.md
├── requirements.txt
├── config_template.py
└── pipeline.py
```

## Setup

```bash
git clone https://github.com/USERNAME/media-monitoring-nlp-pipeline.git
cd media-monitoring-nlp-pipeline
pip install -r requirements.txt
```

### 1. Create config.py

```bash
cp config_template.py config.py
```

Fill in `config.py` with:
- `drive_xlsx_url`: Google Drive link to your data file
- `columns`: match your spreadsheet's actual column names
- `themes`: your classification themes + their keywords
- `google_api_key_env`, rate limits, and ranking weights as needed

`config.py` is intentionally **not** committed (listed in `.gitignore`) since its content is specific to each project/dataset.

### 2. Set the API key

Get a free Gemini API key at https://aistudio.google.com/apikey, then set it as the `GOOGLE_API_KEY` environment variable (or via Colab Secrets if running on Colab).

### 3. Fill in the few-shot examples

Before running, you must manually fill in these sections of `pipeline.py`:
- `FEWSHOT_THEME_EXAMPLES` (Step 4) — real text examples per theme
- `FEWSHOT_NER_EXAMPLES` (Step 6) — real entity examples from your topic
- `KW_ACTOR` / `KW_CONTEXT` etc. (Step 4a) — keyword prefilter, optional but saves API calls

Leaving the `[REPLACE: ...]` placeholders in place will produce poor classification results.

### 4. Run

```bash
python pipeline.py
```

This script was originally built for Google Colab (uses `drive.mount`, `userdata.get`) — to run it outside Colab, replace those parts with regular environment variables and local paths.

## Output

- Console: statistics at each stage (number of media accounts filtered, theme distribution, NER results, top authors per theme)
- File: `top_author_analysis_results.xlsx` — summary + sentiment per top author

## Notes

This pipeline is generic/reusable across projects — the core logic (cleaning, media filtering, classification, NER, ranking) doesn't need to change. Only `config.py` and the few-shot examples above need to be adjusted per project.
