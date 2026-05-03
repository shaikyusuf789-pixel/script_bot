# ============================================================
# SCRIPT_ENGINE.py — SKY Academy Video Script Generator v3.1
# Three Input Modes: Topic | Multi-Transcript Merge | Book PDF
# Video Types: General (Strategy/Motivation) | Subjective (Deep Teaching)
# v3.1: Per-Segment Regen · SEO Pack · Study Notes · Video Type DNA
# Bug Fixes: Zero emojis in TTS · Edited text syncs to Sheets/Downloads
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
    .vtype-general {
        background: linear-gradient(to right, #fff7ed, #ffedd5);
        border-left: 5px solid #f97316;
        padding: 10px 14px; border-radius: 0 10px 10px 0;
        font-size: 0.82rem; color: #7c2d12; margin: 8px 0 12px 0;
    }
    .vtype-subjective {
        background: linear-gradient(to right, #f0fdf4, #dcfce7);
        border-left: 5px solid #22c55e;
        padding: 10px 14px; border-radius: 0 10px 10px 0;
        font-size: 0.82rem; color: #14532d; margin: 8px 0 12px 0;
    }
    .seo-box {
        background: linear-gradient(to right, #fdf4ff, #fae8ff);
        border-left: 5px solid #a855f7;
        padding: 12px 16px; border-radius: 0 10px 10px 0;
        font-size: 0.83rem; color: #581c87; margin: 10px 0;
    }
    .regen-hint {
        background: linear-gradient(to right, #eff6ff, #e0f2fe);
        border: 1px dashed #7dd3fc;
        border-radius: 8px; padding: 8px 12px;
        font-size: 0.78rem; color: #075985; margin-bottom: 6px;
    }
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
    <div class="sky-tagline">SCRIPT ENGINE v3.1</div>
    <div class="sky-sub">Telugu Video Script Generator &nbsp;·&nbsp; Internal Tool &nbsp;·&nbsp; AP Tutor Voice</div>
    <div class="sky-pills">
        <span class="sky-pill">📌 Topic → Original</span>
        <span class="sky-pill">📝 Multi-Transcript → Merge</span>
        <span class="sky-pill">📚 Book PDF → SKY Voice</span>
        <span class="sky-pill">🎯 General · 📖 Subjective</span>
        <span class="sky-pill">🔄 Per-Segment Regen</span>
        <span class="sky-pill">🎬 SEO Pack</span>
        <span class="sky-pill">📄 Study Notes</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# CONSTANTS
# ============================================================
PAGEGRID_BASE_URL = "https://api.pagegrid.in"
WORDS_PER_SEGMENT = 120

SHEET_ID = "1dNHDgkX6vhdhZSi5SavBgNihWe04zayRQwyMcCwNlOI"

# ──────────────────────────────────────────────────────────
# HARDCODED GOOGLE SERVICE ACCOUNT CREDENTIALS
# ──────────────────────────────────────────────────────────
_HARDCODED_CREDS = {
    "type": "service_account",
    "project_id": "gen-lang-client-0268678328",
    "private_key_id": "06350e4cf0251abf195e1ad49cc5eaf5827ba5ca",
    "private_key": (
        "-----BEGIN PRIVATE KEY-----\n"
        "MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCkxNptNHDP8qKi\n"
        "JSqkGbx3SvgY1gnlUoKGzJoldMYvVb6Yw4j7fg/+G5h9P0ze2GtFFD97A7yaUsk0\n"
        "VaH4ODeB5cf414QYP4WU3FoyvgcefkAlGANcZEOt+Enb3K+hhd1bJjfqFXiBO9QT\n"
        "AmsORofIwKJUhdt4+it/4XlC+ADJFd/JKvWLvGUK0p6Aqaz9cgftXoBybF7nTelE\n"
        "j1BofII0hKZ3jrV767SJ7k6qXNVZRydMQY4cqua/8yuVpkM6ALiJZF8/n9Q317y3\n"
        "/DOKgHV4SMno2jf/8MvnIwQExJH5uv0TWo+iFxQ794J0ytpz+Pya83gYFX2eIo6Z\n"
        "gnBnpUnXAgMBAAECggEACN/5i+xJL0o4bFdoJpKkTiChoGTW/50kHrKikuXpTt9l\n"
        "dsEBfdpabit6WTSxpUcu7/eZO70FyaIv6Du8j6wngT2pOcQR/2Rcg5oi2ZzWsVPH\n"
        "jLfwZmeYJaS8BbWrWB3nwGMcm+UwKnXYhHWa4pf19GA73iWfnrKK6UZxy6OkFzCa\n"
        "QyCHEjjNTG/8oCSz5caUCef7IfmaFqu/sg7A2cTekYyltDdYEmWUOx+9nCzvD/KQ\n"
        "wPqkn6jxWuZ2+Ec9+gUuISHpc9G248Rgi97LCufh0JI4NV+zNMG0bEtwz0IpL9sA\n"
        "Q76OoxcdIFoNJSSrUx/F+Ut7hnYJ/1zbH4oPa1CjIQKBgQDbPLgiYeR96nZ24DjI\n"
        "mDVNyhZTauIBbSZR7/u5jI3P5VLLMbfW93hkBQ/3P0IIIJDJIzoHOOnTnNn3KhJE\n"
        "seLjwg9djJKtAtjIWKOXiiOUz/gHnuLnfnmwyKtQnbASfVEjo5AUifVMF90/VkSE\n"
        "elHw6iPA/tE06f9Bm0V9QzaIGQKBgQDAZfR6fPZAYfiUG+u9fUeeZkpGtIXdPWTF\n"
        "wg0RrBa0Kh7o/T35OVgAQnDtG7odE3akrxenytacyzc87IFpC+BSgf+t4mVJnqPY\n"
        "XH5BFORLhVuUoUnNNYq/BF6sY9GZ4e35b+Baxn25GGntT/9pkihYDPPql8Z/t9jb\n"
        "1NCttldfbwKBgEMWvqZO3JQnpp7UGKxR36XxXImkYIrdMufKD3cFavQekgp6KW7Q\n"
        "BfhdkDgyFGvWQ1g5vm0tXmiSTCUVq8d3xB28aeVPuibVgy8z6MPb0u2cAqOaXIdI\n"
        "rcaKcdpWluXhkW3dhJ60ZOsnNl5GcOs1X1Pg4pYRpEWUAbe64zXk1pApAoGBALx2\n"
        "4r3djMbScVJ76zeJ8c7a+mU6TmrCyeThyjWGchL3s6Gc98ka//X5H29UGsKCn1SA\n"
        "Y1as3f9nHOvj7Hw+8vU/fHoTbA5qhKrbJ52O3naP4n68Y3PNv+SPXkHV4aqwYpFV\n"
        "otqo1tyqapDZLSN31WczAPfKxtmy+I2WcPfIxtunAoGBAIVXg/TVXY7KZL/ZLVHx\n"
        "AP2rq/12zXeuUiC13MpZ6RtbiWfNwiPd2HjCNpwjyAxuLjPTTqYUVFZKaKhgvB8/\n"
        "IUQmz1dnM8mdB27jLzjchPSeJFH6yZQKklJqbtopwN557j3vyFIrcxNQJcgpj9UD\n"
        "VyLML2CO4hHr3eoKQ+BNmZj6\n"
        "-----END PRIVATE KEY-----\n"
    ),
    "client_email": "forscripting@gen-lang-client-0268678328.iam.gserviceaccount.com",
    "client_id": "110013612770034478540",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": (
        "https://www.googleapis.com/robot/v1/metadata/x509/"
        "forscripting%40gen-lang-client-0268678328.iam.gserviceaccount.com"
    ),
    "universe_domain": "googleapis.com",
}

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

ABSOLUTE RULE — ELEVENLABS TTS COMPATIBILITY:
  The "telugu_text" field MUST contain ZERO emoji characters.
  No emoticons, no Unicode symbols used as decoration, no pictographs whatsoever.
  Example forbidden: "సో friends! 🎯 ఈరోజు మనం..."
  Correct: "సో friends! ఈరోజు మనం..."
  ElevenLabs will either ERROR OUT or read emoji names aloud if emojis are present.
  "slide_prompt" MAY use emojis freely — only "telugu_text" is restricted.

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
  "India ని Sovereign, Socialist, Secular, Democratic Republic గా చేయాలనుకున్నారు"
     WHO wants this? WHY? WHEN? Zero context. Hollow sentence.
  "ఈ concept యొక్క importance అర్థం చేసుకోవాలంటే మనం history లోకి వెళ్ళాలి"
     Filler opener. Just go into history — don't announce it.
  "Constitution రాయడానికి వారు నిర్ణయించుకున్నారు"
     WHO is 'వారు'? WHY? This tells the student nothing.
  "ఇది చాలా ఇంపార్టెంట్ ఓకేనా" — said BEFORE proving why it's important.
  "ఇప్పుడు మనం ఈ topic గురించి చూద్దాం" — hollow transition; just start explaining.

GOOD — natural, contextual, meaningful, AP tutor style:
  "సో friends — 1947 లో Independence వచ్చింది — great! కానీ ఇప్పుడు real problem వచ్చింది —
   ఈ దేశాన్ని ఎలా run చేయాలి? Power ఎవరి దగ్గర ఉంటుంది? Courts ఎలా work చేస్తాయి?
   Rights ఏం ఉంటాయి? — ఇవన్నీ define చేయడానికే Constitution పుట్టింది, ఓకేనా!"

  "Sovereign అంటే — చాలా simple గా చెప్పాలంటే — మనం ఏ country కి bow చేయాల్సిన పని లేదు.
   America చెప్పినా, Britain చెప్పినా — India తన decisions తానే తీసుకుంటుంది.
   That's what Sovereign means. Clear గా అర్థమైందా?"

  "ఇప్పుడు ఒక important question — UPSC 2019 లో exact గా ఇది అడిగారు —
   Preamble లో Socialist, Secular అనే words originally ఉన్నాయా? — లేదు friends!
   1976 లో 42nd Amendment లో add చేశారు. Note it down!"

  "B.R. Ambedkar — ఈ person గురించి చెప్పాలంటే — రోజూ 18-20 గంటలు work చేశారు.
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
- Telugu + English natural mix — technical/exam terms in English, explanation in Telugu
- Direct address: "మీరు", "మీకు", "friends", "చూడు"
- Light humor only when it fits — never forced
- Build suspense only when there's genuinely something to reveal

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MEMORY HINTS — MEMORY TRICK RULES — STRICT:RICH EXAMPLES LIBRARY (SKY ACADEMY STYLE)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HOW SKY ACADEMY MEMORY HINTS WORK:
The hint must be: OBVIOUS — CLEVER — IMPOSSIBLE TO FORGET.
Student should laugh or say "oh wow, I will never forget this!"
If you need to explain the hint, it is a BAD hint. Start over.
- NEVER use abbreviation mnemonics (no BKKKOMMS, VIBGYOR-type tricks, zero letter shortcuts)
- ONLY use WORD-ASSOCIATION and INTERLINKING:
  * Find meaning INSIDE the word itself (Katha=story → Kathak from story-land UP)
  * Link to geography/history naturally (Kuchipudi = village in AP = dance named after it)
  * Chain connections like: Sattra→monastery→Assam→Sattriya
  * Number links: 42 degree heat → 42nd Amendment style
  * If no trick possible, — don't force abbreviations
- Student must feel the CONNECTION, not memorize a random letter string

POLITY / CONSTITUTION:
  "Fancy words = France" (Liberty, Equality, Fraternity -> French Revolution)
  "42 degrees C fever -> Emergency -> 42nd Amendment 1976"
  "Article 21 — 21st birthday = LIFE's most important day -> Right to LIFE & Liberty"
  "DPSP = Doctor's Prescription -> Non-justiciable"
  "BRO wrote the Constitution -> B.R. Ambedkar -> Father of Constitution"
  "CAG = Check And Guard government money"
  "Preamble = Entrance door of a house -> tells you what's inside"
  "73rd Amendment = Panchayati Raj -> 7+3=10 -> 10 fingers = hands-on local governance"
  "Emergency Article 352 -> 3-5-2 = three types: National, State, Financial"

HISTORY / FREEDOM STRUGGLE:
  "1857 = 18-57 -> 57 year old person's first revolt = First War of Independence"
  "Quit India 1942 -> 9+4+2=15 -> August 15 -> Independence 1947!"
  "Simon Commission = 1927 -> No Indian members -> Simon says — but India says NO!"

GEOGRAPHY:
  "Narmada flows WEST -> Flip N sideways -> looks like W for West!"
  "Thar Desert -> Thar sounds like Tar road -> hot, dry, burned = desert"

SCIENCE / BIOLOGY:
  "Mitochondria = Powerhouse -> MITO = My Toe -> your toe pushes you forward = POWER"
  "Photosynthesis: everything is SIX -> 6CO2 + 6H2O -> C6H12O6 + 6O2"
  "Noble Gases = 0 valency -> Nobel Prize winners share NOTHING -> zero sharing"

ECONOMY / CURRENT AFFAIRS:
  "GDP vs GNP: D = Domestic (inside India), N = National (Indians anywhere)"
  "Repo Rate -> REPO = RBI REPOssesses money from banks"
  "Inflation and Interest Rate: they are married -> one goes up, other follows"

WHEN TO USE MEMORY HINTS:
- Number / date / name is genuinely hard to remember
- Hint is INSTANTLY obvious — no explanation needed
- Skip when the fact is already simple/memorable
- NEVER generate a forced or confusing hint

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STRICT RULES FOR ALL MODES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. NO bookish headings inside voiceover (SECTION 1, CHAPTER, PART N, etc.)
2. NO "Part 1", "Segment 2", "Chapter N" labels anywhere in voiceover
3. Script flows as ONE continuous natural conversation
4. NEVER mention competitor channels, instructors, books, apps, courses by name
5. ONLY SKY Academy — weave "SKY Academy లో" naturally where it fits
6. LAST SEGMENT must close with SKY Academy CTA
7. ZERO emojis in telugu_text — this is a hard technical requirement for TTS
"""

_OUTPUT_FORMAT = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HOOK + WELCOME — MANDATORY FOR SEGMENT 1 ONLY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Segment 1 MUST ALWAYS open with:

ONE POWERFUL HOOK LINE — stops the student from scrolling.
WELCOME LINE — immediately follows:
   "[WARM, FRIENDLY — WELCOME] SKY Academy కి welcome friends! ఇక్కడ మీరు subject
    నేర్చుకోవడమే కాదు — exam కి forever memorise అవుతారు. [Energetic] Let's start!"
Then flow DIRECTLY into content — no transition filler.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CLOSING CTA — MANDATORY FOR LAST SEGMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Last segment must end with this COMPLETE block (adapt naturally):
"[Energetic] సో friends — ఈరోజు మనం [TOPIC] గురించి చాలా deep గా చూసుకున్నాం ఓకేనా.
ఈ video యొక్క classroom notes — print చేసుకోవడానికి ready గా ఉన్న complete study material —
SKY Academy Telegram channel లో share చేస్తాను, video చూసిన తర్వాత download చేసుకుని
revision కి use చేయండి — absolutely free!
మీకు ఇంకా ఏ topic కావాలో, ఏ subject మీద video కావాలో — comment section లో చెప్పండి.
నేను personally ప్రతి comment చదువుతాను and reply ఇస్తాను — ఇది నా word మీకు!
Any doubts ఉన్నాయా? Comment below — I will answer each one personally!"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTPUT FORMAT — STRICT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Return ONLY a valid JSON array. No preamble, no markdown fences, no explanations.
CRITICAL: telugu_text must have ZERO emojis. slide_prompt may have emojis.

[
  {{
    "seg": 1,
    "telugu_text": "full voiceover text — Hook -> Welcome -> content — NO EMOJIS HERE",
    "slide_prompt": "Heading: Short Slide Title\\n• bullet 1\\n• bullet 2\\n• bullet 3\\nImage Prompt: cinematic visual, color palette, mood"
  }},
  ...
]

- Segment 1 telugu_text: Hook + Welcome + content (~{WORDS_PER_SEGMENT} words total)
- All other segments: ~{WORDS_PER_SEGMENT} words of natural spoken Telugu
- Generate exactly {NUM_SEGS} segments
- ONE continuous natural conversation — no labels, no part numbers
- Every sentence meaningful and logically connected to the next
- Memory hints sprinkled wherever genuinely useful
- DOUBLE CHECK: scan every telugu_text field and remove any emoji before returning
"""

# ============================================================
# VIDEO TYPE DNA BLOCKS — NEW IN v3.1
# ============================================================

_DNA_GENERAL_VIDEO = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VIDEO TYPE: GENERAL — STRATEGY / GUIDANCE / MOTIVATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

THIS IS A STRATEGY / GUIDANCE / MOTIVATION VIDEO — NOT DEEP SUBJECT TEACHING.

TONE AND ENERGY:
- Think of a passionate senior who cracked the exam talking to juniors with full heart.
- High motivation energy throughout — "You CAN do this", "మీరు CRACK చేస్తారు!"
- Constant assurance: "SKY Academy మీతో ఉంది — మీరు ఒంటరిగా లేరు."
- Treat students like family — direct, warm, intensely personal.
- Make them FEEL that this channel is genuinely invested in their success.

STRATEGY MEMORY HINTS — HOW TO BUILD THEM FOR GUIDANCE VIDEOS:
These are STUDY STRATEGY hints that tell students WHAT IS IMPORTANT and WHY.
They connect syllabus topics to memorable pegs so students can prioritize correctly.
Maximum 3 to 4 strategy hints per script — each must be impactful, not just filler.

EXAMPLE STRATEGY MEMORY HINT (geography video):
  "National Parks is one of the most important areas — never skip it.
   Take Dibru Saikhova — in the name DIBRU you can see BRU.
   Assam is famous for TEA, and BRU is a famous coffee brand — tea and coffee both
   come from Assam! Now you will NEVER forget Dibru Saikhova is in Assam.
   SKY Academy teaches you this kind of connection so you remember for a lifetime."

FOLLOW THIS FORMULA for all strategy hints:
  State what topic area is important -> Give the specific fact -> Build the connection
  -> Connect to something funny/familiar -> Student laughs/says wow -> Forever locked in.

CONTENT STRUCTURE TO FOLLOW:
- Open with motivation: why this topic/subject is winnable if approached correctly
- Subject overview: what is truly important vs what can be skipped
- Study schedule or approach guidance with clear reasoning
- Book and resource guidance (without naming competitors) — "standard reference books"
- SKY Academy strategy advantage — why our approach works better
- Mid-section motivation — real exam success stories, effort stories
- Closing: community building, Telegram, next steps

SKY ACADEMY COMMUNITY PHRASES — weave naturally:
  "SKY Academy family లో మీరు important part — మీ success నాకు personally important."
  "నేను ప్రతి రోజు మీ కోసం content తయారు చేస్తున్నాను — మీరు just study చేయండి."
  "SKY Academy Telegram channel join అవ్వండి — daily updates, PDFs, free content అన్నీ ఉంటాయి."
  "Comment లో మీ current preparation status చెప్పండి — నేను personally guide చేస్తాను."
  "మీరు fail అవుతారు అని ఎవరైనా చెప్పారా? — వారికి ఈ video చూపించండి."
"""

_DNA_SUBJECTIVE_VIDEO = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VIDEO TYPE: SUBJECTIVE — DEEP SUBJECT TEACHING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

THIS IS A DEEP SUBJECT TEACHING VIDEO — MAXIMUM CONCEPTUAL DEPTH WITH MEMORY AIDS.

MEMORY HINTS — MANDATORY DENSITY RULE:
- MINIMUM ONE memory hint per major concept, hard-to-remember fact, or important number.
- Every difficult name, date, article number, term MUST have a hint attempt.
- Use ALL categories freely: acronyms, visual images, rhymes, funny connections, word plays, stories.
- Hints must be INSTANT and OBVIOUS — student should never need the hint explained.
- Do NOT cluster all hints at the end — sprinkle as each new concept appears in the flow.
- The student should walk away with more memory tricks than they can count.

EXAM INTEGRATION — mandatory throughout:
- After each major concept, mention relevant PYQ angle naturally:
  "UPSC 2019 లో exactly ఇది అడిగారు" or "APPSC Mains లో ఈ question twice వచ్చింది"
- Flag high-yield vs low-yield content within the same topic clearly.
- "ఇది exam లో definite — note it down" for facts that appear repeatedly in papers.

SILENT SKY ACADEMY APP CTA (Last Segment Only — weave naturally):
  Somewhere in the last segment closing, include organically:
  "SKY Academy app లో ఈ topic యొక్క full course available ఉంది —
   video description లో download link ఉంది — memory hint-based complete courses,
   practice tests, PYQ solutions అన్నీ ఒకే చోట — exam guarantee తో!"
  This must feel like a genuine tip, not an advertisement.

STUDY NOTES CTA (Last Segment — mandatory addition to closing):
  "ఈ video యొక్క classroom notes — print చేసుకోవడానికి ready గా ఉన్న complete study
   material — SKY Academy Telegram channel లో share చేస్తాను, video చూసిన తర్వాత
   download చేసుకుని revision కి use చేయండి — absolutely free!"
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
    "CRITICAL: telugu_text must contain ZERO emoji characters — ElevenLabs TTS will break.\n"
) + _SKY_DNA + _OUTPUT_FORMAT


_SYSTEM_TRANSCRIPT = (
    "You are an expert Telugu video script writer for SKY Academy — "
    "India's leading competitive exam preparation YouTube channel in Telugu medium.\n\n"
    "Your job: TRANSFORM one or more competitor video transcripts into a single 100% original "
    "SKY Academy script.\n"
    "The output must feel like it was WRITTEN for SKY Academy from day one — not a conversion.\n"
    "The student must not be able to tell this was ever from a competitor.\n"
    "CRITICAL: telugu_text must contain ZERO emoji characters — ElevenLabs TTS will break.\n\n"
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
    "If the student can tell you're reading from a book, you have FAILED.\n"
    "CRITICAL: telugu_text must contain ZERO emoji characters — ElevenLabs TTS will break.\n\n"
    "Step 1 — DESTROY THE BOOKISH TONE COMPLETELY\n"
    "Step 2 — INJECT LIFE AND DEPTH\n"
    "Step 3 — FULL SKY ACADEMY VOICE\n"
) + _SKY_DNA + _OUTPUT_FORMAT


# ============================================================
# UTILITY — STRIP EMOJIS (ElevenLabs safety net)
# ============================================================

def strip_emojis(text: str) -> str:
    """
    Remove all emoji / pictograph Unicode characters from text.
    This is a hard safety net — the system prompt also instructs the AI
    to produce zero emojis, but this ensures it at parse time.
    Only applies to telugu_text; slide_prompt is left untouched.
    """
    emoji_pattern = re.compile(
        "["
        "\U0001F1E0-\U0001F1FF"   # flags
        "\U0001F300-\U0001F5FF"   # symbols & pictographs
        "\U0001F600-\U0001F64F"   # emoticons
        "\U0001F680-\U0001F6FF"   # transport & map
        "\U0001F700-\U0001F77F"   # alchemical symbols
        "\U0001F780-\U0001F7FF"   # geometric shapes extended
        "\U0001F800-\U0001F8FF"   # supplemental arrows-c
        "\U0001F900-\U0001F9FF"   # supplemental symbols
        "\U0001FA00-\U0001FA6F"   # chess symbols
        "\U0001FA70-\U0001FAFF"   # symbols extended-a
        "\u2600-\u26FF"           # misc symbols
        "\u2700-\u27BF"           # dingbats
        "\uFE0F"                  # variation selector-16
        "\u200D"                  # zero-width joiner
        "\u23CF"                  # eject symbol
        "\u23E9-\u23F3"           # clock/timer symbols
        "\u231A-\u231B"           # watch symbols
        "\u25AA-\u25FE"           # geometric shapes
        "\u2614-\u2615"           # umbrella/coffee
        "\u2648-\u2653"           # zodiac
        "\u267F"                  # wheelchair
        "\u2693"                  # anchor
        "\u26A1"                  # lightning
        "\u26AA-\u26AB"           # circles
        "\u26BD-\u26BE"           # soccer/baseball
        "\u26C4-\u26C5"           # snowman/sun
        "\u26CE"                  # ophiuchus
        "\u26D4"                  # no entry
        "\u26EA"                  # church
        "\u26F2-\u26F3"           # fountain/golf
        "\u26F5"                  # sailboat
        "\u26FA"                  # tent
        "\u26FD"                  # fuel pump
        "]+",
        flags=re.UNICODE,
    )
    return emoji_pattern.sub("", text).strip()


# ============================================================
# UTILITY — STORE NEW CHUNKS (sets widget session state too)
# ============================================================

def store_new_chunks(parsed: list):
    """
    Stores newly generated/recovered chunks into session state.
    - Strips emojis from telugu_text (ElevenLabs safety)
    - Explicitly sets tv_i / sv_i session state keys so text areas
      always show the latest generation, overriding any stale edits
    - Clears SEO pack (stale for new generation)
    """
    for i, c in enumerate(parsed):
        cleaned = strip_emojis(c.get("telugu_text", ""))
        c["telugu_text"] = cleaned
        st.session_state[f"tv_{i}"] = cleaned
        st.session_state[f"sv_{i}"] = c.get("slide_prompt", "")
    st.session_state.chunks   = parsed
    st.session_state.seo_pack = None


# ============================================================
# UTILITY — SYNC EDITS TO CHUNKS (reads widget state → export)
# ============================================================

def sync_edits_to_chunks() -> list:
    """
    Builds an export-ready copy of chunks by reading the CURRENT
    text area widget values (tv_i / sv_i) from session state.
    This ensures whatever the user typed / edited in the UI is what
    gets pushed to Google Sheets and downloaded — not the original AI output.
    """
    chunks = st.session_state.chunks
    if not chunks:
        return []
    synced = []
    for i, c in enumerate(chunks):
        synced.append({
            "seg":          c.get("seg", i + 1),
            "telugu_text":  strip_emojis(
                st.session_state.get(f"tv_{i}", c.get("telugu_text", ""))
            ),
            "slide_prompt": st.session_state.get(f"sv_{i}", c.get("slide_prompt", "")),
        })
    return synced


# ============================================================
# PROMPT BUILDERS — all accept video_type now
# ============================================================

def _inject_counts(system: str, num_segs: int) -> str:
    return (
        system
        .replace("{NUM_SEGS}", str(num_segs))
        .replace("{WORDS_PER_SEGMENT}", str(WORDS_PER_SEGMENT))
    )


def build_prompts_topic(
    topic: str, num_segs: int, special_instructions: str, video_type: str = "subjective"
):
    vdna   = _DNA_GENERAL_VIDEO if video_type == "general" else _DNA_SUBJECTIVE_VIDEO
    system = _inject_counts(_SYSTEM_TOPIC + "\n\n" + vdna, num_segs)
    si     = f"\nSpecial Instructions:\n{special_instructions.strip()}" if special_instructions.strip() else ""
    user   = (
        f"Generate a complete SKY Academy Telugu video script on:\n\n"
        f"**Topic:** {topic.strip()}\n"
        f"**Video Type:** {'General / Strategy / Motivation' if video_type == 'general' else 'Subjective / Deep Teaching'}\n"
        f"**Segments required:** {num_segs}\n"
        f"**Words per segment:** ~{WORDS_PER_SEGMENT}\n"
        f"{si}\n\n"
        f"REMINDERS:\n"
        f"- Segment 1: HOOK -> Welcome -> Content\n"
        f"- Natural AP tutor voice — meaning first, style second\n"
        f"- {'Strategy memory hints: max 3-4, high impact, study guidance focused' if video_type == 'general' else 'Memory hints: minimum one per major concept / hard area'}\n"
        f"- No bookish headings, no Part/Segment labels in voiceover\n"
        f"- Last segment must have SKY Academy CTA + Telegram notes CTA\n"
        f"- ZERO emojis in telugu_text — hard technical requirement\n"
        f"- Return ONLY valid JSON array, nothing else"
    )
    return system, user


def build_prompts_multi_transcript(
    transcripts: list,
    topic_hint: str,
    num_segs: int,
    special_instructions: str,
    merge_mode: str = "auto",
    video_type: str = "subjective",
):
    vdna   = _DNA_GENERAL_VIDEO if video_type == "general" else _DNA_SUBJECTIVE_VIDEO
    system = _inject_counts(_SYSTEM_TRANSCRIPT + "\n\n" + vdna, num_segs)
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
        f"COMPETITOR TRANSCRIPT {i + 1} of {n}\n"
        f"[File: {t['filename']}]\n"
        f"{t['text'].strip()}\n"
        f"END TRANSCRIPT {i + 1}"
        for i, t in enumerate(transcripts)
    )

    user = (
        f"Transform the {n} competitor transcript(s) below into a SINGLE SKY Academy voiceover.\n"
        f"**Video Type:** {'General / Strategy / Motivation' if video_type == 'general' else 'Subjective / Deep Teaching'}\n"
        f"**Segments required:** {num_segs}\n"
        f"**Words per segment:** ~{WORDS_PER_SEGMENT}\n"
        f"**Merge strategy:** {merge_guide}\n"
        f"{hint}{si}\n\n"
        f"{transcript_blocks}\n\n"
        f"REMINDERS:\n"
        f"- Segment 1: HOOK -> Welcome -> Content\n"
        f"- Strip EVERY competitor brand/name/CTA trace from ALL transcripts\n"
        f"- Add 25%+ more value through enrichment\n"
        f"- Last segment must have SKY Academy CTA + Telegram notes CTA\n"
        f"- ZERO emojis in telugu_text — hard technical requirement\n"
        f"- Return ONLY valid JSON array, nothing else"
    )
    return system, user


def build_prompts_pdf(
    pdf_text: str,
    topic_hint: str,
    num_segs: int,
    special_instructions: str,
    video_type: str = "subjective",
):
    vdna   = _DNA_GENERAL_VIDEO if video_type == "general" else _DNA_SUBJECTIVE_VIDEO
    system = _inject_counts(_SYSTEM_PDF + "\n\n" + vdna, num_segs)
    hint   = f"\n**Topic / Chapter context:** {topic_hint.strip()}" if topic_hint.strip() else ""
    si     = f"\nSpecial Instructions:\n{special_instructions.strip()}" if special_instructions.strip() else ""
    user   = (
        f"Convert the book/study material below into a SKY Academy voiceover script.\n"
        f"**Video Type:** {'General / Strategy / Motivation' if video_type == 'general' else 'Subjective / Deep Teaching'}\n"
        f"**Segments required:** {num_segs}\n"
        f"**Words per segment:** ~{WORDS_PER_SEGMENT}\n"
        f"{hint}{si}\n\n"
        f"BOOK / STUDY MATERIAL (start)\n"
        f"{pdf_text.strip()}\n"
        f"BOOK / STUDY MATERIAL (end)\n\n"
        f"REMINDERS:\n"
        f"- Segment 1: HOOK -> Welcome -> Content\n"
        f"- Bookish tone must be completely destroyed\n"
        f"- Last segment must have SKY Academy CTA + Telegram notes CTA\n"
        f"- ZERO emojis in telugu_text — hard technical requirement\n"
        f"- Return ONLY valid JSON array, nothing else"
    )
    return system, user


# ============================================================
# PROMPT BUILDER — PER-SEGMENT REGENERATE
# ============================================================

def build_regen_segment_prompt(
    video_type: str,
    topic: str,
    chunks: list,
    seg_idx: int,
    instruction: str,
    num_segs: int,
) -> tuple:
    """Build system + user prompts to regenerate a single segment."""
    vdna      = _DNA_GENERAL_VIDEO if video_type == "general" else _DNA_SUBJECTIVE_VIDEO
    is_first  = seg_idx == 0
    is_last   = seg_idx == len(chunks) - 1
    prev_text = chunks[seg_idx - 1].get("telugu_text", "")[:350] if seg_idx > 0 else ""
    next_text = chunks[seg_idx + 1].get("telugu_text", "")[:350] if seg_idx < len(chunks) - 1 else ""

    system = (
        "You are an expert Telugu video script writer for SKY Academy.\n"
        "Regenerate EXACTLY ONE segment of an existing script based on a specific instruction.\n"
        "Match the voice, tone, and energy of the surrounding segments precisely.\n"
        "CRITICAL: telugu_text MUST contain ZERO emoji characters.\n\n"
    ) + vdna + _SKY_DNA

    user = (
        f"Topic: {topic}\n"
        f"Total segments in script: {num_segs}\n"
        f"Regenerating: Segment {seg_idx + 1}\n"
        f"Change instruction: {instruction or 'Improve this segment — better flow, more energy, sharper memory hints'}\n\n"
        + (f"PREVIOUS SEGMENT (for continuity):\n{prev_text}\n\n" if prev_text else "")
        + f"CURRENT SEGMENT TO REPLACE:\n{chunks[seg_idx].get('telugu_text','')}\n\n"
        + (f"NEXT SEGMENT (for continuity):\n{next_text}\n\n" if next_text else "")
        + "RULES FOR THIS REGENERATION:\n"
        + ("- This IS Segment 1: must include Hook + Welcome + Content\n" if is_first else "")
        + ("- This IS the LAST segment: must include SKY Academy CTA + Telegram notes CTA\n" if is_last else "")
        + f"- Target: ~{WORDS_PER_SEGMENT} words in telugu_text\n"
        + f"- ZERO emojis in telugu_text — hard requirement\n"
        + f"- slide_prompt: Heading + 3 bullets + Image Prompt\n"
        + f"- Return ONLY valid JSON for ONE segment (not an array):\n"
        + '{"seg": ' + str(seg_idx + 1) + ', "telugu_text": "...", "slide_prompt": "..."}'
    )
    return system, user


# ============================================================
# PROMPT BUILDER — YOUTUBE SEO PACK
# ============================================================

def build_seo_prompt(topic: str, chunks: list, video_type: str) -> tuple:
    """Build prompts to generate YouTube title + tags for the script."""
    preview = " ".join(
        c.get("telugu_text", "")[:180] for c in chunks[:3]
    )
    system = (
        "You are a YouTube SEO expert specializing in Telugu competitive exam content. "
        "Generate highly optimized YouTube metadata for maximum reach. "
        "Return ONLY valid JSON, no markdown, no explanation."
    )
    vtype_label = (
        "General Strategy / Guidance / Motivation video"
        if video_type == "general"
        else "Deep Subject Teaching / Explanation video"
    )
    user = (
        f"Script Topic: {topic}\n"
        f"Video Type: {vtype_label}\n"
        f"Script Preview: {preview[:450]}\n\n"
        f"Generate:\n"
        f"1. ONE compelling YouTube video TITLE\n"
        f"   - Telugu + English natural mix\n"
        f"   - Max 70 characters\n"
        f"   - Must contain primary topic keyword\n"
        f"   - Click-worthy for Telugu competitive exam students\n"
        f"   - Include year (2025 or 2026) where relevant\n\n"
        f"2. 20 YouTube TAGS (comma-separated single string)\n"
        f"   - Mix of: exam names in Telugu, subject keywords, SKY Academy variants\n"
        f"   - Include: sky academy telugu, telugu competitive exams, appsc, tspsc, upsc telugu\n"
        f"   - Topic-specific high-search keywords\n\n"
        f"Return ONLY this exact JSON structure:\n"
        f'{{"title": "your title here", "tags": "tag1, tag2, tag3, ...20 tags total"}}'
    )
    return system, user


# ============================================================
# STUDY NOTES HTML GENERATOR — Beautiful PDF-ready export
# ============================================================

def generate_study_notes_html(topic: str, chunks: list, video_type: str) -> str:
    """
    Generates a beautiful, SKY Academy branded HTML file.
    User downloads -> opens in Chrome/Edge -> Ctrl+P -> Save as PDF.
    Telugu fonts render perfectly via browser engine.
    """
    # Color palettes per section (dark_color, light_bg, accent)
    palettes = [
        ("#1e3a8a", "#eff6ff", "#3b82f6"),   # blue
        ("#7f1d1d", "#fef2f2", "#ef4444"),   # red
        ("#14532d", "#f0fdf4", "#22c55e"),   # green
        ("#7c2d12", "#fff7ed", "#f97316"),   # orange
        ("#312e81", "#eef2ff", "#6366f1"),   # indigo
        ("#701a75", "#fdf4ff", "#a855f7"),   # purple
        ("#713f12", "#fefce8", "#eab308"),   # yellow-amber
        ("#134e4a", "#f0fdfa", "#14b8a6"),   # teal
    ]

    sections_html = ""
    for i, chunk in enumerate(chunks):
        slide = chunk.get("slide_prompt", "")
        heading = f"Section {i + 1}"
        bullets = []

        for line in slide.strip().split("\n"):
            ln = line.strip()
            if not ln:
                continue
            if ln.lower().startswith("heading:"):
                heading = ln[8:].strip()
            elif ln.startswith(("•", "-", "*")) and not ln.lower().startswith("image prompt"):
                b = ln.lstrip("•-* ").strip()
                if b:
                    bullets.append(b)
            elif ":" not in ln and not ln.lower().startswith("image"):
                # bare text line — might be a continuation bullet
                if len(ln) > 4:
                    bullets.append(ln)

        dark, light, accent = palettes[i % len(palettes)]

        bullet_items_html = "".join(
            f'<li style="margin:7px 0;color:#1f2937;font-size:13.5px;'
            f'line-height:1.65;font-family:Segoe UI,Arial Unicode MS,Arial,sans-serif">'
            f'{b}</li>'
            for b in bullets
        )

        sections_html += f"""
        <div style="background:{light};border-left:5px solid {accent};
                    border-radius:12px;padding:16px 20px;margin:14px 0;
                    page-break-inside:avoid;box-shadow:0 2px 8px rgba(0,0,0,0.07)">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px">
                <span style="background:{dark};color:#fff;border-radius:50%;
                             width:30px;height:30px;min-width:30px;
                             display:inline-flex;align-items:center;justify-content:center;
                             font-weight:800;font-size:13px">{i + 1}</span>
                <h3 style="color:{dark};font-size:15px;font-weight:800;margin:0;
                           font-family:Segoe UI,Arial Unicode MS,Arial,sans-serif;
                           line-height:1.3">{heading}</h3>
            </div>
            {'<ul style="margin:0;padding-left:20px">' + bullet_items_html + '</ul>'
              if bullet_items_html
              else '<p style="color:#6b7280;font-size:12.5px;font-style:italic;margin:0">'
                   'Refer to video for detailed explanation.</p>'}
        </div>
        """

    vtype_label = "STRATEGY NOTES" if video_type == "general" else "SUBJECT NOTES"
    vtype_color = "#f97316" if video_type == "general" else "#22c55e"
    seg_count   = len(chunks)
    total_words = sum(len(c.get("telugu_text", "").split()) for c in chunks)

    html = f"""<!DOCTYPE html>
<html lang="te">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>SKY Academy — {topic} — Classroom Notes</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Segoe UI','Arial Unicode MS',Arial,sans-serif;
      background:#e8eeff;padding:20px;color:#1f2937}}
.wrap{{max-width:800px;margin:0 auto;background:#fff;border-radius:20px;
        overflow:hidden;box-shadow:0 10px 50px rgba(0,0,0,0.18)}}
@media print{{
  body{{background:#fff;padding:0}}
  .wrap{{box-shadow:none;border-radius:0;max-width:100%}}
  .no-print{{display:none!important}}
  @page{{margin:1.5cm}}
}}
</style>
</head>
<body>
<div class="wrap">

  <!-- HEADER -->
  <div style="background:linear-gradient(135deg,#020024 0%,#090979 45%,#00d4ff 100%);
              padding:30px 28px 24px;text-align:center">
    <div style="font-size:44px;font-weight:900;letter-spacing:10px;margin-bottom:3px;
                line-height:1">
      <span style="color:#FF6B6B;text-shadow:0 0 24px rgba(255,107,107,.55)">S</span>
      <span style="color:#FFE66D;text-shadow:0 0 24px rgba(255,230,109,.55)">K</span>
      <span style="color:#4ECDC4;text-shadow:0 0 24px rgba(78,205,196,.55)">Y</span>
    </div>
    <div style="color:rgba(255,255,255,.85);font-size:10px;font-weight:800;
                letter-spacing:5px;margin-bottom:18px">ACADEMY</div>
    <div style="background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.32);
                border-radius:12px;padding:12px 22px;display:inline-block;
                max-width:90%">
      <div style="color:#FFE66D;font-size:20px;font-weight:800;line-height:1.3">
        {topic}
      </div>
    </div>
    <div style="margin-top:12px;display:flex;gap:8px;justify-content:center;flex-wrap:wrap">
      <span style="background:{vtype_color};color:#fff;border-radius:20px;
                   padding:3px 16px;font-size:11px;font-weight:700;letter-spacing:1px">
        {vtype_label}
      </span>
      <span style="background:rgba(255,255,255,.18);color:#fff;border-radius:20px;
                   padding:3px 14px;font-size:11px;font-weight:600">
        {seg_count} sections  |  ~{total_words} words
      </span>
    </div>
  </div>

  <!-- INTRO STRIP -->
  <div style="background:linear-gradient(135deg,#eff6ff,#dbeafe);
              padding:12px 22px;text-align:center;
              font-size:13px;color:#1e40af;border-bottom:1px solid #bfdbfe">
    <strong>Classroom Notes</strong> — Video చూసిన తర్వాత print చేసుకుని revision కి use చేయండి!
    &nbsp;|&nbsp; <strong>SKY Academy Telugu Competitive Exam Preparation</strong>
  </div>

  <!-- PRINT BUTTON -->
  <div class="no-print" style="text-align:center;padding:16px 22px 4px">
    <button onclick="window.print()" style="
      background:linear-gradient(135deg,#020024,#090979);color:#fff;
      border:none;border-radius:10px;padding:11px 32px;font-size:14px;
      font-weight:700;cursor:pointer;letter-spacing:1px;
      box-shadow:0 4px 16px rgba(9,9,121,.35)">
      Print / Save as PDF
    </button>
    <p style="font-size:11px;color:#6b7280;margin-top:7px">
      Chrome or Edge recommended for best Telugu font rendering
    </p>
  </div>

  <!-- CONTENT -->
  <div style="padding:12px 22px 22px">
    {sections_html}
  </div>

  <!-- TELEGRAM BOX -->
  <div style="margin:0 22px 22px;background:linear-gradient(135deg,#eff6ff,#dbeafe);
              border:2px solid #3b82f6;border-radius:14px;padding:18px 22px;
              text-align:center">
    <div style="font-size:26px;margin-bottom:8px">📱</div>
    <h4 style="color:#1e40af;font-size:16px;font-weight:800;margin-bottom:8px">
      SKY Academy Telegram Channel
    </h4>
    <p style="color:#1e40af;font-size:13.5px;line-height:1.75">
      ఈ notes, daily PDFs, previous year questions, exam alerts —<br>
      అన్నీ <strong>FREE</strong> గా Telegram channel లో available!<br>
      Join చేసి మీ preparation ని next level కి తీసుకెళ్ళండి!
    </p>
  </div>

  <!-- FOOTER -->
  <div style="background:linear-gradient(135deg,#020024,#090979);
              padding:16px 22px;text-align:center">
    <div style="font-size:18px;font-weight:900;letter-spacing:5px;margin-bottom:4px">
      <span style="color:#FF6B6B">S</span>
      <span style="color:#FFE66D">K</span>
      <span style="color:#4ECDC4">Y</span>
    </div>
    <div style="color:rgba(255,255,255,.6);font-size:10px">
      SKY ACADEMY &nbsp;|&nbsp; Script Engine v3.1 &nbsp;|&nbsp; {vtype_label}
      &nbsp;|&nbsp; Internal Tool
    </div>
  </div>

</div>
</body>
</html>"""
    return html


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
# AI CALL FUNCTIONS — ALL USE STREAMING
# ============================================================

def call_claude_pagegrid(
    api_key: str, model: str, system: str, user: str, progress_cb=None
) -> str:
    import anthropic
    if not api_key.startswith("sk-pgrid-"):
        raise ValueError(
            "PageGrid key must start with 'sk-pgrid-'. "
            "Get yours at pagegrid.in -> Dashboard -> API Keys."
        )
    client = anthropic.Anthropic(
        api_key=api_key,
        base_url=PAGEGRID_BASE_URL,
        timeout=300.0,
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
    import openai
    client       = openai.OpenAI(api_key=api_key, timeout=300.0)
    is_reasoning = model.startswith("o1") or model.startswith("o3")

    if is_reasoning:
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
# STREAMING DISPATCHER
# ============================================================

def run_generation(
    api_key: str,
    provider: str,
    model: str,
    system_p: str,
    user_p: str,
    status_placeholder,
) -> str:
    def _cb(n_chars: int):
        status_placeholder.markdown(
            f'<div class="stream-progress">'
            f'<b>Generating...</b> &nbsp; {n_chars:,} characters received'
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
    if not raw or not raw.strip():
        return None

    cleaned = raw.strip()
    cleaned = re.sub(r"^```[a-zA-Z]*\s*\n?", "", cleaned)
    cleaned = re.sub(r"\n?```\s*$",          "", cleaned)
    cleaned = cleaned.strip()

    try:
        result = json.loads(cleaned)
        if isinstance(result, list) and result:
            return result
    except json.JSONDecodeError:
        pass

    start = cleaned.find("[")
    end   = cleaned.rfind("]")
    if start != -1 and end > start:
        try:
            result = json.loads(cleaned[start : end + 1])
            if isinstance(result, list) and result:
                return result
        except json.JSONDecodeError:
            pass

    for attempt in (raw, re.sub(r"```(?:json)?", "", raw).strip()):
        try:
            result = json.loads(attempt)
            if isinstance(result, list):
                return result
        except Exception:
            pass
        m = re.search(r"\[[\s\S]*\]", attempt)
        if m:
            try:
                result = json.loads(m.group())
                if isinstance(result, list):
                    return result
            except Exception:
                pass

    return None


def parse_single_segment(raw: str):
    """Parse a single segment JSON object (for per-segment regen)."""
    cleaned = raw.strip()
    cleaned = re.sub(r"^```[a-zA-Z]*\s*\n?", "", cleaned)
    cleaned = re.sub(r"\n?```\s*$",          "", cleaned).strip()

    # Try as object directly
    try:
        result = json.loads(cleaned)
        if isinstance(result, dict):
            return result
        if isinstance(result, list) and result:
            return result[0]
    except Exception:
        pass

    # Find JSON object
    m = re.search(r'\{[\s\S]*\}', cleaned)
    if m:
        try:
            result = json.loads(m.group())
            if isinstance(result, dict):
                return result
        except Exception:
            pass
    return None


def parse_seo_json(raw: str):
    """Parse SEO pack JSON response."""
    cleaned = raw.strip()
    cleaned = re.sub(r"^```[a-zA-Z]*\s*\n?", "", cleaned)
    cleaned = re.sub(r"\n?```\s*$",          "", cleaned).strip()
    try:
        result = json.loads(cleaned)
        if isinstance(result, dict):
            return result
    except Exception:
        pass
    m = re.search(r'\{[\s\S]*\}', cleaned)
    if m:
        try:
            return json.loads(m.group())
        except Exception:
            pass
    return None


# ============================================================
# GOOGLE SHEETS — A:C for segments, D2 = title, E2 = tags
# ============================================================

def push_to_gsheet(chunks: list, seo_title: str = "", seo_tags: str = ""):
    """
    Pushes synced chunks to Sheet1.
    - A2:C = seg number, telugu_text, slide_prompt
    - D2   = YouTube title (if SEO pack generated)
    - E2   = YouTube tags  (if SEO pack generated)
    - Preserves row-1 headers
    """
    try:
        import gspread
        from google.oauth2.service_account import Credentials

        scopes = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = Credentials.from_service_account_info(_HARDCODED_CREDS, scopes=scopes)
        gc    = gspread.authorize(creds)
        sheet = gc.open_by_key(SHEET_ID)
        ws    = sheet.get_worksheet(0)

        # Clear A2:E (segments + SEO columns)
        ws.batch_clear(["A2:E10000"])

        # Write segments A2:C
        rows = [
            [
                i + 1,
                c.get("telugu_text", ""),
                c.get("slide_prompt", ""),
            ]
            for i, c in enumerate(chunks)
        ]
        ws.update("A2", rows, value_input_option="RAW")

        # Write SEO pack if available
        seo_msg = ""
        if seo_title.strip():
            ws.update("D2", [[seo_title.strip()]], value_input_option="RAW")
            seo_msg += " · Title → D2"
        if seo_tags.strip():
            ws.update("E2", [[seo_tags.strip()]], value_input_option="RAW")
            seo_msg += " · Tags → E2"

        last_row = 1 + len(rows)
        return True, (
            f"Pushed {len(rows)} segments to Sheet1 "
            f"(A2:C{last_row}){seo_msg} — previous data cleared."
        )

    except Exception as exc:
        return False, f"Sheets error: {exc}"


# ============================================================
# ERROR HANDLER
# ============================================================

def _handle_api_error(exc: Exception, model_choice: str):
    err = str(exc)
    if "401" in err or "authentication_error" in err:
        st.error(
            "**401 — Invalid API key.**\n\n"
            "- PageGrid key must start with `sk-pgrid-`\n"
            "- Regenerate at pagegrid.in -> Dashboard -> API Keys"
        )
    elif "402" in err or "billing_error" in err:
        st.error(
            "**402 — Wallet balance is $0.**\n\n"
            "Add funds at pagegrid.in -> Dashboard -> Wallet & Billing"
        )
    elif "404" in err or "not found or inactive" in err:
        st.error(
            f"**404 — Model `{model_choice}` not found.**\n\n"
            f"Valid PageGrid models: `claude-opus-4-6`, `claude-sonnet-4-6`, `claude-haiku-4-5`"
        )
    elif "403" in err or "permission_error" in err:
        st.error(
            "**403 — Permission denied.**\n\n"
            "Check key permissions in the PageGrid dashboard."
        )
    elif "429" in err or "rate_limit" in err:
        st.error(
            "**429 — Rate limited.**\n\n"
            "Default limit: 10 RPM. Wait ~60 sec and retry."
        )
    elif "524" in err or "timeout" in err.lower():
        st.error(
            "**524 / Timeout — Request took too long.**\n\n"
            "- Try a faster model (e.g. `claude-haiku-4-5` or `gemini-2.0-flash`)\n"
            "- Reduce total word count (try 480 words -> 4 segments)\n"
            "- If using PDF/Transcript mode, upload a shorter document\n"
            "- Retry — the next attempt usually succeeds"
        )
    else:
        st.error(f"Generation error: {exc}")


# ============================================================
# MANUAL RECOVERY WIDGET
# ============================================================

def _show_manual_recovery(display_topic: str, display_source: str):
    st.markdown("#### Manual Recovery")
    st.caption(
        "The script was generated but JSON parsing failed. "
        "Paste the raw response here to retry parsing:"
    )
    manual_raw = st.text_area(
        "Paste Raw JSON here",
        height=200,
        placeholder='[{"seg": 1, "telugu_text": "...", "slide_prompt": "..."}]',
        key="manual_json_input",
    )
    if st.button("Retry Parse", key="retry_parse_btn"):
        parsed = parse_segments(manual_raw or st.session_state.raw_response)
        if parsed:
            store_new_chunks(parsed)
            st.session_state.last_topic  = display_topic
            st.session_state.last_source = display_source
            st.success(f"Recovered! {len(parsed)} segments parsed.")
            st.rerun()
        else:
            st.error(
                "Still could not parse. "
                "Check for unescaped quotes in the JSON."
            )


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
    "seo_pack":               None,
}
for _k, _v in _defaults.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("## Configuration")
    st.markdown("### AI Provider & Model")
    provider     = st.selectbox("Provider", list(MODEL_OPTIONS.keys()))
    model_choice = st.selectbox("Model", MODEL_OPTIONS[provider])

    _key_meta = {
        "☁️  Claude  (via PageGrid)": (
            "PageGrid API Key", "sk-pgrid-...",
            "pagegrid.in -> Dashboard -> API Keys", "sk-pgrid-",
        ),
        "🟢  OpenAI  (GPT)": (
            "OpenAI API Key", "sk-...",
            "platform.openai.com -> API Keys", "sk-",
        ),
        "🔵  Google  (Gemini)": (
            "Google AI API Key", "AIzaSy...",
            "aistudio.google.com -> Get API Key", "AIzaSy",
        ),
    }
    _lbl, _ph, _hlp, _prefix = _key_meta[provider]
    st.markdown(f"### {_lbl}")
    st.caption(f"Get yours: {_hlp}")
    api_key = st.text_input(_lbl, type="password", placeholder=_ph,
                            label_visibility="collapsed")
    if api_key:
        if api_key.startswith(_prefix):
            st.markdown('<p class="key-ok">Key format looks valid</p>',
                        unsafe_allow_html=True)
        else:
            st.markdown(
                f'<p class="key-warn">Key should start with <code>{_prefix}</code></p>',
                unsafe_allow_html=True,
            )

    if "PageGrid" in provider:
        st.info(
            "**PageGrid valid models:**\n"
            "- `claude-opus-4-6` — Most intelligent\n"
            "- `claude-sonnet-4-6` — Fast & smart\n"
            "- `claude-haiku-4-5` — Fastest\n\n"
            "**base_url:** `https://api.pagegrid.in`",
            icon="📋",
        )

    st.divider()
    st.markdown("### Google Sheets")
    st.success(
        "Service account loaded\n\n"
        "**forscripting@gen-lang-client...**\n\n"
        "Push to Sheets always ready.",
        icon="🔑",
    )
    st.caption(
        f"[Open Target Sheet]"
        f"(https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit)"
    )

    st.divider()
    st.caption("SCRIPT ENGINE v3.1 · SKY Academy Internal Tool")
    st.caption(f"Each segment ~{WORDS_PER_SEGMENT} words ~55 sec speech")


# ============================================================
# MAIN LAYOUT
# ============================================================
left, right = st.columns([1, 1], gap="large")

topic_input      = ""
topic_hint_input = ""
input_mode       = ""
merge_mode_val   = "auto"
video_type       = "subjective"   # default — overwritten below

with left:
    st.markdown("## Script Input")

    # ── VIDEO TYPE SELECTOR ────────────────────────────────
    st.markdown("### Video Type")
    vtype_label = st.radio(
        "Select video type",
        options=[
            "📚 Subjective  —  Deep Subject Teaching",
            "🎯 General  —  Strategy / Motivation / Guidance",
        ],
        key="video_type_select",
        label_visibility="collapsed",
    )
    video_type = "general" if vtype_label.startswith("🎯") else "subjective"

    if video_type == "general":
        st.markdown("""
        <div class="vtype-general">
        <b>General / Strategy Mode</b> — High motivation energy, study approach guidance,
        smart prioritization hints (e.g. Dibru + BRU + TEA style connections),
        SKY Academy community building. Perfect for: strategy videos, how-to-study,
        cutoffs, syllabus, book-list, schedule, exam-date videos.
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="vtype-subjective">
        <b>Subjective / Deep Teaching Mode</b> — Maximum memory hints (minimum one per
        major concept), full exam angle integration, PYQ references, silent app CTA,
        Telegram study notes CTA in last segment.
        Perfect for: topic explanations, PYQ series, full-subject deep-dives.
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── INPUT MODE ────────────────────────────────────────
    input_mode = st.radio(
        "What are you providing?",
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
        <b>Topic Mode</b> — Type any subject. SKY Engine writes a complete original
        voiceover from scratch: hook intro, exam angles, real-world examples,
        memory hints, natural AP tutor voice throughout.
        </div>""", unsafe_allow_html=True)

        topic_input = st.text_area(
            "Topic / Subject *",
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
        <b>Multi-Transcript Mode</b> — Upload one or more competitor transcript files
        (.docx / .txt / .pdf). SKY Engine will: strip all competitor branding,
        intelligently merge/synthesize across files, enrich by +25%,
        rewrite in natural SKY Academy voice with hook intro.
        </div>""", unsafe_allow_html=True)

        topic_hint_input = st.text_input(
            "Topic hint  (optional — helps accurate slide prompts)",
            placeholder="e.g.  UPSC 2025 Cutoff, TSPSC Exam Date, SSC CGL Strategy...",
        )

        merge_label = st.radio(
            "How should multiple files be merged?",
            options=[
                "Auto-detect  (AI decides)",
                "Synthesize same topic  (different data on same subject)",
                "Merge different topics  (weave different aspects together)",
            ],
            horizontal=False,
        )
        merge_mode_val = {
            "Auto-detect  (AI decides)":                                "auto",
            "Synthesize same topic  (different data on same subject)":  "synthesize",
            "Merge different topics  (weave different aspects together)": "merge_aspects",
        }[merge_label]

        transcript_files = st.file_uploader(
            "Upload Transcript Files *",
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
                with st.spinner(f"Extracting text from {len(transcript_files)} file(s)..."):
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
                    f'<b>{ok_count} file(s) ready</b>'
                    + (f' · {err_count} failed' if err_count else '')
                    + f' | ~{total_words:,} total words'
                    + f' | Merge: <b>{merge_label}</b>'
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
                    f"Preview extracted content ({len(ok_exts)} files)", expanded=False
                ):
                    for e in ok_exts:
                        st.markdown(f"**{e['filename']}** — {e['words']:,} words")
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
        <b>PDF Mode</b> — Upload a book chapter or study notes PDF.
        SKY Engine extracts the text and transforms dry academic content into
        a fully engaging SKY Academy voiceover — zero bookish tone,
        hook intro, rich memory hints, pure AP tutor energy.
        </div>""", unsafe_allow_html=True)

        topic_hint_input = st.text_input(
            "Topic / Chapter context  (optional)",
            placeholder="e.g.  Chapter 3: Directive Principles, Unit 5: Cell Respiration...",
        )

        pdf_file = st.file_uploader(
            "Upload PDF *", type=["pdf"],
            help="Upload the book section, study notes, or chapter to be scripted",
        )
        topic_input = ""

        if pdf_file is not None:
            file_bytes = pdf_file.read()
            file_sig   = f"{pdf_file.name}_{len(file_bytes)}"
            if file_sig != st.session_state.last_pdf_sig:
                with st.spinner("Extracting text from PDF..."):
                    extracted, lib_info = extract_pdf_text(file_bytes)
                    if extracted:
                        st.session_state.pdf_text     = extracted
                        st.session_state.last_pdf_sig = file_sig
                        st.session_state.last_pdf_lib = lib_info
                    else:
                        st.session_state.pdf_text     = ""
                        st.session_state.last_pdf_sig = ""
                        st.error(f"Could not extract PDF text. {lib_info}")

            if st.session_state.pdf_text:
                wc = len(st.session_state.pdf_text.split())
                st.success(
                    f"Extracted: ~{wc:,} words · {st.session_state.last_pdf_lib}"
                )
                with st.expander("Preview extracted text", expanded=False):
                    st.text(st.session_state.pdf_text[:800] + "\n\n[... more ...]")
                topic_input = st.session_state.pdf_text

    # ── Word count / segments ─────────────────────────────
    st.markdown("---")
    approx_words = st.number_input(
        "Approximate Total Script Words",
        min_value=120, max_value=6000, value=600, step=120,
        help=(
            f"Auto-splits into ~{WORDS_PER_SEGMENT}-word segments (~55 sec each). "
            "600 words -> 5 segments -> ~5 min video."
        ),
    )
    num_segs = max(1, math.ceil(approx_words / WORDS_PER_SEGMENT))
    est_dur  = round(approx_words / 130, 1)
    st.markdown(
        f'<div class="word-info">'
        f'<b>{num_segs} segments</b> will be generated &nbsp;·&nbsp; '
        f'~{approx_words} words &nbsp;·&nbsp; ~{est_dur} min video'
        f'</div>',
        unsafe_allow_html=True,
    )

    special_instructions = st.text_area(
        "Special Instructions  (optional)",
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
        gen_btn   = st.button("Generate Script", type="primary",
                              use_container_width=True)
    with c2:
        clear_btn = st.button("Clear All", use_container_width=True)


# ── Clear ──────────────────────────────────────────────────
if clear_btn:
    for _k, _v in _defaults.items():
        st.session_state[_k] = _v
    # Also clear any widget states for old segments
    for _i in range(50):
        for _pfx in ["tv_", "sv_", "regen_instr_"]:
            if f"{_pfx}{_i}" in st.session_state:
                del st.session_state[f"{_pfx}{_i}"]
    for _k in ["seo_title_edit", "seo_tags_edit"]:
        if _k in st.session_state:
            del st.session_state[_k]
    st.rerun()


# ============================================================
# GENERATE
# ============================================================
if gen_btn:
    if   input_mode.startswith("📌"): mode_name = "topic"
    elif input_mode.startswith("📝"): mode_name = "transcript"
    else:                              mode_name = "pdf"

    if not api_key.strip():
        st.error("Please enter your API key in the sidebar!")

    elif mode_name == "topic" and not topic_input.strip():
        st.error("Please enter a topic!")

    elif mode_name == "transcript":
        ok_exts = [e for e in st.session_state.transcript_extractions if e["ok"]]
        if not ok_exts:
            st.error(
                "Please upload at least one transcript file "
                "(.docx / .txt / .pdf) and make sure it extracts successfully."
            )
        else:
            safe_transcripts = [
                {"filename": e["filename"], "text": e["text"]}
                for e in ok_exts
            ]
            vtype_disp = "General/Strategy" if video_type == "general" else "Subjective/Teaching"
            st.info(
                f"Merging {len(safe_transcripts)} transcript(s) → SKY Academy voice "
                f"[{vtype_disp}]... Do not close this tab.",
                icon="⏳",
            )
            _status = st.empty()
            try:
                system_p, user_p = build_prompts_multi_transcript(
                    safe_transcripts, topic_hint_input,
                    num_segs, special_instructions, merge_mode_val,
                    video_type,
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
                    store_new_chunks(parsed)
                    st.session_state.last_topic  = display_topic
                    st.session_state.last_source = display_source
                    st.success(
                        f"{len(parsed)} segments generated from "
                        f"{len(safe_transcripts)} file(s)! [{display_source}]"
                    )
                    st.rerun()
                else:
                    st.error(
                        "Could not parse JSON from AI response. "
                        "Expand Raw AI Response below to inspect."
                    )
                    _show_manual_recovery(display_topic, display_source)

            except Exception as exc:
                _status.empty()
                _handle_api_error(exc, model_choice)

    elif mode_name == "pdf" and not topic_input.strip():
        st.error("Please upload a PDF. Make sure text was extracted successfully.")

    else:
        vtype_disp = "General/Strategy" if video_type == "general" else "Subjective/Teaching"
        _mode_label = (
            f"Generating {num_segs} segments [{vtype_disp}] via "
            f"{'PageGrid -> ' + model_choice if 'PageGrid' in provider else model_choice}"
            if mode_name == "topic"
            else f"Converting PDF content -> SKY Academy voice [{vtype_disp}]"
        )
        st.info(
            f"{_mode_label}... Progress shown below. Do not close this tab.",
            icon="⏳",
        )
        _status = st.empty()
        try:
            if mode_name == "topic":
                system_p, user_p = build_prompts_topic(
                    topic_input, num_segs, special_instructions, video_type
                )
                display_topic  = topic_input.strip()[:60]
                display_source = "📌 Topic"
            else:
                system_p, user_p = build_prompts_pdf(
                    topic_input, topic_hint_input, num_segs, special_instructions, video_type
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
                store_new_chunks(parsed)
                st.session_state.last_topic  = display_topic
                st.session_state.last_source = display_source
                st.success(f"{len(parsed)} segments generated! [{display_source}]")
                st.rerun()
            else:
                st.error(
                    "Could not parse JSON from AI response. "
                    "Expand Raw AI Response below to inspect."
                )
                _show_manual_recovery(display_topic, display_source)

        except Exception as exc:
            _status.empty()
            _handle_api_error(exc, model_choice)


# ============================================================
# RIGHT: PREVIEW
# ============================================================
with right:
    st.markdown("## Preview")
    chunks = st.session_state.chunks

    if chunks:
        total_words = sum(len(c.get("telugu_text", "").split()) for c in chunks)
        est_min     = round(total_words / 130, 1)

        badge_class = {
            "📌 Topic":            "badge-topic",
            "📝 Transcript → SKY": "badge-transcript",
            "📚 PDF → SKY":        "badge-pdf",
        }.get(st.session_state.last_source, "badge-topic")

        vtype_badge_color = "#f97316" if video_type == "general" else "#22c55e"
        vtype_badge_label = "General" if video_type == "general" else "Subjective"

        st.markdown(
            f'<span class="{badge_class}">{st.session_state.last_source}</span>'
            f'&nbsp;&nbsp;'
            f'<span style="background:{vtype_badge_color};color:#fff;border-radius:8px;'
            f'padding:4px 12px;font-size:.8rem;font-weight:700">{vtype_badge_label}</span>'
            f'&nbsp;&nbsp;'
            f'<span class="stat-pill">{len(chunks)} segments</span>'
            f'<span class="stat-pill">~{total_words:,} words</span>'
            f'<span class="stat-pill">~{est_min} min</span>',
            unsafe_allow_html=True,
        )
        st.markdown("")

        # ── SEGMENT TABS ──────────────────────────────────
        tabs = st.tabs([f"▶ {i + 1}" for i in range(len(chunks))])
        for tab, chunk, idx in zip(tabs, chunks, range(len(chunks))):
            with tab:
                seg_words = len(chunk.get("telugu_text", "").split())
                st.caption(
                    f"~{seg_words} words · ~{round(seg_words / 130, 1)} min"
                    + (" · Hook + Welcome" if idx == 0 else "")
                    + (" · Closing CTA" if idx == len(chunks) - 1 else "")
                )

                st.markdown("**Voiceover Script**")
                st.text_area(
                    f"vo_{idx}",
                    key=f"tv_{idx}",
                    height=220,
                    label_visibility="collapsed",
                )
                st.markdown("**Slide Prompt**")
                st.text_area(
                    f"sl_{idx}",
                    key=f"sv_{idx}",
                    height=130,
                    label_visibility="collapsed",
                )

                # ── PER-SEGMENT REGENERATE ─────────────────
                with st.expander(f"🔄 Redo Segment {idx + 1}", expanded=False):
                    st.markdown(
                        '<div class="regen-hint">Describe what to change — '
                        'only this segment will be regenerated, rest stays untouched.</div>',
                        unsafe_allow_html=True,
                    )
                    regen_instr = st.text_area(
                        "Change instruction",
                        placeholder=(
                            "e.g. Add 2 memory hints for the key dates\n"
                            "Make this more energetic and punchy\n"
                            "Too long — trim to 100 words\n"
                            "Rephrase — current version sounds too bookish"
                        ),
                        height=90,
                        key=f"regen_instr_{idx}",
                        label_visibility="collapsed",
                    )
                    regen_btn = st.button(
                        f"Regenerate Segment {idx + 1}",
                        key=f"regen_btn_{idx}",
                        use_container_width=True,
                    )
                    if regen_btn:
                        if not api_key.strip():
                            st.error("Enter API key in sidebar first!")
                        else:
                            _regen_status = st.empty()
                            with st.spinner(f"Regenerating segment {idx + 1}..."):
                                try:
                                    _instr = (
                                        st.session_state.get(f"regen_instr_{idx}", "")
                                        or "Improve this segment — better flow, sharper memory hints"
                                    )
                                    sys_r, usr_r = build_regen_segment_prompt(
                                        video_type,
                                        st.session_state.last_topic,
                                        st.session_state.chunks,
                                        idx,
                                        _instr,
                                        len(st.session_state.chunks),
                                    )
                                    raw_r = run_generation(
                                        api_key, provider, model_choice,
                                        sys_r, usr_r, _regen_status,
                                    )
                                    _regen_status.empty()
                                    new_chunk = parse_single_segment(raw_r)
                                    if new_chunk and isinstance(new_chunk, dict):
                                        cleaned_tv = strip_emojis(
                                            new_chunk.get("telugu_text", "")
                                        )
                                        new_chunk["telugu_text"] = cleaned_tv
                                        # Update chunks list
                                        st.session_state.chunks[idx] = new_chunk
                                        # Update widget states so UI refreshes correctly
                                        st.session_state[f"tv_{idx}"] = cleaned_tv
                                        st.session_state[f"sv_{idx}"] = new_chunk.get("slide_prompt", "")
                                        st.success(f"Segment {idx + 1} regenerated!")
                                        st.rerun()
                                    else:
                                        st.error(
                                            "Could not parse regenerated segment. "
                                            "Try again or adjust the instruction."
                                        )
                                except Exception as _exc:
                                    _regen_status.empty()
                                    st.error(f"Regen error: {_exc}")

        # ── FULL SCRIPT ───────────────────────────────────
        with st.expander("Full Script — Continuous Flow", expanded=False):
            full = "\n\n".join(
                st.session_state.get(f"tv_{i}", c.get("telugu_text", ""))
                for i, c in enumerate(chunks)
            )
            st.text_area(
                "full_script", value=full, height=400,
                label_visibility="collapsed",
            )

        st.divider()

        # ── SEO PACK ──────────────────────────────────────
        st.markdown("#### YouTube SEO Pack")
        st.markdown(
            '<div class="seo-box">'
            'Generate an optimized YouTube title and 20 tags for this script. '
            'Title will be written to <b>D2</b>, Tags to <b>E2</b> when you push to Sheets.'
            '</div>',
            unsafe_allow_html=True,
        )
        seo_gen_btn = st.button(
            "Generate SEO Pack",
            key="seo_gen_btn",
            use_container_width=True,
        )
        if seo_gen_btn:
            if not api_key.strip():
                st.error("Enter API key in sidebar first!")
            else:
                _seo_status = st.empty()
                with st.spinner("Generating YouTube SEO Pack..."):
                    try:
                        sys_seo, usr_seo = build_seo_prompt(
                            st.session_state.last_topic,
                            sync_edits_to_chunks(),
                            video_type,
                        )
                        raw_seo = run_generation(
                            api_key, provider, model_choice,
                            sys_seo, usr_seo, _seo_status,
                        )
                        _seo_status.empty()
                        seo_data = parse_seo_json(raw_seo)
                        if seo_data and isinstance(seo_data, dict):
                            st.session_state.seo_pack = seo_data
                            # Pre-populate edit keys
                            st.session_state["seo_title_edit"] = seo_data.get("title", "")
                            st.session_state["seo_tags_edit"]  = seo_data.get("tags", "")
                            st.success("SEO Pack generated! Edit below before pushing to Sheets.")
                            st.rerun()
                        else:
                            st.error("Could not parse SEO response. Try again.")
                    except Exception as _exc:
                        _seo_status.empty()
                        st.error(f"SEO generation error: {_exc}")

        if st.session_state.seo_pack:
            with st.expander("Edit SEO Pack before pushing to Sheets", expanded=True):
                st.text_input(
                    "YouTube Title  →  D2",
                    key="seo_title_edit",
                    help="Max 70 characters recommended",
                )
                st.text_area(
                    "YouTube Tags  →  E2  (comma-separated)",
                    key="seo_tags_edit",
                    height=80,
                    help="20 tags recommended for maximum reach",
                )
                char_count = len(st.session_state.get("seo_title_edit", ""))
                st.caption(f"Title: {char_count}/70 chars")

        st.divider()

        # ── DOWNLOADS + PUSH ──────────────────────────────
        _fname      = st.session_state.last_topic[:20].replace(" ", "_")
        synced_data = sync_edits_to_chunks()

        ba, bb, bc = st.columns(3)
        with ba:
            st.download_button(
                "Download JSON",
                data=json.dumps(synced_data, ensure_ascii=False, indent=2).encode("utf-8"),
                file_name=f"sky_script_{_fname}.json",
                mime="application/json",
                use_container_width=True,
            )
        with bb:
            txt_out = "\n\n".join(
                f"--- Segment {i + 1} ---\n{c.get('telugu_text', '')}\n\n"
                f"[Slide Prompt]\n{c.get('slide_prompt', '')}"
                for i, c in enumerate(synced_data)
            )
            st.download_button(
                "Download TXT",
                data=txt_out.encode("utf-8"),
                file_name=f"sky_script_{_fname}.txt",
                mime="text/plain",
                use_container_width=True,
            )
        with bc:
            notes_html = generate_study_notes_html(
                st.session_state.last_topic or "Topic",
                synced_data,
                video_type,
            )
            st.download_button(
                "Download Study Notes",
                data=notes_html.encode("utf-8"),
                file_name=f"sky_notes_{_fname}.html",
                mime="text/html",
                use_container_width=True,
                help="Open in Chrome/Edge -> Ctrl+P -> Save as PDF. Telugu fonts render perfectly.",
            )

        st.caption(
            "Study Notes: open downloaded .html in Chrome, press Ctrl+P, save as PDF. "
            "Share the PDF in your Telegram channel!"
        )

        push_btn = st.button(
            "Push to Sheets",
            use_container_width=True,
            type="primary",
        )

        if push_btn:
            seo_title = st.session_state.get("seo_title_edit", "")
            seo_tags  = st.session_state.get("seo_tags_edit", "")
            with st.spinner("Clearing old data and writing to Sheet1..."):
                ok, msg = push_to_gsheet(synced_data, seo_title, seo_tags)
            if ok:
                st.success(msg)
                st.markdown(
                    f"[Open Sheet]"
                    f"(https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit)"
                )
            else:
                st.error(msg)

    else:
        st.markdown("""
        <div class="empty-preview">
            <h3>Preview will appear here</h3>
            <p style="margin-top:12px; font-size:0.9rem;">
                Choose video type → Input mode → Provide content → Click <b>Generate Script</b>
            </p>
            <p style="margin-top:18px; font-size:0.82rem; line-height:2.2; color:#6366f1;">
                📚 <b>Subjective</b> — Max memory hints, exam angles, app CTA<br>
                🎯 <b>General</b> — High motivation, strategy hints, community building<br>
                📌 <b>Topic</b> — Original script from any subject<br>
                📝 <b>Multi-Transcript</b> — Upload competitor files -> merged SKY voice<br>
                📚 <b>PDF</b> — Book content -> SKY voiceover with hook & memory hints<br>
                📄 <b>Study Notes</b> — Beautiful branded HTML -> print as PDF -> Telegram
            </p>
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# RAW RESPONSE DEBUG
# ============================================================
if st.session_state.raw_response:
    with st.expander(
        "Raw AI Response  (debug / manual copy-paste fallback)", expanded=False
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
    " <b>ACADEMY</b> &nbsp;|&nbsp; SCRIPT ENGINE v3.1 &nbsp;|&nbsp; "
    "Internal Tool &nbsp;|&nbsp; "
    "General + Subjective Modes &nbsp;|&nbsp; "
    "Powered by PageGrid + Anthropic SDK"
    "</div>",
    unsafe_allow_html=True,
)
