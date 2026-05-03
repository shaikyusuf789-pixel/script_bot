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
MEMORY HINTS — MEMORY TRICK RULES — RICH EXAMPLES LIBRARY (SKY ACADEMY STYLE)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HOW SKY ACADEMY MEMORY HINTS WORK:
The hint must be: OBVIOUS — CLEVER — IMPOSSIBLE TO FORGET.
Student should laugh or say "oh wow, I will never forget this!"
If you need to explain the hint, it is a BAD hint. Start over.

CORE RULES:
- NEVER use abbreviation mnemonics (no BKKKOMMS, VIBGYOR-type tricks, zero letter shortcuts)
- ONLY use WORD-ASSOCIATION and INTERLINKING:
  * Find meaning INSIDE the word itself (Katha=story → Kathak from story-land UP)
  * Link to geography/history naturally (Kuchipudi = village in AP = dance named after it)
  * Number links: 42 degree heat → 42nd Amendment style
  * Telugu number sound links: 6=aaru → sounds like "aaravadhu" (don't shout) → link to topic
  * Calendar date links: Feb 14 = Valentine's → find a love/union/bonding angle with topic
  * If no trick is natural — skip entirely, never force one
- Student must feel the CONNECTION, not memorize a random letter string

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TELUGU NUMBER → SOUND → TOPIC LINKING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
When a number must be remembered, take its Telugu word,
find a sound-alike Telugu word, and link that sound to the topic meaning.
The connection must be INSTANT — no explanation needed.
example: 
  1  = okati    → "oka chance" (only one shot)
                  → use for unique / once-in-history facts
  2  = rendu    → "rendu" (double trouble / second time)
                  → use for pairs, two conflicting events
  3  = mudu     → "mudu" (fuss / complication/in english three sounds like tree, connect it with some greenery,oxygen,co2,freshness,shadow,leaves,pollution, etc)
                  → use for three-way splits, tricky articles
  4  = nalugu   → sounds like English "nail", or sounds like door, four-door, so link with home door scene, or shutting door
                  → "nail it down" → 4 pillars, 4 Vedas, 4 fundamental duties
  5  = aidu     → "five fingers/hand/punch/boxing/fighting like with this scenerios to the sentence" (tension / anxiety)
                  → 5 year plans, 5 schedules → always creates tension!
  6  = aaru     → "aaravadhu" (don't shout / keep quiet)
                  → 6th Schedule = tribal areas, their own laws, outsiders keep quiet!
  7  = edu      → "edupu" (crying / weeping)
                  → 7 Wonders → so beautiful you cry; 7 sins → cry for humanity
  8  = enimidi  → sounds like English "enemy"
                  → 8th Schedule = 22 languages, enemy of those who want to forget them
  9  = tommidi  → sounds like "tommy" (stomach ache) or nine sounds like wine, link with some alcohol,drunken person,irresponsible so on
                  → 9 Fundamental Duties → stomach it, you have to do them!
  10 = padi     → "padipoyadu" (he fell / collapsed)
                  → 10th Schedule = Anti-Defection Law → politician who switches party FALLS
  11 = padakondu → "padakondu" 11 looks like two hands or two legs, link with two parallel things like railway tracks.
                  → 11th Schedule = Panchayati Raj - panchayat should run as central government runs parallelly in india
  12 = pannendu → "pannaga" (snake wrapping around)
                  → 12 months wrap around the year like a snake
  14 = padinalugu → link to Feb 14 Valentine's Day (see Calendar Links below)
  21 = iravai-okati → "like with mariage day, because two becomes one by marriage, 2 to 1"
                  → Article 21 = Right to Life & Liberty = life get disturbed after 21(marriage day) funnyway.
  42 = natai-rendu → "42 degree fever" → emergency in your body
                  → 42nd Amendment 1976 = Emergency era, most controversial amendment
  like this use numbers logics naturally, dont force, search web for good logics and use it in script.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CALENDAR DATE MEMORY LINKS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Use dates the student already knows emotionally — bind the topic to that emotion.
Student already has the date locked — you just attach new meaning to it.

  Jan 26  = Republic Day → Constitution came into FORCE → India became a Republic
            "Jan 26, 1950 — Constitution was enforced — India stopped being under British rule
             even on paper — Happy Republic Day means Happy Constitution Day!"

  Feb 14  = Valentine's Day (love / union / bonding)
            → Link to any topic about agreements, unions, treaties, joint efforts
            "Panchsheel Agreement 1954 — India-China's 5 love promises to each other —
             Feb 14 energy — 5 principles of peaceful love between neighbors —
             but this love story didn't last!"

  Mar 8   = International Women's Day
            → Link to women's rights laws, gender schemes, women leaders in history
            "Savitribai Phule started India's first girls' school — Mar 8 energy —
             every Women's Day, remember her name before any other!"

  Apr 1   = Fool's Day → Link to exam traps, commonly confused facts
            "Don't be a fool — Article 32 is the RIGHT to Constitutional Remedies,
             NOT Article 226 — that's High Court's writ power — Fool's Day trap in every exam!"

  Apr 14  = Ambedkar Jayanti → All Constitution drafting facts anchor here
            "B.R. Ambedkar born April 14, 1891 — Constitution drafting completed
             November 26, 1949 — his whole life was the Constitution"

  Aug 15  = Independence Day → 1947
            "Quit India 1942 → 9+4+2=15 → August 15 → Independence 1947 — math never lies!"

  Oct 2   = Gandhi Jayanti → Non-violence, Satyagraha, Civil Disobedience
            "Dandi March started March 12 → 3+1+2=6 → aaru = aaravadhu →
             British told Gandhi to keep quiet — he didn't!"

  Nov 14  = Children's Day (Nehru's birthday) → First Prime Minister facts
            "Nov 14 = Children's Day because Nehru loved children —
             but he also LOVED power — India's first and longest-serving PM!"

  Nov 26  = Constitution Day (Samvidhan Divas) → Constitution ADOPTED 1949
            "Nov 26 adopted, Jan 26 enforced — adopted = baby born, enforced = baby walks —
             two months gap between birth and first steps!"

  Dec 10  = Human Rights Day → UDHR adopted 1948 → Fundamental Rights comparison
            "UN gave world its Rights on Dec 10, 1948 —
             India gave its own Rights in Constitution, Jan 26, 1950 —
             India was just 16 months behind the whole world!"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EXAMPLES LIBRARY — ALL SUBJECTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

POLITY / CONSTITUTION:
  "Fancy words = France" (Liberty, Equality, Fraternity → French Revolution)
  "42 degrees C fever → Emergency → 42nd Amendment 1976"
  "Article 21 — 21st birthday = LIFE's most important day → Right to LIFE & Liberty"
  "DPSP = Doctor's Prescription → Non-justiciable (doctor advises, court can't force)"
  "BRO wrote the Constitution → B.R. Ambedkar → Father of Constitution"(bro word we use naturally in everyday life, so easy to connect)
  "CAG = Checks And Guards government money — CAG = watchdog with a calculator"
  "Preamble = Entrance door of a house → tells you what's inside before you enter"
  "73rd Amendment = Panchayati Raj → 7+3=10 → 10 fingers = hands-on local governance"
  "10th Schedule = Anti-Defection Law → padi = fell → politician who betrays party FALLS"
  "Article 356 → 3+5+6=14 → Feb 14 Valentine's → President 'loves' the state so much
   he takes over it directly — but this love is not welcome!"
  "Rajya Sabha never fully dissolves → like a marriage — no complete divorce ever"
  "Lok Sabha = 5 years → aidu = tension → every 5 years, election tension guaranteed!"
  "Writ of Habeas Corpus → Habeas = 'you have the body' → produce the person in court
   → think: 'Hey, where is the body?' — court asking the jailer!"
  "Writ of Mandamus = 'we command' → Manda sounds like 'manda' (dull/slow) →
   court telling the slow government officer — stop being manda, DO YOUR JOB NOW!"

HISTORY / FREEDOM STRUGGLE:
  "1857 = 18-57 → 57 year old person's first revolt = First War of Independence"
  "Quit India 1942 → 9+4+2=15 → August 15 → Independence 1947!"
  "Simon Commission = 1927 → No Indian members → Simon says — but India says NO!"
  "Jallianwala Bagh = 1919 → 1+9+1+9=20 → 20 seconds of firing changed India forever"
  "Dandi March = 241 miles → 2+4+1=7 → edu = crying → British cried after this!"
  "Partition 1947 → rendu countries born → India and Pakistan → painful second birth of the subcontinent"
  "Battle of Plassey 1757 → paddnalugu (1+7+5+7=20, near 14) → Valentine's betrayal →
   Mir Jafar's treachery was the ultimate backstab — worse than a breakup!"
  "Rowlatt Act 1919 → 'No lawyer, no appeal, no daleel' → row + latt = no room to fight back"

GEOGRAPHY:
  "Narmada flows WEST → Flip N sideways → looks like W for West!"
  "Thar Desert → Thar sounds like Tar road → hot, dry, burned = desert"
  "Brahmaputra = Brahma's son → putra = son → mighty river born from Brahma himself"
  "Western Ghats = windward side = W for Wet; Eastern side = shadow = dry"
  "Chilika Lake, Odisha → CHILI = hot and famous → largest coastal lagoon in India, spicy important!"
  "Loktak Lake = Manipur → LOK = people, TAK = floating → floating phumdis, people's floating lake"
  "Deccan Plateau = DEC = DECEMBER = dry cold month → Deccan is the dry heart of India"
  "Konkan coast = narrow strip between Mumbai and Goa → Konkan sounds like 'concern' → always narrow and worrying to navigate!"
  "Indus River = flows through Pakistan mostly → IN-dus = INternational river, left India!"

SCIENCE / BIOLOGY:
  "Mitochondria = Powerhouse → MITO = My Toe → toe pushes you forward = POWER source"
  "Photosynthesis: everything is SIX → 6CO2 + 6H2O → C6H12O6 + 6O2 → aaru = aaravadhu
   → plant says aaravadhu (don't shout) while quietly making food with six of everything!"
  "Noble Gases = 0 valency → Nobel Prize winners share NOTHING → zero sharing, zero bonding"
  "Nucleus = control center → NUCLE sounds like UNCLE → the bossy uncle of the cell who controls everything"
  "Osmosis = water moves toward higher concentration → water always moves toward the crowd, just like people!"
  "Newton's 3rd law = every action has equal opposite reaction → push a wall, wall pushes back
   → aaru! aaravadhu! wall shouts back at you with equal force!"
  "DNA = Deoxyribonucleic Acid → DE-OXY = oxygen removed → DNA is the blueprint with oxygen stripped out"
  "Enzyme = biological catalyst → EN-ZYME sounds like 'engine' → enzyme is the engine that speeds up reactions"

ECONOMY / CURRENT AFFAIRS:
  "GDP vs GNP: D = Domestic (inside India borders), N = National (Indians anywhere in world)"
  "Repo Rate → REPO = RBI REPOssesses money from banks when it's too much in market"
  "Reverse Repo = banks give money TO RBI → reverse direction → RBI becomes the borrower"
  "Inflation and Interest Rate are married → one goes up, other must follow!"
  "Bull Market = prices rising → bull CHARGES UP with its horns pointed up"
  "Bear Market = prices falling → bear SWIPES DOWN with its paws pointed down"
  "SEBI = Stock market watchdog → SEBI sounds like 'sabi' (everyone) → watches everyone in market"
  "CRR = Cash Reserve Ratio → Cash Reserved with RBI → bank deposits cash with RBI as security deposit"
  "SLR = Statutory Liquidity Ratio → STATUTORY = by law → bank must keep liquid assets by law, no choice"
  "Fiscal Deficit = govt spends more than it earns → like a student spending more than pocket money
   → every single month — and borrowing from parents (public) to cover it!"

ARTS & CULTURE:
  "Bharatanatyam = Tamil Nadu → Bharat + Natyam = India's own dance → oldest classical form"
  "Kuchipudi = village in AP → dance named after its own village — proud hometown dance!"
  "Kathak = UP / North India → Katha = story → Kathak tells stories through every single step"
  "Odissi = Odisha → OD = ODisha → too easy, direct name connection!"
  "Manipuri = Manipur → direct name → Manipur's gift to classical dance world"
  "Mohiniyattam = Kerala → Mohini = enchantress from mythology → enchanting, graceful, feminine"
  "Sattriya = Assam → Satra = Vaishnavite monastery → born inside Assam's monasteries"
  "Kuchipudi vs Bharatanatyam confusion: K = Krishna (Kuchipudi has more Krishna themes),
   B = Bharat = whole India (Bharatanatyam is pan-India in feel)"
  "Indian painting styles order:
   Ajanta (2nd BCE) → Mughal (16th early) → Rajput (16th late) → Pahari (17th century)
   → A Morning Raag Playing → A=Ajanta M=Mughal R=Rajput P=Pahari → oldest to newest!"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CRITICAL RULE — NEVER SAY "MEMORY HINT" IN THE SCRIPT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The phrase "Memory Hint" or "Memory Trick" must NEVER appear in telugu_text.
It sounds robotic, breaks the natural tutor voice, and kills the flow.
A real tutor never announces "I am now giving you a memory hint."
They just GIVE IT naturally, like it is part of the explanation.

Instead, introduce every memory connection using one of these NATURAL FILLER WORDS:

  "dinni simple ga"
  "ela gurtu pettukovalantey —"
  "easy ga gurtupettukovataniki —"
  "best trick entantey —"
  "oka simple connection chudandi —"
  "oka fun way lo చెప్పాలంటే —"
  "simple గా link పెట్టుకోవాలంటే —"
  "ఇది mind లో fix అవ్వాలంటే —"
  "ఇక్కడ ఒక connection ఉంది —"
  "దీన్ని lock చేయాలంటే —"

BAD — awkward, robotic, DO NOT USE:
  "Memory hint — AMRP — A Morning Raag Playing..."
  "Memory trick గా గుర్తుంచుకోండి..."
  "ఇప్పుడు memory hint చెప్తాను..."
  "Memory hint: Article 21 = 21st birthday..."

GOOD — natural, warm, DO USE:
  "ela gurtu పెట్టుకోవాలంటే — 42 degrees fever అనుకో — 42nd Amendment, Emergency, 1976!"
  "best trick entantey — BRO wrote the Constitution — B.R. Ambedkar — never forget!"
  "dinni simple ga — Article 21, 21st birthday = life's biggest day = Right to Life!"
  "oka fun way lo చెప్పాలంటే — 6th Schedule, aaru, aaravadhu — tribal areas tell outsiders
   to keep quiet about their governance — their land, their rules!"

WHEN TO USE MEMORY HINTS:
- Number / date / name is genuinely hard to remember
- Skip entirely when the fact is already simple or self-explanatory
- NEVER generate a forced or confusing hint — if the connection is not instant, skip it
- ALWAYS introduce with a natural filler word — NEVER use the phrase "Memory Hint"

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
   "[WARM, FRIENDLY — WELCOME] Hello Everyone, Welcome to sky academy, where you not only learn the subect but memorise it for ever. [Energetic] Let's start!"
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
    emoji_pattern = re.compile(
        "["
        "\U0001F1E0-\U0001F1FF"
        "\U0001F300-\U0001F5FF"
        "\U0001F600-\U0001F64F"
        "\U0001F680-\U0001F6FF"
        "\U0001F700-\U0001F77F"
        "\U0001F780-\U0001F7FF"
        "\U0001F800-\U0001F8FF"
        "\U0001F900-\U0001F9FF"
        "\U0001FA00-\U0001FA6F"
        "\U0001FA70-\U0001FAFF"
        "\u2600-\u26FF"
        "\u2700-\u27BF"
        "\uFE0F"
        "\u200D"
        "\u23CF"
        "\u23E9-\u23F3"
        "\u231A-\u231B"
        "\u25AA-\u25FE"
        "\u2614-\u2615"
        "\u2648-\u2653"
        "\u267F"
        "\u2693"
        "\u26A1"
        "\u26AA-\u26AB"
        "\u26BD-\u26BE"
        "\u26C4-\u26C5"
        "\u26CE"
        "\u26D4"
        "\u26EA"
        "\u26F2-\u26F3"
        "\u26F5"
        "\u26FA"
        "\u26FD"
        "]+",
        flags=re.UNICODE,
    )
    return emoji_pattern.sub("", text).strip()


# ============================================================
# UTILITY — STORE NEW CHUNKS
# ============================================================

def store_new_chunks(parsed: list):
    for i, c in enumerate(parsed):
        cleaned = strip_emojis(c.get("telugu_text", ""))
        c["telugu_text"] = cleaned
        st.session_state[f"tv_{i}"] = cleaned
        st.session_state[f"sv_{i}"] = c.get("slide_prompt", "")
    st.session_state.chunks   = parsed
    st.session_state.seo_pack = None


# ============================================================
# UTILITY — SYNC EDITS TO CHUNKS
# ============================================================

def sync_edits_to_chunks() -> list:
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
# PROMPT BUILDERS
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
# STUDY NOTES HTML GENERATOR — REVISED
# Clean English-only classroom notes. No Telugu. No metadata.
# Header: just SKY Academy Classroom Notes + Topic.
# ============================================================

def generate_study_notes_html(topic: str, chunks: list, video_type: str) -> str:
    """
    Generates clean SKY Academy classroom notes — English only, print-ready.
    Header shows only: SKY Academy + Topic + 'Classroom Notes'.
    No segment count, no word count, no STRATEGY/SUBJECT NOTES label.
    Download -> open in Chrome/Edge -> Ctrl+P -> Save as PDF (~3 pages).
    """

    accent_colors = [
        "#3b82f6",  # blue
        "#ef4444",  # red
        "#16a34a",  # green
        "#f97316",  # orange
        "#7c3aed",  # violet
        "#0891b2",  # cyan
        "#be185d",  # pink
        "#b45309",  # amber
    ]

    sections_html = ""
    for i, chunk in enumerate(chunks):
        slide   = chunk.get("slide_prompt", "")
        heading = f"Topic {i + 1}"
        bullets = []

        for line in slide.strip().split("\n"):
            ln = line.strip()
            if not ln:
                continue
            lo = ln.lower()
            if lo.startswith("heading:"):
                heading = ln[8:].strip()
            elif lo.startswith("image prompt") or lo.startswith("image:"):
                continue
            elif ln.startswith(("•", "-", "*", "–", "▪")):
                b = ln.lstrip("•-*–▪ ").strip()
                if b and not b.lower().startswith("image"):
                    bullets.append(b)

        color     = accent_colors[i % len(accent_colors)]
        bullet_li = "".join(f"<li>{b}</li>" for b in bullets)

        sections_html += f"""
        <div class="ns" style="border-left-color:{color}">
          <div class="ns-head">
            <span class="ns-num" style="background:{color}">{i + 1}</span>
            <span class="ns-title">{heading}</span>
          </div>
          {"<ul class='nb'>" + bullet_li + "</ul>"
           if bullet_li
           else "<p class='nb-empty'>Refer to video for detailed explanation.</p>"}
          <div class="ann">
            <div class="ann-label">My Notes</div>
            <div class="ann-line"></div>
            <div class="ann-line"></div>
          </div>
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>SKY Academy — {topic} — Classroom Notes</title>
<style>
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

body {{
    font-family: 'Segoe UI', Arial, sans-serif;
    background: #dde3f0;
    padding: 20px;
    color: #111;
    font-size: 14px;
}}

.page {{
    max-width: 800px;
    margin: 0 auto;
    background: #fff;
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 6px 32px rgba(0,0,0,.15);
}}

/* ── HEADER ── */
.hdr {{
    background: linear-gradient(135deg, #020024 0%, #090979 50%, #00d4ff 100%);
    padding: 30px 26px 26px;
    text-align: center;
}}
.logo {{
    font-size: 46px;
    font-weight: 900;
    letter-spacing: 10px;
    line-height: 1;
    margin-bottom: 3px;
}}
.ls {{ color: #FF6B6B; text-shadow: 0 0 18px rgba(255,107,107,.5); }}
.lk {{ color: #FFE66D; text-shadow: 0 0 18px rgba(255,230,109,.5); }}
.ly {{ color: #4ECDC4; text-shadow: 0 0 18px rgba(78,205,196,.5); }}
.acad {{
    color: rgba(255,255,255,.7);
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 5px;
    text-transform: uppercase;
    margin-bottom: 20px;
}}
.tbox {{
    background: rgba(255,255,255,.12);
    border: 1px solid rgba(255,255,255,.28);
    border-radius: 10px;
    padding: 13px 22px;
    display: inline-block;
    max-width: 92%;
}}
.tlabel {{
    color: rgba(255,255,255,.55);
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 6px;
}}
.tname {{
    color: #FFE66D;
    font-size: 22px;
    font-weight: 800;
    line-height: 1.35;
}}
.nbadge {{
    margin-top: 13px;
    background: rgba(255,255,255,.16);
    color: #fff;
    border-radius: 20px;
    padding: 4px 18px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
    display: inline-block;
    text-transform: uppercase;
}}

/* ── INTRO STRIP ── */
.intro {{
    background: #eff6ff;
    padding: 9px 20px;
    text-align: center;
    font-size: 12px;
    color: #1e40af;
    border-bottom: 1px solid #bfdbfe;
}}

/* ── PRINT BUTTON ── */
.pbtn-wrap {{
    text-align: center;
    padding: 14px 20px 6px;
}}
.pbtn {{
    background: linear-gradient(135deg, #020024, #090979);
    color: #fff;
    border: none;
    border-radius: 8px;
    padding: 10px 30px;
    font-size: 13px;
    font-weight: 700;
    cursor: pointer;
    letter-spacing: 1px;
    box-shadow: 0 4px 14px rgba(9,9,121,.3);
}}
.phint {{
    font-size: 11px;
    color: #9ca3af;
    margin-top: 5px;
}}

/* ── CONTENT ── */
.body {{ padding: 14px 20px 20px; }}

/* ── NOTE SECTION ── */
.ns {{
    background: #fafafa;
    border: 1px solid #e5e7eb;
    border-left: 4px solid;
    border-radius: 8px;
    margin-bottom: 14px;
    overflow: hidden;
    page-break-inside: avoid;
}}
.ns-head {{
    display: flex;
    align-items: center;
    gap: 9px;
    padding: 9px 12px;
    background: rgba(0,0,0,.03);
    border-bottom: 1px solid #e5e7eb;
}}
.ns-num {{
    width: 24px;
    height: 24px;
    min-width: 24px;
    border-radius: 50%;
    color: #fff;
    font-size: 11px;
    font-weight: 800;
    display: flex;
    align-items: center;
    justify-content: center;
}}
.ns-title {{
    font-size: 13.5px;
    font-weight: 700;
    color: #111827;
    line-height: 1.3;
}}
.nb {{
    padding: 9px 12px 9px 32px;
    list-style: disc;
}}
.nb li {{
    font-size: 13px;
    color: #374151;
    line-height: 1.8;
    margin-bottom: 2px;
}}
.nb li:last-child {{ margin-bottom: 0; }}
.nb-empty {{
    padding: 8px 12px;
    font-size: 12px;
    color: #9ca3af;
    font-style: italic;
}}

/* ── ANNOTATION LINES ── */
.ann {{
    padding: 7px 12px 9px;
    border-top: 1px dashed #e5e7eb;
}}
.ann-label {{
    font-size: 9px;
    color: #bbb;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 4px;
}}
.ann-line {{
    height: 1px;
    background: #ebebeb;
    margin-bottom: 8px;
}}

/* ── TELEGRAM BOX ── */
.tg {{
    margin: 4px 20px 20px;
    background: linear-gradient(to right, #eff6ff, #dbeafe);
    border: 2px solid #3b82f6;
    border-radius: 12px;
    padding: 16px 20px;
    text-align: center;
}}
.tg h4 {{
    color: #1e40af;
    font-size: 14px;
    font-weight: 800;
    margin-bottom: 7px;
}}
.tg p {{
    color: #1e40af;
    font-size: 12.5px;
    line-height: 1.85;
}}

/* ── FOOTER ── */
.ftr {{
    background: linear-gradient(135deg, #020024, #090979);
    padding: 13px 20px;
    text-align: center;
}}
.flogo {{
    font-size: 18px;
    font-weight: 900;
    letter-spacing: 5px;
    margin-bottom: 3px;
}}
.fsub {{
    color: rgba(255,255,255,.45);
    font-size: 9px;
}}

/* ── PRINT ── */
@media print {{
    body {{ background: #fff; padding: 0; }}
    .page {{ box-shadow: none; border-radius: 0; max-width: 100%; }}
    .pbtn-wrap, .tg {{ display: none !important; }}
    .ns {{ break-inside: avoid; }}
    @page {{ margin: 1.2cm 1.5cm; }}
}}
</style>
</head>
<body>
<div class="page">

  <!-- HEADER — only SKY logo + topic + Classroom Notes label -->
  <div class="hdr">
    <div class="logo">
      <span class="ls">S</span><span class="lk">K</span><span class="ly">Y</span>
    </div>
    <div class="acad">Academy</div>
    <div class="tbox">
      <div class="tlabel">Classroom Notes</div>
      <div class="tname">{topic}</div>
    </div>
    <div><span class="nbadge">Study Notes</span></div>
  </div>

  <!-- INTRO STRIP -->
  <div class="intro">
    Read these notes while watching the video for maximum retention
    &nbsp;&middot;&nbsp;
    <strong>SKY Academy Competitive Exam Preparation</strong>
  </div>

  <!-- PRINT BUTTON -->
  <div class="pbtn-wrap">
    <button class="pbtn" onclick="window.print()">Print / Save as PDF</button>
    <p class="phint">Use Chrome or Edge for best results</p>
  </div>

  <!-- NOTES CONTENT -->
  <div class="body">
    {sections_html}
  </div>

  <!-- TELEGRAM BOX -->
  <div class="tg">
    <h4>SKY Academy Telegram Channel</h4>
    <p>
      Free notes, daily PDFs, previous year questions and exam alerts —<br>
      all available on the Telegram channel.<br>
      Join and take your preparation to the next level!
    </p>
  </div>

  <!-- FOOTER -->
  <div class="ftr">
    <div class="flogo">
      <span style="color:#FF6B6B">S</span>
      <span style="color:#FFE66D">K</span>
      <span style="color:#4ECDC4">Y</span>
    </div>
    <div class="fsub">
      SKY ACADEMY &nbsp;|&nbsp; Script Engine v3.1 &nbsp;|&nbsp; Internal Tool
    </div>
  </div>

</div>
</body>
</html>"""


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
    cleaned = raw.strip()
    cleaned = re.sub(r"^```[a-zA-Z]*\s*\n?", "", cleaned)
    cleaned = re.sub(r"\n?```\s*$",          "", cleaned).strip()

    try:
        result = json.loads(cleaned)
        if isinstance(result, dict):
            return result
        if isinstance(result, list) and result:
            return result[0]
    except Exception:
        pass

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

        ws.batch_clear(["A2:E10000"])

        rows = [
            [
                i + 1,
                c.get("telugu_text", ""),
                c.get("slide_prompt", ""),
            ]
            for i, c in enumerate(chunks)
        ]
        ws.update("A2", rows, value_input_option="RAW")

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
video_type       = "subjective"

with left:
    st.markdown("## Script Input")

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
                                        st.session_state.chunks[idx] = new_chunk
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
                help="Open in Chrome/Edge -> Ctrl+P -> Save as PDF.",
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
                📄 <b>Study Notes</b> — Clean English HTML -> print as PDF -> Telegram
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
