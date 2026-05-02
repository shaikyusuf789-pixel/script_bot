# ============================================================
# SCRIPT_ENGINE.py — SKY Academy Video Script Generator
# ============================================================

import streamlit as st
import json
import re

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
    .chunk-tab-content {
        background: #fafafa;
        border-left: 4px solid #302b63;
        padding: 14px;
        border-radius: 6px;
        margin-top: 8px;
    }
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
    .empty-preview {
        background: #f0f2f6;
        border: 2px dashed #ccc;
        border-radius: 12px;
        padding: 60px 20px;
        text-align: center;
        color: #999;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #302b63, #0f0c29);
        color: white;
        border: none;
        font-weight: 600;
    }
    div[data-testid="stExpander"] { border: 1px solid #e0e0e0; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────────────────────
st.markdown("""
<div class="header-box">
    <h1>🎬 SCRIPT ENGINE</h1>
    <p>SKY Academy · Telugu Video Script Generator · Internal Tool</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SYSTEM PROMPT  (Internal — not shown to user)
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
• Rhetorical questions to pull attention: "ఎప్పుడైనా ఆలోచించారా...?"
• Light humor: "[Laughing] వాళ్ళు అంత kind కాదు ఓకేనా — ఇది strategic necessity"

MEMORY HINTS STYLE:
Generate ONLY when a fact is genuinely hard to remember. Never force.
Pattern: Create a vivid, surprising, Telugu-English connection.
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

1. NO bookish section headings inside the voiceover script.
   WRONG ✗  "SECTION 1: THE PHILOSOPHY & THE FATHER"
   RIGHT  ✓  "[Energetic] సో ఇప్పుడు మనం చూద్దాం — ఈ concept యొక్క father ఎవరో తెలుసా?"

2. Transition between topics naturally using phrases like:
   "సో ఇప్పుడు మనం next important point కి వెళ్దాం ఓకేనా"
   "ఇప్పుడు [topic] చూద్దాం — ఇది చాలా ఇంపార్టెంట్"
   "సో ఇప్పుడు [topic] గురించి మాట్లాడుకుందాం"

3. NEVER mention any competitor academy, coaching center, or book name.

4. ONLY SKY Academy is your home — if any reference needed, say "SKY Academy లో".

5. NO promises about free materials, PDFs, or upcoming courses
   UNLESS the Special Instructions box explicitly says to include them.

6. LAST CHUNK must always end with this exact closing CTA (adapt naturally):
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
    "chunk_no": 1,
    "telugu_text": "full voiceover script with [Delivery Cues] inline...",
    "slide_prompt": "Heading: Short Title Here\\n• bullet 1\\n• bullet 2\\n• bullet 3\\n• bullet 4\\n• bullet 5\\nImage Prompt: detailed cinematic image description, color palette, mood"
  },
  ...
]

Each chunk telugu_text = 150–250 words of natural speech.
Generate exactly {NUM_CHUNKS} chunks.
"""


# ============================================================
# GENERATION HELPERS
# ============================================================

def build_messages(topic: str, num_chunks: int, special_instructions: str) -> tuple[str, str]:
    system = SYSTEM_PROMPT.replace("{NUM_CHUNKS}", str(num_chunks))
    si_block = f"\nSpecial Instructions from creator:\n{special_instructions.strip()}" if special_instructions.strip() else ""
    user = (
        f"Generate a complete SKY Academy Telugu video script on:\n\n"
        f"**Topic:** {topic.strip()}\n"
        f"**Chunks required:** {num_chunks}\n"
        f"{si_block}\n\n"
        f"Strict reminder:\n"
        f"- No bookish headings inside voiceover\n"
        f"- Memory hints only where truly needed\n"
        f"- No competitor/book names\n"
        f"- Last chunk must have comment CTA\n"
        f"- Return ONLY valid JSON array"
    )
    return system, user


def call_claude(api_key: str, model: str, system: str, user: str) -> str:
    import anthropic
    client = anthropic.Anthropic(api_key=api_key)
    resp = client.messages.create(
        model=model,
        max_tokens=8192,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return resp.content[0].text


def call_openai(api_key: str, model: str, system: str, user: str) -> str:
    import openai
    client = openai.OpenAI(api_key=api_key)
    resp = client.chat.completions.create(
        model=model,
        max_tokens=8192,
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": user},
        ],
    )
    return resp.choices[0].message.content


def call_gemini(api_key: str, model: str, system: str, user: str) -> str:
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    m = genai.GenerativeModel(model_name=model, system_instruction=system)
    resp = m.generate_content(user)
    return resp.text


def parse_chunks(raw: str):
    """Extract JSON array from AI response (handles markdown fences)."""
    # Strip ```json ... ``` fences
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
SHEET_ID      = "1dNHDgkX6vhdhZSi5SavBgNihWe04zayRQwyMcCwNlOI"
SCRIPTS_TAB   = "Scripts_bot"
SHEET_HEADERS = ["Chunk No.", "Telugu Text", "Slide Prompt",
                 "Audio Url", "Slide Url", "Status", "Audio Done"]


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

        # Ensure header row
        existing = ws.get_all_values()
        if not existing or existing[0] != SHEET_HEADERS:
            ws.insert_row(SHEET_HEADERS, 1)
            existing = ws.get_all_values()

        # Find first empty row (column A)
        col_a      = ws.col_values(1)
        next_row   = len(col_a) + 1   # 1-indexed; row after last occupied

        rows_to_add = []
        for c in chunks:
            rows_to_add.append([
                c.get("chunk_no",    ""),
                c.get("telugu_text", ""),
                c.get("slide_prompt",""),
                "",          # Audio Url
                "",          # Slide Url
                "pending",   # Status
                "no",        # Audio Done
            ])

        ws.append_rows(rows_to_add, value_input_option="RAW")

        return True, (
            f"✅ {len(rows_to_add)} chunks pushed to **{SCRIPTS_TAB}** "
            f"(rows {next_row} – {next_row + len(rows_to_add) - 1})"
        )

    except Exception as exc:
        return False, f"❌ Sheets error: {exc}"


# ============================================================
# SESSION STATE INIT
# ============================================================
for key, default in [
    ("chunks",       None),
    ("raw_response", ""),
    ("last_topic",   ""),
]:
    if key not in st.session_state:
        st.session_state[key] = default


# ============================================================
# SIDEBAR — CONFIGURATION
# ============================================================
with st.sidebar:
    st.markdown("## ⚙️ Configuration")

    # ── Model selection ──────────────────────────────────
    st.markdown("### 🤖 AI Provider & Model")
    provider = st.selectbox(
        "Provider",
        ["Claude (Anthropic)", "OpenAI (GPT)", "Google (Gemini)"],
    )

    MODEL_OPTIONS = {
        "Claude (Anthropic)": [
            "claude-sonnet-4-5",
            "claude-3-5-haiku-20241022",
            "claude-opus-4-5",
        ],
        "OpenAI (GPT)": [
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-4-turbo",
        ],
        "Google (Gemini)": [
            "gemini-1.5-pro",
            "gemini-1.5-flash",
            "gemini-2.0-flash",
        ],
    }
    model_choice = st.selectbox("Model", MODEL_OPTIONS[provider])

    # ── API Key ──────────────────────────────────────────
    st.markdown("### 🔑 API Key")
    api_key = st.text_input(
        "Paste API Key",
        type="password",
        placeholder="sk-... | AIzaSy... | sk-ant-...",
        help="Key is never stored. Lives only in this session.",
    )
    if api_key:
        st.success("🔐 Key loaded (session only)")

    st.divider()

    # ── Google Sheets credentials ────────────────────────
    st.markdown("### 📊 Google Sheets Credentials")
    st.caption(
        "Needed only for **Push to Sheets**. "
        "Download Service Account JSON from Google Cloud Console."
    )
    creds_option = st.radio(
        "Credentials input",
        ["Upload JSON file", "Paste JSON text"],
        horizontal=True,
    )

    gsheet_creds_str = ""

    if creds_option == "Upload JSON file":
        uploaded = st.file_uploader("Service Account JSON", type=["json"])
        if uploaded:
            gsheet_creds_str = uploaded.read().decode("utf-8")
            st.success("✅ Credentials loaded")
    else:
        pasted = st.text_area(
            "Paste JSON here",
            height=120,
            placeholder='{"type": "service_account", ...}',
        )
        if pasted.strip():
            try:
                json.loads(pasted)   # validate
                gsheet_creds_str = pasted
                st.success("✅ Valid JSON")
            except Exception:
                st.error("❌ Invalid JSON — please check")

    st.divider()
    st.markdown("### ℹ️ About")
    st.caption("**SCRIPT ENGINE v1.0**\nSKY Academy Internal Tool")
    st.caption(
        "🔗 [Open Target Sheet](https://docs.google.com/spreadsheets"
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

    num_chunks = st.slider(
        "📦 Number of Chunks",
        min_value=2, max_value=12, value=4,
        help="Each chunk ≈ 150–250 words of voiceover (~1.5–2 min of video)",
    )

    special_instructions = st.text_area(
        "🎯 Special Instructions  (optional)",
        placeholder=(
            "Focus on memory tricks\n"
            "Target audience: UPSC aspirants\n"
            "Include all Article numbers\n"
            "Add comparison table in slide 3\n"
            "Include free PDF CTA"          # only if you type it
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
        with st.spinner("✍️ Generating script… (may take 20–40 s for longer scripts)"):
            try:
                system_p, user_p = build_messages(topic, num_chunks, special_instructions)

                if   "Claude"  in provider:
                    raw = call_claude (api_key, model_choice, system_p, user_p)
                elif "OpenAI"  in provider:
                    raw = call_openai (api_key, model_choice, system_p, user_p)
                else:
                    raw = call_gemini (api_key, model_choice, system_p, user_p)

                st.session_state.raw_response = raw
                parsed = parse_chunks(raw)

                if parsed:
                    st.session_state.chunks     = parsed
                    st.session_state.last_topic = topic.strip()
                    st.success(f"✅ {len(parsed)} chunks generated!")
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
        # ── Stats bar ──────────────────────────────────
        total_words = sum(len(c.get("telugu_text", "").split()) for c in chunks)
        est_min     = round(total_words / 130, 1)
        st.markdown(
            f'<span class="stat-pill">📦 {len(chunks)} chunks</span>'
            f'<span class="stat-pill">📝 ~{total_words} words</span>'
            f'<span class="stat-pill">⏱ ~{est_min} min video</span>',
            unsafe_allow_html=True,
        )
        st.markdown("")

        # ── Per-chunk tabs ──────────────────────────────
        tab_labels = [f"Chunk {c.get('chunk_no', i+1)}" for i, c in enumerate(chunks)]
        tabs = st.tabs(tab_labels)

        for tab, chunk, idx in zip(tabs, chunks, range(len(chunks))):
            with tab:
                st.markdown("**🎤 Voiceover Script**")
                st.text_area(
                    label=f"telugu_{idx}",
                    value=chunk.get("telugu_text", ""),
                    height=220,
                    key=f"tv_{idx}",
                    label_visibility="collapsed",
                )
                st.markdown("**📋 Slide Prompt**")
                st.text_area(
                    label=f"slide_{idx}",
                    value=chunk.get("slide_prompt", ""),
                    height=130,
                    key=f"sv_{idx}",
                    label_visibility="collapsed",
                )

        st.divider()

        # ── Action buttons ──────────────────────────────
        ba, bb = st.columns(2)

        with ba:
            json_bytes = json.dumps(chunks, ensure_ascii=False, indent=2).encode("utf-8")
            st.download_button(
                "⬇️ Download JSON",
                data=json_bytes,
                file_name=f"script_{st.session_state.last_topic[:25].replace(' ','_')}.json",
                mime="application/json",
                use_container_width=True,
            )

        with bb:
            push_disabled = not bool(gsheet_creds_str.strip())
            push_btn = st.button(
                "📤 Push to Google Sheets",
                disabled=push_disabled,
                use_container_width=True,
                type="primary",
            )
            if push_disabled:
                st.caption("⚠️ Add Google credentials in sidebar")

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
        # Empty state
        st.markdown("""
        <div class="empty-preview">
            <h3>🎬 Preview will appear here</h3>
            <p style="margin-top:8px;">
                1. Enter topic &nbsp;→&nbsp;
                2. Set chunks &nbsp;→&nbsp;
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
    "SCRIPT ENGINE v1.0 &nbsp;|&nbsp; SKY Academy Internal Tool &nbsp;|&nbsp; Built with Streamlit"
    "</div>",
    unsafe_allow_html=True,
)
