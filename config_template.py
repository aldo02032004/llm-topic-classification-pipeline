# Copy this file to config.py and fill in every section below.
# config.py is project-specific and is NOT committed to this repo
# (add it to .gitignore) — it holds your data source, themes, and
# keyword lists, which differ per project.

CONFIG = {
    # === 1. SOURCE DATA (Google Drive) ===
    # Google Drive share link to your .xlsx file (must be publicly
    # viewable or shared with "Anyone with the link").
    "drive_xlsx_url": "https://docs.google.com/spreadsheets/d/XXXXXXXXXXXXXXXX/edit?usp=sharing",
    "sheet_name": "Sheet1",
    "header_skiprows": 1,

    # === 2. CHECKPOINT / RESUME FILE ===
    # Give a specific name per project so it doesn't get overwritten
    # by other projects using the same pipeline.
    "checkpoint_path": "/content/drive/MyDrive/df_clean_after_theme__my_project.pkl",

    # === 3. COLUMN NAME MAPPING ===
    # Do not change the key (left), adjust the value (right) to match
    # your spreadsheet's actual column headers.
    "columns": {
        "no": "No",
        "type": "Type",
        "headline": "Headline",
        "mentions": "Mentions",
        "date": "Date",
        "link": "Link",
        "media": "Media",
        "sentiment": "Sentiment",
        "author_id": "Author",
        "followers": "Followers",
        "retweeted": "Retweeted",
        "favourited": "Favourited",
    },

    # === 4. THEMES ===
    # Always leave one "others"/catch-all bucket.
    # description = concise keyword collection (official names, nicknames,
    # events, common typos, hashtags) — this text directly becomes part
    # of the LLM classification prompt.
    "themes": {
        "example_theme_a": "replace with concise keywords for theme A",
        "example_theme_b": "replace with concise keywords for theme B",
        "others": "topics outside the themes above",
    },

    # === 5. LLM PROVIDER & MODEL ===
    "gemini_model": "gemini-3.1-flash-lite",
    "google_api_key_env": "GOOGLE_API_KEY",

    # === 6. RATE LIMITING / BATCHING ===
    "sleep_between_calls": 4,
    "batch_size_classify": 40,
    "batch_size_ner": 20,

    # === 7. TOP-AUTHOR RANKING (weights must sum to 1.0) ===
    "weight_post_count": 0.6,
    "weight_engagement": 0.25,
    "weight_followers": 0.15,
    "top_n_authors_per_theme": 10,
    "max_posts_per_author_summary": 15,

    # === 8. OPTIONAL EXTENSIONS ===
    # Extra media accounts to filter out on top of the built-in list
    # (pipeline.py's MEDIA_ACCOUNTS). Normalized: lowercase, no "@",
    # no digits/symbols.
    "extra_media_accounts": [],

    # Extra Indonesian slang/abbreviations on top of the built-in
    # KAMUS_ALAY dictionary, as {slang: standard_form}.
    "extra_kamus_alay": {},
}
