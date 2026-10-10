"""
Explainer Agent: Generates short, compassionate lab report explanations at a Class 5 elementary reading level.
STRICT CLINICAL SAFETY RULES:
1. NEVER DIAGNOSES: Never labels the patient with a disease or medical condition.
2. MANDATORY SAFETY DISCLAIMER: Appends this exact text to every result:
   'This explains your report. It is not a diagnosis. Please consult a doctor.'
"""

import json
import logging
import os
import re
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

# Exact required safety disclaimer
EXACT_SAFETY_DISCLAIMER = "This explains your report. It is not a diagnosis. Please consult a doctor."

LOCALIZED_SAFETY_DISCLAIMERS = {
    "en": EXACT_SAFETY_DISCLAIMER,
    "hi": "यह केवल आपकी रिपोर्ट को सरल भाषा में समझाता है, यह कोई डॉक्टरी निदान नहीं है। कृपया डॉक्टर से सलाह लें।",
    "ml": "ഇത് നിങ്ങളുടെ ലാബ് റിപ്പോർട്ട് ലളിതമായി വിശദീകരിക്കുന്നു. ഇതൊരു രോഗനിർണ്ണയമല്ല. ദയവായി ഒരു ഡോക്ടറെ കാണുക.",
    "ta": "இது உங்கள் அறிக்கையை எளிமையாக விளக்குகிறது. இது ஒரு மருத்துவ நோயறிதல் அல்ல. தயவுசெய்து மருத்துவரை அணுகவும்.",
    "te": "ఇది మీ ల్యాబ్ నివేదికను సరళంగా వివరిస్తుంది. ఇది ఎటువంటి వ్యాధి నిర్ధారణ కాదు. దయచేసి వైద్యుడిని సంప్రదించండి.",
    "kn": "ಇದು ನಿಮ್ಮ ಲ್ಯಾಬ್ ವರದಿಯನ್ನು ಸರಳವಾಗಿ ವಿವರಿಸುತ್ತದೆ. ಇದು ರೋಗನಿರ್ಣಯವಲ್ಲ. ದಯವಿಟ್ಟು ವೈದ್ಯರನ್ನು ಸಂಪರ್ಕಿಸಿ.",
    "bn": "এটি আপনার ল্যাব রিপোর্ট সহজ ভাষায় বুঝিয়ে দেয়। এটি কোনো রোগ নির্ণয় নয়। অনুগ্রহ করে একজন ডাক্তারের সাথে পরামর্শ করুন।",
    "mr": "हे तुमच्या लॅब रिपोर्टचे सोप्या भाषेत स्पष्टीकरण देते. हे कोणतेही वैद्यकीय निदान नाही. कृपया डॉक्टरांचा सल्ला घ्या.",
    "gu": "આ તમારા લેબ રિપોર્ટને સરળ ભાષામાં સમજાવે છે. આ કોઈ રોગનું નિદાન નથી. કૃપા કરીને ડૉક્ટરની સલાહ લો.",
    "pa": "ਇਹ ਤੁਹਾਡੀ ਲੈਬ ਰਿਪੋਰਟ ਨੂੰ ਸਰਲ ਸ਼ਬਦਾਂ ਵਿੱਚ ਸਮਝਾਉਂਦਾ ਹੈ। ਇਹ ਕੋਈ ਬਿਮਾਰੀ ਦੀ ਜਾਂਚ ਨਹੀਂ ਹੈ। ਕਿਰਪਾ ਕਰਕੇ ਡਾਕਟਰ ਦੀ ਸਲਾਹ ਲਵੋ।",
    "or": "ଏହା ଆପଣଙ୍କ ଲ୍ୟାବ୍ ରିପୋର୍ଟକୁ ସରଳ ଭାଷାରେ ବୁଝାଏ। ଏହା କୌଣସି ରୋଗ ନିର୍ଣ୍ଣୟ ନୁহେଁ। ଦୟାକରି ଡାକ୍ତରଙ୍କ ପରାମର୍ଶ ନିଅନ୍ତୁ।",
    "as": "ইয়াৰ দ্বাৰা আপোনাৰ লেব ৰিপ'ৰ্ট সহজ ভাষাত বুজোৱা হৈছে। এইটো কোনো ৰোগ নিৰ্ণয় নহয়। অনুগ্ৰহ কৰি এজন চিকিৎসকৰ পৰামৰ্শ লওক।",
    "ur": "یہ آپ کی لیب رپورٹ کو آسان زبان میں سمجھاتا ہے۔ یہ کوئی طبی تشخیص نہیں ہے۔ براہ کرم ڈاکٹر سے رجوع کریں۔"
}

# Forbidden diagnostic phrasing to safeguard against unauthorized clinical claims
FORBIDDEN_DIAGNOSTIC_PATTERNS = [
    r"\byou have (diabetes|anemia|leukemia|infection|kidney disease|thyroid disorder|cancer)\b",
    r"\byou are suffering from\b",
    r"\byou are diagnosed with\b",
    r"\bthe diagnosis is\b",
    r"\byou are a diabetic\b",
    r"\byou have high blood pressure\b"
]


class ExplainerAgent:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self.client = None
        if self.api_key:
            try:
                # pyrefly: ignore [missing-import]
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                logger.warning(f"Failed to initialize google-genai for Explainer: {e}")

    @staticmethod
    def _sanitize_diagnoses(text: str) -> str:
        """Removes or neutralizes accidental diagnostic claims to preserve clinical safety."""
        sanitized = text
        for pattern in FORBIDDEN_DIAGNOSTIC_PATTERNS:
            sanitized = re.sub(pattern, "your lab reading differs from the usual reference range", sanitized, flags=re.IGNORECASE)
        return sanitized

    @staticmethod
    def _ensure_safety_disclaimer(text: str) -> str:
        """Guarantees the exact required safety disclaimer is appended to the text."""
        stripped = text.strip()
        if not stripped.endswith(EXACT_SAFETY_DISCLAIMER):
            # If already partially present, strip and re-append cleanly
            if EXACT_SAFETY_DISCLAIMER in stripped:
                stripped = stripped.replace(EXACT_SAFETY_DISCLAIMER, "").strip()
            return f"{stripped} {EXACT_SAFETY_DISCLAIMER}".strip()
        return stripped

    async def generate_explanation(
        self,
        checked_data: Dict[str, Any],
        language: str = "en",
        comparison: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generates a short, compassionate explanation at a Class 5 reading level.
        Never diagnoses and appends the exact mandatory disclaimer to every result.
        Explicitly mentions longitudinal progress or regression since the last test if provided.
        """
        lang = language if language in LOCALIZED_SAFETY_DISCLAIMERS else "en"
        localized_safety = LOCALIZED_SAFETY_DISCLAIMERS.get(lang, EXACT_SAFETY_DISCLAIMER)

        # Build comparison prompt snippet if history exists
        comparison_context = ""
        if comparison and comparison.get("has_comparison"):
            comparison_context = f"""
LONGITUDINAL COMPARISON SINCE PREVIOUS TEST:
{json.dumps(comparison.get("comparisons", []), indent=2)}
Overall trajectory: {comparison.get("overall_trajectory", "stable")}
Spoken trend cues: {json.dumps(comparison.get("spoken_summary", {}), indent=2)}

MANDATORY LONGITUDINAL PROGRESS INSTRUCTION:
The patient has taken a previous test. You MUST explicitly mention the progress or regression since the last test in both the summary and the spoken voice script (e.g. 'Your sugar is lower than last time' or 'Your hemoglobin has improved since your last test').
Acknowledge positive improvements warmly and encourage them if any values need doctor consultation.
"""

        # If Gemini client is active, request empathetic Class 5 explanation
        if self.client:
            try:
                prompt = f"""You are 'ReportSakhi', an empathetic, comforting AI health friend helping a rural patient in India understand their routine lab report.
Target reading level: Class 5 (Grade 5 elementary school level).
Language requested: {lang} (ml=Malayalam, hi=Hindi, ta=Tamil, en=English).

Evaluated lab report items:
{json.dumps(checked_data, indent=2)}
{comparison_context}
MANDATORY SAFETY RULES:
1. READING LEVEL: Class 5 elementary vocabulary. Keep sentences short, warm, and comforting (no complex medical jargon like 'hyperglycemia', 'erythrocytes', etc.).
2. NEVER DIAGNOSE: You MUST NOT diagnose any disease, illness, or medical condition. Never say 'You have diabetes' or 'You have anemia'. Only mention whether values are in the usual safe range or need a doctor's checkup.
3. LONGITUDINAL TREND: If previous test data is given above, you MUST explicitly speak about whether values are higher, lower, or improved compared to the last test.
4. LENGTH: Keep the entire summary concise and calm (2 to 4 sentences).
5. MANDATORY CONCLUSION: The summary and speech script MUST end with this exact sentence:
"{EXACT_SAFETY_DISCLAIMER}"

Format output strictly as JSON with keys:
{{
  "headline": "Short 1-sentence calming summary (Class 5 level)",
  "summary_text": "Short 2-4 sentence warm explanation in {lang} mentioning progress since last test and ending with the mandatory disclaimer",
  "key_points": ["Point 1 in {lang}", "Point 2 in {lang}"],
  "full_speech_script": "The spoken voice script to read aloud to the patient explicitly mentioning the progress/difference since last test and ending with the mandatory disclaimer"
}}"""

                # pyrefly: ignore [missing-import]
                from google.genai import types

                candidate_models = [
                    getattr(self, "model", None) or os.getenv("GEMINI_MODEL", "gemini-flash-latest"),
                    "gemini-flash-latest",
                    "gemini-3.1-flash-lite",
                    "gemini-flash-lite-latest",
                    "gemini-3.5-flash"
                ]
                models_to_try = []
                for m in candidate_models:
                    if m and m not in models_to_try:
                        models_to_try.append(m)

                response = None
                for model_candidate in models_to_try:
                    try:
                        import asyncio
                        response = await asyncio.to_thread(
                            self.client.models.generate_content,
                            model=model_candidate,
                            contents=prompt,
                            config=types.GenerateContentConfig(
                                response_mime_type="application/json",
                                temperature=0.1
                            )
                        )
                        if response and response.text:
                            logger.info(f"Gemini explanation succeeded using model: {model_candidate}")
                            break
                    except Exception as me:
                        logger.warning(f"Explainer model '{model_candidate}' failed: {me}. Trying next candidate...")
                        continue

                if not response or not response.text:
                    raise RuntimeError("All candidate Gemini models failed for explanation.")

                parsed = json.loads(response.text or "{}")

                # Sanitize any diagnostic terminology
                headline = self._sanitize_diagnoses(parsed.get("headline", "Report Overview"))
                summary_raw = self._sanitize_diagnoses(parsed.get("summary_text", ""))
                speech_raw = self._sanitize_diagnoses(parsed.get("full_speech_script", summary_raw))
                key_points = [self._sanitize_diagnoses(p) for p in parsed.get("key_points", [])]

                # Ensure exact safety disclaimer is appended
                summary_text = self._ensure_safety_disclaimer(summary_raw)
                full_speech_script = self._ensure_safety_disclaimer(speech_raw)

                return {
                    "language": lang,
                    "headline": headline,
                    "summary_text": summary_text,
                    "key_points": key_points,
                    "safety_line": EXACT_SAFETY_DISCLAIMER,
                    "safety_line_localized": localized_safety,
                    "full_speech_script": full_speech_script
                }
            except Exception as e:
                logger.error(f"Gemini generation error in ExplainerAgent: {e}")

        # High-fidelity localized Class 5 template fallback
        return self._generate_templated_explanation(checked_data, lang, comparison=comparison)

    def _generate_templated_explanation(
        self,
        checked_data: Dict[str, Any],
        lang: str,
        comparison: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Deterministic, Class 5 reading level explanation fallback.
        Strictly never diagnoses and appends the exact mandatory disclaimer.
        Explicitly mentions longitudinal progress or regression since the last test if provided.
        """
        items = checked_data.get("items", [])
        
        green_items = [i.get("canonical_name", i.get("test_name", "")) for i in items if i.get("color") == "green"]
        yellow_items = [i.get("canonical_name", i.get("test_name", "")) for i in items if i.get("color") == "yellow"]
        red_items = [i.get("canonical_name", i.get("test_name", "")) for i in items if i.get("color") == "red"]

        comp_spoken = ""
        if comparison and comparison.get("has_comparison"):
            spoken_dict = comparison.get("spoken_summary", {})
            comp_spoken = (spoken_dict.get(lang) or spoken_dict.get("en") or "").strip()

        if lang == "ml":
            if red_items:
                headline = "ചില പരിശോധനാ ഫലങ്ങൾ അടിയന്തിരമായി ഡോക്ടറെ കാണിക്കേണ്ടതുണ്ട്."
                body = "നമസ്കാരം. നിങ്ങളുടെ ചില പരിശോധനാ ഫലങ്ങൾ സാധാരണ അളവിൽ നിന്ന് മാറിയിരിക്കുന്നു. എത്രയും വേഗം ഡോക്ടറെ കാണുക."
            elif yellow_items:
                headline = "ചില ഫലങ്ങൾ സാധാരണ പരിധിക്ക് പുറത്താണ്; ഡോക്ടറെ കാണുക."
                body = "നമസ്കാരം. ഭൂരിഭാഗം ഫലങ്ങളും തൃപ്തികരമാണ്. ചില അളവുകൾ ഡോക്ടറുമായി സംസാരിക്കുന്നത് നന്നായിരിക്കും."
            else:
                headline = "എല്ലാ പ്രധാന പരിശോധനാ ഫലങ്ങളും സാധാരണ നിലയിലാണ്."
                body = "നമസ്കാരം. സന്തോഷവാർത്ത! നിങ്ങളുടെ പരിശോധിച്ച പ്രധാന ഫലങ്ങളെല്ലാം സാധാരണ സുരക്ഷിത നിലയിലാണ്."

            if comp_spoken:
                body = f"{body} {comp_spoken}"

            points = []
            if green_items:
                points.append(f"സാധാരണ നിലയിലുള്ളവ: {', '.join(green_items)}")
            if yellow_items:
                points.append(f"ശ്രദ്ധിക്കേണ്ടവ: {', '.join(yellow_items)}")
            if red_items:
                points.append(f"ഉടൻ കാണിക്കേണ്ടവ: {', '.join(red_items)}")
            if comp_spoken:
                points.append(f"കഴിഞ്ഞ റിപ്പോർട്ടുമായുള്ള മാറ്റം: {comp_spoken}")

            summary = f"{body} {EXACT_SAFETY_DISCLAIMER}"

        elif lang == "hi":
            if red_items:
                headline = "कुछ जांचों पर तुरंत डॉक्टर का ध्यान जरूरी है।"
                body = "नमस्ते। आपकी रिपोर्ट के कुछ मान सामान्य सीमा से काफी अलग हैं। कृपया जल्द से जल्द डॉक्टर से मिलें।"
            elif yellow_items:
                headline = "कुछ मानों पर डॉक्टर से परामर्श की सलाह दी जाती है।"
                body = "नमस्ते। आपकी ज्यादातर जांचें ठीक हैं, लेकिन कुछ मान सामान्य सीमा से थोड़े अलग हैं। डॉक्टर से सलाह लें।"
            else:
                headline = "सभी मुख्य परिणाम सामान्य और सुरक्षित सीमा में हैं।"
                body = "नमस्ते। अच्छी खबर है! आपकी सभी मुख्य जांचें सामान्य और सुरक्षित दायरे में हैं।"

            if comp_spoken:
                body = f"{body} {comp_spoken}"

            points = []
            if green_items:
                points.append(f"सामान्य परिणाम: {', '.join(green_items)}")
            if yellow_items:
                points.append(f"ध्यान देने योग्य: {', '.join(yellow_items)}")
            if red_items:
                points.append(f"तुरंत डॉक्टर को दिखाने योग्य: {', '.join(red_items)}")
            if comp_spoken:
                points.append(f"पिछली जांच से तुलना: {comp_spoken}")

            summary = f"{body} {EXACT_SAFETY_DISCLAIMER}"

        elif lang == "ta":
            if red_items:
                headline = "சில சோதனைகளை உடனடியாக மருத்துவரிடம் காட்ட வேண்டும்."
                body = "வணக்கம். சில பரிசோதனை அளவுகள் இயல்பான வரம்பை விட வேறுபட்டுள்ளன. உடனடியாக மருத்துவரை அணுகவும்."
            elif yellow_items:
                headline = "சில முடிவுகள் குறித்து மருத்துவரிடம் ஆலோசனை பெறவும்."
                body = "வணக்கம். பெரும்பாலான முடிவுகள் நன்றாக உள்ளன. சில அளவுகளை மருத்துவரிடம் காட்டுங்கள்."
            else:
                headline = "முக்கிய முடிவுகள் அனைத்தும் இயல்பான வரம்பில் உள்ளன."
                body = "வணக்கம். மகிழ்ச்சியான செய்தி! உங்கள் பரிசோதனை முடிவுகள் அனைத்தும் இயல்பான ஆரோக்கியமான வரம்பில் உள்ளன."

            if comp_spoken:
                body = f"{body} {comp_spoken}"

            points = []
            if green_items:
                points.append(f"இயல்பானவை: {', '.join(green_items)}")
            if yellow_items:
                points.append(f"கவனிக்க வேண்டியவை: {', '.join(yellow_items)}")
            if red_items:
                points.append(f"உடனடி கவனம் தேவை: {', '.join(red_items)}")
            if comp_spoken:
                points.append(f"கடந்த சோதனையுடன் ஒப்பீடு: {comp_spoken}")

            summary = f"{body} {EXACT_SAFETY_DISCLAIMER}"

        else:  # English (Class 5 Elementary Level)
            if red_items:
                headline = "A few results need urgent attention from a doctor."
                body = "Hello. Some of your test numbers are outside the safe normal range. Please see your doctor soon for guidance."
            elif yellow_items:
                headline = "A few test values are outside the usual range."
                body = "Hello. Most of your tests look good, but a few numbers differ from standard bounds. Please consult your doctor."
            else:
                headline = "All checked routine test numbers are in the healthy normal range."
                body = "Hello. Good news! All of your checked test values are within healthy normal limits."

            if comp_spoken:
                body = f"{body} {comp_spoken}"

            points = []
            if green_items:
                points.append(f"Healthy normal: {', '.join(green_items)}")
            if yellow_items:
                points.append(f"Needs doctor review: {', '.join(yellow_items)}")
            if red_items:
                points.append(f"Needs urgent review: {', '.join(red_items)}")
            if comp_spoken:
                points.append(f"Trend vs Last Report: {comp_spoken}")

            summary = f"{body} {EXACT_SAFETY_DISCLAIMER}"

        return {
            "language": lang,
            "headline": headline,
            "summary_text": summary,
            "key_points": points,
            "safety_line": EXACT_SAFETY_DISCLAIMER,
            "safety_line_localized": LOCALIZED_SAFETY_DISCLAIMERS.get(lang, EXACT_SAFETY_DISCLAIMER),
            "full_speech_script": summary
        }

    async def answer_question(
        self,
        question: str,
        language: str = "en",
        report_context: Optional[str] = None
    ) -> str:
        """
        Answers patient follow-up questions at a Class 5 elementary reading level.
        Strictly forbids diagnosing medical conditions and appends the mandatory disclaimer.
        """
        lang = language if language in LOCALIZED_SAFETY_DISCLAIMERS else "en"

        # 1. If Gemini client is active, generate a compassionate Class-5 answer
        if self.client:
            try:
                context_str = f"\nPatient's lab report context:\n{report_context}" if report_context else ""
                prompt = f"""You are 'ReportSakhi', an empathetic, comforting AI health friend helping a rural patient in India understand their lab report.
The patient is asking this question: "{question}"
{context_str}

Language requested: {lang} (ml=Malayalam, hi=Hindi, ta=Tamil, en=English).
Target reading level: Class 5 elementary school.

MANDATORY SAFETY RULES:
1. READING LEVEL: Class 5 vocabulary. Keep sentences short, warm, and comforting.
2. NEVER DIAGNOSE: You MUST NOT diagnose any disease, illness, or medical condition. Never say 'You have diabetes' or 'You have anemia'. Only explain what the numbers mean or advise talking to a doctor.
3. MANDATORY DISCLAIMER: You must conclude your answer reminding the patient to consult their doctor.

Respond strictly in {lang} with simple, comforting text."""

                candidate_models = [
                    getattr(self, "model", None) or os.getenv("GEMINI_MODEL", "gemini-flash-latest"),
                    "gemini-flash-latest",
                    "gemini-3.1-flash-lite",
                    "gemini-flash-lite-latest",
                    "gemini-3.5-flash"
                ]
                models_to_try = []
                for m in candidate_models:
                    if m and m not in models_to_try:
                        models_to_try.append(m)

                response = None
                for model_candidate in models_to_try:
                    try:
                        response = self.client.models.generate_content(
                            model=model_candidate,
                            contents=prompt
                        )
                        if response and response.text:
                            break
                    except Exception:
                        continue

                if response and response.text:
                    cleaned = self._sanitize_diagnoses(response.text.strip())
                    return self._ensure_safety_disclaimer(cleaned)
            except Exception as e:
                logger.warning(f"Gemini explainer question answering error: {e}. Falling back to rule-based response...")

        # 2. Rule-based compassionate fallback dictionary
        q_lower = (question or "").lower()
        
        fallback_answers = {
            "ml": {
                "sugar": "നിങ്ങളുടെ ഷുഗർ അളവുകൾ പരിശോധിച്ചിട്ടുണ്ട്. ഭക്ഷണത്തിന് മുൻപും ശേഷവുമുള്ള അളവുകൾ സാധാരണ നിലയിലാണോ എന്ന് ഡോക്ടറോട് ചോദിച്ചു മനസ്സിലാക്കാവുന്നതാണ്.",
                "hb": "ഹീമോഗ്ലോബിൻ അളവ് ശരീരത്തിലെ രക്തത്തിന്റെ കരുത്ത് കാണിക്കുന്നു. കൃത്യമായ ഭക്ഷണക്രമത്തെക്കുറിച്ച് ഡോക്ടർ പറയും.",
                "doctor": "റിപ്പോർട്ടിലെ ഏതെങ്കിലും അളവ് വ്യത്യാസപ്പെട്ടിട്ടുണ്ടെങ്കിൽ, അടുത്തുള്ള ഡോക്ടറെ കണ്ട് പരിശോധിക്കുന്നത് ഉത്തമമാണ്.",
                "default": f"നിങ്ങളുടെ ചോദ്യം '{question}' മനസ്സിലായി. ഈ ലാബ് പരിശോധനാ ഫലങ്ങളെക്കുറിച്ച് നിങ്ങളുടെ ഡോക്ടറുമായി സംസാരിക്കുന്നത് ആരോഗ്യത്തിന് ഏറ്റവും നല്ലതാണ്."
            },
            "hi": {
                "sugar": "आपकी शुगर की जांच रिपोर्ट में दर्ज है। खाली पेट या खाने के बाद का स्तर सामान्य सीमा में है या नहीं, यह डॉक्टर से जरूर समझें।",
                "hb": "हीमोग्लोबिन आपके शरीर में खून की ताकत बताता है। सही खान-पान और सलाह के लिए डॉक्टर से बात करें।",
                "doctor": "यदि रिपोर्ट का कोई मान अलग है, तो जल्द से जल्द नजदीकी डॉक्टर से मिलकर सलाह लेना सबसे सुरक्षित है।",
                "default": f"आपका प्रश्न '{question}' मिला। आपकी रिपोर्ट के इन मानों के संदर्भ में डॉक्टर से बात करना सबसे सुरक्षित रहेगा।"
            },
            "ta": {
                "sugar": "உங்கள் சர்க்கரை அளவு சோதிக்கப்பட்டுள்ளது. இந்த அளவு இயல்பானதா என்பதை உங்கள் மருத்துவரிடம் கேட்டு உறுதி செய்யவும்.",
                "hb": "ஹீமோகுளோபின் இரத்தத்தின் ஆரோக்கியத்தைக் குறிக்கிறது. உங்கள் மருத்துவரிடம் ஆலோசனை பெறுங்கள்.",
                "doctor": "அறிக்கையில் ஏதேனும் மாற்றம் இருந்தால், அருகிலுள்ள மருத்துவரை அணுகுவது நல்லது.",
                "default": f"உங்கள் கேள்வி '{question}' பெறப்பட்டது. இந்த முடிவுகள் குறித்து உங்கள் மருத்துவரிடம் ஆலோசனை பெறுவது சிறந்தது."
            },
            "te": {
                "sugar": "మీ రక్తంలో చక్కెర స్థాయిలు పరీక్షించబడ్డాయి. ఈ వివరాలను మీ వైద్యుడితో చర్చించండి.",
                "hb": "హీమోగ్లోబిన్ మీ రక్త ఆరోగ్యాన్ని తెలియజేస్తుంది. తగిన సూచనల కోసం వైద్యుడిని సంప్రదించండి.",
                "doctor": "రిపోర్టులో ఏవైనా తేడాలు ఉంటే దగ్గరలోని వైద్యుడిని సంప్రదించడం మంచిది.",
                "default": f"మీ ప్రశ్న '{question}' స్వీకరించబడింది. ఖచ్చితమైన సమాచారం కోసం దయచేసి వైద్యుడిని సంప్రదించండి."
            },
            "kn": {
                "sugar": "ನಿಮ್ಮ ಸಕ್ಕರೆ ಮಟ್ಟವನ್ನು ಪರೀಕ್ಷಿಸಲಾಗಿದೆ. ಈ ಬಗ್ಗೆ ನಿಮ್ಮ ವೈದ್ಯರಿಂದ ಸಲಹೆ ಪಡೆಯಿರಿ.",
                "hb": "ಹಿಮೋಗ್ಲೋಬಿನ್ ನಿಮ್ಮ ರಕ್ತದ ಶಕ್ತಿಯನ್ನು ಸೂಚಿಸುತ್ತದೆ. ಹೆಚ್ಚಿನ ಮಾಹಿತಿಗಾಗಿ ವೈದ್ಯರನ್ನು ಸಂಪರ್ಕಿಸಿ.",
                "doctor": "ವರದಿಯಲ್ಲಿ ಯಾವುದೇ ಬದಲಾವಣೆ ಇದ್ದರೆ ಹತ್ತಿರದ ವೈದ್ಯರನ್ನು ಭೇಟಿ ಮಾಡಿ.",
                "default": f"ನಿಮ್ಮ ಪ್ರಶ್ನೆ '{question}' ಅರ್ಥವಾಯಿತು. ದಯವಿಟ್ಟು ನಿಮ್ಮ ವೈದ್ಯರೊಂದಿಗೆ ಮಾತನಾಡಿ."
            },
            "bn": {
                "sugar": "আপনার রক্তে শর্করার মাত্রা পরীক্ষা করা হয়েছে। রিপোর্টটি ডাক্তারকে দেখিয়ে পরামর্শ নিন।",
                "hb": "হিমোগ্লোবিন রক্তের স্বাস্থ্য নির্দেশ করে। সঠিক পরামর্শের জন্য চিকিৎসকের সাথে কথা বলুন।",
                "doctor": "কোনো মান পরিবর্তিত হলে নিকটস্থ ডাক্তারের সাথে যোগাযোগ করা নিরাপদ।",
                "default": f"আপনার প্রশ্ন '{question}' পেয়েছি। এই রিপোর্ট সম্পর্কে ডাক্তারের পরামর্শ নেওয়াই সবচেয়ে ভালো।"
            },
            "mr": {
                "sugar": "तुमच्या रक्तातील साखरेची पातळी तपासली आहे. योग्य माहितीसाठी डॉक्टरांशी चर्चा करा.",
                "hb": "हिमोग्लोबिन रक्तातील ताकद दर्शवते. आहाराविषयी डॉक्टरांचा सल्ला घ्या.",
                "doctor": "रिपोर्टमधील आकडे बदललेले असल्यास डॉक्टरांना दाखवणे योग्य ठरेल.",
                "default": f"तुमचा प्रश्न '{question}' समजला. योग्य मार्गदर्शनासाठी डॉक्टरांचा सल्ला घ्या."
            },
            "gu": {
                "sugar": "તમારા સુગર લેવલની તપાસ કરવામાં આવી છે. કૃપા કરીને આ અંગે ડૉક્ટરની સલાહ લો.",
                "hb": "હિમોગ્લોબિન રક્તની તંદુરસ્તી દર્શાવે છે. યોગ્ય આહાર માટે ડૉક્ટર સાથે વાત કરો.",
                "doctor": "રિપોર્ટમાં કોઈ ફેરફાર હોય તો નજીકના ડૉક્ટરનો સંપર્ક કરવો હિતાવહ છે.",
                "default": f"તમારો પ્રશ્ન '{question}' મળ્યો. સલાહ માટે કૃપા કરીને ડૉક્ટરને મળો."
            },
            "pa": {
                "sugar": "ਤੁਹਾਡੀ ਸ਼ੂਗਰ ਦੀ ਜਾਂਚ ਕੀਤੀ ਗਈ ਹੈ। ਇਸ ਬਾਰੇ ਆਪਣੇ ਡਾਕਟਰ ਦੀ ਸਲਾਹ ਜ਼ਰੂਰ ਲਵੋ।",
                "hb": "ਹੀਮੋਗਲੋਬਿਨ ਖੂਨ ਦੀ ਸਿਹਤ ਦਰਸਾਉਂਦਾ ਹੈ। ਸਹੀ ਖੁਰਾਕ ਲਈ ਡਾਕਟਰ ਨਾਲ ਗੱਲ ਕਰੋ।",
                "doctor": "ਜੇਕਰ ਰਿਪੋਰਟ ਵਿੱਚ ਕੋਈ ਫਰਕ ਹੈ ਤਾਂ ਨਜ਼ਦੀਕੀ ਡਾਕਟਰ ਨੂੰ ਦਿਖਾਉਣਾ ਸਭ ਤੋਂ ਵਧੀਆ ਹੈ।",
                "default": f"ਤੁਹਾਡਾ ਸਵਾਲ '{question}' ਮਿਲਿਆ। ਕਿਰਪਾ ਕਰਕੇ ਆਪਣੇ ਡਾਕਟਰ ਨਾਲ ਸਲਾਹ ਕਰੋ।"
            },
            "or": {
                "sugar": "ଆପଣଙ୍କ ରକ୍ତ ଶର୍କରା ସ୍ତର ଯାଞ୍ଚ କରାଯାଇଛି। ଡାକ୍ତରଙ୍କ ସହ ପରାମର୍ଶ କରନ୍ତୁ।",
                "hb": "ହିମୋଗ୍ଲୋବିନ ରକ୍ତର ସ୍ୱାସ୍ଥ୍ୟ ଦର୍ଶାଏ। ଉପଯୁକ୍ତ ପରାମର୍ଶ ପାଇଁ ଡାକ୍ତରଙ୍କୁ ଦେଖାନ୍ତୁ।",
                "doctor": "ରିପୋର୍ଟରେ ପରିବର୍ତ୍ତନ ଥିଲେ ନିକଟସ୍ଥ ଡାକ୍ତରଙ୍କ ସହ ପରାମର୍ଶ କରିବା ଉଚିତ।",
                "default": f"ଆପଣଙ୍କ ପ୍ରଶ୍ନ '{question}' ମିଳିଲା। ଦୟାକରି ଡାକ୍ତରଙ୍କ ପରାମର୍ଶ ନିଅନ୍ତୁ।"
            },
            "as": {
                "sugar": "আপোনাৰ তেজৰ চেনিৰ মাত্ৰা পৰীক্ষা কৰা হৈছে। এই বিষয়ে চিকিৎসকৰ পৰামৰ্শ লওক।",
                "hb": "হিমোগ্ল'বিনে তেজৰ স্বাস্থ্য সূচায়। সঠিক পৰামৰ্শৰ বাবে চিকিৎসকৰ সৈতে কথা পাতক।",
                "doctor": "ৰিপ'ৰ্টত সালসলনি থাকিলে ওচৰৰ চিকিৎসকক দেখুওৱাটো নিৰাপদ।",
                "default": f"আপোনাৰ প্ৰশ্ন '{question}' পোৱা গ'ল। অনুগ্ৰহ কৰি চিকিৎসকৰ পৰামৰ্শ লওক।"
            },
            "ur": {
                "sugar": "آپ کے خون میں شوگر کی سطح چیک کی گئی ہے۔ براہ کرم اس بارے میں ڈاکٹر سے مشورہ کریں۔",
                "hb": "ہیموگلوبن خون کی صحت کو ظاہر کرتا ہے۔ مناسب رہنمائی کے لیے ڈاکٹر سے رابطہ کریں۔",
                "doctor": "اگر رپورٹ میں کوئی تبدیلی ہو تو قریبی ڈاکٹر کو دکھانا سب سے بہتر ہے۔",
                "default": f"آپ کا سوال '{question}' موصول ہوا۔ مزید رہنمائی کے لیے ڈاکٹر سے رجوع کریں۔"
            },
            "en": {
                "sugar": "Your blood sugar levels are recorded on the report. It is best to review fasting or post-meal values with your doctor.",
                "hb": "Hemoglobin reflects your red blood cell levels. Your doctor can suggest healthy dietary habits if needed.",
                "doctor": "If any of your test values differ from the standard range, visiting a nearby doctor or health centre is always the safest step.",
                "default": f"Thank you for asking: '{question}'. While these lab values give an overview, your doctor will guide you on the exact next steps for your health."
            }
        }

        lang_dict = fallback_answers.get(lang, fallback_answers["en"])
        if any(w in q_lower for w in ["sugar", "glucose", "ഷുഗർ", "शुगर", "சர்க்கரை"]):
            body = lang_dict["sugar"]
        elif any(w in q_lower for w in ["hb", "hemoglobin", "haemoglobin", "blood", "രക്തം", "खून", "இரத்தம்"]):
            body = lang_dict["hb"]
        elif any(w in q_lower for w in ["doctor", "clinic", "hospital", "ഡോക്ടർ", "डॉक्टर", "மருத்துவர்"]):
            body = lang_dict["doctor"]
        else:
            body = lang_dict["default"]

        return self._ensure_safety_disclaimer(body)
