# ============================================================
# SCRIPT_ENGINE.py — SKY Academy Video Script Generator v3.0
# Three Input Modes: Topic | Multi-Transcript Merge | Book PDF
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
    page_title="🎬 SKY Academy – Script Engine",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────
# CUSTOM CSS — SKY Academy Branding
# ──────────────────────────────────────────────────────────
st.markdown("""
<style>
    .sky-header {
        background: linear-gradient(135deg, #020024 0%, #090979 40%, #00d4ff 100%);
        padding: 30px 20px 22px;
        border-radius: 18px;
        text-align: center;
        margin-bottom: 24px;
        border: 2px solid rgba(255, 215, 0, 0.55);
        box-shadow: 0 8px 48px rgba(0, 180, 255, 0.28), inset 0 0 80px rgba(0,0,0,0.25);
    }
    .sky-logo {
        font-size: 3.6rem; font-weight: 900;
        letter-spacing: 8px; margin: 0; line-height: 1;
    }
    .sky-s { color: #FF6B6B; text-shadow: 0 0 28px #FF6B6B, 0 0 56px rgba(255,107,107,0.45); }
    .sky-k { color: #FFE66D; text-shadow: 0 0 28px #FFE66D, 0 0 56px rgba(255,230,109,0.45); }
    .sky-y { color: #4ECDC4; text-shadow: 0 0 28px #4ECDC4, 0 0 56px rgba(78,205,196,0.45); }
    .sky-acad {
        color: rgba(255,255,255,0.92); font-size: 0.88rem;
        font-weight: 800; letter-spacing: 3px; margin: 4px 0 0;
        text-transform: uppercase;
    }
    .sky-tagline {
        color: #FFE66D; font-size: 1.55rem;
        font-weight: 800; margin: 10px 0 3px;
    }
    .sky-sub { color: rgba(185,225,255,0.88); font-size: 0.82rem; margin: 4px 0 12px; }
    .sky-pills { display: flex; justify-content: center; gap: 8px; flex-wrap: wrap; }
    .sky-pill {
        background: rgba(255,255,255,0.13); color: #fff;
        border: 1px solid rgba(255,255,255,0.28);
        border-radius: 20px; padding: 3px 14px;
        font-size: 0.74rem; font-weight: 600;
    }
    .mode-topic {
        background: linear-gradient(to right, #eff6ff, #dbeafe);
        border-left: 5px solid #3b82f6;
        padding: 12px 16px; border-radius: 0 10px 10px 0;
        font-size: 0.84rem; color: #1e40af; margin-bottom: 14px;
    }
    .mode-transcript {
        background: linear-gradient(to right, #fffbeb, #fef3c7);
        border-left: 5px solid #f59e0b;
        padding: 12px 16px; border-radius: 0 10px 10px 0;
        font-size: 0.84rem; color: #78350f; margin-bottom: 14px;
    }
    .mode-pdf {
        background: linear-gradient(to right, #ecfdf5, #d1fae5);
        border-left: 5px solid #10b981;
        padding: 12px 16px; border-radius: 0 10px 10px 0;
        font-size: 0.84rem; color: #065f46; margin-bottom: 14px;
    }
    .fcard-ok {
        background: #f0fdf4; border: 1px solid #86efac;
        border-radius: 10px; padding: 8px 14px; margin: 4px 0;
        font-size: 0.82rem; color: #14532d;
    }
    .fcard-err {
        background: #fff1f2; border: 1px solid #fca5a5;
        border-radius: 10px; padding: 8px 14px; margin: 4px 0;
        font-size: 0.82rem; color: #991b1b;
    }
    .merge-box {
        background: linear-gradient(to right, #fefce8, #fef9c3);
        border: 1px solid #fde047; border-radius: 10px;
        padding: 10px 14px; font-size: 0.83rem;
        color: #713f12; margin: 8px 0;
    }
    .stat-pill {
        display: inline-block;
        background: linear-gradient(135deg, #e8e0ff, #dbeafe);
        color: #302b63; border-radius: 20px;
        padding: 3px 12px; font-size: 0.8rem; margin: 2px; font-weight: 600;
    }
    .badge-topic {
        background: linear-gradient(135deg,#3b82f6,#1d4ed8);
        color:#fff; border-radius:8px; padding:4px 12px;
        font-size:.8rem; font-weight:700;
    }
    .badge-transcript {
        background: linear-gradient(135deg,#f59e0b,#d97706);
        color:#fff; border-radius:8px; padding:4px 12px;
        font-size:.8rem; font-weight:700;
    }
    .badge-pdf {
        background: linear-gradient(135deg,#10b981,#059669);
        color:#fff; border-radius:8px; padding:4px 12px;
        font-size:.8rem; font-weight:700;
    }
    .word-info {
        background: linear-gradient(to right, #f0edff, #e8e0ff);
        border-left: 5px solid #302b63;
        padding: 10px 14px; border-radius: 0 10px 10px 0;
        font-size: 0.85rem; color: #302b63; margin: 4px 0 10px 0;
    }
    .stream-progress {
        background: linear-gradient(to right, #eff6ff, #dbeafe);
        border-left: 4px solid #3b82f6;
        padding: 10px 16px; border-radius: 0 10px 10px 0;
        font-size: 0.84rem; color: #1e40af; margin: 8px 0;
    }
    .empty-preview {
        background: linear-gradient(135deg, #f8faff, #f0f2f6);
        border: 2px dashed #c7d2fe;
        border-radius: 16px; padding: 60px 20px;
        text-align: center; color: #6366f1;
    }
    .key-ok   { color: #0da271; font-size: 11px; margin-top: -6px; }
    .key-warn { color: #f59e0b; font-size: 11px; margin-top: -6px; }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #302b63, #0f0c29) !important;
        color: white !important; border: none !important;
        font-weight: 600 !important; border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────────────────────
st.markdown("""
<div class="sky-header">
    <div class="sky-logo">
        <span class="sky-s">S</span><span class="sky-k">K</span><span class="sky-y">Y</span>
    </div>
    <div class="sky-acad">ACADEMY</div>
    <div class="sky-tagline">🎬 SCRIPT ENGINE v3.0</div>
    <div class="sky-sub">Telugu Video Script Generator &nbsp;·&nbsp; Internal Tool &nbsp;·&nbsp; AP Tutor Voice</div>
    <div class="sky-pills">
        <span class="sky-pill">📌 Topic → Original</span>
        <span class="sky-pill">📝 Multi-Transcript → Merge</span>
        <span class="sky-pill">📚 Book PDF → SKY Voice</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# CONSTANTS
# ============================================================
PAGEGRID_BASE_URL = "https://api.pagegrid.in"
WORDS_PER_SEGMENT = 120

SHEET_ID      = "1dNHDgkX6vhdhZSi5SavBgNihWe04zayRQwyMcCwNlOI"
SCRIPTS_TAB   = "Scripts_bot"
SHEET_HEADERS = ["Seg No.", "Telugu Text", "Slide Prompt",
                 "Audio Url", "Slide Url", "Status", "Audio Done"]

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
# SKY ACADEMY STYLE DNA
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
     → WHO wants this? WHY? WHEN? Zero context. Hollow sentence.
  ✗ "ఈ concept యొక్క importance అర్థం చేసుకోవాలంటే మనం history లోకి వెళ్ళాలి"
     → Filler opener. Just go into history — don't announce it.
  ✗ "Constitution రాయడానికి వారు నిర్ణయించుకున్నారు"
     → WHO is 'వారు'? WHY? This tells the student nothing.
  ✗ "ఇది చాలా ఇంపార్టెంట్ ఓకేనా" — said BEFORE proving why it's important.
  ✗ "ఇప్పుడు మనం ఈ topic గురించి చూద్దాం" — hollow transition; just start explaining.

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

1. CONTEXT BEFORE CONTENT — Always set up WHY before saying WHAT.
2. NEVER LEAVE A GAP — Each sentence must logically connect to the next.
3. EXPLAIN, DON'T JUST STATE
4. RHETORICAL QUESTIONS MUST HAVE IMMEDIATE ANSWERS
5. DELIVERY CUES ARE SEASONING — NOT THE MEAL

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DELIVERY CUES — use only where they genuinely fit
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Energetic]  [Serious]  [Whisper/Secret Tip]  [High Pitch]
[Laughing]   [Deep Pause]  [Assertive]  [Calm, Instructional]
[WARM, FRIENDLY — WELCOME]

CONNECTOR PHRASES — weave naturally, never force:
"ఓకేనా"  "ఓకే రైట్"  "అవునా కాదా"  "చాలా ఇంపార్టెంట్"
"తెలుసు కదా"  "మీకు తెలుసు కదా"  "Clear గా అర్థమైందా?"
"లెట్స్ గో"  "నోట్ ఇట్ డౌన్"  "Got it?"

LANGUAGE STYLE:
• Telugu + English natural mix — technical/exam terms in English, explanation in Telugu
• Direct address: "మీరు", "మీకు", "friends", "చూడు"
• Light humor only when it fits — never forced
• Build suspense only when there's genuinely something to reveal

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MEMORY HINTS — RICH EXAMPLES LIBRARY (SKY ACADEMY STYLE)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HOW SKY ACADEMY MEMORY HINTS WORK:
The hint must be: OBVIOUS → CLEVER → IMPOSSIBLE TO FORGET.
Student should laugh or say "oh wow, I'll never forget this!"
If you need to explain the hint, it is a BAD hint. Start over.

── POLITY / CONSTITUTION:
  → "Fancy words = France" (Liberty, Equality, Fraternity → French Revolution)
  → "42°C fever → Emergency → 42nd Amendment 1976"
  → "Article 21 — 21st birthday = LIFE's most important day → Right to LIFE & Liberty"
  → "DPSP = Doctor's Prescription → Non-justiciable"
  → "BRO wrote the Constitution → B.R. Ambedkar → Father of Constitution"
  → "CAG = 'Check And Guard' government money"
  → "Preamble = Entrance door of a house → tells you what's inside"
  → "73rd Amendment = Panchayati Raj → 7+3=10 → 10 fingers = hands-on local governance"
  → "Emergency Article 352 → 3-5-2 = three types: National, State, Financial"

── HISTORY / FREEDOM STRUGGLE:
  → "1857 = 18-57 → 57 year old person's first revolt = First War of Independence"
  → "Quit India 1942 → 9+4+2=15 → August 15 → Independence 1947!"
  → "Simon Commission = 1927 → No Indian members → 'Simon says' — but India says NO!"

── GEOGRAPHY:
  → "Narmada flows WEST → Flip 'N' sideways → looks like 'W' for West!"
  → "Thar Desert → 'Thar' sounds like 'Tar road' → hot, dry, burned = desert"

── SCIENCE / BIOLOGY:
  → "Mitochondria = Powerhouse → 'MITO' = 'My Toe' → your toe pushes you forward = POWER"
  → "Photosynthesis: everything is SIX → 6CO2 + 6H2O → C6H12O6 + 6O2"
  → "Noble Gases = 0 valency → Nobel Prize winners share NOTHING → zero sharing"

── ECONOMY / CURRENT AFFAIRS:
  → "GDP vs GNP: D = Domestic (inside India), N = National (Indians anywhere)"
  → "Repo Rate → 'REPO' = RBI REPOssesses money from banks"
  → "Inflation and Interest Rate: they're married → one goes up, other follows"

WHEN TO USE MEMORY HINTS:
✅ Number / date / name is genuinely hard to remember
✅ Hint is INSTANTLY obvious — no explanation needed
❌ Skip when the fact is already simple/memorable
❌ NEVER generate a forced or confusing hint
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STRICT RULES FOR ALL MODES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. NO bookish headings inside voiceover (SECTION 1, CHAPTER, PART N, etc.)
2. NO "Part 1", "Segment 2", "Chapter N" labels anywhere in voiceover
3. Script flows as ONE continuous natural conversation
4. NEVER mention competitor channels, instructors, books, apps, courses by name
5. ONLY SKY Academy — weave "SKY Academy లో" naturally where it fits
6. LAST SEGMENT must close with SKY Academy CTA
"""

_OUTPUT_FORMAT = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HOOK + WELCOME — MANDATORY FOR SEGMENT 1 ONLY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Segment 1 MUST ALWAYS open with:

① ONE POWERFUL HOOK LINE — stops the student from scrolling.
② WELCOME LINE — immediately follows:
   "[WARM, FRIENDLY — WELCOME] SKY Academy కి welcome friends! ఇక్కడ మీరు subject
    నేర్చుకోవడమే కాదు — exam కి forever memorise అవుతారు. [Energetic] Let's start
    with a smile and a like! 😊👍"
③ Then flow DIRECTLY into content — no transition filler.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CLOSING CTA — MANDATORY FOR LAST SEGMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Last segment must end with:
"[Energetic] సో friends — ఈరోజు మనం [TOPIC] గురించి చాలా deep గా చూసుకున్నాం ఓకేనా.
మీకు ఇంకా ఏ topic కావాలో, ఏ subject మీద video కావాలో — comment section లో చెప్పండి.
నేను personally ప్రతి comment చదువుతాను and reply ఇస్తాను — ఇది నా word మీకు!
Any doubts ఉన్నాయా? Comment below — I will answer each one personally!"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTPUT FORMAT — STRICT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Return ONLY a valid JSON array. No preamble, no markdown fences, no explanations.

[
  {{
    "seg": 1,
    "telugu_text": "full voiceover text — Hook → Welcome → content flow...",
    "slide_prompt": "Heading: Short Slide Title\\n• bullet 1\\n• bullet 2\\n• bullet 3\\nImage Prompt: cinematic visual, color palette, mood"
  }},
  ...
]

• Segment 1 telugu_text: Hook + Welcome + content (~{WORDS_PER_SEGMENT} words total)
• All other segments: ~{WORDS_PER_SEGMENT} words of natural spoken Telugu
• Generate exactly {NUM_SEGS} segments
• ONE continuous natural conversation — no labels, no part numbers
• Every sentence meaningful and logically connected to the next
• Memory hints sprinkled wherever genuinely useful
"""

# ============================================================
# THREE SYSTEM PROMPTS
# ============================================================

_SYSTEM_TOPIC = (
    "You are an expert Telugu video script writer for SKY Academy — "
    "India's leading competitive exam preparation YouTube channel in Telugu medium.\n\n"
    "Your job: Write a COMPLETE, ORIGINAL SKY Academy voiceover script on the given topic.\n"
    "Bring your full depth of knowledge — facts, context, exam angles, real-world examples.\n"
    "Use memory hints generously wherever a fact is genuinely hard to remember.\n"
    "The student must feel excited and informed by the end of every single sentence.\n"
) + _SKY_DNA + _OUTPUT_FORMAT


_SYSTEM_TRANSCRIPT = (
    "You are an expert Telugu video script writer for SKY Academy — "
    "India's leading competitive exam preparation YouTube channel in Telugu medium.\n\n"
    "Your job: TRANSFORM one or more competitor video transcripts into a single 100% original "
    "SKY Academy script.\n"
    "The output must feel like it was WRITTEN for SKY Academy from day one — not a conversion.\n"
    "The student must not be able to tell this was ever from a competitor.\n\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "MULTI-TRANSCRIPT ANALYSIS (do this BEFORE writing anything)\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    "CASE A — Same topic, different data: SYNTHESIZE all data, give full range.\n"
    "CASE B — Different aspects of same subject: MERGE and INTERLINK into one narrative.\n"
    "CASE C — Redundant content: Take BEST explanation from each, combine, enrich.\n\n"
    "Step 1 — STRIP ALL COMPETITOR TRACES (zero tolerance)\n"
    "Step 2 — ENRICH CONTENT (+25% minimum above all combined originals)\n"
    "Step 3 — FULL SKY ACADEMY VOICE\n"
) + _SKY_DNA + _OUTPUT_FORMAT


_SYSTEM_PDF = (
    "You are an expert Telugu video script writer for SKY Academy — "
    "India's leading competitive exam preparation YouTube channel in Telugu medium.\n\n"
    "Your job: CONVERT dry book or study material into an engaging SKY Academy voiceover.\n"
    "The student must feel like they're listening to a passionate knowledgeable tutor — "
    "NOT a textbook being read aloud.\n"
    "If the student can tell you're reading from a book, you have FAILED.\n\n"
    "Step 1 — DESTROY THE BOOKISH TONE COMPLETELY\n"
    "Step 2 — INJECT LIFE AND DEPTH\n"
    "Step 3 — FULL SKY ACADEMY VOICE\n"
) + _SKY_DNA + _OUTPUT_FORMAT


# ============================================================
# PROMPT BUILDERS
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
        f"- Segment 1: HOOK → Welcome → Content\n"
        f"- Natural AP tutor voice — meaning first, style second\n"
        f"- Memory hints generously wherever genuinely useful\n"
        f"- No bookish headings, no Part/Segment labels in voiceover\n"
        f"- Last segment must have SKY Academy CTA\n"
        f"- Return ONLY valid JSON array, nothing else"
    )
    return system, user


def build_prompts_multi_transcript(
    transcripts: list,
    topic_hint: str,
    num_segs: int,
    special_instructions: str,
    merge_mode: str = "auto",
):
    system = _inject_counts(_SYSTEM_TRANSCRIPT, num_segs)
    n      = len(transcripts)

    merge_guide = {
        "auto": (
            "AUTO-DETECT the relationship between the transcripts and apply the correct "
            "merge strategy (CASE A / B / C) as described in your instructions above."
        ),
        "synthesize": (
            "These transcripts COVER THE SAME TOPIC with different data or opinions. "
            "SYNTHESIZE all data points, present ranges, reconcile differences."
        ),
        "merge_aspects": (
            "These transcripts cover DIFFERENT ASPECTS of the same broad subject. "
            "MERGE and INTERLINK all aspects into one cohesive flowing narrative."
        ),
    }[merge_mode]

    hint = f"\n**Topic context:** {topic_hint.strip()}" if topic_hint.strip() else ""
    si   = f"\nSpecial Instructions:\n{special_instructions.strip()}" if special_instructions.strip() else ""

    transcript_blocks = "\n\n".join(
        f"━━━ COMPETITOR TRANSCRIPT {i + 1} of {n} ━━━\n"
        f"[File: {t['filename']}]\n"
        f"{t['text'].strip()}\n"
        f"━━━ END TRANSCRIPT {i + 1} ━━━"
        for i, t in enumerate(transcripts)
    )

    user = (
        f"Transform the {n} competitor transcript(s) below into a SINGLE SKY Academy voiceover.\n"
        f"**Segments required:** {num_segs}\n"
        f"**Words per segment:** ~{WORDS_PER_SEGMENT}\n"
        f"**Merge strategy:** {merge_guide}\n"
        f"{hint}{si}\n\n"
        f"{transcript_blocks}\n\n"
        f"REMINDERS:\n"
        f"- Segment 1: HOOK → Welcome → Content\n"
        f"- Strip EVERY competitor brand/name/CTA trace from ALL transcripts\n"
        f"- Add 25%+ more value through enrichment\n"
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
        f"Convert the book/study material below into a SKY Academy voiceover script.\n"
        f"**Segments required:** {num_segs}\n"
        f"**Words per segment:** ~{WORDS_PER_SEGMENT}\n"
        f"{hint}{si}\n\n"
        f"━━━ BOOK / STUDY MATERIAL (start) ━━━\n"
        f"{pdf_text.strip()}\n"
        f"━━━ BOOK / STUDY MATERIAL (end) ━━━\n\n"
        f"REMINDERS:\n"
        f"- Segment 1: HOOK → Welcome → Content\n"
        f"- Bookish tone must be completely destroyed\n"
        f"- Last segment must have SKY Academy CTA\n"
        f"- Return ONLY valid JSON array, nothing else"
    )
    return system, user


# ============================================================
# FILE TEXT EXTRACTION
# ============================================================

def extract_pdf_text(file_bytes: bytes):
    try:
        import pypdf
        reader = pypdf.PdfReader(io.BytesIO(file_bytes))
        pages  = [p.extract_text() for p in reader.pages if p.extract_text()]
        if pages:
            return "\n".join(pages).strip(), f"pypdf · {len(reader.pages)} pages"
    except (ImportError, Exception):
        pass
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        pages  = [p.extract_text() for p in reader.pages if p.extract_text()]
        if pages:
            return "\n".join(pages).strip(), f"PyPDF2 · {len(reader.pages)} pages"
    except (ImportError, Exception):
        pass
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
    except (ImportError, Exception):
        pass
    return None, "No PDF library. Run: pip install pypdf"


def extract_docx_text(file_bytes: bytes):
    try:
        from docx import Document
        doc   = Document(io.BytesIO(file_bytes))
        parts = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        for tbl in doc.tables:
            for row in tbl.rows:
                for cell in row.cells:
                    if cell.text.strip():
                        parts.append(cell.text.strip())
        text = "\n".join(parts)
        if text.strip():
            return text.strip(), f"python-docx · {len(doc.paragraphs)} paragraphs"
        return None, "DOCX file appears to be empty or image-only"
    except ImportError:
        return None, "python-docx not installed. Run: pip install python-docx"
    except Exception as exc:
        return None, f"DOCX error: {exc}"


def extract_any_file(file_bytes: bytes, filename: str):
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext == "txt":
        for enc in ("utf-8", "utf-16", "latin-1"):
            try:
                text = file_bytes.decode(enc)
                if text.strip():
                    return text.strip(), f"TXT · {len(text.split())} words"
            except Exception:
                pass
        return None, "Could not decode TXT file"
    elif ext == "docx":
        return extract_docx_text(file_bytes)
    elif ext == "pdf":
        return extract_pdf_text(file_bytes)
    return None, f"Unsupported file type: .{ext}"


# ============================================================
# ✅ AI CALL FUNCTIONS — ALL USE STREAMING (fixes 524 timeout)
# ============================================================

def call_claude_pagegrid(
    api_key: str, model: str, system: str, user: str, progress_cb=None
) -> str:
    """Stream via Anthropic SDK — keeps connection alive, prevents 524."""
    import anthropic
    if not api_key.startswith("sk-pgrid-"):
        raise ValueError(
            "PageGrid key must start with 'sk-pgrid-'. "
            "Get yours at pagegrid.in → Dashboard → API Keys."
        )
    client = anthropic.Anthropic(
        api_key=api_key,
        base_url=PAGEGRID_BASE_URL,
        timeout=300.0,          # 5-minute hard timeout on the SDK side
    )
    full = ""
    with client.messages.stream(
        model=model,
        max_tokens=8192,
        system=system,
        messages=[{"role": "user", "content": user}],
    ) as stream:
        for chunk in stream.text_stream:
            full += chunk
            if progress_cb:
                progress_cb(len(full))
    return full


def call_openai(
    api_key: str, model: str, system: str, user: str, progress_cb=None
) -> str:
    """Stream via OpenAI SDK (reasoning models fall back to non-stream)."""
    import openai
    client       = openai.OpenAI(api_key=api_key, timeout=300.0)
    is_reasoning = model.startswith("o1") or model.startswith("o3")

    if is_reasoning:
        # o-series models don't support streaming — use regular call
        resp = client.chat.completions.create(
            model=model,
            max_completion_tokens=16000,
            messages=[{"role": "user", "content": f"{system}\n\n---\n\n{user}"}],
        )
        return resp.choices[0].message.content
    else:
        full = ""
        for chunk in client.chat.completions.create(
            model=model,
            max_tokens=8192,
            stream=True,
            messages=[
                {"role": "system", "content": system},
                {"role": "user",   "content": user},
            ],
        ):
            delta = chunk.choices[0].delta.content or ""
            full += delta
            if progress_cb and delta:
                progress_cb(len(full))
        return full


def call_gemini(
    api_key: str, model: str, system: str, user: str, progress_cb=None
) -> str:
    """Stream via Google Generative AI SDK."""
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    m    = genai.GenerativeModel(model_name=model, system_instruction=system)
    full = ""
    for chunk in m.generate_content(user, stream=True):
        t = getattr(chunk, "text", "") or ""
        full += t
        if progress_cb and t:
            progress_cb(len(full))
    return full


# ============================================================
# STREAMING DISPATCHER — single entry point for all providers
# ============================================================

def run_generation(
    api_key: str,
    provider: str,
    model: str,
    system_p: str,
    user_p: str,
    status_placeholder,
) -> str:
    """
    Call the correct provider with streaming.
    Updates status_placeholder with live char count.
    Returns raw text string.
    """
    def _cb(n_chars: int):
        status_placeholder.markdown(
            f'<div class="stream-progress">'
            f'⚡ <b>Generating…</b> &nbsp; {n_chars:,} characters received'
            f' &nbsp;·&nbsp; please keep this tab open'
            f'</div>',
            unsafe_allow_html=True,
        )

    if "PageGrid" in provider:
        return call_claude_pagegrid(api_key, model, system_p, user_p, _cb)
    elif "OpenAI" in provider:
        return call_openai(api_key, model, system_p, user_p, _cb)
    else:
        return call_gemini(api_key, model, system_p, user_p, _cb)


# ============================================================
# JSON PARSER
# ============================================================

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
        creds = Credentials.from_service_account_info(creds_data, scopes=scopes)
        gc    = gspread.authorize(creds)
        sheet = gc.open_by_key(SHEET_ID)
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
            [i + 1, c.get("telugu_text", ""), c.get("slide_prompt", ""),
             "", "", "pending", "no"]
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
# ✅ ERROR HANDLER — defined BEFORE gen_btn block
# ============================================================

def _handle_api_error(exc: Exception, model_choice: str):
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
            f"✅ Valid PageGrid models: `claude-opus-4-6`, "
            f"`claude-sonnet-4-6`, `claude-haiku-4-5`"
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
    elif "524" in err or "timeout" in err.lower():
        st.error(
            "❌ **524 / Timeout — Request took too long.**\n\n"
            "• Try a **faster model** (e.g. `claude-haiku-4-5` or `gemini-2.0-flash`)\n"
            "• Reduce **total word count** (try 480 words → 4 segments)\n"
            "• If using PDF/Transcript mode, upload a shorter document\n"
            "• Retry — the next attempt usually succeeds"
        )
    else:
        st.error(f"❌ Generation error: {exc}")


# ============================================================
# SESSION STATE INIT
# ============================================================
_defaults = {
    "chunks":                 None,
    "raw_response":           "",
    "last_topic":             "",
    "last_source":            "",
    "pdf_text":               "",
    "last_pdf_sig":           "",
    "last_pdf_lib":           "",
    "transcript_extractions": [],
    "transcript_files_sig":   "",
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
        "☁️  Claude  (via PageGrid)": (
            "PageGrid API Key", "sk-pgrid-…",
            "pagegrid.in → Dashboard → API Keys", "sk-pgrid-",
        ),
        "🟢  OpenAI  (GPT)": (
            "OpenAI API Key", "sk-…",
            "platform.openai.com → API Keys", "sk-",
        ),
        "🔵  Google  (Gemini)": (
            "Google AI API Key", "AIzaSy…",
            "aistudio.google.com → Get API Key", "AIzaSy",
        ),
    }
    _lbl, _ph, _hlp, _prefix = _key_meta[provider]
    st.markdown(f"### 🔑 {_lbl}")
    st.caption(f"Get yours: {_hlp}")
    api_key = st.text_input(_lbl, type="password", placeholder=_ph,
                            label_visibility="collapsed")
    if api_key:
        if api_key.startswith(_prefix):
            st.markdown('<p class="key-ok">✅ Key format looks valid</p>',
                        unsafe_allow_html=True)
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
            "- `claude-haiku-4-5` — Fastest ⚡\n\n"
            "**base_url:** `https://api.pagegrid.in`\n"
            "(SDK auto-appends `/v1`)",
            icon="📋",
        )

    st.divider()
    st.markdown("### 📊 Google Sheets Credentials")
    st.caption("Needed only for Push to Sheets. Service Account JSON.")
    creds_option = st.radio(
        "Credentials input", ["Upload JSON file", "Paste JSON text"], horizontal=True
    )
    gsheet_creds_str = ""
    if creds_option == "Upload JSON file":
        _up = st.file_uploader("Service Account JSON", type=["json"])
        if _up:
            gsheet_creds_str = _up.read().decode("utf-8")
            st.success("✅ Credentials loaded")
    else:
        _paste = st.text_area(
            "Paste JSON here", height=100,
            placeholder='{"type": "service_account", ...}',
        )
        if _paste.strip():
            try:
                json.loads(_paste)
                gsheet_creds_str = _paste
                st.success("✅ Valid JSON")
            except Exception:
                st.error("❌ Invalid JSON")

    st.divider()
    st.caption("SCRIPT ENGINE v3.0 · SKY Academy Internal Tool")
    st.caption(f"Each segment ≈ {WORDS_PER_SEGMENT} words ≈ ~55 sec speech")
    st.caption(
        f"[🔗 Open Target Sheet]"
        f"(https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit)"
    )


# ============================================================
# MAIN LAYOUT
# ============================================================
left, right = st.columns([1, 1], gap="large")

topic_input      = ""
topic_hint_input = ""
input_mode       = ""
merge_mode_val   = "auto"

with left:
    st.markdown("## 📝 Script Input")

    input_mode = st.radio(
        "✏️ What are you providing?",
        options=[
            "📌 Topic Name  →  Generate from Scratch",
            "📝 Competitor Transcripts  →  Merge to SKY Style",
            "📚 Book / PDF Section  →  Convert to SKY Style",
        ],
    )
    st.markdown("---")

    # ════════════════════════════════════════════════════════
    # MODE 1 — TOPIC
    # ════════════════════════════════════════════════════════
    if input_mode.startswith("📌"):
        st.markdown("""
        <div class="mode-topic">
        🎯 <b>Topic Mode</b> — Type any subject. SKY Engine writes a complete original
        voiceover from scratch: hook intro, exam angles, real-world examples,
        memory hints, natural AP tutor voice throughout.
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
    # MODE 2 — MULTI-TRANSCRIPT
    # ════════════════════════════════════════════════════════
    elif input_mode.startswith("📝"):
        st.markdown("""
        <div class="mode-transcript">
        🔄 <b>Multi-Transcript Mode</b> — Upload one or more competitor transcript files
        (.docx / .txt / .pdf). SKY Engine will: ① strip all competitor branding,
        ② intelligently merge/synthesize across files, ③ enrich by +25%,
        ④ rewrite in natural SKY Academy voice with hook intro.
        </div>""", unsafe_allow_html=True)

        topic_hint_input = st.text_input(
            "📌 Topic hint  (optional — helps accurate slide prompts)",
            placeholder="e.g.  UPSC 2025 Cutoff, TSPSC Exam Date, SSC CGL Strategy...",
        )

        merge_label = st.radio(
            "🔀 How should multiple files be merged?",
            options=[
                "🤖 Auto-detect  (AI decides)",
                "🔄 Synthesize same topic  (different data on same subject)",
                "🧩 Merge different topics  (weave different aspects together)",
            ],
            horizontal=False,
        )
        merge_mode_val = {
            "🤖 Auto-detect  (AI decides)":                               "auto",
            "🔄 Synthesize same topic  (different data on same subject)":  "synthesize",
            "🧩 Merge different topics  (weave different aspects together)": "merge_aspects",
        }[merge_label]

        transcript_files = st.file_uploader(
            "📤 Upload Transcript Files *",
            type=["docx", "txt", "pdf"],
            accept_multiple_files=True,
            help="Upload 1–10 competitor transcript files. Supported: .docx, .txt, .pdf",
        )
        topic_input = ""

        if transcript_files:
            new_sig = "|".join(
                f"{f.name}_{len(f.getvalue())}" for f in transcript_files
            )
            if new_sig != st.session_state.transcript_files_sig:
                extractions = []
                with st.spinner(f"🔍 Extracting text from {len(transcript_files)} file(s)..."):
                    for f in transcript_files:
                        fb         = f.getvalue()
                        text, info = extract_any_file(fb, f.name)
                        if text:
                            extractions.append({
                                "filename": f.name,
                                "text":     text,
                                "words":    len(text.split()),
                                "ok":       True,
                                "error":    "",
                                "info":     info,
                            })
                        else:
                            extractions.append({
                                "filename": f.name,
                                "text":     "",
                                "words":    0,
                                "ok":       False,
                                "error":    info,
                                "info":     "",
                            })
                st.session_state.transcript_extractions = extractions
                st.session_state.transcript_files_sig   = new_sig

            exts      = st.session_state.transcript_extractions
            ok_count  = sum(1 for e in exts if e["ok"])
            err_count = len(exts) - ok_count

            if ok_count:
                total_words = sum(e["words"] for e in exts if e["ok"])
                st.markdown(
                    f'<div class="merge-box">'
                    f'📁 <b>{ok_count} file(s) ready</b>'
                    + (f' · ⚠️ {err_count} failed' if err_count else '')
                    + f' &nbsp;|&nbsp; ~{total_words:,} total words'
                    + f' &nbsp;|&nbsp; Merge: <b>{merge_label}</b>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

            for e in exts:
                if e["ok"]:
                    st.markdown(
                        f'<div class="fcard-ok">✅ <b>{e["filename"]}</b> — '
                        f'~{e["words"]:,} words · {e["info"]}</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f'<div class="fcard-err">❌ <b>{e["filename"]}</b> — {e["error"]}</div>',
                        unsafe_allow_html=True,
                    )

            ok_exts = [e for e in exts if e["ok"]]
            if ok_exts:
                with st.expander(
                    f"👁️ Preview extracted content ({len(ok_exts)} files)", expanded=False
                ):
                    for e in ok_exts:
                        st.markdown(f"**📄 {e['filename']}** — {e['words']:,} words")
                        st.text(e["text"][:500] + ("\n\n[... more ...]" if len(e["text"]) > 500 else ""))
                        st.markdown("---")

        elif st.session_state.transcript_extractions:
            st.session_state.transcript_extractions = []
            st.session_state.transcript_files_sig   = ""

    # ════════════════════════════════════════════════════════
    # MODE 3 — BOOK PDF
    # ════════════════════════════════════════════════════════
    else:
        st.markdown("""
        <div class="mode-pdf">
        📚 <b>PDF Mode</b> — Upload a book chapter or study notes PDF.
        SKY Engine extracts the text and transforms dry academic content into
        a fully engaging SKY Academy voiceover — zero bookish tone,
        hook intro, rich memory hints, pure AP tutor energy.
        </div>""", unsafe_allow_html=True)

        topic_hint_input = st.text_input(
            "📌 Topic / Chapter context  (optional)",
            placeholder="e.g.  Chapter 3: Directive Principles, Unit 5: Cell Respiration...",
        )

        pdf_file = st.file_uploader(
            "📤 Upload PDF *", type=["pdf"],
            help="Upload the book section, study notes, or chapter to be scripted",
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
                st.success(
                    f"✅ Extracted: ~{wc:,} words · {st.session_state.last_pdf_lib}"
                )
                with st.expander("👁️ Preview extracted text", expanded=False):
                    st.text(st.session_state.pdf_text[:800] + "\n\n[... more ...]")
                topic_input = st.session_state.pdf_text

    # ── Word count / segments ─────────────────────────────
    st.markdown("---")
    approx_words = st.number_input(
        "📝 Approximate Total Script Words",
        min_value=120, max_value=6000, value=600, step=120,
        help=(
            f"Auto-splits into ~{WORDS_PER_SEGMENT}-word segments (~55 sec each). "
            "600 words → 5 segments → ~5 min video."
        ),
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
        gen_btn   = st.button("🚀 Generate Script", type="primary",
                              use_container_width=True)
    with c2:
        clear_btn = st.button("🗑️ Clear All", use_container_width=True)


# ── Clear ──────────────────────────────────────────────────
if clear_btn:
    for _k, _v in _defaults.items():
        st.session_state[_k] = _v
    st.rerun()


# ============================================================
# ✅ GENERATE — uses run_generation() with streaming
# ============================================================
if gen_btn:
    if   input_mode.startswith("📌"): mode_name = "topic"
    elif input_mode.startswith("📝"): mode_name = "transcript"
    else:                              mode_name = "pdf"

    if not api_key.strip():
        st.error("❌ Please enter your API key in the sidebar!")

    elif mode_name == "topic" and not topic_input.strip():
        st.error("❌ Please enter a topic!")

    elif mode_name == "transcript":
        ok_exts = [e for e in st.session_state.transcript_extractions if e["ok"]]
        if not ok_exts:
            st.error(
                "❌ Please upload at least one transcript file "
                "(.docx / .txt / .pdf) and make sure it extracts successfully."
            )
        else:
            # Full text — no truncation
            safe_transcripts = [
                {"filename": e["filename"], "text": e["text"]}
                for e in ok_exts
            ]
            st.info(
                f"🔄 Merging {len(safe_transcripts)} transcript(s) → SKY Academy voice…  "
                f"Progress shown below. Do not close this tab.",
                icon="⏳",
            )
            _status = st.empty()
            try:
                system_p, user_p = build_prompts_multi_transcript(
                    safe_transcripts, topic_hint_input,
                    num_segs, special_instructions, merge_mode_val,
                )
                display_topic  = (
                    topic_hint_input.strip()[:60]
                    or f"{len(safe_transcripts)} Transcript(s)"
                )
                display_source = "📝 Transcript → SKY"

                raw = run_generation(
                    api_key, provider, model_choice, system_p, user_p, _status
                )
                _status.empty()
                st.session_state.raw_response = raw
                parsed = parse_segments(raw)
                if parsed:
                    st.session_state.chunks      = parsed
                    st.session_state.last_topic  = display_topic
                    st.session_state.last_source = display_source
                    st.success(
                        f"✅ {len(parsed)} segments generated from "
                        f"{len(safe_transcripts)} file(s)! [{display_source}]"
                    )
                    st.rerun()
                else:
                    st.error(
                        "❌ Could not parse JSON from AI response. "
                        "Expand Raw AI Response below to inspect."
                    )
            except Exception as exc:
                _status.empty()
                _handle_api_error(exc, model_choice)

    elif mode_name == "pdf" and not topic_input.strip():
        st.error("❌ Please upload a PDF. Make sure text was extracted successfully.")

    else:
        # Topic or PDF — full text, no truncation
        _mode_label = (
            f"✍️ Generating {num_segs} segments via "
            f"{'PageGrid → ' + model_choice if 'PageGrid' in provider else model_choice}"
            if mode_name == "topic"
            else "📚 Converting PDF content → SKY Academy voice"
        )
        st.info(
            f"{_mode_label}…  Progress shown below. Do not close this tab.",
            icon="⏳",
        )
        _status = st.empty()
        try:
            if mode_name == "topic":
                system_p, user_p = build_prompts_topic(
                    topic_input, num_segs, special_instructions
                )
                display_topic  = topic_input.strip()[:60]
                display_source = "📌 Topic"
            else:
                system_p, user_p = build_prompts_pdf(
                    topic_input, topic_hint_input, num_segs, special_instructions
                )
                display_topic  = topic_hint_input.strip()[:60] or "PDF Content"
                display_source = "📚 PDF → SKY"

            raw = run_generation(
                api_key, provider, model_choice, system_p, user_p, _status
            )
            _status.empty()
            st.session_state.raw_response = raw
            parsed = parse_segments(raw)
            if parsed:
                st.session_state.chunks      = parsed
                st.session_state.last_topic  = display_topic
                st.session_state.last_source = display_source
                st.success(f"✅ {len(parsed)} segments generated! [{display_source}]")
                st.rerun()
            else:
                st.error(
                    "❌ Could not parse JSON from AI response. "
                    "Expand Raw AI Response below to inspect."
                )
        except Exception as exc:
            _status.empty()
            _handle_api_error(exc, model_choice)


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
            "📌 Topic":            "badge-topic",
            "📝 Transcript → SKY": "badge-transcript",
            "📚 PDF → SKY":        "badge-pdf",
        }.get(st.session_state.last_source, "badge-topic")

        st.markdown(
            f'<span class="{badge_class}">{st.session_state.last_source}</span>'
            f'&nbsp;&nbsp;'
            f'<span class="stat-pill">📦 {len(chunks)} segments</span>'
            f'<span class="stat-pill">📝 ~{total_words:,} words</span>'
            f'<span class="stat-pill">⏱ ~{est_min} min</span>',
            unsafe_allow_html=True,
        )
        st.markdown("")

        tabs = st.tabs([f"▶ {i + 1}" for i in range(len(chunks))])
        for tab, chunk, idx in zip(tabs, chunks, range(len(chunks))):
            with tab:
                seg_words = len(chunk.get("telugu_text", "").split())
                st.caption(
                    f"~{seg_words} words · ~{round(seg_words / 130, 1)} min"
                    + (" · 🎣 Hook + Welcome" if idx == 0 else "")
                )
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

        with st.expander("📜 Full Script — Continuous Flow", expanded=False):
            full = "\n\n".join(c.get("telugu_text", "") for c in chunks)
            st.text_area(
                "full_script", value=full, height=400,
                label_visibility="collapsed",
            )

        st.divider()

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
                st.markdown(
                    f"[🔗 Open Sheet]"
                    f"(https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit)"
                )
            else:
                st.error(msg)

    else:
        st.markdown("""
        <div class="empty-preview">
            <h3>🎬 Preview will appear here</h3>
            <p style="margin-top:12px; font-size:0.9rem;">
                Choose input mode → Provide content → Click <b>Generate Script</b>
            </p>
            <p style="margin-top:18px; font-size:0.82rem; line-height:2.2; color:#6366f1;">
                📌 <b>Topic</b> — Original script from any subject<br>
                📝 <b>Multi-Transcript</b> — Upload competitor files → merged SKY voice<br>
                📚 <b>PDF</b> — Book content → SKY voiceover with hook &amp; memory hints
            </p>
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# RAW RESPONSE DEBUG
# ============================================================
if st.session_state.raw_response:
    with st.expander(
        "🔍 Raw AI Response  (debug / manual copy-paste fallback)", expanded=False
    ):
        st.code(st.session_state.raw_response[:8000], language="json")


# ============================================================
# FOOTER
# ============================================================
st.divider()
st.markdown(
    "<div style='text-align:center;color:#aaa;font-size:11px;'>"
    "<span style='color:#FF6B6B;font-weight:800;'>S</span>"
    "<span style='color:#FFE66D;font-weight:800;'>K</span>"
    "<span style='color:#4ECDC4;font-weight:800;'>Y</span>"
    " <b>ACADEMY</b> &nbsp;|&nbsp; SCRIPT ENGINE v3.0 &nbsp;|&nbsp; "
    "Internal Tool &nbsp;|&nbsp; Powered by PageGrid + Anthropic SDK"
    "</div>",
    unsafe_allow_html=True,
)
