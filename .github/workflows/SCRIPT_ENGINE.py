# ============================================================
# SCRIPT_ENGINE.py — SKY Academy Video Script Generator v2
# ============================================================

import streamlit as st
import json
import re
import math

# ──────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🎬 SCRIPT ENGINE – SKY Academy",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────
# CUSTOM CSS
# ──────────────────────────────────────────────────────────
st.markdown("""
<style>
    body { font-family: 'Segoe UI', sans-serif; }
    .header-box {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        padding: 24px 20px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 24px;
    }
    .header-box h1 { color: #fff; font-size: 2rem; margin: 0; }
    .header-box p  { color: #aaa; margin: 6px 0 0 0; font-size: 0.9rem; }
    .stat-pill {
        display: inline-block;
        background: #e8e0ff;
        color: #302b63;
        border-radius: 20px;
        padding: 3px 12px;
        font-size: 0.8rem;
        margin: 2px;
        font-weight: 600;
    }
    .word-info {
        background: #f0edff;
        border-left: 4px solid #302b63;
        padding: 10px 14px;
        border-radius: 0 8px 8px 0;
        font-size: 0.85rem;
        color: #302b63;
        margin-top: 4px;
        margin-bottom: 10px;
    }
    .empty-preview {
        background: #f0f2f6;
        border: 2px dashed #ccc;
        border-radius: 12px;
        padding: 60px 20px;
        text-align: center;
        color: #999;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #302b63, #0f0c29) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
    }
    div[data-testid="stExpander"] {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────────────────────
st.markdown("""
<div class="header-box">
    <h1>🎬 SCRIPT ENGINE</h1>
    <p>SKY Academy · Telugu Video Script Generator · Internal Tool v2</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# CONSTANTS
# ============================================================
PAGEGRID_BASE_URL = "https://api.pagegrid.in"
WORDS_PER_SEGMENT = 120   # ~55 seconds of speech

SHEET_ID      = "1dNHDgkX6vhdhZSi5SavBgNihWe04zayRQwyMcCwNlOI"
SCRIPTS_TAB   = "Scripts_bot"
SHEET_HEADERS = ["Seg No.", "Telugu Text", "Slide Prompt",
                 "Audio Url", "Slide Url", "Status", "Audio Done"]

# ============================================================
# MODEL OPTIONS  (highest-end per provider)
# ============================================================
MODEL_OPTIONS = {
    "Claude (via PageGrid)": [
        "claude-opus-4-5",
        "claude-sonnet-4-5",
        "claude-3-5-haiku-20241022",
    ],
    "OpenAI (GPT)": [
        "o3",
        "o1",
        "gpt-4.5-preview",
        "gpt-4o",
    ],
    "Google (Gemini)": [
        "gemini-2.5-pro",
        "gemini-2.0-pro-exp",
        "gemini-2.0-flash",
        "gemini-1.5-pro",
    ],
}

# ============================================================
# SYSTEM PROMPT
# ============================================================
SYSTEM_PROMPT = """\
You are an expert Telugu video script writer for SKY Academy — India's leading competitive exam
preparation YouTube channel taught in Telugu medium.

━━━━━━━━━━━━━━━━━━━━━━━━━━
STYLE DNA  (replicate exactly)
━━━━━━━━━━━━━━━━━━━━━━━━━━

DELIVERY CUES — always embed inside brackets in the script:
[Energetic]  [Serious]  [Whisper/Secret Tip]  [High Pitch]  [Laughing]
[Deep Pause] [Assertive] [WARM, FRIENDLY — WELCOME] [Calm, Instructional]

CONNECTOR PHRASES — weave naturally:
• "ఓకేనా", "ఓకే రైట్", "అవునా కాదా", "చాలా ఇంపార్టెంట్"
• "చూసుకున్నాం అనుకుంటే", "మనం చూసుకుంటే"
• "తెలుసు కదా", "మీకు తెలుసు కదా"
• "లెట్స్ స్టార్ట్", "లెట్స్ బిగిన్"

LANGUAGE STYLE:
• Telugu + English natural mix — technical terms in English, explanation in Telugu
• Build suspense: "మస్ట్ గా మీరు గుర్తుపెట్టుకోవాల్సింది ఒక పేరు — [Deep Pause] — [NAME]"
• Direct address: "మీరు", "మీకు", "friends"
• Rhetorical questions: "ఎప్పుడైనా ఆలోచించారా...?"
• Light humor: "[Laughing] వాళ్ళు అంత kind కాదు ఓకేనా — ఇది strategic necessity"

MEMORY HINTS STYLE:
Generate ONLY when a fact is genuinely hard to remember. Never force.
Examples from SKY Academy DNA:
  → "Fancy words = France"  (Liberty, Equality, Fraternity → France)
  → "42°C fever → Emergency → 42nd Amendment"
  → "పాన్ తినకూడదు → Japan"  (discipline → no pan → Japan)
  → "రాముడి మిత్రుడు విభీషణుడు → లంక → Sri Lanka"
  → "మామిడికాయ పచ్చడి = Mamidipudi Venkata Rangaiah"
DO NOT generate a memory hint for every point. Silence is better than a forced hint.

━━━━━━━━━━━━━━━━━━━━━━━━━━
STRICT RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━

1. NO bookish section headings inside voiceover.
   WRONG ✗  "SECTION 1: THE PHILOSOPHY & THE FATHER"
   RIGHT  ✓  "[Energetic] సో ఇప్పుడు మనం చూద్దాం — ఈ concept యొక్క father ఎవరు?"

2. NO "Part 1", "Part 2", "Segment 1", "Segment 2", "Chapter" etc. anywhere
   in the voiceover text. The script flows like ONE continuous natural speech.

3. Transition between topics naturally:
   "సో ఇప్పుడు మనం next important point కి వెళ్దాం ఓకేనా"
   "ఇప్పుడు [topic] చూద్దాం — ఇది చాలా ఇంపార్టెంట్"
   "సో ఇప్పుడు [topic] గురించి మాట్లాడుకుందాం"

4. NEVER mention any competitor academy, coaching center, or book name.

5. ONLY SKY Academy is your home — if any reference needed, say "SKY Academy లో".

6. NO promises about free materials, PDFs, or upcoming courses
   UNLESS the Special Instructions box explicitly says to include them.

7. LAST SEGMENT must always end with this exact closing CTA (adapt naturally):
   "[Energetic] సో friends — ఈరోజు మనం [TOPIC] గురించి చాలా deep గా చూసుకున్నాం ఓకేనా.
   మీకు ఇంకా ఏ topic కావాలో, ఏ subject మీద video కావాలో — comment section లో చెప్పండి.
   నేను personally ప్రతి comment చదువుతాను and reply ఇస్తాను — ఇది నా word మీకు!
   Any doubts ఉన్నాయా? Comment below — I will answer each one personally!"

━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTPUT FORMAT
━━━━━━━━━━━━━━━━━━━━━━━━━━

Return ONLY a valid JSON array — no preamble, no markdown fences, no extra text.

[
  {
    "seg": 1,
    "telugu_text": "full voiceover script with [Delivery Cues] inline...",
    "slide_prompt": "Heading: Short Title Here\\n• bullet 1\\n• bullet 2\\n• bullet 3\\n• bullet 4\\n• bullet 5\\nImage Prompt: detailed cinematic image description, color palette, mood"
  },
  ...
]

Each segment telugu_text ≈ {WORDS_PER_SEGMENT} words of natural speech.
Generate exactly {NUM_SEGS} segments.
The entire script reads as ONE continuous conversation — no bookish labels, no part numbers.
"""


# ============================================================
# GENERATION HELPERS
# ============================================================

def build_messages(topic: str, num_segs: int, special_instructions: str) -> tuple[str, str]:
    system = (
        SYSTEM_PROMPT
        .replace("{NUM_SEGS}", str(num_segs))
        .replace("{WORDS_PER_SEGMENT}", str(WORDS_PER_SEGMENT))
    )
    si_block = (
        f"\nSpecial Instructions from creator:\n{special_instructions.strip()}"
        if special_instructions.strip() else ""
    )
    user = (
        f"Generate a complete SKY Academy Telugu video script on:\n\n"
        f"**Topic:** {topic.strip()}\n"
        f"**Segments required:** {num_segs}\n"
        f"**Words per segment:** ~{WORDS_PER_SEGMENT}\n"
        f"{si_block}\n\n"
        f"Strict reminders:\n"
        f"- No bookish headings, no 'Part 1/Segment 1' labels in voiceover text\n"
        f"- Memory hints only where truly needed\n"
        f"- No competitor/book names\n"
        f"- Last segment must have comment CTA\n"
        f"- Return ONLY valid JSON array"
    )
    return system, user


# ── Claude via PageGrid (mirroring app.py pattern exactly) ──
def call_claude_pagegrid(api_key: str, model: str, system: str, user: str) -> str:
    import anthropic
    client = anthropic.Anthropic(api_key=api_key, base_url=PAGEGRID_BASE_URL)
    resp = client.messages.create(
        model=model,
        max_tokens=8192,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return resp.content[0].text


# ── OpenAI (o-series reasoning models handled separately) ──
def call_openai(api_key: str, model: str, system: str, user: str) -> str:
    import openai
    client = openai.OpenAI(api_key=api_key)
    is_reasoning = model.startswith("o1") or model.startswith("o3")
    if is_reasoning:
        # o1/o3: no separate system role; merge into user message
        resp = client.chat.completions.create(
            model=model,
            max_completion_tokens=16000,
            messages=[{"role": "user", "content": f"{system}\n\n---\n\n{user}"}],
        )
    else:
        resp = client.chat.completions.create(
            model=model,
            max_tokens=8192,
            messages=[
                {"role": "system", "content": system},
                {"role": "user",   "content": user},
            ],
        )
    return resp.choices[0].message.content


# ── Google Gemini ──
def call_gemini(api_key: str, model: str, system: str, user: str) -> str:
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    m = genai.GenerativeModel(model_name=model, system_instruction=system)
    resp = m.generate_content(user)
    return resp.text


def parse_segments(raw: str):
    """Extract JSON array from AI response (handles markdown fences)."""
    raw = re.sub(r"```(?:json)?", "", raw).strip().rstrip("`").strip()
    match = re.search(r"\[[\s\S]*\]", raw)
    if match:
        try:
            return json.loads(match.group())
        except Exception:
            pass
    try:
        return json.loads(raw)
    except Exception:
        return None


# ============================================================
# GOOGLE SHEETS HELPER
# ============================================================
def push_to_gsheet(chunks: list, creds_json_str: str) -> tuple[bool, str]:
    try:
        import gspread
        from google.oauth2.service_account import Credentials

        creds_data = json.loads(creds_json_str)
        scopes = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        creds  = Credentials.from_service_account_info(creds_data, scopes=scopes)
        gc     = gspread.authorize(creds)
        sheet  = gc.open_by_key(SHEET_ID)

        try:
            ws = sheet.worksheet(SCRIPTS_TAB)
        except gspread.WorksheetNotFound:
            ws = sheet.add_worksheet(SCRIPTS_TAB, rows=500, cols=10)

        existing = ws.get_all_values()
        if not existing or existing[0] != SHEET_HEADERS:
            ws.insert_row(SHEET_HEADERS, 1)

        col_a    = ws.col_values(1)
        next_row = len(col_a) + 1

        rows_to_add = [
            [
                i + 1,
                c.get("telugu_text",  ""),
                c.get("slide_prompt", ""),
                "",          # Audio Url
                "",          # Slide Url
                "pending",   # Status
                "no",        # Audio Done
            ]
            for i, c in enumerate(chunks)
        ]
        ws.append_rows(rows_to_add, value_input_option="RAW")

        return True, (
            f"✅ {len(rows_to_add)} segments pushed to **{SCRIPTS_TAB}** "
            f"(rows {next_row}–{next_row + len(rows_to_add) - 1})"
        )
    except Exception as exc:
        return False, f"❌ Sheets error: {exc}"


# ============================================================
# SESSION STATE INIT
# ============================================================
for _key, _default in [
    ("chunks",       None),
    ("raw_response", ""),
    ("last_topic",   ""),
]:
    if _key not in st.session_state:
        st.session_state[_key] = _default


# ============================================================
# SIDEBAR — CONFIGURATION
# ============================================================
with st.sidebar:
    st.markdown("## ⚙️ Configuration")

    # ── Provider & Model ──────────────────────────────────
    st.markdown("### 🤖 AI Provider & Model")
    provider = st.selectbox(
        "Provider",
        list(MODEL_OPTIONS.keys()),
    )
    model_choice = st.selectbox("Model", MODEL_OPTIONS[provider])

    # ── API Key (label adapts to provider) ───────────────
    st.markdown("### 🔑 API Key")
    _key_meta = {
        "Claude (via PageGrid)": ("PageGrid API Key",  "sk-pgrid-…",  "pagegrid.in/dashboard"),
        "OpenAI (GPT)":          ("OpenAI API Key",    "sk-…",        "platform.openai.com"),
        "Google (Gemini)":       ("Google AI API Key", "AIzaSy…",     "aistudio.google.com"),
    }
    _lbl, _ph, _hlp = _key_meta[provider]
    api_key = st.text_input(_lbl, type="password", placeholder=_ph, help=f"Get from {_hlp}")
    if api_key:
        st.success("🔐 Key loaded (session only)")

    st.divider()

    # ── Google Sheets Credentials ─────────────────────────
    st.markdown("### 📊 Google Sheets Credentials")
    st.caption("Needed only for **Push to Sheets**. Service Account JSON from Google Cloud Console.")
    creds_option = st.radio(
        "Credentials input",
        ["Upload JSON file", "Paste JSON text"],
        horizontal=True,
    )
    gsheet_creds_str = ""

    if creds_option == "Upload JSON file":
        _uploaded = st.file_uploader("Service Account JSON", type=["json"])
        if _uploaded:
            gsheet_creds_str = _uploaded.read().decode("utf-8")
            st.success("✅ Credentials loaded")
    else:
        _pasted = st.text_area(
            "Paste JSON here",
            height=110,
            placeholder='{"type": "service_account", ...}',
        )
        if _pasted.strip():
            try:
                json.loads(_pasted)
                gsheet_creds_str = _pasted
                st.success("✅ Valid JSON")
            except Exception:
                st.error("❌ Invalid JSON — please check")

    st.divider()
    st.markdown("### ℹ️ About")
    st.caption(f"**SCRIPT ENGINE v2.0** · SKY Academy Internal Tool")
    st.caption(f"Each segment ≈ {WORDS_PER_SEGMENT} words ≈ ~55 sec of speech")
    st.caption(
        f"🔗 [Open Target Sheet](https://docs.google.com/spreadsheets"
        f"/d/{SHEET_ID}/edit#gid=0)"
    )


# ============================================================
# MAIN LAYOUT — Input + Preview
# ============================================================
left, right = st.columns([1, 1], gap="large")

# ── LEFT : Inputs ─────────────────────────────────────────
with left:
    st.markdown("## 📝 Script Parameters")

    topic = st.text_area(
        "📌 Topic / Subject *",
        placeholder=(
            "e.g.  Panchayati Raj – 73rd Amendment\n"
            "       Photosynthesis Process\n"
            "       Types of Soil in India\n"
            "       Indian Constitution Preamble"
        ),
        height=110,
    )

    # ── Word count → auto segments ────────────────────────
    approx_words = st.number_input(
        "📝 Approx Total Script Words",
        min_value=120,
        max_value=6000,
        value=600,
        step=120,
        help=(
            f"System auto-splits into segments of ~{WORDS_PER_SEGMENT} words each "
            f"(~55 sec/segment). 600 words → 5 segments → ~5 min video."
        ),
    )
    num_segs = max(1, math.ceil(approx_words / WORDS_PER_SEGMENT))
    est_dur  = round(approx_words / 130, 1)

    st.markdown(
        f'<div class="word-info">'
        f'🎬 <b>{num_segs} segments</b> will be generated &nbsp;·&nbsp; '
        f'~{approx_words} words &nbsp;·&nbsp; ⏱ ~{est_dur} min video'
        f'</div>',
        unsafe_allow_html=True,
    )

    special_instructions = st.text_area(
        "🎯 Special Instructions  (optional)",
        placeholder=(
            "Focus on memory tricks\n"
            "Target audience: UPSC aspirants\n"
            "Include all Article numbers\n"
            "Add comparison table in slide 3\n"
            "Include free PDF CTA"
        ),
        height=90,
    )

    c1, c2 = st.columns(2)
    with c1:
        gen_btn = st.button("🚀 Generate Script", type="primary", use_container_width=True)
    with c2:
        clear_btn = st.button("🗑️ Clear All", use_container_width=True)


# ── Clear handler ──────────────────────────────────────────
if clear_btn:
    st.session_state.chunks       = None
    st.session_state.raw_response = ""
    st.session_state.last_topic   = ""
    st.rerun()


# ── Generate handler ──────────────────────────────────────
if gen_btn:
    if not topic.strip():
        st.error("❌ Please enter a topic!")
    elif not api_key.strip():
        st.error("❌ Please enter your API key in the sidebar!")
    else:
        with st.spinner(
            f"✍️ Generating {num_segs} segments… (may take 20–60 s for longer scripts)"
        ):
            try:
                system_p, user_p = build_messages(topic, num_segs, special_instructions)

                if   "PageGrid" in provider:
                    raw = call_claude_pagegrid(api_key, model_choice, system_p, user_p)
                elif "OpenAI"   in provider:
                    raw = call_openai(api_key, model_choice, system_p, user_p)
                else:
                    raw = call_gemini(api_key, model_choice, system_p, user_p)

                st.session_state.raw_response = raw
                parsed = parse_segments(raw)

                if parsed:
                    st.session_state.chunks     = parsed
                    st.session_state.last_topic = topic.strip()
                    st.success(f"✅ {len(parsed)} segments generated!")
                else:
                    st.error(
                        "❌ Could not parse JSON response. "
                        "Check **Raw AI Response** expander below."
                    )
            except Exception as exc:
                st.error(f"❌ Generation error: {exc}")


# ============================================================
# RIGHT : Preview
# ============================================================
with right:
    st.markdown("## 👁️ Preview")

    chunks = st.session_state.chunks

    if chunks:
        # ── Stats bar ──────────────────────────────────────
        total_words = sum(len(c.get("telugu_text", "").split()) for c in chunks)
        est_min     = round(total_words / 130, 1)
        st.markdown(
            f'<span class="stat-pill">📦 {len(chunks)} segments</span>'
            f'<span class="stat-pill">📝 ~{total_words} words</span>'
            f'<span class="stat-pill">⏱ ~{est_min} min video</span>',
            unsafe_allow_html=True,
        )
        st.markdown("")

        # ── Segment tabs (▶ 1, ▶ 2 … no "Chunk N" labels) ──
        tab_labels = [f"▶ {i + 1}" for i in range(len(chunks))]
        tabs = st.tabs(tab_labels)

        for tab, chunk, idx in zip(tabs, chunks, range(len(chunks))):
            with tab:
                st.markdown("**🎤 Voiceover Script**")
                st.text_area(
                    f"voiceover_label_{idx}",
                    value=chunk.get("telugu_text", ""),
                    height=220,
                    key=f"tv_{idx}",
                    label_visibility="collapsed",
                )
                st.markdown("**📋 Slide Prompt**")
                st.text_area(
                    f"slide_label_{idx}",
                    value=chunk.get("slide_prompt", ""),
                    height=130,
                    key=f"sv_{idx}",
                    label_visibility="collapsed",
                )

        # ── Full continuous script view ─────────────────────
        with st.expander("📜 Full Script — Continuous Flow", expanded=False):
            full_script = "\n\n".join(c.get("telugu_text", "") for c in chunks)
            st.text_area(
                "full_script_label",
                value=full_script,
                height=400,
                label_visibility="collapsed",
            )

        st.divider()

        # ── Action buttons ──────────────────────────────────
        ba, bb, bc = st.columns(3)

        with ba:
            json_bytes = json.dumps(chunks, ensure_ascii=False, indent=2).encode("utf-8")
            st.download_button(
                "⬇️ Download JSON",
                data=json_bytes,
                file_name=(
                    f"script_{st.session_state.last_topic[:20].replace(' ', '_')}.json"
                ),
                mime="application/json",
                use_container_width=True,
            )

        with bb:
            txt_content = "\n\n".join(
                f"--- ▶ {i + 1} ---\n{c.get('telugu_text', '')}\n\n"
                f"[Slide Prompt]\n{c.get('slide_prompt', '')}"
                for i, c in enumerate(chunks)
            )
            st.download_button(
                "⬇️ Download TXT",
                data=txt_content.encode("utf-8"),
                file_name=(
                    f"script_{st.session_state.last_topic[:20].replace(' ', '_')}.txt"
                ),
                mime="text/plain",
                use_container_width=True,
            )

        with bc:
            push_disabled = not bool(gsheet_creds_str.strip())
            push_btn = st.button(
                "📤 Push to Sheets",
                disabled=push_disabled,
                use_container_width=True,
                type="primary",
            )
            if push_disabled:
                st.caption("⚠️ Add Google creds in sidebar")

        if push_btn and gsheet_creds_str:
            with st.spinner("📤 Writing to Scripts_bot tab…"):
                ok, msg = push_to_gsheet(chunks, gsheet_creds_str)
                if ok:
                    st.success(msg)
                    st.markdown(
                        f"[🔗 Open Google Sheet](https://docs.google.com/spreadsheets"
                        f"/d/{SHEET_ID}/edit#gid=0)"
                    )
                else:
                    st.error(msg)

    else:
        st.markdown("""
        <div class="empty-preview">
            <h3>🎬 Preview will appear here</h3>
            <p style="margin-top:8px;">
                1. Enter topic &nbsp;→&nbsp;
                2. Set word count &nbsp;→&nbsp;
                3. Click <b>Generate Script</b>
            </p>
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# RAW RESPONSE DEBUG EXPANDER
# ============================================================
if st.session_state.raw_response:
    with st.expander("🔍 Raw AI Response  (debug / copy-paste fallback)"):
        st.code(st.session_state.raw_response, language="json")


# ============================================================
# FOOTER
# ============================================================
st.divider()
st.markdown(
    "<div style='text-align:center;color:#aaa;font-size:11px;'>"
    "SCRIPT ENGINE v2.0 &nbsp;|&nbsp; SKY Academy Internal Tool &nbsp;|&nbsp; Built with Streamlit"
    "</div>",
    unsafe_allow_html=True,
)
