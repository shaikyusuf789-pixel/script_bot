# ============================================================
# SCRIPT_ENGINE.py — SKY Academy Video Script Generator v2.1
# Three Input Modes: Topic | Competitor Transcript | Book PDF
# SKY Academy Internal Tool
# ============================================================

import streamlit as st
import json
import re
import math
import io

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
    .source-badge-topic      { background:#dbeafe; color:#1e40af; border-radius:8px; padding:4px 12px; font-size:0.8rem; font-weight:700; }
    .source-badge-transcript { background:#fef3c7; color:#92400e; border-radius:8px; padding:4px 12px; font-size:0.8rem; font-weight:700; }
    .source-badge-pdf        { background:#d1fae5; color:#065f46; border-radius:8px; padding:4px 12px; font-size:0.8rem; font-weight:700; }
    .word-info {
        background: #f0edff;
        border-left: 4px solid #302b63;
        padding: 10px 14px;
        border-radius: 0 8px 8px 0;
        font-size: 0.85rem;
        color: #302b63;
        margin: 4px 0 10px 0;
    }
    .mode-info-topic {
        background: #eff6ff;
        border-left: 4px solid #3b82f6;
        padding: 10px 14px;
        border-radius: 0 8px 8px 0;
        font-size: 0.83rem;
        color: #1e40af;
        margin-bottom: 12px;
    }
    .mode-info-transcript {
        background: #fffbeb;
        border-left: 4px solid #f59e0b;
        padding: 10px 14px;
        border-radius: 0 8px 8px 0;
        font-size: 0.83rem;
        color: #92400e;
        margin-bottom: 12px;
    }
    .mode-info-pdf {
        background: #ecfdf5;
        border-left: 4px solid #10b981;
        padding: 10px 14px;
        border-radius: 0 8px 8px 0;
        font-size: 0.83rem;
        color: #065f46;
        margin-bottom: 12px;
    }
    .warn-box {
        background: #fff7ed;
        border-left: 4px solid #ea580c;
        padding: 8px 12px;
        border-radius: 0 8px 8px 0;
        font-size: 0.82rem;
        color: #9a3412;
        margin-top: 6px;
    }
    .empty-preview {
        background: #f0f2f6;
        border: 2px dashed #ccc;
        border-radius: 12px;
        padding: 60px 20px;
        text-align: center;
        color: #999;
    }
    .key-ok   { color: #0da271; font-size: 11px; margin-top: -6px; }
    .key-warn { color: #f59e0b; font-size: 11px; margin-top: -6px; }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #302b63, #0f0c29) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────────────────────
st.markdown("""
<div class="header-box">
    <h1>🎬 SCRIPT ENGINE</h1>
    <p>SKY Academy · Telugu Video Script Generator · Internal Tool v2.1</p>
    <p style="font-size:0.78rem; color:#888; margin-top:6px;">
        📌 Topic &nbsp;|&nbsp; 📝 Competitor Transcript &nbsp;|&nbsp; 📚 Book PDF
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# CONSTANTS
# ============================================================
PAGEGRID_BASE_URL = "https://api.pagegrid.in"   # NO /v1 — SDK appends automatically
WORDS_PER_SEGMENT = 120                          # ~55 sec natural speech
MAX_INPUT_CHARS   = 80_000

SHEET_ID      = "1dNHDgkX6vhdhZSi5SavBgNihWe04zayRQwyMcCwNlOI"
SCRIPTS_TAB   = "Scripts_bot"
SHEET_HEADERS = ["Seg No.", "Telugu Text", "Slide Prompt",
                 "Audio Url", "Slide Url", "Status", "Audio Done"]

# ============================================================
# MODEL OPTIONS
# ============================================================
MODEL_OPTIONS = {
    "☁️  Claude  (via PageGrid)": [
        "claude-opus-4-6",
        "claude-sonnet-4-6",
        "claude-haiku-4-5",
    ],
    "🟢  OpenAI  (GPT)": [
        "o3",
        "o1",
        "gpt-4.5-preview",
        "gpt-4o",
    ],
    "🔵  Google  (Gemini)": [
        "gemini-2.5-pro",
        "gemini-2.0-pro-exp",
        "gemini-2.0-flash",
        "gemini-1.5-pro",
    ],
}

# ============================================================
# ════════════════════════════════════════════════════════════
#   SKY ACADEMY STYLE DNA  — shared across ALL three modes
# ════════════════════════════════════════════════════════════
# ============================================================

_SKY_DNA = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CORE PHILOSOPHY — READ THIS FIRST BEFORE ANYTHING ELSE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You are a REAL tutor from Andhra Pradesh standing in front of students.
You are NOT translating a textbook into Telugu.
You are NOT inserting Telugu words into an English sentence structure.
You are THINKING in Telugu first, then speaking.

THE MOST IMPORTANT RULE:
  MEANING COMES FIRST. STYLE COMES SECOND.
  
  Every sentence must mean something on its own.
  The student should be able to follow the LOGIC even if all delivery cues are removed.
  Never sacrifice the explanation for a connector phrase or a delivery cue.
  Never leave a gap in context between two sentences.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NATURAL AP TUTOR VOICE — EXPLICIT GOOD vs BAD EXAMPLES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BAD — bookish, translated, hollow, meaningless:
  ✗ "India ని Sovereign, Socialist, Secular, Democratic Republic గా చేయాలనుకున్నారు"
     → WHO wants this? WHY? When? The listener has zero context. Hollow sentence.
  ✗ "ఈ concept యొక్క importance అర్థం చేసుకోవాలంటే మనం history లోకి వెళ్ళాలి"
     → Filler opener. Just go into history — don't announce you're going.
  ✗ "Constitution రాయడానికి వారు నిర్ణయించుకున్నారు"
     → WHO is 'వారు'? WHY did they decide? This tells the student nothing.
  ✗ "ఇది చాలా ఇంపార్టెంట్ ఓకేనా" — said BEFORE showing why it's important
     → Hype without substance. Say it AFTER proving it's important.
  ✗ "ఇప్పుడు మనం ఈ topic గురించి చూద్దాం" — hollow filler transition
     → Just start explaining the topic. Don't announce it.

GOOD — natural, contextual, meaningful, AP tutor style:
  ✓ "సో friends — 1947 లో Independence వచ్చింది — great! కానీ ఇప్పుడు real problem వచ్చింది —
     ఈ దేశాన్ని ఎలా run చేయాలి? Power ఎవరి దగ్గర ఉంటుంది? Courts ఎలా work చేస్తాయి? 
     Rights ఏం ఉంటాయి? — ఇవన్నీ define చేయడానికే Constitution పుట్టింది, ఓకేనా!"
     
  ✓ "Sovereign అంటే — చాలా simple గా చెప్పాలంటే — మనం ఏ country కి bow చేయాల్సిన పని లేదు.
     America చెప్పినా, Britain చెప్పినా — India తన decisions తానే తీసుకుంటుంది. 
     That's what Sovereign means. Clear గా అర్థమైందా?"
     
  ✓ "ఇప్పుడు ఒక important question — UPSC 2019 లో exact గా ఇది అడిగారు — 
     Preamble లో Socialist, Secular అనే words originally ఉన్నాయా? — లేదు friends!
     1976 లో 42nd Amendment లో add చేశారు. Note it down!"
     
  ✓ "B.R. Ambedkar — ఈ person గురించి చెప్పాలంటే — రోజూ 18-20 గంటలు work చేశారు.
     2 సంవత్సరాలు, 11 మాసాలు, 17 రోజులు — just to give us a perfect Constitution.
     అందుకే ఆయన్ని Father of the Constitution అంటారు — అది empty title కాదు, deserve చేశారు!"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MEANING FLOW RULES — NON-NEGOTIABLE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. CONTEXT BEFORE CONTENT
   Always set up WHY before saying WHAT.
   BAD:  "42nd Amendment 1976 లో వచ్చింది"
   GOOD: "Emergency period లో — 1975-77 — Indira Gandhi government చాలా changes చేసింది
          Constitution లో. అందులో most controversial — 42nd Amendment. 
          దీన్నే Mini Constitution అని కూడా అంటారు — ఎందుకంటే ఇందులో..."

2. NEVER LEAVE A GAP
   Each sentence must logically connect to the next.
   The student should never think "wait, ఇది ఎక్కడ నుండి వచ్చింది?"

3. EXPLAIN, DON'T JUST STATE
   BAD:  "Preamble is the soul of the Constitution"
   GOOD: "Preamble ని soul of the Constitution అంటారు — why? Because ఇది చదివితే
          మొత్తం Constitution ఎందుకు రాశారు, దేని కోసం రాశారు అనేది 3 minutes లో అర్థమవుతుంది.
          Any judge, any lawyer — confusion వచ్చినప్పుడు Preamble చూస్తారు."

4. RHETORICAL QUESTIONS MUST HAVE IMMEDIATE ANSWERS
   Don't ask a question and then forget it.
   BAD:  "ఎందుకు ఇది important అని అడిగారా? సో ఇప్పుడు మనం చూద్దాం..."
   GOOD: "ఎందుకు important? — Because ఈ ఒక్క word — Secular — 
          India లో religion-based discrimination illegal చేసింది. Simple గా!"

5. DELIVERY CUES ARE SEASONING — NOT THE MEAL
   Sprinkle [Energetic], [Whisper/Secret Tip] etc. naturally where they genuinely fit.
   DO NOT insert them just to "look like SKY style."
   Never add a cue if it interrupts the meaning flow.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DELIVERY CUES — use only where they genuinely fit
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Energetic]  [Serious]  [Whisper/Secret Tip]  [High Pitch]
[Laughing]   [Deep Pause]  [Assertive]  [Calm, Instructional]
[WARM, FRIENDLY — WELCOME]

CONNECTOR PHRASES — weave naturally, never force:
"ఓకేనా"  "ఓకే రైట్"  "అవునా కాదా"  "చాలా ఇంపార్టెంట్"
"తెలుసు కదా"  "మీకు తెలుసు కదా"  "Clear గా అర్థమైందా?"
"లెట్స్ గో"  "నోట్ ఇట్ డౌన్"

LANGUAGE STYLE:
• Telugu + English natural mix — technical/exam terms in English, explanation in Telugu
• Direct address: "మీరు", "మీకు", "friends", "చూడు"
• Light humor only when it fits — never forced
• Build suspense only when there's genuinely something to reveal

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MEMORY HINTS — STRICT RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generate ONLY when a fact is genuinely hard to remember.
The hint must be obvious and clever — never confusing.
  → "Fancy words = France"  (Liberty, Equality, Fraternity → France)
  → "42°C fever → Emergency → 42nd Amendment"
  → "పాన్ తినకూడదు → Japan"  (discipline → no pan → Japan)
SILENCE IS ALWAYS BETTER THAN A FORCED OR WEAK HINT.
Never generate a memory hint just to "look like SKY style."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STRICT RULES FOR ALL MODES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. NO bookish headings inside voiceover text (SECTION 1, CHAPTER, PART N, etc.)
2. NO "Part 1", "Segment 2", "Chapter N" labels anywhere in voiceover
3. Script flows as ONE continuous natural conversation
4. NEVER mention competitor channels, instructors, books, apps, courses by name
5. ONLY SKY Academy — weave "SKY Academy లో" naturally where it fits
6. LAST SEGMENT must close with SKY Academy CTA (given below in each prompt)
"""

_SKY_CTA = (
    "[Energetic] సో friends — ఈరోజు మనం {TOPIC} గురించి చాలా deep గా చూసుకున్నాం ఓకేనా. "
    "మీకు ఇంకా ఏ topic కావాలో, ఏ subject మీద video కావాలో — comment section లో చెప్పండి. "
    "నేను personally ప్రతి comment చదువుతాను and reply ఇస్తాను — ఇది నా word మీకు! "
    "Any doubts ఉన్నాయా? Comment below — I will answer each one personally!"
)

_OUTPUT_FORMAT = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTPUT FORMAT — STRICT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Return ONLY a valid JSON array. No preamble, no markdown fences, no explanations.

[
  {{
    "seg": 1,
    "telugu_text": "full voiceover text with [Delivery Cues] sprinkled naturally...",
    "slide_prompt": "Heading: Short Slide Title\\n• bullet 1\\n• bullet 2\\n• bullet 3\\nImage Prompt: cinematic visual description, color palette, mood"
  }},
  ...
]

• Each segment telugu_text ≈ {WORDS_PER_SEGMENT} words of natural spoken Telugu
• Generate exactly {NUM_SEGS} segments
• The script reads as ONE continuous natural conversation — no labels, no part numbers
• Every sentence must be meaningful and contextually connected to the next
• Closing CTA must appear in the last segment's telugu_text
"""


# ============================================================
# ════════════════════════════════════════════════════════════
#   THREE SYSTEM PROMPTS — ONE PER INPUT MODE
# ════════════════════════════════════════════════════════════
# ============================================================

# ── MODE 1: TOPIC → Generate Original Script ─────────────────
_SYSTEM_TOPIC = (
    "You are an expert Telugu video script writer for SKY Academy — "
    "India's leading competitive exam preparation YouTube channel in Telugu medium.\n\n"
    "Your job: Write a COMPLETE, ORIGINAL SKY Academy voiceover script on the given topic.\n"
    "Bring your full depth of knowledge — facts, context, exam angles, real-world examples.\n"
    "The student must feel excited and informed by the end of every single sentence.\n"
) + _SKY_DNA + _OUTPUT_FORMAT


# ── MODE 2: COMPETITOR TRANSCRIPT → SKY Style ────────────────
_SYSTEM_TRANSCRIPT = (
    "You are an expert Telugu video script writer for SKY Academy — "
    "India's leading competitive exam preparation YouTube channel in Telugu medium.\n\n"
    "Your job: TRANSFORM a competitor video transcript into a 100% original SKY Academy script.\n"
    "The output must feel like it was WRITTEN for SKY Academy from day one — not a conversion.\n"
    "The student must not be able to tell this was ever from a competitor.\n\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "TRANSFORMATION STEPS\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    "STEP 1 — STRIP ALL COMPETITOR TRACES (zero tolerance):\n"
    "• Delete: every competitor channel name, instructor name, brand, app, course, website, PDF\n"
    "• Delete: 'subscribe to us', 'our app', 'join our batch', 'download our material'\n"
    "• Delete: 'as explained by [name]', 'only at [channel]', 'exclusive to [brand]'\n"
    "• If transcript is in Hindi or English — translate to natural Telugu-English mix\n"
    "• Replace ALL 'our channel / our course / our content' → SKY Academy framing\n\n"
    "STEP 2 — ENRICH CONTENT (add at least 25% more value than the original):\n"
    "• Add extra facts, context, real-world examples the competitor missed\n"
    "• Add exam angles: 'UPSC లో ఇది ఇలా అడుగుతారు', 'Previous year question లో ఇలా వచ్చింది'\n"
    "• Deepen explanations — go beyond whatever surface level the competitor used\n"
    "• Add 'why this matters' and 'what changes because of this' for every key concept\n"
    "• Memory tricks only where genuinely useful — never forced\n\n"
    "STEP 3 — FULL SKY ACADEMY VOICE:\n"
    "• Apply all SKY style rules below — natural AP tutor, meaning first, style second\n"
    "• Weave in SKY Academy identity: 'SKY Academy లో మనం ఈ concept deeply చూద్దాం'\n"
) + _SKY_DNA + _OUTPUT_FORMAT


# ── MODE 3: BOOK PDF → SKY Style ─────────────────────────────
_SYSTEM_PDF = (
    "You are an expert Telugu video script writer for SKY Academy — "
    "India's leading competitive exam preparation YouTube channel in Telugu medium.\n\n"
    "Your job: CONVERT dry book or study material content into an engaging SKY Academy voiceover script.\n"
    "The student must feel like they are listening to a passionate, knowledgeable tutor — "
    "NOT a textbook being read aloud.\n"
    "If the student can tell you're reading from a book, you have failed.\n\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "CONVERSION STEPS\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    "STEP 1 — DESTROY THE BOOKISH TONE COMPLETELY:\n"
    "• Kill: passive voice, 'it is stated that', 'as per the above', 'according to the text'\n"
    "• Kill: long academic sentences — break into short punchy conversational phrases\n"
    "• Kill: dry definitions — replace with 'WHY this matters' and 'WHAT changes because of this'\n"
    "• Kill: numbered/bulleted book lists — convert into flowing spoken narrative\n"
    "• Kill: jargon — simplify without losing accuracy\n"
    "• Kill: book section headings inside voiceover — never mention 'Section 3.2' etc.\n\n"
    "STEP 2 — INJECT LIFE AND DEPTH:\n"
    "• Add real-world examples and relatable analogies for every major concept\n"
    "• Add exam angles: 'ఇది UPSC prelims లో exact గా ఇలా అడిగారు'\n"
    "• Add 'before vs after' storytelling for historical or policy topics\n"
    "• Add context: why was this law/event/concept created? Who opposed it? What changed?\n"
    "• Add connecting narrative — the student should feel the STORY, not just the facts\n"
    "• Memory tricks only where genuinely useful — never forced\n\n"
    "STEP 3 — FULL SKY ACADEMY VOICE:\n"
    "• Apply all SKY style rules below — natural AP tutor, meaning first, style second\n"
    "• The script should make someone who 'hates' the subject genuinely interested\n"
    "• Weave in SKY Academy identity naturally where it fits\n"
) + _SKY_DNA + _OUTPUT_FORMAT


# ============================================================
# PROMPT BUILDERS — ONE PER MODE
# ============================================================

def _inject_counts(system: str, num_segs: int) -> str:
    return (
        system
        .replace("{NUM_SEGS}", str(num_segs))
        .replace("{WORDS_PER_SEGMENT}", str(WORDS_PER_SEGMENT))
    )


def build_prompts_topic(topic: str, num_segs: int, special_instructions: str):
    system = _inject_counts(_SYSTEM_TOPIC, num_segs)
    si = f"\nSpecial Instructions:\n{special_instructions.strip()}" if special_instructions.strip() else ""
    user = (
        f"Generate a complete SKY Academy Telugu video script on:\n\n"
        f"**Topic:** {topic.strip()}\n"
        f"**Segments required:** {num_segs}\n"
        f"**Words per segment:** ~{WORDS_PER_SEGMENT}\n"
        f"{si}\n\n"
        f"REMINDERS:\n"
        f"- Natural AP tutor voice — meaning first, style second\n"
        f"- Context before content — set up WHY before saying WHAT\n"
        f"- Every sentence must be meaningful — no hollow fillers\n"
        f"- No bookish headings, no Part/Segment labels in voiceover\n"
        f"- Memory hints only where genuinely needed\n"
        f"- Last segment must have SKY Academy CTA\n"
        f"- Return ONLY valid JSON array, nothing else"
    )
    return system, user


def build_prompts_transcript(
    transcript: str, topic_hint: str, num_segs: int, special_instructions: str
):
    system = _inject_counts(_SYSTEM_TRANSCRIPT, num_segs)
    hint = f"\n**Topic context:** {topic_hint.strip()}" if topic_hint.strip() else ""
    si   = f"\nSpecial Instructions:\n{special_instructions.strip()}" if special_instructions.strip() else ""
    user = (
        f"Transform the competitor transcript below into a SKY Academy voiceover script.\n"
        f"**Segments required:** {num_segs}\n"
        f"**Words per segment:** ~{WORDS_PER_SEGMENT}\n"
        f"{hint}{si}\n\n"
        f"━━━ COMPETITOR TRANSCRIPT (start) ━━━\n"
        f"{transcript.strip()}\n"
        f"━━━ COMPETITOR TRANSCRIPT (end) ━━━\n\n"
        f"REMINDERS:\n"
        f"- Strip every single competitor brand/name trace — zero tolerance\n"
        f"- Add 25%+ more content value than the original\n"
        f"- Natural AP tutor voice — meaning first, no hollow filler sentences\n"
        f"- Last segment must have SKY Academy CTA\n"
        f"- Return ONLY valid JSON array, nothing else"
    )
    return system, user


def build_prompts_pdf(
    pdf_text: str, topic_hint: str, num_segs: int, special_instructions: str
):
    system = _inject_counts(_SYSTEM_PDF, num_segs)
    hint = f"\n**Topic / Chapter context:** {topic_hint.strip()}" if topic_hint.strip() else ""
    si   = f"\nSpecial Instructions:\n{special_instructions.strip()}" if special_instructions.strip() else ""
    user = (
        f"Convert the book/study material content below into a SKY Academy voiceover script.\n"
        f"**Segments required:** {num_segs}\n"
        f"**Words per segment:** ~{WORDS_PER_SEGMENT}\n"
        f"{hint}{si}\n\n"
        f"━━━ BOOK / STUDY MATERIAL CONTENT (start) ━━━\n"
        f"{pdf_text.strip()}\n"
        f"━━━ BOOK / STUDY MATERIAL CONTENT (end) ━━━\n\n"
        f"REMINDERS:\n"
        f"- Bookish tone must be completely destroyed — no trace of 'textbook reading'\n"
        f"- Every dry fact needs context, example, and 'why it matters'\n"
        f"- Natural AP tutor voice — meaning first, no hollow filler sentences\n"
        f"- Last segment must have SKY Academy CTA\n"
        f"- Return ONLY valid JSON array, nothing else"
    )
    return system, user


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================
def extract_pdf_text(file_bytes: bytes):
    """Returns (text, info_string) or (None, error_message)."""

    # 1. pypdf (modern)
    try:
        import pypdf
        reader = pypdf.PdfReader(io.BytesIO(file_bytes))
        pages  = [p.extract_text() for p in reader.pages if p.extract_text()]
        if pages:
            return "\n".join(pages).strip(), f"pypdf · {len(reader.pages)} pages"
    except ImportError:
        pass
    except Exception:
        pass

    # 2. PyPDF2 (legacy)
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        pages  = [p.extract_text() for p in reader.pages if p.extract_text()]
        if pages:
            return "\n".join(pages).strip(), f"PyPDF2 · {len(reader.pages)} pages"
    except ImportError:
        pass
    except Exception:
        pass

    # 3. pdfplumber
    try:
        import pdfplumber
        pages = []
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for pg in pdf.pages:
                t = pg.extract_text()
                if t:
                    pages.append(t)
        if pages:
            return "\n".join(pages).strip(), f"pdfplumber · {len(pages)} pages"
    except ImportError:
        pass
    except Exception:
        pass

    return None, "No PDF library found. Run: pip install pypdf"


# ============================================================
# AI CALL FUNCTIONS
# ============================================================

def call_claude_pagegrid(api_key: str, model: str, system: str, user: str) -> str:
    import anthropic
    if not api_key.startswith("sk-pgrid-"):
        raise ValueError(
            "PageGrid key must start with 'sk-pgrid-'. "
            "Get yours at pagegrid.in → Dashboard → API Keys."
        )
    client = anthropic.Anthropic(api_key=api_key, base_url=PAGEGRID_BASE_URL)
    resp   = client.messages.create(
        model=model, max_tokens=8192, system=system,
        messages=[{"role": "user", "content": user}],
    )
    return resp.content[0].text


def call_openai(api_key: str, model: str, system: str, user: str) -> str:
    import openai
    client = openai.OpenAI(api_key=api_key)
    is_reasoning = model.startswith("o1") or model.startswith("o3")
    if is_reasoning:
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


def call_gemini(api_key: str, model: str, system: str, user: str) -> str:
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    m    = genai.GenerativeModel(model_name=model, system_instruction=system)
    resp = m.generate_content(user)
    return resp.text


def parse_segments(raw: str):
    raw   = re.sub(r"```(?:json)?", "", raw).strip().rstrip("`").strip()
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
# GOOGLE SHEETS
# ============================================================
def push_to_gsheet(chunks: list, creds_json_str: str):
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        creds_data = json.loads(creds_json_str)
        scopes     = [
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
            [i + 1, c.get("telugu_text", ""), c.get("slide_prompt", ""), "", "", "pending", "no"]
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
_defaults = {
    "chunks":        None,
    "raw_response":  "",
    "last_topic":    "",
    "last_source":   "",
    "pdf_text":      "",
    "last_pdf_sig":  "",
    "last_pdf_lib":  "",
}
for _k, _v in _defaults.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    st.markdown("### 🤖 AI Provider & Model")
    provider     = st.selectbox("Provider", list(MODEL_OPTIONS.keys()))
    model_choice = st.selectbox("Model", MODEL_OPTIONS[provider])

    _key_meta = {
        "☁️  Claude  (via PageGrid)": ("PageGrid API Key",   "sk-pgrid-…", "pagegrid.in → Dashboard → API Keys",     "sk-pgrid-"),
        "🟢  OpenAI  (GPT)":          ("OpenAI API Key",     "sk-…",        "platform.openai.com → API Keys",         "sk-"),
        "🔵  Google  (Gemini)":        ("Google AI API Key",  "AIzaSy…",     "aistudio.google.com → Get API Key",      "AIzaSy"),
    }
    _lbl, _ph, _hlp, _prefix = _key_meta[provider]
    st.markdown(f"### 🔑 {_lbl}")
    st.caption(f"Get yours: {_hlp}")
    api_key = st.text_input(_lbl, type="password", placeholder=_ph, label_visibility="collapsed")
    if api_key:
        if api_key.startswith(_prefix):
            st.markdown('<p class="key-ok">✅ Key format looks valid</p>', unsafe_allow_html=True)
        else:
            st.markdown(
                f'<p class="key-warn">⚠️ Key should start with <code>{_prefix}</code></p>',
                unsafe_allow_html=True,
            )

    if "PageGrid" in provider:
        st.info(
            "**PageGrid valid models:**\n"
            "- `claude-opus-4-6` — Most intelligent\n"
            "- `claude-sonnet-4-6` — Fast & smart\n"
            "- `claude-haiku-4-5` — Fastest\n\n"
            "**base_url:** `https://api.pagegrid.in`\n"
            "(SDK auto-appends `/v1`)",
            icon="📋",
        )

    st.divider()
    st.markdown("### 📊 Google Sheets Credentials")
    st.caption("Needed only for Push to Sheets. Service Account JSON from Google Cloud.")
    creds_option = st.radio("Credentials input", ["Upload JSON file", "Paste JSON text"], horizontal=True)
    gsheet_creds_str = ""
    if creds_option == "Upload JSON file":
        _up = st.file_uploader("Service Account JSON", type=["json"])
        if _up:
            gsheet_creds_str = _up.read().decode("utf-8")
            st.success("✅ Credentials loaded")
    else:
        _paste = st.text_area("Paste JSON here", height=100, placeholder='{"type": "service_account", ...}')
        if _paste.strip():
            try:
                json.loads(_paste)
                gsheet_creds_str = _paste
                st.success("✅ Valid JSON")
            except Exception:
                st.error("❌ Invalid JSON")

    st.divider()
    st.caption("SCRIPT ENGINE v2.1 · SKY Academy Internal Tool")
    st.caption(f"Each segment ≈ {WORDS_PER_SEGMENT} words ≈ ~55 sec speech")
    st.caption(f"[🔗 Open Target Sheet](https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit)")


# ============================================================
# MAIN LAYOUT
# ============================================================
left, right = st.columns([1, 1], gap="large")

# ── Variable defaults (prevents NameError if no mode selected yet) ──
topic_input      = ""
topic_hint_input = ""
input_mode       = ""

with left:
    st.markdown("## 📝 Script Input")

    input_mode = st.radio(
        "✏️ What are you providing?",
        options=[
            "📌 Topic Name  →  Generate from Scratch",
            "📝 Competitor Transcript  →  Convert to SKY Style",
            "📚 Book / PDF Section  →  Convert to SKY Style",
        ],
    )
    st.markdown("---")

    # ════════════════════════════════════════════════════════
    # MODE 1 — TOPIC
    # ════════════════════════════════════════════════════════
    if input_mode.startswith("📌"):
        st.markdown("""
        <div class="mode-info-topic">
        🎯 <b>Topic Mode</b> — Type any subject. SKY Engine generates a complete original
        voiceover script from scratch with exam angles, real-world examples, memory tricks,
        and full natural AP tutor voice.
        </div>""", unsafe_allow_html=True)

        topic_input = st.text_area(
            "📌 Topic / Subject *",
            placeholder=(
                "e.g.  Panchayati Raj – 73rd Amendment\n"
                "       Photosynthesis Process\n"
                "       Types of Soil in India\n"
                "       Indian Constitution Preamble"
            ),
            height=130,
        )
        topic_hint_input = ""

    # ════════════════════════════════════════════════════════
    # MODE 2 — COMPETITOR TRANSCRIPT
    # ════════════════════════════════════════════════════════
    elif input_mode.startswith("📝"):
        st.markdown("""
        <div class="mode-info-transcript">
        🔄 <b>Transcript Mode</b> — Paste any competitor video transcript (Telugu / Hindi / English).<br>
        SKY Engine will: ① wipe all competitor branding completely,
        ② enrich content by +25%, ③ rewrite in natural SKY Academy AP tutor voice.
        </div>""", unsafe_allow_html=True)

        topic_hint_input = st.text_input(
            "📌 Topic hint  (optional — helps generate accurate slide prompts)",
            placeholder="e.g.  73rd Amendment, Photosynthesis, Preamble...",
        )
        topic_input = st.text_area(
            "📝 Paste Competitor Transcript here *",
            placeholder=(
                "Paste the full transcript here...\n\n"
                "✅ Works in Telugu, Hindi, or English\n"
                "✅ Competitor names / brands will be completely removed\n"
                "✅ Content enriched and rewritten in SKY Academy voice"
            ),
            height=230,
        )
        if topic_input:
            wc = len(topic_input.split())
            cc = len(topic_input)
            st.caption(f"📊 Input: ~{wc} words · {cc:,} chars")
            if cc > MAX_INPUT_CHARS:
                st.markdown(
                    f'<div class="warn-box">⚠️ Very long input ({cc:,} chars). '
                    f'Trim to key sections to stay within model context window.</div>',
                    unsafe_allow_html=True,
                )

    # ════════════════════════════════════════════════════════
    # MODE 3 — BOOK PDF
    # ════════════════════════════════════════════════════════
    else:
        st.markdown("""
        <div class="mode-info-pdf">
        📚 <b>PDF Mode</b> — Upload a book chapter or study notes PDF.
        SKY Engine extracts the text and transforms dry academic content into
        a fully engaging SKY Academy voiceover — zero bookish tone, pure AP tutor energy.
        </div>""", unsafe_allow_html=True)

        topic_hint_input = st.text_input(
            "📌 Topic / Chapter context  (optional)",
            placeholder="e.g.  Chapter 3: Directive Principles, Unit 5: Cell Respiration...",
        )

        pdf_file   = st.file_uploader(
            "📤 Upload PDF *",
            type=["pdf"],
            help="Upload the book section, study notes, or chapter you want scripted",
        )
        topic_input = ""

        if pdf_file is not None:
            file_bytes = pdf_file.read()
            file_sig   = f"{pdf_file.name}_{len(file_bytes)}"

            if file_sig != st.session_state.last_pdf_sig:
                with st.spinner("🔍 Extracting text from PDF..."):
                    extracted, lib_info = extract_pdf_text(file_bytes)
                    if extracted:
                        st.session_state.pdf_text     = extracted
                        st.session_state.last_pdf_sig = file_sig
                        st.session_state.last_pdf_lib = lib_info
                    else:
                        st.session_state.pdf_text     = ""
                        st.session_state.last_pdf_sig = ""
                        st.error(f"❌ Could not extract PDF text. {lib_info}")

            if st.session_state.pdf_text:
                wc = len(st.session_state.pdf_text.split())
                cc = len(st.session_state.pdf_text)
                st.success(f"✅ Extracted: ~{wc} words · {st.session_state.last_pdf_lib}")
                if cc > MAX_INPUT_CHARS:
                    st.markdown(
                        f'<div class="warn-box">⚠️ PDF is very long ({cc:,} chars). '
                        f'Only the first {MAX_INPUT_CHARS:,} chars will be sent to the model. '
                        f'Upload one chapter at a time for best results.</div>',
                        unsafe_allow_html=True,
                    )
                with st.expander("👁️ Preview extracted text", expanded=False):
                    st.text(st.session_state.pdf_text[:800] + "\n\n[... more ...]")
                topic_input = st.session_state.pdf_text

    # ── Word count / segments ────────────────────────────
    st.markdown("---")
    approx_words = st.number_input(
        "📝 Approximate Total Script Words",
        min_value=120, max_value=6000, value=600, step=120,
        help=f"Auto-splits into ~{WORDS_PER_SEGMENT}-word segments (~55 sec each). "
             "600 words → 5 segments → ~5 min video.",
    )
    num_segs = max(1, math.ceil(approx_words / WORDS_PER_SEGMENT))
    est_dur  = round(approx_words / 130, 1)
    st.markdown(
        f'<div class="word-info">'
        f'🎬 <b>{num_segs} segments</b> will be generated &nbsp;·&nbsp; '
        f'≈ {approx_words} words &nbsp;·&nbsp; ⏱ ≈ {est_dur} min video'
        f'</div>',
        unsafe_allow_html=True,
    )

    special_instructions = st.text_area(
        "🎯 Special Instructions  (optional)",
        placeholder=(
            "Focus on memory tricks\n"
            "Target: UPSC Mains aspirants\n"
            "Include all Article numbers\n"
            "Add free PDF CTA in last segment"
        ),
        height=80,
    )

    c1, c2 = st.columns(2)
    with c1:
        gen_btn   = st.button("🚀 Generate Script", type="primary", use_container_width=True)
    with c2:
        clear_btn = st.button("🗑️ Clear All", use_container_width=True)


# ── Clear ─────────────────────────────────────────────────
if clear_btn:
    for _k in list(_defaults.keys()):
        st.session_state[_k] = None if _k == "chunks" else ""
    st.rerun()


# ── Generate ──────────────────────────────────────────────
if gen_btn:
    # Determine mode
    if   input_mode.startswith("📌"): mode_name = "topic"
    elif input_mode.startswith("📝"): mode_name = "transcript"
    else:                              mode_name = "pdf"

    # Validation
    if not api_key.strip():
        st.error("❌ Please enter your API key in the sidebar!")
    elif mode_name == "topic" and not topic_input.strip():
        st.error("❌ Please enter a topic!")
    elif mode_name == "transcript" and not topic_input.strip():
        st.error("❌ Please paste a competitor transcript!")
    elif mode_name == "pdf" and not topic_input.strip():
        st.error("❌ Please upload a PDF. Make sure text was extracted successfully.")
    else:
        safe_input = topic_input[:MAX_INPUT_CHARS] if len(topic_input) > MAX_INPUT_CHARS else topic_input

        spinner_msg = {
            "topic":      f"✍️ Generating {num_segs} original segments via {'PageGrid → Claude' if 'PageGrid' in provider else provider.split()[1]}…",
            "transcript": f"🔄 Transforming transcript → SKY Academy voice…",
            "pdf":        f"📚 Converting PDF content → SKY Academy voice…",
        }[mode_name]

        with st.spinner(spinner_msg + " (20–90 sec)"):
            try:
                # Build mode-specific prompts
                if mode_name == "topic":
                    system_p, user_p = build_prompts_topic(safe_input, num_segs, special_instructions)
                    display_topic  = topic_input.strip()[:60]
                    display_source = "📌 Topic"

                elif mode_name == "transcript":
                    system_p, user_p = build_prompts_transcript(
                        safe_input, topic_hint_input, num_segs, special_instructions
                    )
                    display_topic  = topic_hint_input.strip()[:60] or "Competitor Transcript"
                    display_source = "📝 Transcript → SKY"

                else:
                    system_p, user_p = build_prompts_pdf(
                        safe_input, topic_hint_input, num_segs, special_instructions
                    )
                    display_topic  = topic_hint_input.strip()[:60] or "PDF Content"
                    display_source = "📚 PDF → SKY"

                # Call selected provider
                if   "PageGrid" in provider:
                    raw = call_claude_pagegrid(api_key, model_choice, system_p, user_p)
                elif "OpenAI"   in provider:
                    raw = call_openai(api_key, model_choice, system_p, user_p)
                else:
                    raw = call_gemini(api_key, model_choice, system_p, user_p)

                st.session_state.raw_response = raw
                parsed = parse_segments(raw)

                if parsed:
                    st.session_state.chunks      = parsed
                    st.session_state.last_topic  = display_topic
                    st.session_state.last_source = display_source
                    st.success(f"✅ {len(parsed)} segments generated! [{display_source}]")
                else:
                    st.error(
                        "❌ Could not parse JSON from AI response. "
                        "Expand **Raw AI Response** below to inspect and copy manually."
                    )

            except Exception as exc:
                err = str(exc)
                if "401" in err or "authentication_error" in err:
                    st.error(
                        "❌ **401 — Invalid API key.**\n\n"
                        "• PageGrid key must start with `sk-pgrid-`\n"
                        "• Regenerate at pagegrid.in → Dashboard → API Keys"
                    )
                elif "402" in err or "billing_error" in err:
                    st.error(
                        "❌ **402 — Wallet balance is $0.**\n\n"
                        "Add funds at pagegrid.in → Dashboard → Wallet & Billing"
                    )
                elif "404" in err or "not found or inactive" in err:
                    st.error(
                        f"❌ **404 — Model `{model_choice}` not found.**\n\n"
                        f"✅ Valid PageGrid models: `claude-opus-4-6`, `claude-sonnet-4-6`, `claude-haiku-4-5`"
                    )
                elif "403" in err or "permission_error" in err:
                    st.error(
                        "❌ **403 — Permission denied.**\n\n"
                        "Check key permissions in the PageGrid dashboard."
                    )
                elif "429" in err or "rate_limit" in err:
                    st.error(
                        "❌ **429 — Rate limited.**\n\n"
                        "Default limit: 10 RPM. Wait ~60 sec and retry."
                    )
                else:
                    st.error(f"❌ Generation error: {exc}")


# ============================================================
# RIGHT: PREVIEW
# ============================================================
with right:
    st.markdown("## 👁️ Preview")
    chunks = st.session_state.chunks

    if chunks:
        total_words = sum(len(c.get("telugu_text", "").split()) for c in chunks)
        est_min     = round(total_words / 130, 1)

        badge_class = {
            "📌 Topic":             "source-badge-topic",
            "📝 Transcript → SKY":  "source-badge-transcript",
            "📚 PDF → SKY":         "source-badge-pdf",
        }.get(st.session_state.last_source, "source-badge-topic")

        st.markdown(
            f'<span class="{badge_class}">{st.session_state.last_source}</span>&nbsp;&nbsp;'
            f'<span class="stat-pill">📦 {len(chunks)} segments</span>'
            f'<span class="stat-pill">📝 ~{total_words} words</span>'
            f'<span class="stat-pill">⏱ ~{est_min} min</span>',
            unsafe_allow_html=True,
        )
        st.markdown("")

        # ── Segment tabs ──────────────────────────────────
        tabs = st.tabs([f"▶ {i + 1}" for i in range(len(chunks))])
        for tab, chunk, idx in zip(tabs, chunks, range(len(chunks))):
            with tab:
                seg_words = len(chunk.get("telugu_text", "").split())
                st.caption(f"~{seg_words} words · ~{round(seg_words / 130, 1)} min")

                st.markdown("**🎤 Voiceover Script**")
                st.text_area(
                    f"vo_{idx}",
                    value=chunk.get("telugu_text", ""),
                    height=220,
                    key=f"tv_{idx}",
                    label_visibility="collapsed",
                )
                st.markdown("**📋 Slide Prompt**")
                st.text_area(
                    f"sl_{idx}",
                    value=chunk.get("slide_prompt", ""),
                    height=130,
                    key=f"sv_{idx}",
                    label_visibility="collapsed",
                )

        # ── Full continuous script ────────────────────────
        with st.expander("📜 Full Script — Continuous Flow", expanded=False):
            full = "\n\n".join(c.get("telugu_text", "") for c in chunks)
            st.text_area("full_script", value=full, height=400, label_visibility="collapsed")

        st.divider()

        # ── Action buttons ────────────────────────────────
        ba, bb, bc = st.columns(3)
        _fname = st.session_state.last_topic[:20].replace(" ", "_")

        with ba:
            st.download_button(
                "⬇️ Download JSON",
                data=json.dumps(chunks, ensure_ascii=False, indent=2).encode("utf-8"),
                file_name=f"sky_script_{_fname}.json",
                mime="application/json",
                use_container_width=True,
            )
        with bb:
            txt_out = "\n\n".join(
                f"--- ▶ {i + 1} ---\n{c.get('telugu_text', '')}\n\n"
                f"[Slide Prompt]\n{c.get('slide_prompt', '')}"
                for i, c in enumerate(chunks)
            )
            st.download_button(
                "⬇️ Download TXT",
                data=txt_out.encode("utf-8"),
                file_name=f"sky_script_{_fname}.txt",
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
                st.markdown(f"[🔗 Open Sheet](https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit)")
            else:
                st.error(msg)

    else:
        st.markdown("""
        <div class="empty-preview">
            <h3>🎬 Preview will appear here</h3>
            <p style="margin-top:12px; font-size:0.9rem;">
                Choose input mode → Provide content → Click <b>Generate Script</b>
            </p>
            <p style="margin-top:16px; font-size:0.82rem; line-height:2;">
                📌 <b>Topic</b> — Original script from any subject<br>
                📝 <b>Transcript</b> — Competitor video → SKY style<br>
                📚 <b>PDF</b> — Book content → SKY voiceover
            </p>
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# RAW RESPONSE DEBUG
# ============================================================
if st.session_state.raw_response:
    with st.expander("🔍 Raw AI Response  (debug / manual copy-paste fallback)", expanded=False):
        st.code(st.session_state.raw_response[:6000], language="json")


# ============================================================
# FOOTER
# ============================================================
st.divider()
st.markdown(
    "<div style='text-align:center;color:#aaa;font-size:11px;'>"
    "SCRIPT ENGINE v2.1 &nbsp;|&nbsp; SKY Academy Internal Tool &nbsp;|&nbsp; "
    "Powered by PageGrid + Anthropic SDK"
    "</div>",
    unsafe_allow_html=True,
)
