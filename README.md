# LLM Topic Classification Pipeline

Classify Indonesian social-media posts into themes for any topic, rank the most influential accounts per theme, and summarise each account's stance with Gemini.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/aldo02032004/llm-topic-classification-pipeline/blob/main/topic_classification_pipeline.ipynb)

## What it does

You type a topic in one sentence (e.g. *"Kunjungan Presiden Prabowo ke Vladivostok"*) and point it at a monitoring export. The notebook then:

1. **Builds the topic config with AI**: Gemini proposes 2–4 themes (with inclusion/exclusion rules), 20–60 topic keywords, and media accounts to exclude. The config is saved to Drive and reused.
2. **Loads** one or more exports from Google Sheets / Drive links.
3. **Removes media accounts** (built-in list from [GREAT-Tools](https://github.com/azmkto/GREAT-Tools) plus the AI-suggested ones), so only organic accounts are ranked.
4. **Cleans text**: strips `RT` / `[RE user]` markers, turns emoji into words, shortens stretched letters (`mantaaap` → `mantaap`), drops short posts and duplicates. Original posts are kept over retweets.
5. **Assigns themes (hybrid)**: posts without any topic keyword go straight to `lainnya` without an API call. The rest are classified by Gemini in batches of 20 with structured (Pydantic) output.
6. **Ranks top authors per theme**: `0.6 × post count + 0.25 × engagement + 0.15 × followers`, each normalised within the theme. Retweets and low-confidence labels are excluded.
7. **Summarises stance**: Gemini reads each top author's highest-engagement posts and returns `positif / negatif / netral / kontroversi`, a 2–3 sentence summary, and the reason.

Long runs survive quota limits: progress is checkpointed to Drive every 10 batches, and re-running the cell resumes where it stopped.

## Quick start (Colab)

1. Get a free Gemini API key at <https://aistudio.google.com/apikey>.
2. In Colab, open **Secrets** (key icon), add `GOOGLE_API_KEY`, and enable *Notebook access*.
3. Open the notebook with the badge above and fill in the **form** cell:
   - `PROJECT`: short name used for output files
   - `TOPIC`: one sentence describing the topic
   - `SOURCES_TEXT`: one or more Google Sheets / Drive links (shared as *Anyone with the link*), separated by commas or spaces
4. `Runtime → Run all`. Google Drive is mounted for config, checkpoints, and results.

## Input format

A monitoring-tool export (Excel) with one title row, then a header row containing the standard columns checked by GREAT-Tools (`EXPORT_COLUMNS`), including `Headline`, `Mentions`, `Media`, `Author`, `Followers`, `Retweeted`, `Favourited`.

## Output (in `MyDrive/`)

| File | Contents |
|---|---|
| `topic_config_<project>.json` | AI-generated themes, keywords, media accounts |
| `df_clean_after_theme_<project>.pkl` | cleaned posts with theme + confidence |
| `kol_<project>.csv` | top authors per theme with score |
| `kol_summary_<project>.csv` | top authors + stance, summary, reason |
| `pending_tema_data.jsonl` | Gemini theme labels, appended as training data for a future classifier |

## Tech stack

Gemini (`gemini-3.7-flash`, via the OpenAI-compatible endpoint) · Pydantic structured output · pandas · emoji · [GREAT-Tools](https://github.com/azmkto/GREAT-Tools) (export schema, media-account filter, text cleaning) · Google Colab

## Notes

- Free-tier friendly: a 7-second pause between calls, automatic retries, and a clean stop on daily quota.
- Prompts are in English; the AI's answers and code comments are in Indonesian.

## License

MIT — see [LICENSE](LICENSE).
